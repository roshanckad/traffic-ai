class TravelInfo:
    def __init__(self, origin, destination, distance, duration, duration_in_second, duration_in_traffic, duration_in_traffic_in_second):
        self.origin = origin
        self.destination = destination
        self.distance = distance
        self.duration = duration
        self.duration_in_second = duration_in_second
        self.duration_in_traffic = duration_in_traffic
        self.duration_in_traffic_in_second = duration_in_traffic_in_second

    def __repr__(self):
        return (f"TravelInfo(origin='{self.origin}', destination='{self.destination}', distance='{self.distance}', "
                f"duration='{self.duration}', duration_in_traffic='{self.duration_in_traffic}')")
