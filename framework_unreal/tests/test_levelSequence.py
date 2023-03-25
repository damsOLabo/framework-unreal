import unreal
import pytest
from framework_unreal.core import LevelSequenceAsset


@pytest.fixture(scope="module")
def unreal_level_sequence_asset():
    unreal.EditorAssetLibrary.delete_asset("/Game/Test/Test_Sequence", True)
    yield LevelSequenceAsset("/Game/Test/Test_Sequence")
    unreal.EditorAssetLibrary.delete_asset("/Game/Test/Test_Sequence", True)


def test_create_level_sequence_asset(unreal_level_sequence_asset):
    """
    Test if LevelSequenceAsset can create a Level Sequence asset.
    """
    assert unreal.EditorAssetLibrary.does_asset_exist("/Game/Test/Test_Sequence")
    assert isinstance(unreal_level_sequence_asset.asset, unreal.LevelSequence)