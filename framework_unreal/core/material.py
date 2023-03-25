import unreal
from . import asset


class MaterialAsset(asset.BaseAsset):
    """Class for creating Material type assets.

    Args:
        asset_path (str): The path where the asset will be created.
        template_name (str): The template to use for the asset name. Must contain the {asset_type} field.

    Attributes:
        asset_path (str): The path where the asset will be created.
        template_name (str): The template to use for the asset name. Must contain the {asset_type} field.

    Raises:
        NotImplementedError: If the _get_asset_name or _get_creation_options methods are not implemented in
        the derived class.

    """

    def __init__(
        self, asset_path: str, asset_name: str, is_material_instance=False
    ) -> None:
        """Initializes a new MaterialAsset object with the given asset name and path.

        Args:
            asset_name (str): The name of the LevelSequence asset.
            asset_path (str): The path where the LevelSequence asset will be created.
            is_material_instance (bool): The type of Material will be create.
        """
        if is_material_instance:
            super().__init__(asset_path, asset_name, unreal.MaterialInstance)
        else:
            super().__init__(asset_path, asset_name, unreal.Material)
        self.is_material_instance = is_material_instance

    def _master_material(self) -> str:
        """Returns the master material asset path to instanciate.

        Returns:
            str: The asset path of the master material to instanciate.
        """
        return "/Engine/"

    def attribute_name_template(self) -> str:
        """Returns the attribute name template for the Material.

        Returns:
            str: The attribute name template for the Material.
        """
        if self.is_material_instance:
            return "MM_{asset_name}"
        else:
            return "MI_{asset_name}"

    def _get_creation_options(self) -> unreal.MaterialFactoryNew:
        """Defines the creation options for the Material type asset.

        Returns:
            unreal.MaterialFactoryNew: The creation options.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.

        """
        return unreal.MaterialFactoryNew()
