from typing import Any

class ResponseOK:
    def __init__(self, status_code: int, message: str, transaction_id: str, time_elapsed: int, data: Any = None):
        self.status_code = status_code
        self.message = message
        self.transaction_id = transaction_id
        self.time_elapsed = time_elapsed
        self.data = data

    def to_dict(self):
        return {
            "status": self.status_code,
            "message": self.message,
            "transactionId": self.transaction_id,
            "timeElapsed": self.time_elapsed,
            "data": self.data
        }
