const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("country-input");
const searchButton = document.getElementById("search-button");
const searchStatus = document.getElementById("search-status");
const emptyState = document.getElementById("empty-state");
const resultCard = document.getElementById("country-result");

const compareForm = document.getElementById("compare-form");
const countryOneInput = document.getElementById("country-one");
const countryTwoInput = document.getElementById("country-two");
const compareButton = document.getElementById("compare-button");
const compareStatus = document.getElementById("compare-status");
const comparisonResult = document.getElementById("comparison-result");

// Endpoint esperado del backend del equipo.
// CORREGIDO: URL absoluta para evitar errores de enrutamiento 404 en Vercel
const BACKEND_SEARCH_ENDPOINT = "https://proyecto-final-progweb.vercel.app/api/countries/search";

/**
 * Solicita un país al backend del proyecto.
 */
async function fetchCountry(countryName) {
    const cleanName = countryName.trim();

    if (!cleanName) {
        throw new Error("Debes escribir el nombre de un país.");
    }

    if (window.location.protocol === "file:") {
        throw new Error(
            "La interfaz está lista. Para consultar datos debe ejecutarse junto al servidor web del backend."
        );
    }

    let response;
    try {
        response = await fetch(
            `${BACKEND_SEARCH_ENDPOINT}?name=${encodeURIComponent(cleanName)}`,
            { headers: { Accept: "application/json" } }
        );
    } catch (error) {
        throw new Error(
            "No fue posible conectar con el backend. Verifica que el servidor web esté ejecutándose."
        );
    }

    // ✅ CORREGIDO: Si el status NO es 200, lanza error
    if (response.status === 404) {
        throw new Error("No encontramos ese país. Revisa el nombre e inténtalo nuevamente.");
    }

    if (!response.ok) {
        throw new Error(`El servidor respondió con un error (${response.status}).`);
    }

    const data = await response.json();

    if (!data || (typeof data === "object" && Object.keys(data).length === 0)) {
        throw new Error("El servidor devolvió una respuesta vacía.");
    }

    return normalizeBackendCountry(data);
}

/**
 * Normaliza el JSON del backend para que la interfaz no dependa
 * de detalles internos de implementación.
 */
function normalizeBackendCountry(data) {
    const country = data && data.country ? data.country : data;

    return {
        name: country?.name || "No disponible",
        officialName: country?.official_name || country?.officialName || "",
        capital: country?.capital || "No disponible",
        region: country?.region || "No disponible",
        subregion: country?.subregion || "No disponible",
        population: Number(country?.population || 0),
        area: Number(country?.area_km2 ?? country?.area ?? 0),
        currency: country?.currency || "No disponible",
        languages: country?.language || country?.languages || "No disponible",
        flagUrl: country?.flag_url || country?.flagUrl || "",
        emojiFlag: country?.emoji_flag || country?.emojiFlag || "",
        continents: Array.isArray(country?.continents) ? country.continents : []
    };
}

function renderCountry(country) {
    setText("country-name", country.name);
    setText("official-name", country.officialName || "");
    setText(
        "country-region",
        [country.region, country.subregion].filter(Boolean).join(" · ")
    );
    setText("capital", country.capital);
    setText("population", formatNumber(country.population));
    setText("currency", country.currency);
    setText("language", country.languages);
    setText("subregion", country.subregion);
    setText("area", country.area ? `${formatNumber(country.area)} km²` : "No disponible");
    setText(
        "continent",
        country.continents.length ? country.continents.join(", ") : "No disponible"
    );

    const flag = document.getElementById("country-flag");
    if (country.flagUrl) {
        flag.src = country.flagUrl;
        flag.alt = `Bandera de ${country.name}`;
        flag.parentElement.classList.remove("hidden");
    } else {
        flag.removeAttribute("src");
        flag.alt = "";
        flag.parentElement.classList.add("hidden");
    }

    emptyState.classList.add("hidden");
    resultCard.classList.remove("hidden");
    resultCard.scrollIntoView({ behavior: "smooth", block: "center" });
}

function renderComparison(countries) {
    comparisonResult.innerHTML = countries
        .map(country => `
            <article class="compare-card">
                <div class="compare-card-top">
                    ${
                        country.flagUrl
                            ? `<img class="compare-flag" src="${escapeHtml(country.flagUrl)}" alt="Bandera de ${escapeHtml(country.name)}">`
                            : `<div class="compare-flag" aria-hidden="true"></div>`
                    }
                    <div>
                        <h3>${escapeHtml(country.name)}</h3>
                        <p>${escapeHtml(country.officialName || country.region)}</p>
                    </div>
                </div>

                <dl class="compare-list">
                    ${compareRow("Capital", country.capital)}
                    ${compareRow("Población", formatNumber(country.population))}
                    ${compareRow("Región", country.region)}
                    ${compareRow("Subregión", country.subregion)}
                    ${compareRow("Moneda", country.currency)}
                    ${compareRow("Idioma(s)", country.languages)}
                    ${compareRow(
                        "Área",
                        country.area ? `${formatNumber(country.area)} km²` : "No disponible"
                    )}
                    ${compareRow(
                        "Continente",
                        country.continents.length ? country.continents.join(", ") : "No disponible"
                    )}
                </dl>
            </article>
        `)
        .join("");
}

function compareRow(label, value) {
    return `
        <div class="compare-row">
            <dt>${escapeHtml(label)}</dt>
            <dd>${escapeHtml(String(value || "No disponible"))}</dd>
        </div>
    `;
}

searchForm.addEventListener("submit", async event => {
    event.preventDefault();

    const countryName = searchInput.value.trim();

    if (!countryName) {
        setStatus(searchStatus, "Escribe el nombre de un país.", "error");
        searchInput.focus();
        return;
    }

    setLoading(searchButton, true, "Buscando...");
    setStatus(searchStatus, "Consultando información...", "");

    try {
        const country = await fetchCountry(countryName);
        renderCountry(country);
        setStatus(searchStatus, `Información encontrada para ${country.name}.`, "success");
    } catch (error) {
        resultCard.classList.add("hidden");
        emptyState.classList.remove("hidden");
        setStatus(searchStatus, error.message, "error");
    } finally {
        setLoading(searchButton, false, "🔎 Buscar país");
    }
});

compareForm.addEventListener("submit", async event => {
    event.preventDefault();

    const countryOne = countryOneInput.value.trim();
    const countryTwo = countryTwoInput.value.trim();

    if (!countryOne || !countryTwo) {
        setStatus(compareStatus, "Escribe los dos países que deseas comparar.", "error");
        return;
    }

    if (countryOne.toLowerCase() === countryTwo.toLowerCase()) {
        setStatus(compareStatus, "Selecciona dos países diferentes para comparar.", "error");
        return;
    }

    setLoading(compareButton, true, "Comparando...");
    setStatus(compareStatus, "Consultando ambos países...", "");
    comparisonResult.innerHTML = "";

    try {
        const countries = await Promise.all([
            fetchCountry(countryOne),
            fetchCountry(countryTwo)
        ]);

        renderComparison(countries);
        setStatus(compareStatus, "Comparación lista.", "success");
    } catch (error) {
        setStatus(compareStatus, error.message, "error");
    } finally {
        setLoading(compareButton, false, "Comparar");
    }
});

document.querySelectorAll(".quick-chip").forEach(button => {
    button.addEventListener("click", () => {
        searchInput.value = button.dataset.country || "";
        searchForm.requestSubmit();
    });
});

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value || "No disponible";
    }
}

function setStatus(element, message, type) {
    element.textContent = message;
    element.classList.remove("error", "success");
    if (type) {
        element.classList.add(type);
    }
}

function setLoading(button, isLoading, text) {
    button.disabled = isLoading;
    button.textContent = text;
}

function formatNumber(value) {
    const number = Number(value);
    if (!Number.isFinite(number) || number === 0) {
        return "No disponible";
    }
    return new Intl.NumberFormat("es-CR", {
        maximumFractionDigits: 2
    }).format(number);
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}