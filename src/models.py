from dataclasses import dataclass


@dataclass
class Country:
    name: str
    official_name: str
    capital: str
    region: str
    subregion: str
    population: int
    area_km2: float
    currency: str
    language: str
    flag_url: str
    emoji_flag: str = ""
    continents: list[str] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "official_name": self.official_name,
            "capital": self.capital,
            "region": self.region,
            "subregion": self.subregion,
            "population": self.population,
            "area_km2": self.area_km2,
            "currency": self.currency,
            "language": self.language,
            "flag_url": self.flag_url,
            "emoji_flag": self.emoji_flag,
            "continents": self.continents or [],
        }

    @classmethod
    def from_api_response(cls, data: dict) -> "Country":
        names = data.get("names", {}) or {}
        capitals = data.get("capitals", []) or []
        currencies = data.get("currencies", {}) or {}
        languages = data.get("languages", []) or []
        area = data.get("area", {}) or {}
        flag = data.get("flag", {}) or {}
        continents = data.get("continents", []) or []

        if isinstance(capitals, dict):
            capital = capitals.get("name", "No disponible")
        elif isinstance(capitals, list) and capitals:
            first_capital = capitals[0]
            capital = first_capital.get("name") if isinstance(first_capital, dict) else str(first_capital)
        else:
            capital = "No disponible"

        if isinstance(currencies, dict):
            first_currency = next(iter(currencies.values()), {})
            currency = first_currency.get("name", "N/A") if isinstance(first_currency, dict) else str(first_currency)
        else:
            currency = "N/A"

        language_names = []
        if isinstance(languages, dict):
            for value in languages.values():
                if isinstance(value, dict):
                    name = value.get("name")
                    if name:
                        language_names.append(name)
        elif isinstance(languages, list):
            for entry in languages:
                if isinstance(entry, dict):
                    name = entry.get("name")
                    if name:
                        language_names.append(name)
                elif isinstance(entry, str):
                    language_names.append(entry)

        language = ", ".join(language_names) if language_names else "N/A"

        if isinstance(area, dict):
            area_km2 = area.get("kilometers") or area.get("km2") or 0.0
        else:
            area_km2 = 0.0

        flag_url = flag.get("url_png") or flag.get("url_svg") or ""
        emoji_flag = flag.get("emoji") or ""

        if not isinstance(continents, list):
            continents = [continents] if continents else []

        return cls(
            name=names.get("common", "N/A"),
            official_name=names.get("official", "N/A"),
            capital=capital,
            region=data.get("region", ""),
            subregion=data.get("subregion", ""),
            population=data.get("population", 0),
            area_km2=float(area_km2) if isinstance(area_km2, (int, float, str)) and str(area_km2).replace('.', '', 1).isdigit() else 0.0,
            currency=currency,
            language=language,
            flag_url=flag_url,
            emoji_flag=emoji_flag,
            continents=continents,
        )