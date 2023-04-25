from typing import Optional
import yaml
import os

config = {}


def load_config(file_str: Optional[str] = None) -> None:
    if file_str is None:
        script_dir = os.path.dirname(__file__)
        file_str = os.path.join(script_dir, "config.yaml")
    global config
    with open(file_str) as f:
        config.update(yaml.safe_load(f))
