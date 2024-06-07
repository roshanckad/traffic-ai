import json


class TravelPhrase:
    def __init__(self, duration_low, duration_high, phrases):
        self.duration_low = duration_low
        self.duration_high = duration_high
        self.phrases = phrases

    def __repr__(self):
        return (f"TravelPhrase(duration_low={self.duration_low}, duration_high={self.duration_high}, "
                f"phrases={self.phrases})")


def load_travel_phrases(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        travel_phrases = []
        for item in data:
            phrases = {
                "0%_over": item.get("0%_over_phrase"),
                "10%_over": item.get("10%_over_phrase"),
                "25%_over": item.get("25%_over_phrase"),
                "50%_over": item.get("50%_over_phrase"),
            }
            travel_phrase = TravelPhrase(
                duration_low=item["duration_low"],
                duration_high=item["duration_high"],
                phrases=phrases
            )
            travel_phrases.append(travel_phrase)
        return travel_phrases
