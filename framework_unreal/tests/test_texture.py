import unittest
import unreal
import os.path
from ..core import asset


class TestTextureImporter(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up the test environment.
        """
        self.test_source_path: str = "C:/Textures/test_texture.png"
        self.test_destination_path: str = "/Game/Textures/test_texture"

        # Create a test texture file
        with open(self.test_source_path, "w") as f:
            f.write("test texture file")

    def tearDown(self) -> None:
        """
        Clean up the test environment.
        """
        # Delete the test texture file
        if os.path.exists(self.test_source_path):
            os.remove(self.test_source_path)

        # Delete the imported texture asset
        asset_registry: unreal.AssetRegistryHelpers = (
            unreal.AssetRegistryHelpers.get_asset_registry()
        )
        asset_data: unreal.AssetData = asset_registry.get_asset_by_object_path(
            self.test_destination_path
        )
        if asset_data is not None:
            asset_tools: unreal.AssetToolsHelpers = (
                unreal.AssetToolsHelpers.get_asset_tools()
            )
            asset_tools.delete_asset(asset_data.get_asset())

    def test_import_texture(self) -> None:
        """
        Test importing a texture asset using the TextureImporter class.
        """
        importer: asset.TextureImporter = asset.TextureImporter(
            self.test_source_path, self.test_destination_path
        )
        imported_texture: unreal.Texture = importer.import_texture()
        self.assertIsNotNone(imported_texture)


if __name__ == "__main__":
    unittest.main()
