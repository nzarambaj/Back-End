# Calculus Module - Medical Image Processing

The `calculus` module provides comprehensive image processing capabilities for medical imaging, including DICOM handling, filtering, segmentation, and visualization.

## 📁 Module Structure

```
app/calculus/
├── __init__.py              # Main module exports
├── python/                  # Python-based image processing
│   ├── __init__.py
│   ├── dicom_loader.py      # DICOM file loading and metadata
│   ├── image_filters.py     # Image filtering and enhancement
│   ├── segmentation.py      # Image segmentation algorithms
│   └── viewer.py            # Image visualization and display
├── cpp/                     # High-performance C++ processing
│   ├── dicom_processing.cpp # DICOM processing in C++
│   ├── image_filters.cpp    # Optimized image filters
│   └── reconstruction.cpp   # 3D reconstruction algorithms
├── csharp/                  # C# imaging utilities
│   ├── ImageViewer.cs        # Windows forms image viewer
│   └── DicomReader.cs       # DICOM file reader
└── bindings/                # Python-C++ bindings
    └── pybind_interface.cpp # PyBind11 interface
```

## 🚀 Quick Start

### Python Usage

```python
from app.calculus import load_dicom_image, apply_filter, segment_image, create_viewer
import numpy as np

# Load DICOM image
image_array, metadata = load_dicom_image("path/to/dicom.dcm")

# Apply Gaussian filter
filtered = apply_filter(image_array, "gaussian", sigma=1.0)

# Segment using Otsu threshold
segmented = segment_image(filtered, "otsu")

# Create viewer
viewer = create_viewer(segmented, metadata, view_type="2d")
```

### Individual Module Usage

```python
# DICOM loading
from app.calculus.python.dicom_loader import load_dicom_image, validate_dicom_file

# Image filtering
from app.calculus.python.image_filters import apply_gaussian_filter, apply_edge_detection

# Segmentation
from app.calculus.python.segmentation import threshold_segmentation, region_growing_segmentation

# Visualization
from app.calculus.python.viewer import create_2d_viewer, create_3d_viewer
```

## 📦 Dependencies

Install required dependencies:

```bash
pip install -r requirements_calculus.txt
```

Core dependencies:
- `numpy` - Array operations
- `scipy` - Scientific computing
- `scikit-image` - Image processing
- `matplotlib` - Plotting
- `plotly` - Interactive visualization
- `pydicom` - DICOM file handling

## 🔧 Features

### DICOM Processing
- Load DICOM files with metadata extraction
- Window/level adjustment
- Pixel data access and manipulation
- DICOM validation

### Image Filtering
- Gaussian blur
- Edge detection (Sobel, Canny, Prewitt, Roberts)
- Median filtering
- Morphological operations
- Histogram equalization
- Unsharp masking

### Image Segmentation
- Threshold-based segmentation (Otsu, adaptive, manual)
- Region growing
- Watershed segmentation
- Active contours (snakes)
- K-means clustering
- Morphological segmentation

### Visualization
- 2D image viewer with interactive controls
- 3D volume rendering
- Multi-planar reconstruction (MPR)
- Maximum intensity projection (MIP)
- Interactive window/level adjustment
- Histogram and intensity profiles

### High-Performance C++ Processing
- Optimized image filters
- Fast DICOM processing
- 3D reconstruction algorithms
- Ray casting for volume rendering

## 🎯 Examples

### Basic Image Processing

```python
import numpy as np
from app.calculus.python.image_filters import apply_gaussian_filter, apply_edge_detection
from app.calculus.python.segmentation import threshold_segmentation

# Create test image
image = np.random.rand(256, 256) * 255
image = image.astype(np.uint8)

# Apply filters
blurred = apply_gaussian_filter(image, sigma=1.0)
edges = apply_edge_detection(image, method='sobel')

# Segment image
segmented = threshold_segmentation(image, method='otsu')
```

### DICOM File Processing

```python
from app.calculus.python.dicom_loader import load_dicom_image, get_dicom_info

# Load DICOM
image, metadata = load_dicom_image("patient_scan.dcm")

# Get file info without loading pixel data
info = get_dicom_info("patient_scan.dcm")
print(f"Modality: {metadata['series']['modality']}")
print(f"Patient: {metadata['patient']['name']}")
```

### Interactive Visualization

```python
from app.calculus.python.viewer import create_2d_viewer, create_comparison_view

# Create interactive viewer
viewer = create_2d_viewer(image, metadata, interactive=True)

# Compare multiple images
images = [original, filtered, segmented]
titles = ["Original", "Filtered", "Segmented"]
create_comparison_view(images, titles)
```

## ⚡ C++ Performance (Optional)

For high-performance processing, compile the C++ modules:

```bash
# Install pybind11
pip install pybind11

# Compile the module (requires C++ compiler)
cd app/calculus/bindings
c++ -O3 -Wall -shared -std=c++11 -fPIC \
    $(python3 -m pybind11 --includes) \
    pybind_interface.cpp \
    ../cpp/dicom_processing.cpp \
    ../cpp/image_filters.cpp \
    ../cpp/reconstruction.cpp \
    -o calculus_cpp$(python3-config --extension-suffix)
```

Then use in Python:

```python
import calculus_cpp

# Create C++ processor
processor = calculus_cpp.DicomProcessor()
processor.load_dicom_image("scan.dcm")
processor.apply_gaussian_filter(1.0)

# Get processed data
processed_data = processor.get_pixel_data()
```

## 🔬 Advanced Usage

### Custom Filters

```python
from app.calculus.python.image_filters import create_custom_kernel, apply_convolution

# Create custom kernel
kernel = create_custom_kernel("sharpen", size=3)

# Apply convolution
sharpened = apply_convolution(image, kernel)
```

### 3D Processing

```python
import calculus_cpp

# Create volume reconstructor
reconstructor = calculus_cpp.VolumeReconstructor()

# Set 3D volume data
reconstructor.set_volume(volume_3d_array)

# Perform MIP
mip_image = reconstructor.maximum_intensity_projection(512, 512, "z")

# Ray casting
rendered = reconstructor.ray_casting(512, 512, camera_matrix, view_matrix)
```

## 🐛 Troubleshooting

### Common Issues

1. **Missing dependencies**: Install with `pip install -r requirements_calculus.txt`
2. **C++ compilation**: Requires C++ compiler and pybind11
3. **DICOM files**: Ensure files are valid DICOM format
4. **Memory issues**: Large volumes may require more RAM

### Testing

Run the test suite:

```bash
python test_calculus.py
```

## 🤝 Integration with Flask

Add to your Flask routes:

```python
from flask import Blueprint, request, jsonify
from app.calculus import load_dicom_image, apply_filter

calculus_bp = Blueprint('calculus', __name__)

@calculus_bp.route('/api/process_image', methods=['POST'])
def process_image():
    file = request.files['dicom_file']
    # Process image...
    return jsonify(result)
```

## 📚 API Reference

### Main Functions

- `load_dicom_image(file_path)` - Load DICOM with metadata
- `apply_filter(image, filter_name, **kwargs)` - Apply image filter
- `segment_image(image, method, **kwargs)` - Segment image
- `create_viewer(image, metadata, view_type)` - Create viewer

### DICOM Loader

- `load_dicom_image(file_path)` - Load DICOM file
- `extract_metadata(dataset)` - Extract DICOM metadata
- `get_dicom_info(file_path)` - Get file information
- `validate_dicom_file(file_path)` - Validate DICOM file

### Image Filters

- `apply_gaussian_filter(image, sigma)` - Gaussian blur
- `apply_edge_detection(image, method)` - Edge detection
- `apply_window_level(image, center, width)` - Window/level
- `denoise_image(image, method)` - Denoising
- `sharpen_image(image, method)` - Sharpening

### Segmentation

- `threshold_segmentation(image, method)` - Threshold segmentation
- `region_growing_segmentation(image, seed_point, threshold)` - Region growing
- `watershed_segmentation(image, markers)` - Watershed
- `active_contour_segmentation(image, initial_contour)` - Active contours

### Viewer

- `create_2d_viewer(image, metadata)` - 2D viewer
- `create_3d_viewer(volume, metadata)` - 3D viewer
- `create_comparison_view(images, titles)` - Comparison view
- `create_histogram_view(image)` - Histogram display

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
- Python-based image processing
- DICOM support
- Interactive visualization
- C++ high-performance modules (optional)

## 📄 License

This module is part of the Medical Imaging System project.

## 🤝 Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Ensure compatibility with existing system

## 📞 Support

For issues and questions:
- Check the test suite: `python test_calculus.py`
- Review the API documentation
- Verify dependencies are installed
- Ensure DICOM files are valid
