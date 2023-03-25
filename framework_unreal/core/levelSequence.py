import unreal
from . import asset


class LevelSequenceAsset(asset.BaseAsset):
    """A class to handle LevelSequence asset creation and management.

    This class inherits from the BaseAsset class.

    Attributes:
        asset_path (str): The path where the LevelSequence asset will be created.
        asset_name (str): The name of the LevelSequence asset.
    """

    def __init__(self, asset_path: str, asset_name: str):
        """Initializes a new LevelSequenceAsset object with the given asset name and path.

        Args:
            asset_name (str): The name of the LevelSequence asset.
            asset_path (str): The path where the LevelSequence asset will be created.
        """
        super().__init__(asset_name, asset_path, unreal.LevelSequence)

    def attribute_name_template(self) -> str:
        """Returns the attribute name template for the LevelSequence.

        Returns:
            str: The attribute name template for the LevelSequence.
        """
        return "LS_{asset_name}"

    def _get_creation_options(self) -> object:
        """Defines the creation options for the LevelSequence asset.

        Returns:
            object: The creation options for the LevelSequence asset.
        """
        return unreal.LevelSequenceFactoryNew()
