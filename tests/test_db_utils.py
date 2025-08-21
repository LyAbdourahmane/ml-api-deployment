import os
import sys

# Ajout de la racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Importons via le package "infra" (important puisque db_utils utilise des imports relatifs)
from infra.db_utils import (
    save_input,
    save_prediction,
    get_inputs_json,
    get_predictions_json,
)

def test_db_utils_end_to_end():
    data = {
        "PrimaryPropertyType": "Office",
        "YearBuilt": 1999,
        "NumberofBuildings": 1,
        "NumberofFloors": 5,
        "LargestPropertyUseType": "Office",
        "LargestPropertyUseTypeGFA": 1200.0,
    }

    # Sauvegarde de l'input
    input_id = save_input(data)
    assert input_id is not None

    # Sauvegarde de la prédiction
    save_prediction(input_id, 42.0)

    # Vérification via lecture
    inputs = get_inputs_json()
    preds = get_predictions_json()

    # On vérifie que le dernier élément correspond à ce qu'on a inséré
    assert inputs[-1]["PrimaryPropertyType"] == "Office"
    assert preds[-1]["predicted_co2"] == 42.0

