# app/services/dicom_service.py
import os
import uuid
import numpy as np
from pathlib import Path
from datetime import datetime

import pydicom
from pydicom.errors import InvalidDicomError
from PIL import Image

from flask import current_app
from app.database import db
from app.models.dicom import Study, Series, Instance


# ── Upload & parse ────────────────────────────────────────────────────────────

def save_dicom_file(file, patient_db_id: int, worklist_id: int = None):
    """
    Accept a FileStorage object, save to disk, parse DICOM tags,
    persist Study/Series/Instance records, return the Instance.
    """
    storage_root = Path(current_app.config["DICOM_STORAGE_PATH"])

    # Read and validate
    raw = file.read()
    try:
        ds = pydicom.dcmread(pydicom.filebase.DicomBytesIO(raw))
    except InvalidDicomError:
        return None, "File is not a valid DICOM file"

    # Extract UIDs
    study_uid    = _tag(ds, "StudyInstanceUID")  or str(uuid.uuid4())
    series_uid   = _tag(ds, "SeriesInstanceUID") or str(uuid.uuid4())
    instance_uid = _tag(ds, "SOPInstanceUID")    or str(uuid.uuid4())
    modality     = _tag(ds, "Modality")          or "OT"

    # Build storage path:  storage_root / patient_id / study_uid / series_uid / instance.dcm
    dest_dir = storage_root / str(patient_db_id) / _safe(study_uid) / _safe(series_uid)
    dest_dir.mkdir(parents=True, exist_ok=True)
    file_path = dest_dir / f"{_safe(instance_uid)}.dcm"
    file_path.write_bytes(raw)

    # ── Study ──────────────────────────────────────────────────────────────
    study = Study.query.filter_by(study_uid=study_uid).first()
    if not study:
        study = Study(
            study_uid   = study_uid,
            patient_id  = patient_db_id,
            worklist_id = worklist_id,
            modality    = modality,
            study_date  = _parse_da(ds.get("StudyDate")),
            description = _tag(ds, "StudyDescription"),
        )
        db.session.add(study)
        db.session.flush()

    # ── Series ─────────────────────────────────────────────────────────────
    series = Series.query.filter_by(series_uid=series_uid).first()
    if not series:
        series = Series(
            series_uid    = series_uid,
            study_id      = study.id,
            modality      = modality,
            series_number = _int_tag(ds, "SeriesNumber"),
            description   = _tag(ds, "SeriesDescription"),
        )
        db.session.add(series)
        db.session.flush()

    # ── Instance ───────────────────────────────────────────────────────────
    if Instance.query.filter_by(instance_uid=instance_uid).first():
        return None, "Instance already exists"

    wc, ww = _window(ds, modality)
    instance = Instance(
        instance_uid    = instance_uid,
        series_id       = series.id,
        instance_number = _int_tag(ds, "InstanceNumber"),
        file_path       = str(file_path),
        file_size       = len(raw),
        rows            = getattr(ds, "Rows",         None),
        columns         = getattr(ds, "Columns",      None),
        bits_allocated  = getattr(ds, "BitsAllocated", None),
        window_center   = wc,
        window_width    = ww,
    )
    db.session.add(instance)
    db.session.commit()
    return instance, None


# ── Image reconstruction ──────────────────────────────────────────────────────

def get_instance_image(instance_id: int, window_center: float = None, window_width: float = None):
    """
    Return a PIL Image from the DICOM pixel array, with W/L applied.
    Handles US / XR / CT / MRI.
    """
    instance = Instance.query.get(instance_id)
    if not instance:
        return None, "Instance not found"

    try:
        ds = pydicom.dcmread(instance.file_path)
    except Exception as e:
        return None, str(e)

    modality = _tag(ds, "Modality") or "OT"
    wc = window_center or instance.window_center
    ww = window_width  or instance.window_width

    try:
        if modality == "US":
            img = _reconstruct_us(ds)
        else:
            img = _reconstruct_gray(ds, wc, ww, modality)
    except Exception as e:
        return None, f"Reconstruction error: {e}"

    return img, None


# ── Per-modality reconstruction ───────────────────────────────────────────────

def _reconstruct_us(ds):
    """Ultrasound — typically RGB or palette color."""
    pixel_array = ds.pixel_array
    if pixel_array.ndim == 3 and pixel_array.shape[2] == 3:
        return Image.fromarray(pixel_array.astype(np.uint8), mode="RGB")
    if pixel_array.ndim == 4:
        # multi-frame cine — return first frame
        return Image.fromarray(pixel_array[0].astype(np.uint8), mode="RGB")
    return Image.fromarray(pixel_array.astype(np.uint8))


def _reconstruct_gray(ds, window_center, window_width, modality):
    """XR / CT / MRI — grayscale with windowing."""
    pixel_array = ds.pixel_array.astype(np.float32)

    # Apply rescale slope/intercept (CT HU units)
    slope     = float(getattr(ds, "RescaleSlope",     1))
    intercept = float(getattr(ds, "RescaleIntercept", 0))
    pixel_array = pixel_array * slope + intercept

    # Fallback window if none provided
    if not window_center or not window_width:
        window_center, window_width = _default_window(modality, pixel_array)

    # Apply windowing
    lo = window_center - window_width / 2
    hi = window_center + window_width / 2
    pixel_array = np.clip(pixel_array, lo, hi)
    pixel_array = ((pixel_array - lo) / (hi - lo) * 255).astype(np.uint8)

    # Multi-frame (CT volume) — return middle slice
    if pixel_array.ndim == 3:
        mid = pixel_array.shape[0] // 2
        pixel_array = pixel_array[mid]

    return Image.fromarray(pixel_array, mode="L")


# ── Default window presets per modality ───────────────────────────────────────

MODALITY_WINDOWS = {
    "CT":  {"brain":   (40,   80),
            "lung":    (-600, 1500),
            "bone":    (400,  1800),
            "default": (40,   400)},
    "XR":  {"default": (2048, 4096)},
    "MRI": {"default": (500,  1000)},
    "OT":  {"default": (128,  256)},
}

def _default_window(modality: str, pixel_array: np.ndarray):
    presets = MODALITY_WINDOWS.get(modality, MODALITY_WINDOWS["OT"])
    wc, ww  = presets["default"]
    return wc, ww


# ── Queries ───────────────────────────────────────────────────────────────────

def get_studies(patient_id: int = None, modality: str = None, page=1, per_page=20):
    q = Study.query
    if patient_id:
        q = q.filter_by(patient_id=patient_id)
    if modality:
        q = q.filter(Study.modality.ilike(modality))
    return q.order_by(Study.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)


def get_series_for_study(study_id: int):
    return Series.query.filter_by(study_id=study_id).all()


def get_instances_for_series(series_id: int):
    return Instance.query.filter_by(series_id=series_id).order_by(Instance.instance_number).all()


# ── Utilities ─────────────────────────────────────────────────────────────────

def _tag(ds, tag: str, default=None):
    val = getattr(ds, tag, default)
    return str(val).strip() if val is not None else default

def _int_tag(ds, tag: str):
    val = getattr(ds, tag, None)
    try:
        return int(val)
    except (TypeError, ValueError):
        return None

def _safe(uid: str) -> str:
    return uid.replace(".", "_")

def _parse_da(value):
    if not value:
        return None
    try:
        return datetime.strptime(str(value), "%Y%m%d").date()
    except ValueError:
        return None

def _window(ds, modality: str):
    wc = getattr(ds, "WindowCenter", None)
    ww = getattr(ds, "WindowWidth",  None)
    try:
        wc = float(wc[0]) if hasattr(wc, "__len__") else float(wc)
        ww = float(ww[0]) if hasattr(ww, "__len__") else float(ww)
    except (TypeError, ValueError):
        wc, ww = None, None
    return wc, ww