from typing import Dict, List


class Weight:
    data: Dict[str, float]

    def __init__(self, data: Dict[str, float] = {}) -> None:
        self.data = data

    def __post_init__(self) -> None:
        assert (
            len(
                set(
                    isinstance(k, str) and isinstance(v, float)
                    for k, v in self.data.items()
                )
            )
            == 1
        ), "Key value pairs should be str and float types"

        assert (
            sum(v for v in list(self.data.values())) == 1
        ), "Values must be adding up to 1"

    def add_key_value(self, key: str, value: float) -> None:
        if key in self.data:
            self.data[key] += value
        else:
            self.data[key] = value

    def set_value(self, key: str, value: float) -> None:
        if value == 0:
            self.data.pop(key, None)
            return

        self.data[key] = value

    def keys(self) -> List[str]:
        return list(self.data.keys())

    def get_key(self, key: str) -> float:
        return self.data[key]

    def values(self) -> List[float]:
        return list(self.data.values())
