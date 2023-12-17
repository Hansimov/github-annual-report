import json
import os
import requests
from pathlib import Path
from secrets_reader import SecretsReader
from query_constructor import QueryConstructor


class GraphqlRequester:
    def __init__(self, query=None, username=None, token=None):
        self.query = query
        self.secrets_reader = SecretsReader()
        self.username = username or self.secrets_reader.username
        self.github_token = token or self.secrets_reader.token
        self.api_base = "https://api.github.com/graphql"
        self.construct_requests()

    def construct_requests(self):
        self.request_headers = {
            "Authorization": f"Bearer {self.github_token}",
        }
        self.queries = QueryConstructor(self.username).queries

    def post(self):
        query_names = [
            # "contributions",
            # "repositories",
            "contributions_by_type",
        ]
        for query_name in query_names:
            print(query_name)
            self.request_body = {
                "query": self.queries[query_name]["query"],
            }
            self.output_path = self.queries[query_name]["output_path"]
            response = requests.post(
                self.api_base, json=self.request_body, headers=self.request_headers
            )
            print(response.status_code)
            data = response.json()
            with open(self.output_path, mode="w", encoding="utf-8") as wf:
                json.dump(data, wf, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    requester = GraphqlRequester()
    requester.post()
