from pathlib import Path


class QueryConstructor:
    def __init__(self, username=None):
        self.username = username
        self.output_path_root = Path(__file__).parent / "data"
        self.construct()

    def construct(self):
        if not self.output_path_root.exists():
            self.output_path_root.mkdir()
        # https://docs.github.com/en/graphql/reference/objects#contributionscollection
        # https://docs.github.com/en/graphql/reference/objects#contributioncalendar
        # https://docs.github.com/en/graphql/reference/objects#contributioncalendarweek
        # https://docs.github.com/en/graphql/reference/objects#contributioncalendarday
        # https://docs.github.com/en/graphql/reference/objects#createdrepositorycontributionconnection
        self.queries = {
            "contributions": {
                "query": f"""
                    query {{
                        user (login: "{self.username}") {{
                            name
                            contributionsCollection {{
                                contributionCalendar {{
                                    colors
                                    totalContributions
                                    weeks {{
                                        contributionDays {{
                                            color
                                            contributionCount
                                            date
                                            weekday
                                        }}
                                        firstDay
                                    }}
                                }}
                            }}
                        }}
                    }}
                    """,
                "output_path": self.output_path_root / "contributions.json",
            },
            "repositories": {
                "query": f"""
                    query {{
                        search (query: "user:{self.username} created:>2023-01-01", type: REPOSITORY, first: 100) {{
                            repositoryCount
                            edges {{
                                node {{
                                    ... on Repository {{
                                        name
                                        createdAt
                                        updatedAt
                                        description
                                        forkCount
                                        stargazerCount
                                        primaryLanguage {{
                                            name
                                        }}
                                        languages (first: 3) {{
                                            edges {{
                                                node {{
                                                    name
                                                }}
                                                size
                                            }}
                                        }}
                                        owner {{
                                            login
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                    """,
                "output_path": self.output_path_root / "repositories.json",
            },
            "contributions_by_type": {
                "query": f"""
                    query {{
                        user(login: "{self.username}") {{
                            contributionsCollection(from: "2023-01-01T00:00:00Z", to: "2023-12-31T23:59:59Z") {{
                                commitContributionsByRepository(maxRepositories: 100) {{
                                    repository {{
                                        nameWithOwner
                                    }}
                                    contributions(first: 100) {{
                                        edges {{
                                            node {{
                                                commitCount
                                                occurredAt
                                            }}
                                        }}
                                    }}
                                }}
                                issueContributionsByRepository(maxRepositories: 100) {{
                                    repository {{
                                        nameWithOwner
                                    }}
                                    contributions(first: 100) {{
                                        edges {{
                                            node {{
                                                occurredAt
                                                issue {{
                                                    title
                                                    bodyText
                                                    url
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                                pullRequestContributionsByRepository(maxRepositories: 100) {{
                                    repository {{
                                        nameWithOwner
                                    }}
                                    contributions(first: 100) {{
                                        edges {{
                                            node {{
                                                occurredAt
                                                pullRequest {{
                                                    title
                                                    bodyText
                                                    url
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                """,
                "output_path": self.output_path_root / "contributions_by_type.json",
            },
            # Get `github_node_id` :
            #   https://api.github.com/users/<username>
            "commits_by_repository": {
                "query": f"""
                    query {{
                        repository(owner:"{owner_name}", name:"{repo_name}") {{
                            ref(qualifiedName: "main") {{
                            target {{
                                ... on Commit {{
                                    history(first:100, author: {{id: "{self.github_node_id}"}}) {{
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
                    }}
                    }}
                """,
                "output_path": self.output_path_root / "commits_by_repository.json",
            },
        }
