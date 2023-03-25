import unreal
import pytest
from framework_unreal.core.assets import MaterialAsset


@pytest.fixture(scope="module")
def editor_instance():
    # Créer une instance d'Unreal Editor
    unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
    editor_instance = unreal.EditorAssetLibrary.get_editor_world()
    yield editor_instance


def test_material_asset_creation(editor_instance):
    # Créer un nouvel asset de type Material
    material_asset = MaterialAsset(
        asset_path="/Game/Test/Materials/TestMaterial",
        asset_name_template="TestMaterial_{id}",
        editor_instance=editor_instance,
    )

    # Vérifier que l'asset n'existe pas encore
    assert not material_asset.exists()

    # Créer l'asset avec une couleur rouge
    material_asset.create(material_color=(1.0, 0.0, 0.0))

    # Vérifier que l'asset a bien été créé
    assert material_asset.exists()

    # Vérifier que le nom de l'asset a bien été généré selon le template
    assert material_asset.asset_name == "TestMaterial_0"

    # Vérifier que l'asset est bien de type Material
    assert isinstance(material_asset.asset, unreal.Material)

    # Vérifier que la couleur du matériau est bien rouge
    material_color = material_asset.asset.get_base_color()
    assert material_color.r == 1.0
    assert material_color.g == 0.0
    assert material_color.b == 0.0

    # Supprimer l'asset pour nettoyer l'environnement de test
    material_asset.delete()

    # Vérifier que l'asset a bien été supprimé
    assert not material_asset.exists()
