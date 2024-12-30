import json
from pathlib import Path
from datetime import datetime
from typing import TypeVar, Union, Any

T = TypeVar('T', bound=Union[bool, int, str, float, list, dict, datetime])


def encode_states(obj: Any):
    if isinstance(obj, datetime):
        return {'type': 'datetime', 'value': obj.isoformat()}

    raise TypeError(f'Unknown state type: {type(obj).__name__}.')


def decode_state_object(obj: dict):
    if 'type' not in obj:
        return obj

    if obj['type'] == 'datetime':
        return datetime.fromisoformat(obj['value'])

    raise TypeError(f'Unknown state type: {obj["type"]}.')


class StateManager:
    root_dir: Path

    def __init__(self, root_dir: Union[str, Path]):
        self.root_dir = Path(root_dir)

        if not self.root_dir.exists():
            self.root_dir.mkdir(0o755, True)

    def get(self, key: str, default: T = None) -> T:
        filepath = self.root_dir.joinpath(key)

        if not filepath.exists():
            return default

        with filepath.open('r', encoding='utf-8') as fp:
            return json.load(fp, object_hook=decode_state_object)

    def set(self, key: str, value: T):
        with self.root_dir.joinpath(key).open('w', encoding='utf-8') as fp:
            json.dump(value, fp, default=encode_states)
