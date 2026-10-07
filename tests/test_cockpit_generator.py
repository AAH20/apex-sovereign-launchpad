"""Unit tests for CockpitGenerator."""

import unittest
from apex_sovereign_launchpad.core.cockpit_generator import CockpitGenerator
from apex_sovereign_launchpad.core.inventory_parser import InventoryParser


class TestCockpitGenerator(unittest.TestCase):
    def setUp(self):
        self.parser = InventoryParser()
        self.generator = CockpitGenerator()
        self.repos = self.parser.load_inventory()

    def test_generate_html_dashboard(self):
        html = self.generator.generate_html(self.repos)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Apex Growth Systems LLC", html)
        self.assertIn("a2zsoc Corp", html)
        self.assertIn("InvestorOS LLC", html)
        self.assertIn("Sovereign Rails Corp", html)
        self.assertIn("ComputerUse Corp", html)
        self.assertTrue(len(html) > 5000)


if __name__ == "__main__":
    unittest.main()
