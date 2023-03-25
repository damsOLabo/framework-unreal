import unreal
from . import asset


class LevelAsset(asset.BaseAsset):
    """Classe pour la création d'assets de type Level dans Unreal Engine 4.

    Args:
        asset_path (str): Le chemin où créer l'asset.
        level_sequences (list): La liste des level sequences à ajouter au Level.

    Attributes:
        asset_path (str): Le chemin où créer l'asset.
        level_sequences (list): La liste des level sequences à ajouter au Level.
    """

    def __init__(self, asset_path, level_sequences):
        super(LevelAsset, self).__init__(asset_path, "Level")
        self.level_sequences = level_sequences

    def _get_asset_name(self):
        """Définit le nom de l'asset Level.

        Returns:
            str: Le nom de l'asset Level.
        """
        return "NewLevel"

    def _get_creation_options(self):
        """Définit les options de création de l'asset Level.

        Returns:
            obj: Les options de création de l'asset Level.
        """
        options = unreal.EditorAssetCreationOptions()
        options.set_create_new(True)
        options.set_save_asset(False)
        return options

    def _create_level_sequence(self, sequence_path, sequence_name):
        """Crée un nouvel asset de type LevelSequence.

        Args:
            sequence_path (str): Le chemin où trouver/créer l'asset.
            sequence_name (str): Le nom du nouvel asset LevelSequence.

        Returns:
            obj: L'objet asset LevelSequence créé.
        """
        # Get asset tools
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

        level_sequence = unreal.AssetTools.create_asset(
            asset_tools,
            asset_name=sequence_name,
            package_path=sequence_path,
            asset_class=unreal.LevelSequence,
            factory=unreal.LevelSequenceFactoryNew(),
        )
        # Create a frame rate object, change the numerator to the desired fps number
        frame_rate = unreal.FrameRate(numerator=60, denominator=1)
        # Set the display rate
        level_sequence.set_display_rate(frame_rate)

        unreal.EditorAssetLibrary.save_asset(level_sequence)
        unreal.log(
            "L'asset LevelSequence {} a été créé dans le chemin {}.".format(
                sequence_name, sequence_path
            )
        )
        return level_sequence

    def create_asset(self):
        """Crée l'asset Level.

        Returns:
            obj: L'objet asset Level créé.
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
        for sequence_name in self.level_sequences:
            sequence_asset = unreal.EditorAssetLibrary.find_asset_data(
                cinematics_path + "/" + sequence_name
            )
            if sequence_asset is None:
                sequence_asset = self._create_level_sequence(sequence_name)
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
