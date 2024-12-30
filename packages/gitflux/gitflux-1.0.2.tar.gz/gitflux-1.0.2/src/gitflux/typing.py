from dataclasses import dataclass


@dataclass
class Repository:
    name: str
    full_name: str

    def get_prefix(self) -> str:
        return self.full_name[0:self.full_name.index('/')]
