import requests
import json
import os
from getpass import getpass

class ServiceNowClient:
    def __init__(self, url, user, pwd):
        self.url = url
        self.auth = (user, pwd)
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def create_incident(self, short_description, caller_id, assignment_group):
        """Create a single incident in ServiceNow and return the JSON response."""
        payload = {
            "short_description": short_description,
            "caller_id": caller_id,
            "assignment_group": assignment_group
        }

        response = requests.post(
            self.url,
            auth=self.auth,
            headers=self.headers,
            data=json.dumps(payload)
        )

        if response.status_code != 201:  # ServiceNow usually returns 201 for POST success
            raise Exception(
                f"Request failed: {response.status_code}\n"
                f"Headers: {response.headers}\n"
                f"Response: {response.text}"
            )

        return response.json()

    def create_multiple_incidents(self, incidents):
        """
        Create multiple incidents.
        incidents = list of dicts:
        [
          {"short_description": "...", "caller_id": "...", "assignment_group": "..."},
          ...
        ]
        """
        results = []
        for i, inc in enumerate(incidents, start=1):
            try:
                result = self.create_incident(
                    short_description=inc["short_description"],
                    caller_id=inc["caller_id"],
                    assignment_group=inc["assignment_group"]
                )
                results.append({"index": i, "status": "success", "response": result})
            except Exception as e:
                results.append({"index": i, "status": "failed", "error": str(e)})
        return results


if __name__ == "__main__":
    url = "https://dev342687.service-now.com/api/now/v2/table/incident?sysparm_fields=number%2Cshort_description%2Ccaller_id%2Cassignment_group"
    user = "deen-web"
    pwd =   os.getenv("password")

    sn_client = ServiceNowClient(url, user, pwd)

    # Example: list of incidents to open at once
    incidents_to_open = [
        {
            "short_description": "API test incident 6",
            "caller_id": "878a21c4837fe21036bd97a6feaad3e3",
            "assignment_group": "287ebd7da9fe198100f92cc8d1d2154e"
        },
        {
            "short_description": "API test incident 7",
            "caller_id": "878a21c4837fe21036bd97a6feaad3e3",
            "assignment_group": "8a5055c9c61122780043563ef53438e3"
        },
                {
            "short_description": "API test incident 8",
            "caller_id": "878a21c4837fe21036bd97a6feaad3e3",
            "assignment_group": "8a4dde73c6112278017a6a4baf547aa7"
        },
                        {
            "short_description": "API test incident 9",
            "caller_id": "878a21c4837fe21036bd97a6feaad3e3",
            "assignment_group": "287ebd7da9fe198100f92cc8d1d2154e"
        },
    ]

    results = sn_client.create_multiple_incidents(incidents_to_open)

    print(json.dumps(results, indent=4))
