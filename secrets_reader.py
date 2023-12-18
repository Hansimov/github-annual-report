import json
import requests

from getpass import getpass
from pathlib import Path


class SecretsReader:
    def __init__(self):
        self.secrets_path = Path(__file__).parent / "secrets.json"
        if self.secrets_path.exists():
            with open(self.secrets_path, "r") as f:
                self.secrets = json.load(f)
        else:
            self.secrets = {}
        self.load()

    def get_node_id(self):
        api_url = f"https://api.github.com/users/{self.username}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        try:
            response = requests.get(api_url, headers=headers)
            data = response.json()
            return data["node_id"]
        except:
            return None

    def load(self):
        for key in ["username", "token", "node_id"]:
            if key in self.secrets and self.secrets.get(key):
                setattr(self, key, self.secrets[key])
            else:
                if key == "username":
                    val = input(f"Enter your Github {key}: ")
                elif key == "token":
                    val = getpass(f"Enter your Github {key}: ")
                elif key == "node_id":
                    val = self.get_node_id()
                else:
                    raise KeyError(f"{key}")

                setattr(self, key, val)
                self.secrets[key] = val
                with open(self.secrets_path, "w") as wf:
                    json.dump(self.secrets, wf, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    secrets_reader = SecretsReader()
    print(f"username: {secrets_reader.username}")
    print(f"token:    {secrets_reader.token}")
    print(f"node_id:  {secrets_reader.node_id}")
