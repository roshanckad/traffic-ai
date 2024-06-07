import requests

from src.model.google.TravelInfo import TravelInfo


class GoogleMapsAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_travel_info(self, origin, destination):
        url = (f'https://maps.googleapis.com/maps/api/distancematrix/json'
               f'?origins={origin}&destinations={destination}'
               f'&key={self.api_key}&mode=driving&departure_time=now')

        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            element = data['rows'][0]['elements'][0]
            if element['status'] == 'OK':
                distance = element['distance']['text']
                duration = element['duration']['text']
                duration_in_second = element['duration']['value']
                duration_in_traffic = element['duration_in_traffic']['text']
                duration_in_traffic_in_second = element['duration_in_traffic']['value']
                origin_addresses = data['origin_addresses'][0]
                destination_addresses = data['destination_addresses'][0]

                return TravelInfo(
                    origin=origin_addresses,
                    destination=destination_addresses,
                    distance=distance,
                    duration=duration,
                    duration_in_second=duration_in_second,
                    duration_in_traffic=duration_in_traffic,
                    duration_in_traffic_in_second=duration_in_traffic_in_second
                )
            else:
                raise Exception(f"Error in element: {element['status']}")
        else:
            raise Exception(f"Error in response: {data['status']}")
