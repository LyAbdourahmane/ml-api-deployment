# gradio.py
import os, sys
from datetime import datetime
import requests
import gradio as gr

# =======================
# CONFIG
# =======================
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
API_KEY = os.getenv("API_KEY")  # facultatif (si AUTH activée côté API)

# --- mes informations ---
AUTHOR_NAME = "Par Abdourahamane LY"
AUTHOR_EMAIL = "lyabdourahamane66@gmail.com"
AUTHOR_LINKEDIN = "https://www.linkedin.com/in/abdourahamane-ly-ab322a35b/"
AUTHOR_GITHUB = "https://github.com/LyAbdourahmane"
AUTHOR_SITE = "https://lyabdourahamane.netlify.app/"

print(f"[Gradio] API_BASE_URL = {API_BASE_URL}", file=sys.stderr)

def _headers():
    h = {"Content-Type": "application/json"}
    if API_KEY:
        h["X-API-Key"] = API_KEY
    return h

# =======================
# APPELS API
# =======================
def predict_co2(primary_property_type, year_built, number_of_buildings,
                number_of_floors, largest_property_use_type, largest_property_use_type_gfa):
    payload = {
        "PrimaryPropertyType": primary_property_type,
        "YearBuilt": int(year_built),
        "NumberofBuildings": int(number_of_buildings),
        "NumberofFloors": int(number_of_floors),
        "LargestPropertyUseType": largest_property_use_type,
        "LargestPropertyUseTypeGFA": float(largest_property_use_type_gfa),
    }
    try:
        r = requests.post(f"{API_BASE_URL}/predict", json=payload, headers=_headers(), timeout=20)
        if r.status_code != 200:
            return f"**Erreur API** : {r.status_code} — {r.text}"
        result = r.json()
        perf = (result.get("model_info") or {}).get("performance", {})
        desc = (result.get("model_info") or {}).get("description", "")
        unit = result.get("unit", "")

        return (
            f"### Prédiction CO₂ : **{result['prediction']:.2f} {unit}**\n\n"
            f"**Modèle :** {(result.get('model_info') or {}).get('model_type','-')}\n"
            f"- RMSE : {perf.get('rmse','-')}\n"
            f"- MAE : {perf.get('mae','-')}\n"
            f"- WAPE : {perf.get('wape','-')}\n"
            f"- R² : {perf.get('r2_score','-')}\n\n"
            f"{desc}"
        )
    except requests.exceptions.ConnectionError:
        return "Impossible de se connecter à l'API. Vérifie que l’API est lancée et que API_BASE_URL est correct."
    except Exception as e:
        return f"Erreur : {e}"

def fetch_model_info():
    try:
        r = requests.get(f"{API_BASE_URL}/model_info", headers=_headers(), timeout=15)
        r.raise_for_status()
        m = r.json()
        perf = m.get("performance", {})
        return (
            f"**Modèle :** {m.get('model_type','-')}\n"
            f"- RMSE : {perf.get('rmse','-')}\n"
            f"- MAE : {perf.get('mae','-')}\n"
            f"- WAPE : {perf.get('wape','-')}\n"
            f"- R² : {perf.get('r2_score','-')}\n\n"
            f"{m.get('description','')}"
        )
    except Exception as e:
        return f"Impossible de récupérer les infos modèle : {e}"

# =======================
# UI
# =======================
property_types = [
    "Other", "Small- and Mid-Sized Office", "Large Office",
    "Warehouse", "Retail Store", "Mixed Use Property", "Hotel"
]
use_types = [
    "Office", "Other", "Non-Refrigerated Warehouse", "Retail Store", "Hotel",
    "Worship Facility", "Medical Office", "Supermarket/Grocery Store",
    "Distribution Center", "K-12 School", "Other - Recreation",
    "Senior Care Community", "Other - Entertainment/Public Assembly",
    "College/University", "Parking", "Self-Storage Facility"
]

with gr.Blocks(title="Prédiction CO₂ des Bâtiments") as demo:
    gr.Markdown("## Prédicteur d'Émissions de CO₂ — bâtiments non résidentiels (Seattle)")

    with gr.Row():
        gr.Markdown(
            f"**{AUTHOR_NAME}** — "
            f"[Email]({f'mailto:{AUTHOR_EMAIL}'}) · "
            f"[LinkedIn]({AUTHOR_LINKEDIN}) · "
            f"[GitHub]({AUTHOR_GITHUB}) · "
            f"[Site]({AUTHOR_SITE})"
        )

    with gr.Row():
        primary_type = gr.Dropdown(property_types, label="Type de Propriété Principal", value="Small- and Mid-Sized Office")
        year_built = gr.Number(label="Année de Construction", value=2000, minimum=1800, maximum=datetime.now().year)
        num_buildings = gr.Number(label="Nombre de Bâtiments", value=1, minimum=1)

    with gr.Row():
        num_floors = gr.Number(label="Nombre d'Étages", value=4, minimum=0)
        largest_use_type = gr.Dropdown(use_types, label="Plus grand type d’usage", value="Office")
        gfa = gr.Number(label="Surface du plus grand usage (ft²)", value=10000, minimum=10)

    with gr.Row():
        predict_btn = gr.Button("Prédire", variant="primary")
        info_btn = gr.Button("Infos modèle")

    prediction_md = gr.Markdown()
    info_md = gr.Markdown()

    predict_btn.click(
        predict_co2,
        inputs=[primary_type, year_built, num_buildings, num_floors, largest_use_type, gfa],
        outputs=prediction_md
    )
    info_btn.click(fetch_model_info, outputs=info_md)

    with gr.Accordion("À propos", open=False):
        gr.Markdown(
            "- **Stack** : FastAPI, SQLAlchemy, PostgreSQL, scikit-learn/XGBoost, Gradio\n"
            "- **But** : démo de prédiction CO₂ et traçabilité (inputs/outputs en base)\n"
            "- **Contexte** : modèle entraîné sur données de la ville de Seattle — prudence hors distribution\n"
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port, share=True, debug=False)
