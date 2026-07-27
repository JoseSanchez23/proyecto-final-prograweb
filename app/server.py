from flask import Flask, send_file, jsonify, request, send_from_directory
import os
import sys

# Agregar la raíz del proyecto al path para poder importar src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services import buscar_pais, comparar_paises
from src.database import listar_paises_guardados

# Ruta ABSOLUTA a la carpeta del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configurar Flask con las carpetas correctas
app = Flask(__name__,
            static_folder=os.path.join(PROJECT_ROOT, 'static'),
            template_folder=os.path.join(PROJECT_ROOT, 'templates'))

@app.route('/')
def index():
    """Sirve la página principal"""
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """Sirve archivos estáticos (CSS, JS, imágenes)"""
    try:
        return send_from_directory(app.static_folder, path)
    except Exception as e:
        return f"Error al cargar {path}: {e}", 404

@app.route('/api/countries/search')
def search_country():
    """Busca un país por nombre"""
    name = request.args.get('name')
    if not name or not name.strip():
        return jsonify({'error': 'Falta el nombre del país'}), 400
    
    country = buscar_pais(name.strip())
    if country:
        return jsonify(country.to_dict())
    else:
        return jsonify({'error': 'País no encontrado'}), 404

@app.route('/api/countries/compare')
def compare_countries():
    """Compara dos países"""
    country1 = request.args.get('country1')
    country2 = request.args.get('country2')
    
    if not country1 or not country2:
        return jsonify({'error': 'Se necesitan dos países para comparar'}), 400
    
    paises = comparar_paises([country1.strip(), country2.strip()])
    
    if len(paises) == 0:
        return jsonify({'error': 'Ninguno de los países fue encontrado'}), 404
    elif len(paises) == 1:
        return jsonify({'error': 'Uno de los países no fue encontrado'}), 404
    
    return jsonify({
        'country1': paises[0].to_dict(),
        'country2': paises[1].to_dict()
    })

@app.route('/api/countries/saved')
def saved_countries():
    """Devuelve la lista de países guardados"""
    paises = listar_paises_guardados()
    return jsonify(paises)

if __name__ == '__main__':
    print(f"\n🌍 WorldExplorer - Servidor Web")
    print(f"📁 Ruta del proyecto: {PROJECT_ROOT}")
    print(f"📁 Templates: {app.template_folder}")
    print(f"📁 Static: {app.static_folder}")
    print(f"📡 Servidor corriendo en: http://localhost:5001")
    print(f"🔍 Prueba: http://localhost:5001/api/countries/search?name=Costa%20Rica")
    print(f"🔄 Presiona Ctrl+C para detener el servidor\n")
    app.run(debug=True, port=5001, host='0.0.0.0')