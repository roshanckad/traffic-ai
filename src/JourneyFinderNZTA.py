from datetime import datetime
import configparser

from ai.TrafficUpdater import TrafficUpdater
from api.JourneyPlannerAPI import JourneyPlannerAPI


def get_matching_phrase(free_flow_state):
    if free_flow_state == 'green':
        return 'manageable'
    elif free_flow_state == 'orange':
        return 'longer than expected'
    else:
        return 'reconsider your need for this trip'


def get_top_traffic_updates(number_of_records):
    journey_planner_api = JourneyPlannerAPI()
    journeys_data = journey_planner_api.fetch_journeys()
    top_records = []
    records_returned = 0
    for feature in journeys_data.features:
        journey = feature.properties
        if journey.RegionID == 7 and journey.SortOrder > 0:
            record_info = {
                "Route": journey.Title,
                "Current Time": journey.CurrentTime,
                "Delay": journey.CurrentTime - journey.FreeFlowTime,
                "Phrase": get_matching_phrase(journey.FreeFlowState)
            }
            top_records.append(record_info)
            records_returned += 1
            if records_returned >= number_of_records:
                break
    return top_records


if __name__ == "__main__":
    top_traffic_updates = get_top_traffic_updates(3)
    print(top_traffic_updates)

    config = configparser.RawConfigParser()
    config.read('resource/application.properties')

    prompt_for_model = config.get('message_templates', 'message.nzta')
    llm_model = config.get('llm_model', 'model.name')

    traffic_updater = TrafficUpdater(llm_model)
    current_time = datetime.now()

    for traffic_update in top_traffic_updates:
        message = (prompt_for_model.format(current_time, traffic_update["Route"], traffic_update["Current Time"],
                                           traffic_update["Delay"], traffic_update["Phrase"]))
        traffic_updater.get_traffic_update(message)
