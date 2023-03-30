from typing import Type, Optional, Union, List, Dict
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
        """Initialize a new instance of the BaseAsset class.

        Args:
            asset_path (str): The path where to create the asset.
            asset_name (str): The name of the asset to create.
            asset_type (Type[unreal.Object]): The type of asset to create.
        """
        self.asset_path: str = asset_path
        self.asset_type: Type[unreal.Object] = asset_type
        self.asset_name: str = self._get_asset_name(asset_name)

    def attribute_name_template(self) -> str:
        """Get the attribute name template.

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

    def check_asset_exists(self, asset_path: str) -> Optional[bool]:
        """Check if an asset exists in Unreal Engine.

        Args:
            asset_path (str): The path to the asset to check.

        Returns:
            Optional[bool]: True if the asset exists, False if it does not exist,
            and None if an error occurred.
        """
        try:
            return unreal.EditorAssetLibrary.does_asset_exist(asset_path)
        except Exception as e:
            print(f"An error occurred while checking if the asset exists: {e}")
            return None

    def _get_asset_name(self, asset_name: str, key_name: str = "default") -> str:
        """Get the asset name.

        Args:
            asset_name (str): The base name of the asset.
            key_name (str): The key name for the template. Defaults to "default".

        Returns:
            str: The full name of the asset.
        """
        return self.attribute_name_template().format(asset_name)

    def _get_creation_options(self) -> None:
        """Define the asset creation options.

        Returns:
            obj: The asset creation options.
        """
        raise NotImplementedError(
            "The _get_creation_options method must be defined in the derived class."
        )

    def create_asset(self) -> unreal.Object:
        """Create the asset.

        Returns:
            unreal.Object: The created asset object.
        """
        if self.check_asset_exists(self.asset_path):
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
        """Save the asset.

        Args:
            asset (unreal.Object): The asset object to save.
        """
        unreal.EditorAssetLibrary.save_asset(asset.get_path_name())
        unreal.log("The asset {} has been saved.".format(self.asset_name))


class FBXImporter:
    """
    A class for importing FBX files into Unreal Engine 4.

    Attributes:
    asset_tools (unreal.AssetTools): A set of helper functions for creating and manipulating assets.

    Methods:
    import_fbx(fbx_path: str, destination_path: str, asset_name: str, import_animation: bool = False,
                animation_sequence_name: Optional[str] = None) -> unreal.Asset: Imports the FBX file
                located at 'fbx_path' into UE4 at the specified 'destination_path' and 'asset_name'.
    """  # noqa

    def __init__(self):
        """Initialize a new instance of the FBXImporter class."""
        self.asset_tools: unreal.AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
        self.asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()

    def _set_task(
        self,
        fbx_path: str,
        destination_path: str,
        asset_name: str,
        replace_existing: bool = True,
    ) -> unreal.AssetImportTask:
        """Create an import task for an FBX file.

        Args:
            fbx_path (str): The path to the FBX file to be imported.
            destination_path (str): The path in UE4 where the asset should be imported to.
            asset_name (str): The name to give the imported asset
            replace_existing (bool): Whether to replace an existing asset with the same name.

        Returns:
            unreal.AssetImportTask: The import task.
        """  # noqa
        task: unreal.AssetImportTask = unreal.AssetImportTask()
        task.filename = fbx_path
        task.destination_path = destination_path
        task.destination_name = asset_name
        task.replace_existing = replace_existing
        return task

    def set_fbx(
        self,
        fbx_path: str,
        destination_path: str,
        asset_name: str,
        import_animation: bool = False,
        import_materials: bool = True,
        import_textures: bool = True,
        import_mesh: bool = True,
        replace_existing: bool = True,
    ) -> unreal.AssetImportTask:
        """Import an FBX file into UE.

        Args:
            fbx_path (str): The path to the FBX file to be imported.
            destination_path (str): The path in UE4 where the asset should be imported to.
            asset_name (str): The name to give the imported asset.
            import_animation (bool, optional): Whether to import any animations associated with the FBX file.
            import_materials (bool, optional): Whether to import materials from the FBX file.
            import_textures (bool, optional): Whether to import textures from the FBX file.
            import_mesh (bool, optional): Whether to import the mesh from the FBX file.
            replace_existing (bool, optional): Whether to replace an existing asset with the same name as the imported asset.

        Returns:
            unreal.AssetImportTask: The imported asset.
        """  # noqa
        task: unreal.AssetImportTask = self._set_task(
            fbx_path, destination_path, asset_name, replace_existing
        )
        options: unreal.FbxImportUI = unreal.FbxImportUI()
        options.import_mesh = import_mesh
        options.import_materials = import_materials
        options.import_textures = import_textures
        options.import_animations = import_animation

        task.options = options
        return task

    def import_fbx(
        self,
        inputs: List[Dict],
        import_animation: bool = False,
        import_materials: bool = True,
        import_textures: bool = True,
        import_mesh: bool = True,
        replace_existing: bool = True,
    ) -> None:
        """Import an FBX file into unreal.

        Args:
            inputs (List[Dict]): [
                    {
                        'file_path': 'path/to/fbx/file.fbx',
                        'destination_path': '/Game/Content/',
                        'asset_name': 'name_of_asset'
                    }
                ], datas to process.
            import_animation (bool, optional): Whether to import any animations
                                            associated with the FBX file.
            import_materials (bool, optional): Whether to import materials from the FBX file.
            import_textures (bool, optional): Whether to import textures from the FBX file.
            import_mesh (bool, optional): Whether to import the mesh from the FBX file.
            replace_existing (bool, optional): Whether to replace an existing asset with the same name as the imported asset.

        Returns:
            unreal.FbxImportUI: The imported asset.
        """  # noqa
        tasks = []
        for asset_input in inputs:
            task = self.set_fbx(
                asset_input["file_path"],
                asset_input["destination_path"],
                asset_input["asset_name"],
                import_animation=import_animation,
                import_materials=import_materials,
                import_textures=import_textures,
                import_mesh=import_mesh,
                replace_existing=replace_existing,
            )
            tasks.append(task)
        self.asset_tools.import_asset_tasks(tasks)
        self.rename_assets(inputs, import_animation)

    def rename_assets(self, inputs: List[Dict], import_animation: bool = False) -> None:
        """Rename asset from inputs.

        Args:
            inputs (List[Dict]): [
                    {
                        'file_path': 'path/to/fbx/file.fbx',
                        'destination_path': '/Game/Content/',
                        'asset_name': 'name_of_asset'
                    }
                ], datas to process.
            import_animation (bool, optional): Whether to import any animations
                                            associated with the FBX file.
        """
        assets_to_rename = []
        for asset_input in inputs:
            destination_path = asset_input["destination_path"]
            asset_name = asset_input["asset_name"]

            asset_path: str = destination_path + "/" + asset_name
            asset: unreal.Object = unreal.load_asset(asset_path)

            if isinstance(asset, unreal.SkeletalMesh):
                skeletal_rename = unreal.AssetRenameData(
                    asset, destination_path, "SKM_" + asset_name
                )
                assets_to_rename.append(skeletal_rename)

                # Rename physics asset if it exists
                physics_asset: unreal.PhysicsAsset = asset.get_editor_property(
                    "physics_asset"
                )
                if physics_asset:
                    physics_rename = unreal.AssetRenameData(
                        physics_asset, destination_path, "PA_" + asset_name
                    )
                    assets_to_rename.append(physics_rename)

                # Rename skeleton asset if it exists
                skeleton: unreal.Skeleton = asset.get_editor_property("skeleton")
                if skeleton:
                    skeleton_rename = unreal.AssetRenameData(
                        skeleton, destination_path, "SKL_" + asset_name
                    )
                    assets_to_rename.append(skeleton_rename)

            elif isinstance(asset, unreal.StaticMesh):
                assets_to_rename.append(asset)

            if import_animation:
                assets_in_package = self.asset_reg.get_assets_by_path(destination_path)
                for asset_in_package in assets_in_package:
                    if asset_in_package.asset_class == unreal.AnimationAsset:
                        name = asset_in_package.asset_name()
                        if name.startswith("AS_"):
                            continue
                        animseq_rename = unreal.AssetRenameData(
                            asset_in_package,
                            destination_path,
                            "AS_" + asset_name + name,
                        )

                        assets_to_rename.append(animseq_rename)

        self.asset_tools.rename_assets(assets_to_rename)
