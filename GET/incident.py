import requests
import json
import os
from getpass import getpass


class ServiceNowClient:
    def __init__(self, url, user, pwd):
        """
        url: base API URL, e.g. https://<instance>.service-now.com/api/now/table
        """
        self.base_url = url.rstrip("/")
        self.auth = (user, pwd)
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get_records(self, table, query=None, limit=10):
        """
        Generic GET method to fetch records from any ServiceNow table.
        - table: table name (e.g. 'incident')
        - query: sysparm_query string (e.g. 'priority=1^active=true')
        - limit: number of records to return
        """
        params = {
            "sysparm_limit": limit
        }
        if query:
            params["sysparm_query"] = query

        url = f"{self.base_url}/{table}"
        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)

        if response.status_code != 200:
            raise Exception(
                f"Request failed: {response.status_code}\n"
                f"Headers: {response.headers}\n"
                f"Response: {response.text}"
            )

        return response.json()

if __name__ == "__main__":
    # Example usage
    instance = "https://dev342687.service-now.com/api/now/table/"
    user = "deen-web"
    pwd =   os.getenv("password")

    sn_client = ServiceNowClient(instance, user, pwd)

    # Fetch first 5 active, P1 incidents
    records = sn_client.get_records(
        table="incident",
        query="priority=5^state=1^assignment_group!=5ee74940b70022108d4406dd1e11a91^ORassignment_group=NULL",
        limit=2
    )

    print(json.dumps(records, indent=4))
