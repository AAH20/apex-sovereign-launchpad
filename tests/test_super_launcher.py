"""Unit tests for SuperLauncher campaign synthesizer."""

import unittest
from apex_sovereign_launchpad.core.inventory_parser import InventoryParser
from apex_sovereign_launchpad.core.models import MacroPillar
from apex_sovereign_launchpad.core.super_launcher import SuperLauncher


class TestSuperLauncher(unittest.TestCase):
    def setUp(self):
        self.parser = InventoryParser()
        self.launcher = SuperLauncher()
        self.repos = self.parser.load_inventory()

    def test_generate_wave_1_np_hard(self):
        pillar_repos = [r for r in self.repos if r.macro_pillar == MacroPillar.NP_HARD_MICROSECOND]
        manifest = self.launcher.generate_manifest(1, MacroPillar.NP_HARD_MICROSECOND, pillar_repos)
        self.assertEqual(manifest.wave_number, 1)
        self.assertIn("Show HN", manifest.show_hn_title)
        self.assertTrue(len(manifest.x_thread_bullets) >= 3)
        self.assertTrue(manifest.anti_slop_metrics.is_valid_technical_copy)

    def test_generate_wave_2_fintech(self):
        pillar_repos = [r for r in self.repos if r.macro_pillar == MacroPillar.SOVEREIGN_FINTECH_RAILS]
        manifest = self.launcher.generate_manifest(2, MacroPillar.SOVEREIGN_FINTECH_RAILS, pillar_repos)
        self.assertEqual(manifest.wave_number, 2)
        self.assertEqual(manifest.target_hub_id, "sovereign_rails")
        self.assertTrue(manifest.anti_slop_metrics.is_valid_technical_copy)


if __name__ == "__main__":
    unittest.main()
