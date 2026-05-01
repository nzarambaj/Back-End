# Medical Imaging Integration for Project_BackEnd
import sys
import os

# Add medical imaging to path
sys.path.insert(0, os.path.dirname(__file__))

# Import medical imaging modules
from vessel_identifier import VesselIdentifier
from bone_identifier import BoneIdentifier
from nifti_processor import NIfTIProcessor

print("Medical Imaging System Loaded Successfully!")
print("Available modules:")
print("  - VesselIdentifier: Blood vessel detection and analysis")
print("  - BoneIdentifier: Bone detection and analysis")
print("  - NIfTIProcessor: Neuroimaging file processing")

# Example usage:
# vessel_id = VesselIdentifier()
# results = vessel_id.identify_vessels("image.jpg", "threshold")
