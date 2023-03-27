from typing import Dict, Type, Optional
import unreal
import re


class BaseAsset:
    """Base class for creating assets in Unreal.

    Args:
        asset_path (str): The path where to create the asset.
        asset_name (str): The name of the asset to create.
        asset_type (Type[unreal.Object]): The type of asset to create.

    Attributes:
        asset_path (str): The path where to create the asset.
        asset_type (Type[unreal.Object]): The type of asset to create.
        asset_name (str): The name of the asset to create.
    """

    def __init__(
        self, asset_path: str, asset_name: str, asset_type: Type[unreal.Object]
    ):
        """Initializes a new instance of the BaseAsset class.

        Args:
            asset_path (str): The path where to create the asset.
            asset_name (str): The name of the asset to create.
            asset_type (Type[unreal.Object]): The type of asset to create.
        """
        self.asset_path: str = asset_path
        self.asset_type: Type[unreal.Object] = asset_type
        self.asset_name: str = self._get_asset_name(asset_name)

    def attribute_name_template(self) -> str:
        """Gets the attribute name template.

        Raises:
            NotImplementedError: If the method is not implemented in the derived class.

        Returns:
            str: The attribute name template.
        """
        raise NotImplementedError(
            "La méthode _get_creation_options doit être définie dans la classe dérivée."
        )

    def is_valid_attribute_name(self, name: str) -> bool:
        """Checks if an attribute name is valid.

        Args:
            name (str): The attribute name to check.

        Returns:
            bool: True if the attribute name is valid; otherwise False.
        """
        pattern = self.attribute_name_template().format(r"\w+")
        return bool(re.match(pattern, name))

    def check_asset_exists(asset_path: str) -> Optional[bool]:
        """Check if an asset exists in Unreal Engine.

        Args:
            asset_path (str): The path to the asset to check.

        Returns:
            Optional[bool]: True if the asset exists, False if it does not exist, and None if an error occurred.
        """
        try:
            return unreal.EditorAssetLibrary.does_asset_exist(asset_path)
        except Exception as e:
            print(f"An error occurred while checking if the asset exists: {e}")
            return None

    def _get_asset_name(self, asset_name: str, key_name: str = "default") -> str:
        """Gets the asset name.

        Args:
            asset_name (str): The base name of the asset.
            key_name (str): The key name for the template. Defaults to "default".

        Returns:
            str: The full name of the asset.
        """
        return self.attribute_name_template().format(asset_name)

    def _get_creation_options(self) -> None:
        """Defines the asset creation options.

        Returns:
            obj: The asset creation options.
        """
        raise NotImplementedError(
            "The _get_creation_options method must be defined in the derived class."
        )

    def create_asset(self) -> unreal.Object:
        """Creates the asset.

        Returns:
            unreal.Object: The created asset object.
        """

        if self.check_asset_exists():
            unreal.log_warning(
                "The asset {} already exists in the path {}.".format(
                    self.asset_name, self.asset_path
                )
            )
            return None
        else:
            options = self._get_creation_options()
            asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
                self.asset_name, self.asset_path, self.asset_type, options
            )
            if asset:
                self.save_asset(asset)
            unreal.log(
                "The asset {} was created in the path {}.".format(
                    self.asset_name, self.asset_path
                )
            )
            return asset

    def save_asset(self, asset: unreal.Object) -> None:
        """Saves the asset.

        Args:
            asset (unreal.Object): The asset object to save.
        """
        unreal.EditorAssetLibrary.save_asset(asset.get_path_name())
        unreal.log("The asset {} has been saved.".format(self.asset_name))


class TextureImporter:
    def __init__(self, source_path: str, destination_path: str) -> None:
        """
        Initializes a new TextureImporter instance.

        :param source_path: The path of the source texture file.
        :param destination_path: The path of the destination texture asset in Unreal Engine.
        """
        self.source_path = source_path
        self.destination_path = destination_path

    def import_texture(self) -> Optional[unreal.Texture]:
        """
        Imports the texture at the source path to Unreal Engine.

        :returns: The imported texture asset, or None if import failed.
        """
        # Create a TextureImportOptions object to configure the import
        import_options = unreal.TextureImportOptions()
        import_options.texture_group = unreal.TextureGroup.TEXTUREGROUP_PIXEL2D
        import_options.sRGB = False
        import_options.convert_to_grayscale = False
        import_options.alpha_source = unreal.TextureAlphaSource.TAS_NONE
        import_options.texture_compression_settings = (
            unreal.TextureCompressionSettings.TC_BC7
        )
        import_options.material_import_name = ""
        import_options.bilinear_filter = True
        import_options.mipmap_generation = (
            unreal.TextureMipGenSettings.TMGS_GENERATE_MIPS
        )
        import_options.alpha_coverage_threshold = 0.0
        import_options.decompress_on_load = False
        import_options.adjust_brightness = 0.0
        import_options.adjust_saturation = 1.0
        import_options.import_as_linear = True
        import_options.aces_color_space = True

        # Import the texture
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        imported_texture = asset_tools.import_asset(
            self.destination_path, self.source_path, import_options
        )
        if imported_texture is None:
            print("Failed to import texture:", self.source_path)
        return imported_texture
