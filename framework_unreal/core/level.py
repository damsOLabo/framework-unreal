from typing import Dict
import unreal

from . import asset, levelSequence


class LevelAsset(asset.BaseAsset):
    """Class for creating Level assets.

    Args:
        asset_path (str): The path where to create the asset.
        level_sequences (list): The list of level sequences to add to the Level.

    Attributes:
        asset_path (str): The path where to create the asset.
        level_sequences (dict): A dictionary where each key is the name of a level sequence,
                                and each value is the path where to find/create the asset.
    """

    def __init__(
        self, asset_path: str, asset_name: str, level_sequences: Dict[str, str]
    ):
        super(LevelAsset, self).__init__(asset_path, asset_name, unreal.World)
        self.level_sequences = level_sequences

    def attribute_name_template(self) -> str:
        """Returns the attribute name template for the Level.

        Returns:
            str: The attribute name template for the Level.
        """
        return "MAP_{asset_name}"

    def _get_creation_options(self) -> unreal.WorldFactory:
        """Defines the creation options for the Level asset.

        Returns:
            obj: The creation options for the Level asset.
        """
        return unreal.WorldFactory()

    def _create_level_sequence(
        self, sequence_path: str, sequence_name: str
    ) -> unreal.LevelSequence:
        """Creates a new LevelSequence asset.

        Args:
            sequence_path (str): The path where to find/create the asset.
            sequence_name (str): The name of the new LevelSequence asset.

        Returns:
            obj: The created LevelSequence asset object.
        """
        lvl_seq = levelSequence.LevelSequenceAsset(sequence_path, sequence_name)
        return lvl_seq.create_asset()

    def create_asset(self) -> unreal.Level:
        """Creates the Level asset.

        Returns:
            obj: The created Level asset object.
        """
        level: unreal = super(LevelAsset, self).create_asset()
        if level is None:
            return None

        # Ajoute le dossier 1-Cinematics s'il n'existe pas
        cinematics_path = self.asset_path + "/1-Cinematics"
        if not unreal.EditorAssetLibrary.does_directory_exist(cinematics_path):
            unreal.AssetToolsHelpers.get_asset_tools().make_directory(cinematics_path)
            unreal.log(
                "Le dossier 1-Cinematics a été créé dans le chemin {}.".format(
                    self.asset_path
                )
            )

        # Ajoute les level sequences à la liste des acteurs possessables du Level
        for sequence_name, sequence_path in self.level_sequences.items():
            sequence_asset = unreal.EditorAssetLibrary.find_asset_data(
                cinematics_path + "/" + sequence_name
            )
            if sequence_asset is None:
                sequence_asset = self._create_level_sequence(
                    sequence_path, sequence_name
                )
            sequence_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
                sequence_asset, unreal.Vector(0, 0, 0)
            )
            unreal.EditorLevelLibrary.add_actor_to_level(
                sequence_actor, level.get_world()
            )
            # Link l'actor au dossier 1-Cinematics
            sequence_actor.set_folder_path("1-Cinematics")
            unreal.log(
                "L'asset LevelSequence {} a été ajouté à la liste des acteurs possessables du Level.".format(
                    sequence_name
                )
            )

        return level
