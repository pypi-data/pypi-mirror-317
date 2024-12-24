import json
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "defaults.json"
USER_CONFIG_PATH = Path(__file__).parent.parent / "config" / "user.json"


class Config:
    def __init__(self, path: Path):
        self.path = path
        self.data = self.load()

    def load(self) -> dict:
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save(self, data: dict) -> None:
        with open(self.path, "w") as f:
            json.dump(data, f)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save(self.data)


default_config = Config(DEFAULT_CONFIG_PATH)
user_config = Config(USER_CONFIG_PATH)

def load_defaults() -> dict:
    return default_config.load()

def load_default_model() -> str:
    return default_config.get("model", "gpt-4o")

def load_weave_project() -> str | None:
    return user_config.get("weave_project")

def set_weave_project(project: str) -> None:
    user_config.set("weave_project", project)