import requests

from src.model.journeyplanner.FeatureCollection import FeatureCollection


class JourneyPlannerAPI:

    api_url = 'https://www.journeys.nzta.govt.nz/api/keyjourneys'

    def fetch_journeys(self) -> FeatureCollection:
        response = requests.get(self.api_url)
        response.raise_for_status()
        data = response.json()
        return FeatureCollection(**data)
