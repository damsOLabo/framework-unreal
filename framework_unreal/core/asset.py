from typing import List, Type, Optional
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


class FBXImporter:
    """
    A class for importing FBX files into Unreal Engine 4.

    Attributes:
    editor_util (unreal.EditorUtilityLibrary): A utility library for working with the Editor.
    asset_tools (unreal.AssetTools): A set of helper functions for creating and manipulating assets.

    Methods:
    import_fbx(fbx_path: str, destination_path: str, asset_name: str, import_animation: bool = False,
                animation_sequence_name: Optional[str] = None) -> unreal.Asset: Imports the FBX file
                located at 'fbx_path' into UE4 at the specified 'destination_path' and 'asset_name'.
    """

    def __init__(self):
        self.editor_util: unreal.EditorUtilityLibrary = unreal.EditorUtilityLibrary()
        self.asset_tools: unreal.AssetTools = unreal.AssetToolsHelpers.get_asset_tools()

    def import_fbx(
        self,
        fbx_path: str,
        destination_path: str,
        asset_name: str,
        import_animation: bool = False,
        animation_sequence_name: Optional[str] = None,
        import_materials: bool = True,
        import_textures: bool = True,
        import_mesh: bool = True,
        replace_existing: bool = True,
    ) -> unreal.Asset:
        """
        Imports an FBX file into UE.

        Args:
        fbx_path (str): The path to the FBX file to be imported.
        destination_path (str): The path in UE4 where the asset should be imported to.
        asset_name (str): The name to give the imported asset.
        import_animation (bool, optional): Whether to import any animations associated with the FBX file.
        animation_sequence_name (str, optional): The name to give any imported animation sequences.
        import_materials (bool, optional): Whether to import materials from the FBX file.
        import_textures (bool, optional): Whether to import textures from the FBX file.
        import_mesh (bool, optional): Whether to import the mesh from the FBX file.
        replace_existing (bool, optional): Whether to replace an existing asset with the same name as the imported asset.

        Returns:
        unreal.Asset: The imported asset.
        """
        import_task: unreal.AssetImportTask = unreal.AssetImportTask()
        import_task.set_editor_property("filename", fbx_path)
        import_task.set_editor_property("destination_path", destination_path)
        import_task.set_editor_property("destination_name", asset_name)
        import_task.set_editor_property("replace_existing", replace_existing)

        options: unreal.FbxImportUI = unreal.FbxImportUI()
        options.set_editor_property("import_mesh", import_mesh)
        options.set_editor_property("import_materials", import_materials)
        options.set_editor_property("import_textures", import_textures)
        options.set_editor_property("import_animations", import_animation)

        import_task.set_editor_property("options", options)

        self.asset_tools.import_asset_tasks([import_task])

        asset_path: str = destination_path + asset_name
        asset: unreal.Asset = unreal.load_asset(asset_path)

        if isinstance(asset, unreal.StaticMesh):
            self.editor_util.set_actor_label("SM_" + asset.name, asset_name)

            # Rename physics asset if it exists
            physics_asset: unreal.PhysicsAsset = asset.get_editor_property(
                "physics_asset"
            )
            if physics_asset:
                self.editor_util.rename_asset(physics_asset, "PA_" + asset_name)

            # Rename skeleton asset if it exists
            skeleton: unreal.Skeleton = asset.get_editor_property("skeleton")
            if skeleton:
                self.editor_util.rename_asset(skeleton, "SK_" + asset_name)

        elif isinstance(asset, unreal.SkeletalMesh):
            self.editor_util.set_actor_label("SKM_" + asset.name, asset_name)

        if import_animation and animation_sequence_name:
            animations: List[unreal.AnimationAsset] = unreal.find_assets(
                asset_path, asset_class=unreal.AnimationAsset
            )
            for anim in animations:
                self.editor_util.rename_asset(anim, animation_sequence_name)

        return asset
