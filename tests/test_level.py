import unittest
import unreal
from ..core import LevelAsset


class TestLevelAsset(unittest.TestCase):
    def setUp(self):
        self.asset_path = "/Game/TestLevel"
        self.level_sequences = ["Sequence1", "Sequence2"]
        self.level_asset = LevelAsset(self.asset_path, self.level_sequences)

    def test_asset_name(self):
        self.assertEqual(self.level_asset._get_asset_name(), "NewLevel")

    def test_creation_options(self):
        options = self.level_asset._get_creation_options()
        self.assertIsInstance(options, unreal.EditorAssetCreationOptions)
        self.assertTrue(options.create_new)
        self.assertFalse(options.save_asset)

    def test_create_level_sequence(self):
        sequence_path = self.asset_path + "/1-Cinematics"
        sequence_name = "NewSequence"
        level_sequence = self.level_asset._create_level_sequence(
            sequence_path, sequence_name
        )

        self.assertIsNotNone(level_sequence)
        self.assertIsInstance(level_sequence, unreal.LevelSequence)
        self.assertEqual(level_sequence.get_name(), sequence_name)

        # Clean up
        unreal.EditorAssetLibrary.delete_asset(level_sequence)

    def test_create_asset(self):
        level = self.level_asset.create_asset()

        self.assertIsNotNone(level)
        self.assertIsInstance(level, unreal.Level)

        # Clean up
        unreal.EditorAssetLibrary.delete_asset(level.get_path_name())


if __name__ == "__main__":
    unittest.main()
