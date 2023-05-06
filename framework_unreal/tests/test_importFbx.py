import unreal
import unittest
from ..core import asset


class TestFBXImporter(unittest.TestCase):
    def test_import_fbx(self):
        fbx_path = "path/to/fbx_file.fbx"
        destination_path = "/Game/Imported/"
        asset_name = "MyImportedAsset"
        import_animation = True
        animation_sequence_name = "MyAnimation"
        import_materials = True
        import_textures = True
        import_mesh = True
        replace_existing = True

        importer = asset.FBXImporter()
        new_asset = importer.import_fbx(
            fbx_path,
            destination_path,
            asset_name,
            import_animation,
            animation_sequence_name,
            import_materials,
            import_textures,
            import_mesh,
            replace_existing,
        )

        # Check that the asset was imported successfully
        self.assertIsInstance(new_asset, unreal.Asset)

        # Check that the asset has the correct name
        self.assertEqual(new_asset.name, asset_name)

        # Check that animations were imported and have the correct name
        if import_animation and animation_sequence_name:
            animations = unreal.find_assets(
                destination_path + asset_name, asset_class=unreal.AnimationAsset
            )
            self.assertGreater(len(animations), 0)
            for anim in animations:
                self.assertEqual(anim.name, animation_sequence_name)


if __name__ == "__main__":
    unittest.main()
