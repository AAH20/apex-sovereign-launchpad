"""Unit tests for BacklinkMeshGenerator."""

import unittest
from apex_sovereign_launchpad.core.backlink_mesh import BacklinkMeshGenerator
from apex_sovereign_launchpad.core.inventory_parser import InventoryParser


class TestBacklinkMesh(unittest.TestCase):
    def setUp(self):
        self.parser = InventoryParser()
        self.mesh_gen = BacklinkMeshGenerator()
        self.repos = self.parser.load_inventory()

    def test_single_repo_backlink_block(self):
        repo = self.repos[0]
        block = self.mesh_gen.generate_repo_backlink_block(repo, self.repos[:5])
        self.assertIn("Apex Growth Systems LLC", block)
        self.assertIn("Macro Pillar", block)
        self.assertIn("Part of the Sovereign Constellation", block)
        self.assertIn("Ahmed Hassan", block)

    def test_full_portfolio_mesh_build(self):
        blocks, res = self.mesh_gen.build_full_mesh(self.repos)
        self.assertTrue(len(blocks) >= 8)
        self.assertEqual(res.original_repositories_meshed, len(blocks))
        self.assertTrue(res.cross_referral_edges_generated > 0)
        self.assertTrue(res.commercial_hub_referrals_injected > 0)


if __name__ == "__main__":
    unittest.main()
