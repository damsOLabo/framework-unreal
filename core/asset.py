import unreal

class BaseAsset:
    """Classe de base pour la création d'assets dans Unreal.

    Args:
        asset_path (str): Le chemin où créer l'asset.
        asset_type (str): Le type d'asset à créer.

    Attributes:
        asset_path (str): Le chemin où créer l'asset.
        asset_type (str): Le type d'asset à créer.
        asset_name (str): Le nom de l'asset à créer.
    """

    def __init__(self, asset_path, asset_type):
        self.asset_path = asset_path
        self.asset_type = asset_type
        self.asset_name = self._get_asset_name()

    def _get_asset_name(self):
        """Définit le nom de l'asset.

        Returns:
            str: Le nom de l'asset.
        """
        raise NotImplementedError("La méthode _get_asset_name doit être définie dans la classe dérivée.")

    def _get_creation_options(self):
        """Définit les options de création de l'asset.

        Returns:
            obj: Les options de création de l'asset.
        """
        raise NotImplementedError("La méthode _get_creation_options doit être définie dans la classe dérivée.")

    def create_asset(self):
        """Crée l'asset.

        Returns:
            obj: L'objet asset créé.
        """
        asset_exists = unreal.EditorAssetLibrary.does_asset_exist(self.asset_path + "/" + self.asset_name)
        if asset_exists:
            unreal.log_warning("L'asset {} existe déjà dans le chemin {}.".format(self.asset_name, self.asset_path))
            return None
        else:
            options = self._get_creation_options()
            asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(self.asset_name, self.asset_path, self.asset_type, options)
            unreal.log("L'asset {} a été créé dans le chemin {}.".format(self.asset_name, self.asset_path))
            return asset

    def save_asset(self, asset):
        """Sauvegarde l'asset.

        Args:
            asset (obj): L'objet asset à sauvegarder.
        """
        unreal.EditorAssetLibrary.save_asset(asset)
        unreal.log("L'asset {} a été sauvegardé.".format(self.asset_name))
