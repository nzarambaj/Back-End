"""
Image filtering and processing utilities for medical images
"""

import numpy as np
from scipy import ndimage
from scipy.signal import convolve2d
from skimage import filters, exposure, morphology
from typing import Tuple, Optional, Union

def apply_gaussian_filter(image: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """
    Apply Gaussian smoothing filter to reduce noise
    
    Args:
        image: Input image array
        sigma: Standard deviation for Gaussian kernel
        
    Returns:
        Smoothed image array
    """
    return ndimage.gaussian_filter(image, sigma=sigma)

def apply_edge_detection(image: np.ndarray, method: str = 'sobel') -> np.ndarray:
    """
    Apply edge detection to highlight boundaries
    
    Args:
        image: Input image array
        method: Edge detection method ('sobel', 'canny', 'prewitt', 'roberts')
        
    Returns:
        Edge-detected image array
    """
    method = method.lower()
    
    if method == 'sobel':
        return filters.sobel(image)
    elif method == 'canny':
        return filters.canny(image)
    elif method == 'prewitt':
        return filters.prewitt(image)
    elif method == 'roberts':
        return filters.roberts(image)
    else:
        raise ValueError(f"Unknown edge detection method: {method}")

def apply_window_level(image: np.ndarray, window_center: float, window_width: float) -> np.ndarray:
    """
    Apply window/level adjustment for CT/MRI images
    
    Args:
        image: Input image array
        window_center: Center of window (level)
        window_width: Width of window
        
    Returns:
        Windowed image array
    """
    # Calculate window bounds
    window_min = window_center - window_width / 2
    window_max = window_center + window_width / 2
    
    # Apply windowing
    windowed = np.clip(image, window_min, window_max)
    
    # Normalize to 0-255 range
    if window_max > window_min:
        windowed = ((windowed - window_min) / (window_max - window_min) * 255).astype(np.uint8)
    else:
        windowed = np.zeros_like(image, dtype=np.uint8)
    
    return windowed

def enhance_contrast(image: np.ndarray, method: str = 'histogram_equalization') -> np.ndarray:
    """
    Enhance image contrast
    
    Args:
        image: Input image array
        method: Enhancement method ('histogram_equalization', 'clahe', 'gamma')
        
    Returns:
        Contrast-enhanced image array
    """
    method = method.lower()
    
    if method == 'histogram_equalization':
        return exposure.equalize_hist(image)
    elif method == 'clahe':
        return exposure.equalize_adapthist(image)
    elif method == 'gamma':
        return exposure.adjust_gamma(image, gamma=0.7)
    else:
        raise ValueError(f"Unknown contrast enhancement method: {method}")

def apply_median_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Apply median filter for noise reduction
    
    Args:
        image: Input image array
        kernel_size: Size of the median filter kernel
        
    Returns:
        Median-filtered image array
    """
    return ndimage.median_filter(image, size=kernel_size)

def apply_morphological_operations(image: np.ndarray, operation: str, 
                                 kernel_size: int = 3, kernel_shape: str = 'disk') -> np.ndarray:
    """
    Apply morphological operations
    
    Args:
        image: Input binary or grayscale image
        operation: Operation type ('erosion', 'dilation', 'opening', 'closing')
        kernel_size: Size of structuring element
        kernel_shape: Shape of structuring element ('disk', 'square', 'rectangle')
        
    Returns:
        Processed image array
    """
    # Create structuring element
    if kernel_shape == 'disk':
        kernel = morphology.disk(kernel_size)
    elif kernel_shape == 'square':
        kernel = morphology.square(kernel_size)
    elif kernel_shape == 'rectangle':
        kernel = morphology.rectangle(kernel_size, kernel_size // 2)
    else:
        raise ValueError(f"Unknown kernel shape: {kernel_shape}")
    
    operation = operation.lower()
    
    if operation == 'erosion':
        return morphology.erosion(image, kernel)
    elif operation == 'dilation':
        return morphology.dilation(image, kernel)
    elif operation == 'opening':
        return morphology.opening(image, kernel)
    elif operation == 'closing':
        return morphology.closing(image, kernel)
    else:
        raise ValueError(f"Unknown morphological operation: {operation}")

def sharpen_image(image: np.ndarray, method: str = 'unsharp_mask') -> np.ndarray:
    """
    Sharpen image using various methods
    
    Args:
        image: Input image array
        method: Sharpening method ('unsharp_mask', 'laplacian')
        
    Returns:
        Sharpened image array
    """
    method = method.lower()
    
    if method == 'unsharp_mask':
        return filters.unsharp_mask(image, radius=1, amount=1)
    elif method == 'laplacian':
        laplacian = filters.laplace(image)
        return image - 0.5 * laplacian
    else:
        raise ValueError(f"Unknown sharpening method: {method}")

def denoise_image(image: np.ndarray, method: str = 'gaussian') -> np.ndarray:
    """
    Denoise image using various methods
    
    Args:
        image: Input image array
        method: Denoising method ('gaussian', 'bilateral', 'tv_denoise')
        
    Returns:
        Denoised image array
    """
    method = method.lower()
    
    if method == 'gaussian':
        return apply_gaussian_filter(image, sigma=1.0)
    elif method == 'bilateral':
        from skimage.restoration import denoise_bilateral
        return denoise_bilateral(image, sigma_color=0.05, sigma_spatial=2)
    elif method == 'tv_denoise':
        from skimage.restoration import denoise_tv_chambolle
        return denoise_tv_chambolle(image, weight=0.1)
    else:
        raise ValueError(f"Unknown denoising method: {method}")

def create_custom_kernel(kernel_type: str, size: int = 3) -> np.ndarray:
    """
    Create custom convolution kernels
    
    Args:
        kernel_type: Type of kernel ('sharpen', 'blur', 'edge', 'emboss')
        size: Size of the kernel
        
    Returns:
        Convolution kernel array
    """
    kernel_type = kernel_type.lower()
    
    if kernel_type == 'sharpen':
        kernel = np.array([[-1, -1, -1],
                           [-1,  9, -1],
                           [-1, -1, -1]])
    elif kernel_type == 'blur':
        kernel = np.ones((size, size)) / (size * size)
    elif kernel_type == 'edge':
        kernel = np.array([[-1, -1, -1],
                           [-1,  8, -1],
                           [-1, -1, -1]])
    elif kernel_type == 'emboss':
        kernel = np.array([[-2, -1,  0],
                           [-1,  1,  1],
                           [ 0,  1,  2]])
    else:
        raise ValueError(f"Unknown kernel type: {kernel_type}")
    
    return kernel

def apply_convolution(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    Apply custom convolution to image
    
    Args:
        image: Input image array
        kernel: Convolution kernel
        
    Returns:
        Convolved image array
    """
    return convolve2d(image, kernel, mode='same', boundary='fill', fillvalue=0)

# Convenience function for common filter combinations
def apply_filter(image: np.ndarray, filter_name: str, **kwargs) -> np.ndarray:
    """
    Apply a filter by name with parameters
    
    Args:
        image: Input image array
        filter_name: Name of the filter
        **kwargs: Filter-specific parameters
        
    Returns:
        Filtered image array
    """
    filter_name = filter_name.lower()
    
    if filter_name == 'gaussian':
        return apply_gaussian_filter(image, sigma=kwargs.get('sigma', 1.0))
    elif filter_name == 'edge_sobel':
        return apply_edge_detection(image, method='sobel')
    elif filter_name == 'edge_canny':
        return apply_edge_detection(image, method='canny')
    elif filter_name == 'window_level':
        return apply_window_level(image, 
                                window_center=kwargs.get('center', 0),
                                window_width=kwargs.get('width', 400))
    elif filter_name == 'contrast_hist':
        return enhance_contrast(image, method='histogram_equalization')
    elif filter_name == 'contrast_clahe':
        return enhance_contrast(image, method='clahe')
    elif filter_name == 'median':
        return apply_median_filter(image, kernel_size=kwargs.get('kernel_size', 3))
    elif filter_name == 'sharpen':
        return sharpen_image(image, method=kwargs.get('method', 'unsharp_mask'))
    elif filter_name == 'denoise_gaussian':
        return denoise_image(image, method='gaussian')
    elif filter_name == 'denoise_bilateral':
        return denoise_image(image, method='bilateral')
    else:
        raise ValueError(f"Unknown filter: {filter_name}")
