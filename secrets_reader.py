from getpass import getpass
import json
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

    def load(self):
        for key in ["username", "token"]:
            if key in self.secrets and self.secrets.get(key):
                setattr(self, key, self.secrets[key])
            else:
                if key == "token":
                    val = getpass(f"Enter your Github {key}: ")
                else:
                    val = input(f"Enter your Github {key}: ")

                setattr(self, key, val)
                self.secrets[key] = val
                with open(self.secrets_path, "w") as wf:
                    json.dump(self.secrets, wf, ensure_ascii=False, indent=4)
