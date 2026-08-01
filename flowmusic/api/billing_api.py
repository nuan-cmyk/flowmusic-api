from ._base import BaseAPI
from ..models.billing import BillingSummary

class BillingAPI(BaseAPI):
    def summary(self) -> BillingSummary:
        """Возвращает историю начислений и трат кредитов."""
        data = self._get("billing/summary?tz=%2B03%3A00")
        return BillingSummary(**data)

    def get_total_credits(self) -> float:
        """Возвращает текущий баланс кредитов."""
        data = self._get("billing/credits")
        return data.get("data", {}).get("credits_remaining", 0.0)
