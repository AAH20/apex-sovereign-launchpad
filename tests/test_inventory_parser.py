"""Unit tests for InventoryParser and repository categorization."""

import unittest
from apex_sovereign_launchpad.core.inventory_parser import InventoryParser
from apex_sovereign_launchpad.core.models import MacroPillar


class TestInventoryParser(unittest.TestCase):
    def setUp(self):
        self.parser = InventoryParser()

    def test_load_inventory_not_empty(self):
        repos = self.parser.load_inventory()
        self.assertTrue(len(repos) >= 8)  # At least fallback or 554 repos
        originals = [r for r in repos if r.inventory_class == "original"]
        self.assertTrue(len(originals) >= 8)

    def test_pillar_classification(self):
        repos = self.parser.load_inventory()
        pillars = {r.macro_pillar for r in repos}
        # Must have categorized into multiple pillars
        self.assertTrue(len(pillars) >= 3)

    def test_commercial_hub_mapping(self):
        repos = self.parser.load_inventory()
        for r in repos:
            self.assertIn(r.target_commercial_hub, ["a2zsoc", "investor_os", "sovereign_rails", "computer_use"])


if __name__ == "__main__":
    unittest.main()
