from pathlib import Path


class QueryConstructor:
    def __init__(self, username=None):
        self.username = username
        self.construct()

    def construct(self):
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
            }
        }
