from dataclasses import dataclass


@dataclass
class ValidationException(Exception):
    message: str
    status_code: int = 400

    def as_dict(self):
        return dict(
            message=self.message,
            status_code=self.status_code,
        )
