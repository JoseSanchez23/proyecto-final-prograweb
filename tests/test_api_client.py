import unittest
from src.models import Country


class TestCountryModel(unittest.TestCase):
    def test_from_api_response_full_data(self):
        sample = {
            "names": {"common": "Canada", "official": "Canada"},
            "capitals": [{"name": "Ottawa"}],
            "region": "Americas",
            "subregion": "Northern America",
            "population": 39100000,
            "area": {"kilometers": 9984670.0},
            "currencies": {
                "CAD": {"name": "Canadian dollar", "symbol": "$"}
            },
            "languages": [
                {"name": "English"},
                {"name": "French"}
            ],
            "flag": {"url_png": "https://flag.example/canada.png", "emoji": "🇨🇦"},
            "continents": ["North America"],
        }

        country = Country.from_api_response(sample)

        self.assertEqual(country.name, "Canada")
        self.assertEqual(country.official_name, "Canada")
        self.assertEqual(country.capital, "Ottawa")
        self.assertEqual(country.region, "Americas")
        self.assertEqual(country.subregion, "Northern America")
        self.assertEqual(country.population, 39100000)
        self.assertEqual(country.area_km2, 9984670.0)
        self.assertEqual(country.currency, "Canadian dollar")
        self.assertEqual(country.language, "English, French")
        self.assertEqual(country.flag_url, "https://flag.example/canada.png")
        self.assertEqual(country.emoji_flag, "🇨🇦")
        self.assertEqual(country.continents, ["North America"])

    def test_from_api_response_missing_fields(self):
        sample = {
            "names": {"common": "Narnia"},
            "capitals": [],
            "currencies": {},
            "languages": {},
            "flag": {},
        }

        country = Country.from_api_response(sample)

        self.assertEqual(country.name, "Narnia")
        self.assertEqual(country.official_name, "N/A")
        self.assertEqual(country.capital, "No disponible")
        self.assertEqual(country.currency, "N/A")
        self.assertEqual(country.language, "N/A")
        self.assertEqual(country.flag_url, "")
        self.assertEqual(country.emoji_flag, "")
        self.assertEqual(country.continents, [])


if __name__ == "__main__":
    unittest.main()