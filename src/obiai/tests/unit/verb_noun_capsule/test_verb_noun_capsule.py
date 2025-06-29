"""
Unit tests for VerbNounCapsule
QA_LAYER: UNIT
QA_STANDARD: PolyCore QA Validation Plan
AEGIS_COMPLIANCE: Mathematical verification required
"""

import unittest
from obiai.core.verb_noun_capsule import VerbNounCapsule


class TestVerbNounCapsule(unittest.TestCase):
    """Unit tests for the VerbNounCapsule representation."""

    def test_cost_and_constraints(self):
        """Verify cost calculation and constraint derivation."""
        capsule = VerbNounCapsule("running", "test", {"risk": 0.5})

        self.assertEqual(capsule.action, "running")
        self.assertEqual(capsule.object, "test")
        self.assertIsInstance(capsule.cost_weight, float)
        self.assertGreaterEqual(capsule.cost_weight, 0.0)
        self.assertIn("action_type", capsule.schema_constraints)
        self.assertEqual(capsule.schema_constraints["object_required"], "test")


if __name__ == "__main__":
    unittest.main()
