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

    @classmethod
    def from_api_response(cls, data: dict) -> "Country":
        names = data.get("names", {})
        capitals = data.get("capitals", [])
        currencies = data.get("currencies", [])
        languages = data.get("languages", [])
        area = data.get("area", {})
        flag = data.get("flag", {})

        return cls(
            name=names.get("common", "N/A"),
            official_name=names.get("official", "N/A"),
            capital=capitals[0]["name"] if capitals else "No disponible",
            region=data.get("region", ""),
            subregion=data.get("subregion", ""),
            population=data.get("population", 0),
            area_km2=area.get("kilometers", 0.0),
            currency=currencies[0]["name"] if currencies else "N/A",
            language=languages[0]["name"] if languages else "N/A",
            flag_url=flag.get("url_png", ""),
        )