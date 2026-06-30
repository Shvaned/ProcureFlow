import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.analytics_service import AnalyticsService


class TestAnalyticsService:
    def _mock_db(self):
        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar.return_value = 0
        mock_result.one.return_value = (0, 0, 0, 0, 0)
        mock_result.all.return_value = []
        db.execute = AsyncMock(return_value=mock_result)
        return db

    def test_get_executive_summary_has_all_keys(self):
        db = self._mock_db()
        svc = AnalyticsService(db)
        import asyncio
        result = asyncio.run(svc.get_executive_summary())
        for key in ["total_products", "total_suppliers", "total_warehouses",
                     "total_inventory_value", "open_purchase_orders", "pending_approvals",
                     "low_stock_items", "out_of_stock_items"]:
            assert key in result

    def test_kpi_unknown_key_returns_fallback(self):
        db = self._mock_db()
        svc = AnalyticsService(db)
        import asyncio
        result = asyncio.run(svc.get_kpi_data("nonexistent_kpi"))
        assert result["value"] == 0
        assert "not available" in result["description"]

    def test_get_inventory_analytics_returns_dict(self):
        db = self._mock_db()
        svc = AnalyticsService(db)
        import asyncio
        result = asyncio.run(svc.get_inventory_analytics())
        assert isinstance(result, dict)
        assert "total_value" in result
