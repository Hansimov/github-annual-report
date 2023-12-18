from pathlib import Path


class CommitsByRepositoryQuerier:
    def __init__(self, owner_name, repo_name, node_id):
        self.output_path = (
            Path(__file__).parents[1] / "data" / "commits_by_repository.json"
        )
        self.owner_name = owner_name
        self.repo_name = repo_name
        self.node_id = node_id
        self.construct()

    def construct(self):
        self.query = f"""
        query {{
            repository(owner:"{self.owner_name}", name:"{self.repo_name}") {{
                ref(qualifiedName: "main") {{
                    target {{
                        ... on Commit {{
                            history(first:100, author: {{id: "{self.node_id}"}}) {{
                                pageInfo {{
                                    hasNextPage
                                }}
                                edges {{
                                    node {{
                                        messageHeadline
                                        oid
                                        message
                                        author {{
                                            name
                                            email
                                            date
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
                pullRequests(first:100, states:OPEN) {{
                    edges {{
                        node {{
                            title
                            url
                            author {{
                                login
                            }}
                            createdAt
                        }}
                    }}
                }}
                issues(first:100, states:OPEN) {{
                    edges {{
                        node {{
                            title
                            url
                            author {{
                                login
                            }}
                            createdAt
                        }}
                    }}
                }}
            }}
        }}
        """
