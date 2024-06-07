import ollama
import time


class TrafficUpdater:
    def __init__(self, model='gemma:2b'):
        self.model = model

    def get_traffic_update(self, message):
        start_time = time.time()
        response = ollama.chat(model=self.model, messages=[
            {
                'role': 'user',
                'content': message,
            },
        ])
        print(response['message']['content'])
        print("--- %s seconds ---" % round((time.time() - start_time), 2))