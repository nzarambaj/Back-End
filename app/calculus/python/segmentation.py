"""
Image segmentation utilities for medical imaging
"""

import numpy as np
from scipy import ndimage
from skimage import filters, morphology, measure, segmentation
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from typing import List, Tuple, Optional, Union

def threshold_segmentation(image: np.ndarray, method: str = 'otsu', 
                          threshold_value: Optional[float] = None) -> np.ndarray:
    """
    Perform threshold-based segmentation
    
    Args:
        image: Input image array
        method: Thresholding method ('otsu', 'adaptive', 'manual')
        threshold_value: Manual threshold value (required for 'manual' method)
        
    Returns:
        Binary segmentation mask
    """
    method = method.lower()
    
    if method == 'otsu':
        threshold = filters.threshold_otsu(image)
    elif method == 'adaptive':
        # Local adaptive thresholding
        from skimage.filters import threshold_local
        block_size = min(image.shape) // 8
        if block_size % 2 == 0:
            block_size += 1
        threshold = threshold_local(image, block_size=block_size, method='gaussian')
    elif method == 'manual':
        if threshold_value is None:
            raise ValueError("Manual threshold requires threshold_value parameter")
        threshold = threshold_value
    else:
        raise ValueError(f"Unknown thresholding method: {method}")
    
    return image > threshold

def region_growing_segmentation(image: np.ndarray, seed_point: Tuple[int, int],
                              threshold: float, connectivity: int = 8) -> np.ndarray:
    """
    Perform region growing segmentation from a seed point
    
    Args:
        image: Input image array
        seed_point: Starting point (row, col) for region growing
        threshold: Intensity threshold for region growing
        connectivity: Pixel connectivity (4 or 8)
        
    Returns:
        Binary segmentation mask
    """
    # Create output mask
    mask = np.zeros_like(image, dtype=bool)
    
    # Get seed value
    seed_value = image[seed_point[0], seed_point[1]]
    
    # Define connectivity
    if connectivity == 4:
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    elif connectivity == 8:
        neighbors = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),           (0, 1),
                    (1, -1),  (1, 0),  (1, 1)]
    else:
        raise ValueError("Connectivity must be 4 or 8")
    
    # Region growing
    stack = [seed_point]
    mask[seed_point[0], seed_point[1]] = True
    
    while stack:
        current_point = stack.pop()
        
        for dr, dc in neighbors:
            r, c = current_point[0] + dr, current_point[1] + dc
            
            # Check bounds
            if (0 <= r < image.shape[0] and 0 <= c < image.shape[1] and
                not mask[r, c]):
                
                # Check intensity threshold
                if abs(image[r, c] - seed_value) <= threshold:
                    mask[r, c] = True
                    stack.append((r, c))
    
    return mask

def watershed_segmentation(image: np.ndarray, markers: Optional[np.ndarray] = None,
                          compactness: float = 0.001) -> np.ndarray:
    """
    Perform watershed segmentation
    
    Args:
        image: Input image array
        markers: Optional marker array (if None, uses local maxima)
        compactness: Compactness parameter for watershed
        
    Returns:
        Segmented image with labeled regions
    """
    if markers is None:
        # Use local maxima as markers
        distance = ndimage.distance_transform_edt(image > filters.threshold_otsu(image))
        local_maxi = peak_local_max(distance, footprint=np.ones((3, 3)), labels=image)
        markers = measure.label(local_maxi)
    
    # Apply watershed
    labels = watershed(-image, markers, compactness=compactness)
    
    return labels

def active_contour_segmentation(image: np.ndarray, initial_contour: np.ndarray,
                               alpha: float = 0.015, beta: float = 10,
                               gamma: float = 0.001, max_iterations: int = 1000) -> np.ndarray:
    """
    Perform active contour (snake) segmentation
    
    Args:
        image: Input image array
        initial_contour: Initial contour points (Nx2 array)
        alpha: Snake length shape parameter
        beta: Snake smoothness shape parameter
        gamma: Time step parameter
        max_iterations: Maximum number of iterations
        
    Returns:
        Final contour points
    """
    try:
        from skimage.segmentation import active_contour
        return active_contour(image, initial_contour, alpha=alpha, beta=beta, 
                            gamma=gamma, max_iterations=max_iterations)
    except ImportError:
        raise ImportError("Active contour segmentation requires scikit-image with active_contour support")

def kmeans_segmentation(image: np.ndarray, n_clusters: int = 3) -> np.ndarray:
    """
    Perform k-means segmentation
    
    Args:
        image: Input image array
        n_clusters: Number of clusters
        
    Returns:
        Segmented image with labeled regions
    """
    try:
        from sklearn.cluster import KMeans
        
        # Reshape image for clustering
        pixels = image.reshape(-1, 1)
        
        # Apply k-means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(pixels)
        
        # Reshape back to image shape
        segmented = labels.reshape(image.shape)
        
        return segmented
        
    except ImportError:
        raise ImportError("K-means segmentation requires scikit-learn")

def morphological_segmentation(image: np.ndarray, operation: str = 'opening',
                              kernel_size: int = 3) -> np.ndarray:
    """
    Perform morphological segmentation
    
    Args:
        image: Input binary image
        operation: Morphological operation ('opening', 'closing', 'fill_holes')
        kernel_size: Size of morphological kernel
        
    Returns:
        Segmented image
    """
    # Create structuring element
    kernel = morphology.disk(kernel_size)
    
    operation = operation.lower()
    
    if operation == 'opening':
        return morphology.opening(image, kernel)
    elif operation == 'closing':
        return morphology.closing(image, kernel)
    elif operation == 'fill_holes':
        return morphology.remove_small_holes(image, area_threshold=kernel_size**2)
    else:
        raise ValueError(f"Unknown morphological operation: {operation}")

def multi_threshold_segmentation(image: np.ndarray, n_thresholds: int = 2) -> np.ndarray:
    """
    Perform multi-threshold segmentation
    
    Args:
        image: Input image array
        n_thresholds: Number of thresholds to use
        
    Returns:
        Multi-level segmented image
    """
    try:
        from skimage.filters import threshold_multiotsu
        
        # Apply multi-Otsu thresholding
        thresholds = threshold_multiotsu(image, classes=n_thresholds + 1)
        
        # Apply thresholds
        regions = np.digitize(image, bins=thresholds)
        
        return regions
        
    except ImportError:
        raise ImportError("Multi-threshold segmentation requires scikit-image with threshold_multiotsu")

def segment_image(image: np.ndarray, method: str = 'otsu', **kwargs) -> np.ndarray:
    """
    Unified segmentation function
    
    Args:
        image: Input image array
        method: Segmentation method
        **kwargs: Method-specific parameters
        
    Returns:
        Segmented image
    """
    method = method.lower()
    
    if method == 'otsu':
        return threshold_segmentation(image, method='otsu')
    elif method == 'adaptive':
        return threshold_segmentation(image, method='adaptive')
    elif method == 'manual':
        return threshold_segmentation(image, method='manual', 
                                    threshold_value=kwargs.get('threshold'))
    elif method == 'region_growing':
        seed_point = kwargs.get('seed_point')
        if seed_point is None:
            raise ValueError("Region growing requires seed_point parameter")
        return region_growing_segmentation(image, seed_point, 
                                         threshold=kwargs.get('threshold', 50))
    elif method == 'watershed':
        return watershed_segmentation(image, markers=kwargs.get('markers'))
    elif method == 'active_contour':
        initial_contour = kwargs.get('initial_contour')
        if initial_contour is None:
            raise ValueError("Active contour requires initial_contour parameter")
        return active_contour_segmentation(image, initial_contour)
    elif method == 'kmeans':
        return kmeans_segmentation(image, n_clusters=kwargs.get('n_clusters', 3))
    elif method == 'morphological':
        return morphological_segmentation(image, 
                                       operation=kwargs.get('operation', 'opening'),
                                       kernel_size=kwargs.get('kernel_size', 3))
    elif method == 'multi_threshold':
        return multi_threshold_segmentation(image, 
                                           n_thresholds=kwargs.get('n_thresholds', 2))
    else:
        raise ValueError(f"Unknown segmentation method: {method}")

def post_process_segmentation(mask: np.ndarray, operations: List[str]) -> np.ndarray:
    """
    Post-process segmentation mask
    
    Args:
        mask: Input binary mask
        operations: List of operations to apply
        
    Returns:
        Processed mask
    """
    result = mask.copy()
    
    for operation in operations:
        operation = operation.lower()
        
        if operation == 'remove_small_objects':
            result = morphology.remove_small_objects(result, min_size=50)
        elif operation == 'remove_small_holes':
            result = morphology.remove_small_holes(result)
        elif operation == 'binary_closing':
            result = morphology.binary_closing(result)
        elif operation == 'binary_opening':
            result = morphology.binary_opening(result)
        elif operation == 'binary_dilation':
            result = morphology.binary_dilation(result)
        elif operation == 'binary_erosion':
            result = morphology.binary_erosion(result)
        elif operation == 'fill_holes':
            result = ndimage.binary_fill_holes(result)
        else:
            raise ValueError(f"Unknown post-processing operation: {operation}")
    
    return result
