from datetime import datetime, timezone
from typing import Dict

class MockBankAdapter:
    def __init__(self):
        self._links = {}  # user_id -> info

    def create_link(self, user_id: int, provider: str, last_four: str) -> Dict:
        info = {
            "user_id": user_id,
            "provider": provider,
            "last_four": last_four,
            "linked_at": datetime.now(timezone.utc).isoformat(),
        }
        self._links[user_id] = info
        return info

    def get_link(self, user_id: int):
        return self._links.get(user_id)

mock_bank = MockBankAdapter()
