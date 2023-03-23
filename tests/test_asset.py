import unreal
import unittest
from ..core.asset import BaseAsset

class TestBaseAsset(unittest.TestCase):
    """
    Classe de test pour la classe BaseAsset.

    """
    def setUp(self):
        """
        Initialisation des paramètres pour les tests.

        """
        self.asset_path = "/Game/Tests/TestAssets"
        self.asset_type = "Texture2D"
        self.base_asset = BaseAsset(self.asset_path, self.asset_type)

    def test_get_asset_name(self):
        """
        Test de la méthode _get_asset_name.

        """
        with self.assertRaises(NotImplementedError):
            self.base_asset._get_asset_name()

    def test_get_creation_options(self):
        """
        Test de la méthode _get_creation_options.

        """
        with self.assertRaises(NotImplementedError):
            self.base_asset._get_creation_options()

    def test_create_asset(self):
        """
        Test de la méthode create_asset.

        """
        asset = self.base_asset.create_asset()
        self.assertIsNotNone(asset)
        asset_exists = unreal.EditorAssetLibrary.does_asset_exist(self.asset_path + "/" + self.base_asset.asset_name)
        self.assertTrue(asset_exists)

    def test_save_asset(self):
        """
        Test de la méthode save_asset.

        """
        asset = self.base_asset.create_asset()
        self.base_asset.save_asset(asset)
        asset_exists = unreal.EditorAssetLibrary.does_asset_exist(self.asset_path + "/" + self.base_asset.asset_name)
        self.assertTrue(asset_exists)

if __name__ == '__main__':
    unittest.main()