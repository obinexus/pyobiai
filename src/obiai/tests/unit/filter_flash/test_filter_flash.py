"""
Unit tests for filter_flash
QA_LAYER: UNIT
QA_STANDARD: PolyCore QA Validation Plan
AEGIS_COMPLIANCE: Mathematical verification required
"""

import unittest
from poc.bayesian_debiasing.src.filter_flash import FilterFlash, FlashEventManager


class TestFilterFlash(unittest.TestCase):
    """Unit tests for FilterFlash component"""

    def setUp(self):
        self.filter_flash = FilterFlash(consciousness_threshold=0.5)

    def test_data_passes_filter(self):
        """Data should pass when cognitive load is below threshold"""
        data = {"value": 1}
        result = self.filter_flash.filter_data(data, cognitive_load=0.3)
        self.assertEqual(result, data)

    def test_data_filtered_when_load_high(self):
        """Data should be filtered out when load exceeds threshold"""
        data = {"value": 1}
        result = self.filter_flash.filter_data(data, cognitive_load=0.8)
        self.assertEqual(result, [])

    def test_flash_triggered_on_pattern(self):
        """Pattern data should trigger an insight flash"""
        data = {"pattern": True}
        self.filter_flash.filter_data(data, cognitive_load=0.1)
        self.assertEqual(len(self.filter_flash.event_manager.events), 1)
        self.assertTrue(self.filter_flash.event_manager.events[0]["flash_triggered"])


if __name__ == "__main__":
    unittest.main()
