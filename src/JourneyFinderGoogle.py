from ai.TrafficUpdater import TrafficUpdater
from api.GoogleDistanceMatrixAPI import GoogleMapsAPI
from src.util.TravelPhrase import load_travel_phrases
from datetime import datetime
import configparser


def get_google_travel_info(origin, destination):
    configs = configparser.RawConfigParser()
    configs.read('resource/application.properties')

    api_key = configs.get('credentials', 'google.apikey')

    gmaps_api = GoogleMapsAPI(api_key)
    try:
        travel_info = gmaps_api.get_travel_info(origin, destination)
        return travel_info
    except Exception as e:
        print(f"An error occurred: {e}")


def find_matching_scenario(travel_phrases, travel_info):
    duration_in_minutes = round(travel_info.duration_in_second / 60)
    for phrase in travel_phrases:
        if phrase.duration_low <= duration_in_minutes <= phrase.duration_high:
            return phrase
    return None


def calculate_delay_percentage(duration_in_second, duration_in_traffic_in_second):
    return ((duration_in_traffic_in_second - duration_in_second) / duration_in_second) * 100


def get_appropriate_phrase(travel_info, travel_phrases):
    matching_scenario = find_matching_scenario(travel_phrases, travel_info)
    # print(matching_scenario)
    if not matching_scenario:
        return "No matching scenario found"

    delay_percentage = calculate_delay_percentage(travel_info.duration_in_second,
                                                  travel_info.duration_in_traffic_in_second)
    # print("Delay as a percentage: %s" % delay_percentage)
    if delay_percentage >= 50:
        return matching_scenario.phrases["50%_over"]
    elif delay_percentage >= 25:
        return matching_scenario.phrases["25%_over"]
    elif delay_percentage >= 10:
        return matching_scenario.phrases["10%_over"]
    else:
        return matching_scenario.phrases["0%_over"]


if __name__ == "__main__":
    config = configparser.RawConfigParser()
    config.read('resource/application.properties')
    config.get('message_templates', 'message.google')

    origin = config.get('location', 'origin')
    destination = config.get('location', 'destination')

    travel_info = get_google_travel_info(origin, destination)
    print(travel_info)

    travel_phrases = load_travel_phrases('resource/travel_phrases.json')
    appropriate_phrase = get_appropriate_phrase(travel_info, travel_phrases)
    # print("Appropriate phrase: " + appropriate_phrase)

    prompt_for_model = config.get('message_templates', 'message.google')
    llm_model = config.get('llm_model', 'model.name')

    traffic_updater = TrafficUpdater(llm_model)
    current_time = datetime.now()

    message = (prompt_for_model.format(current_time, origin, destination, travel_info.duration_in_traffic,
                                       appropriate_phrase))

    traffic_updater.get_traffic_update(message)
