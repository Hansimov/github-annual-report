from pathlib import Path


class QueryConstructor:
    def __init__(self, username=None):
        self.username = username
        self.construct()

    def construct(self):
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
                "output_path": Path(__file__).parent / "contributions.json",
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
                "output_path": Path(__file__).parent / "repositories.json",
            },
        }
