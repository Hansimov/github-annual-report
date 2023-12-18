import json
import os
import requests
from pathlib import Path
from secrets_reader import SecretsReader
from query_constructor import QueryConstructor
from queriers import CommitsByRepositoryQuerier


class GraphqlRequester:
    def __init__(self, query=None, username=None, token=None, node_id=None):
        self.query = query
        self.secrets_reader = SecretsReader()
        self.username = username or self.secrets_reader.username
        self.token = token or self.secrets_reader.token
        self.node_id = node_id or self.secrets_reader.node_id
        self.api_base = "https://api.github.com/graphql"
        self.construct_requests()

    def construct_requests(self):
        self.request_headers = {
            "Authorization": f"Bearer {self.token}",
        }
        self.queries = QueryConstructor(self.username).queries

    def post(self):
        query_names = [
            "contributions",
            # "repositories",
            "contributions_by_type",
            # "commits_by_repository",
        ]
        for query_name in query_names:
            # print(query_name)
            if query_name == "commits_by_repository":
                querier = CommitsByRepositoryQuerier(
                    "hansimov", "bing-chat-api", self.node_id
                )
                query = querier.query
                output_path = querier.output_path
            else:
                query = self.queries[query_name]["query"]
                output_path = self.queries[query_name]["output_path"]

            self.request_body = {
                "query": query,
            }
            self.output_path = output_path

            response = requests.post(
                self.api_base, json=self.request_body, headers=self.request_headers
            )
            print(f"[{response.status_code}] {query_name}:")
            data = response.json()
            with open(self.output_path, mode="w", encoding="utf-8") as wf:
                json.dump(data, wf, ensure_ascii=False, indent=4)
            print(self.output_path)


if __name__ == "__main__":
    requester = GraphqlRequester()
    requester.post()
