import requests


class ServiceApi:
    def post(self, url, payload):
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            # print("Success:", response.json())  # Assuming the response is JSON
            return response
        else:
            print(f"Failed with status code {response.status_code}: {response.text}")

    def get(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            print("Success:", response.json())  # Assuming the response is JSON
        else:
            print(f"Failed with status code {response.status_code}: {response.text}")
