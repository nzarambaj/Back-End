# app/services/settings_service.py
from app.database import db
from app.models.settings import ModalityConfig, WindowPreset


# ── Modality config ───────────────────────────────────────────────────────────

def get_all_modality_configs():
    return ModalityConfig.query.order_by(ModalityConfig.modality).all()


def get_modality_config(modality: str):
    return ModalityConfig.query.filter_by(modality=modality.upper()).first()


def upsert_modality_config(modality: str, data: dict):
    config = ModalityConfig.query.filter_by(modality=modality.upper()).first()
    if not config:
        config = ModalityConfig(modality=modality.upper())
        db.session.add(config)

    fields = [
        "display_name", "default_window_center", "default_window_width",
        "bits_allocated", "color_map", "is_active", "notes"
    ]
    for f in fields:
        if f in data:
            setattr(config, f, data[f])

    db.session.commit()
    return config, None


def delete_modality_config(modality: str):
    config = ModalityConfig.query.filter_by(modality=modality.upper()).first()
    if not config:
        return False, "Modality config not found"
    db.session.delete(config)
    db.session.commit()
    return True, None


# ── Window presets ────────────────────────────────────────────────────────────

def get_presets(modality: str = None):
    q = WindowPreset.query
    if modality:
        q = q.filter_by(modality=modality.upper())
    return q.order_by(WindowPreset.modality, WindowPreset.name).all()


def create_preset(data: dict):
    existing = WindowPreset.query.filter_by(
        modality=data.get("modality", "").upper(),
        name=data.get("name", "")
    ).first()
    if existing:
        return None, "Preset with this name already exists for this modality"

    preset = WindowPreset(
        modality       = data["modality"].upper(),
        name           = data["name"],
        window_center  = float(data["window_center"]),
        window_width   = float(data["window_width"]),
        description    = data.get("description"),
    )
    db.session.add(preset)
    db.session.commit()
    return preset, None


def update_preset(preset_id: int, data: dict):
    preset = WindowPreset.query.get(preset_id)
    if not preset:
        return None, "Preset not found"
    for f in ["name", "window_center", "window_width", "description"]:
        if f in data:
            setattr(preset, f, data[f])
    db.session.commit()
    return preset, None


def delete_preset(preset_id: int):
    preset = WindowPreset.query.get(preset_id)
    if not preset:
        return False, "Preset not found"
    db.session.delete(preset)
    db.session.commit()
    return True, None
