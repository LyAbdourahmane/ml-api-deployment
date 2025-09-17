import csv
from typing import Optional

from infra.db import SessionLocal
from infra.db_utils import save_input

# Colonnes à garder (toutes les autres seront ignorées)
KEEP_COLS = (
    "PrimaryPropertyType",
    "YearBuilt",
    "NumberofBuildings",
    "NumberofFloors",
    "LargestPropertyUseType",
    "LargestPropertyUseTypeGFA",
)

# Valeurs considérées comme "vides"
EMPTY_TOKENS = {"", "na", "n/a", "none", "null", "nan", "NaN", "NA", "NULL"}


def _is_empty(val: Optional[str]) -> bool:
    if val is None:
        return True
    return str(val).strip() in EMPTY_TOKENS


def _to_int(cell: Optional[str]) -> Optional[int]:
    """Convertit proprement les entiers :
    - '1' -> 1
    - '1.0' -> 1
    - '' / 'NA' / None -> None
    """
    if _is_empty(cell):
        return None
    s = str(cell).strip()
    try:
        # Essaye direct
        return int(s)
    except ValueError:
        # Essaye via float si la valeur est '1.0', '2.000', etc.
        try:
            return int(float(s))
        except ValueError:
            raise ValueError(f"Valeur entière invalide: {cell!r}")


def _to_float(cell: Optional[str]) -> Optional[float]:
    """Convertit proprement les floats :
    - '123.45' -> 123.45
    - '1' -> 1.0
    - '' / 'NA' / None -> None
    """
    if _is_empty(cell):
        return None
    s = str(cell).strip()
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"Valeur flottante invalide: {cell!r}")


def _to_str(cell: Optional[str]) -> Optional[str]:
    """Chaînes normalisées :
    - trim
    - '' / 'NA' / None -> None
    """
    if _is_empty(cell):
        return None
    return str(cell).strip()


def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m infra.ingest_csv path/to/data.csv")
        raise SystemExit(1)

    path = sys.argv[1]
    inserted = 0
    skipped = 0
    errors = 0

    with SessionLocal() as db, open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Vérif de base : s'assurer que les colonnes minimales existent
        missing = [c for c in KEEP_COLS if c not in reader.fieldnames]
        if missing:
            raise SystemExit(
                f"Colonnes manquantes dans le CSV: {missing}. "
                f"Colonnes présentes: {reader.fieldnames}"
            )

        for idx, row in enumerate(reader, start=1):
            try:
                # On lit uniquement les colonnes utiles, tout le reste est ignoré
                data = {
                    "PrimaryPropertyType": _to_str(row.get("PrimaryPropertyType")),
                    "YearBuilt": _to_int(row.get("YearBuilt")),
                    "NumberofBuildings": _to_int(row.get("NumberofBuildings")),
                    "NumberofFloors": _to_int(row.get("NumberofFloors")),
                    "LargestPropertyUseType": _to_str(row.get("LargestPropertyUseType")),
                    "LargestPropertyUseTypeGFA": _to_float(row.get("LargestPropertyUseTypeGFA")),
                }

                # (Optionnel) règles minimales : si tout est vide on skip
                if all(v is None for v in data.values()):
                    skipped += 1
                    continue

                save_input(db, data)
                inserted += 1

            except Exception as e:
                # On log l'index de ligne pour debug rapide
                errors += 1
                print(f"[Ligne {idx}] Erreur d'ingestion: {e}")

        db.commit()

    print(
        f"Ingestion terminée. Insertions: {inserted}, ignorées: {skipped}, erreurs: {errors}."
    )


if __name__ == "__main__":
    main()
