"""
Image viewing and visualization utilities for medical imaging
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Slider, Button
from typing import Optional, Tuple, List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class ImageViewer:
    """
    Interactive image viewer for medical images
    """
    
    def __init__(self, image: np.ndarray, metadata: Optional[Dict] = None):
        """
        Initialize the image viewer
        
        Args:
            image: Input image array
            metadata: Optional DICOM metadata
        """
        self.image = image
        self.metadata = metadata or {}
        self.original_image = image.copy()
        self.current_image = image.copy()
        
        # Window/Level parameters
        self.window_center = np.mean(image)
        self.window_width = np.std(image) * 4
        
        # Pan and zoom parameters
        self.pan_offset = [0, 0]
        self.zoom_factor = 1.0
        
        # Interactive elements
        self.fig = None
        self.ax = None
        self.im = None
        
    def show_2d(self, colormap: str = 'gray', interactive: bool = True) -> None:
        """
        Display 2D image
        
        Args:
            colormap: Matplotlib colormap
            interactive: Enable interactive controls
        """
        if interactive:
            self._show_interactive_2d(colormap)
        else:
            self._show_static_2d(colormap)
    
    def _show_static_2d(self, colormap: str) -> None:
        """Show static 2D image"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Apply window/level if needed
        display_image = self._apply_window_level()
        
        im = ax.imshow(display_image, cmap=colormap, aspect='equal')
        ax.set_title('Medical Image Viewer')
        ax.axis('off')
        
        # Add colorbar
        plt.colorbar(im, ax=ax, label='Intensity')
        
        # Add metadata if available
        if self.metadata:
            info_text = self._format_metadata()
            ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
                   verticalalignment='top', fontsize=8,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
    
    def _show_interactive_2d(self, colormap: str) -> None:
        """Show interactive 2D image with controls"""
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        
        # Initial display
        display_image = self._apply_window_level()
        self.im = self.ax.imshow(display_image, cmap=colormap, aspect='equal')
        self.ax.set_title('Interactive Medical Image Viewer')
        self.ax.axis('off')
        
        # Add sliders for window/level
        ax_window = plt.axes([0.15, 0.02, 0.3, 0.03])
        ax_level = plt.axes([0.55, 0.02, 0.3, 0.03])
        
        self.slider_window = Slider(ax_window, 'Window', 1, 2000, 
                                   valinit=self.window_width, valstep=1)
        self.slider_level = Slider(ax_level, 'Level', np.min(self.image), 
                                  np.max(self.image), valinit=self.window_center, valstep=1)
        
        # Connect sliders
        self.slider_window.on_changed(self._update_window_level)
        self.slider_level.on_changed(self._update_window_level)
        
        # Add reset button
        ax_reset = plt.axes([0.45, 0.06, 0.1, 0.04])
        self.btn_reset = Button(ax_reset, 'Reset')
        self.btn_reset.on_clicked(self._reset_view)
        
        plt.tight_layout()
        plt.show()
    
    def _apply_window_level(self) -> np.ndarray:
        """Apply window/level adjustment"""
        window_min = self.window_center - self.window_width / 2
        window_max = self.window_center + self.window_width / 2
        
        windowed = np.clip(self.original_image, window_min, window_max)
        
        # Normalize to display range
        if window_max > window_min:
            windowed = ((windowed - window_min) / (window_max - window_min))
        else:
            windowed = np.zeros_like(windowed)
        
        return windowed
    
    def _update_window_level(self, val) -> None:
        """Update window/level from sliders"""
        self.window_width = self.slider_window.val
        self.window_center = self.slider_level.val
        
        display_image = self._apply_window_level()
        self.im.set_data(display_image)
        self.fig.canvas.draw_idle()
    
    def _reset_view(self, event) -> None:
        """Reset to original view"""
        self.window_center = np.mean(self.original_image)
        self.window_width = np.std(self.original_image) * 4
        
        self.slider_window.set_val(self.window_width)
        self.slider_level.set_val(self.window_center)
    
    def _format_metadata(self) -> str:
        """Format metadata for display"""
        info_lines = []
        
        if 'patient' in self.metadata:
            patient = self.metadata['patient']
            info_lines.append(f"Patient: {patient.get('name', 'N/A')}")
            info_lines.append(f"ID: {patient.get('id', 'N/A')}")
        
        if 'study' in self.metadata:
            study = self.metadata['study']
            info_lines.append(f"Study: {study.get('description', 'N/A')}")
            info_lines.append(f"Date: {study.get('date', 'N/A')}")
        
        if 'series' in self.metadata:
            series = self.metadata['series']
            info_lines.append(f"Modality: {series.get('modality', 'N/A')}")
            info_lines.append(f"Series: {series.get('description', 'N/A')}")
        
        if 'image' in self.metadata:
            img = self.metadata['image']
            info_lines.append(f"Size: {img.get('rows', 0)}x{img.get('columns', 0)}")
            info_lines.append(f"Bits: {img.get('bits_allocated', 0)}")
        
        return '\n'.join(info_lines)

def create_2d_viewer(image: np.ndarray, metadata: Optional[Dict] = None,
                    colormap: str = 'gray', interactive: bool = True) -> ImageViewer:
    """
    Create a 2D image viewer
    
    Args:
        image: Input image array
        metadata: Optional DICOM metadata
        colormap: Matplotlib colormap
        interactive: Enable interactive controls
        
    Returns:
        ImageViewer instance
    """
    viewer = ImageViewer(image, metadata)
    viewer.show_2d(colormap, interactive)
    return viewer

def create_3d_viewer(volume: np.ndarray, metadata: Optional[Dict] = None) -> None:
    """
    Create a 3D volume viewer using Plotly
    
    Args:
        volume: 3D volume array
        metadata: Optional DICOM metadata
    """
    # Create multi-plane view
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "image"}, {"type": "image"}],
               [{"type": "image"}, {"type": "scatter3d"}]],
        subplot_titles=['Axial', 'Sagittal', 'Coronal', '3D Volume']
    )
    
    # Get middle slices
    mid_z = volume.shape[0] // 2
    mid_y = volume.shape[1] // 2
    mid_x = volume.shape[2] // 2
    
    # Axial slice
    fig.add_trace(
        go.Image(z=volume[mid_z, :, :]),
        row=1, col=1
    )
    
    # Sagittal slice
    fig.add_trace(
        go.Image(z=volume[:, :, mid_x]),
        row=1, col=2
    )
    
    # Coronal slice
    fig.add_trace(
        go.Image(z=volume[:, mid_y, :]),
        row=2, col=1
    )
    
    # 3D volume rendering (simplified)
    threshold = np.mean(volume) + np.std(volume)
    x, y, z = np.where(volume > threshold)
    
    fig.add_trace(
        go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(size=1, color=volume[x, y, z], colorscale='gray'),
            name='Volume'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        title='3D Medical Volume Viewer',
        height=800
    )
    
    fig.show()

def create_comparison_view(images: List[np.ndarray], titles: List[str],
                         colormap: str = 'gray') -> None:
    """
    Create side-by-side comparison view of multiple images
    
    Args:
        images: List of image arrays
        titles: List of titles for each image
        colormap: Matplotlib colormap
    """
    n_images = len(images)
    if n_images == 0:
        return
    
    # Calculate subplot grid
    cols = min(n_images, 4)
    rows = (n_images + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
    
    if n_images == 1:
        axes = [axes]
    elif rows == 1:
        axes = axes.reshape(1, -1)
    
    for i, (image, title) in enumerate(zip(images, titles)):
        row = i // cols
        col = i % cols
        
        ax = axes[row, col] if rows > 1 else axes[col]
        
        im = ax.imshow(image, cmap=colormap, aspect='equal')
        ax.set_title(title)
        ax.axis('off')
        
        # Add colorbar
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    
    # Hide unused subplots
    for i in range(n_images, rows * cols):
        row = i // cols
        col = i % cols
        ax = axes[row, col] if rows > 1 else axes[col]
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()

def create_histogram_view(image: np.ndarray, bins: int = 256) -> None:
    """
    Create histogram view of image intensities
    
    Args:
        image: Input image array
        bins: Number of histogram bins
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Display image
    ax1.imshow(image, cmap='gray', aspect='equal')
    ax1.set_title('Image')
    ax1.axis('off')
    
    # Display histogram
    ax2.hist(image.flatten(), bins=bins, alpha=0.7, color='blue', edgecolor='black')
    ax2.set_title('Intensity Histogram')
    ax2.set_xlabel('Intensity')
    ax2.set_ylabel('Frequency')
    ax2.grid(True, alpha=0.3)
    
    # Add statistics
    mean_val = np.mean(image)
    std_val = np.std(image)
    min_val = np.min(image)
    max_val = np.max(image)
    
    stats_text = f'Mean: {mean_val:.2f}\nStd: {std_val:.2f}\nMin: {min_val:.2f}\nMax: {max_val:.2f}'
    ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

def create_profile_view(image: np.ndarray, point1: Tuple[int, int], 
                       point2: Tuple[int, int]) -> None:
    """
    Create intensity profile view between two points
    
    Args:
        image: Input image array
        point1: Starting point (row, col)
        point2: Ending point (row, col)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Display image with line
    ax1.imshow(image, cmap='gray', aspect='equal')
    ax1.plot([point1[1], point2[1]], [point1[0], point2[0]], 'r-', linewidth=2)
    ax1.plot(point1[1], point1[0], 'ro', markersize=8)
    ax1.plot(point2[1], point2[0], 'ro', markersize=8)
    ax1.set_title('Intensity Profile Line')
    ax1.axis('off')
    
    # Extract profile
    profile = measure.profile_line(image, point1, point2)
    distance = np.arange(len(profile))
    
    # Display profile
    ax2.plot(distance, profile, 'b-', linewidth=2)
    ax2.set_title('Intensity Profile')
    ax2.set_xlabel('Distance (pixels)')
    ax2.set_ylabel('Intensity')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def create_viewer(image: np.ndarray, metadata: Optional[Dict] = None,
                  view_type: str = '2d', **kwargs) -> Any:
    """
    Unified viewer creation function
    
    Args:
        image: Input image array
        metadata: Optional DICOM metadata
        view_type: Type of viewer ('2d', '3d', 'comparison', 'histogram', 'profile')
        **kwargs: Viewer-specific parameters
        
    Returns:
        Viewer instance or None
    """
    view_type = view_type.lower()
    
    if view_type == '2d':
        return create_2d_viewer(image, metadata, **kwargs)
    elif view_type == '3d':
        if len(image.shape) != 3:
            raise ValueError("3D viewer requires 3D volume")
        return create_3d_viewer(image, metadata, **kwargs)
    elif view_type == 'comparison':
        images = kwargs.get('images', [image])
        titles = kwargs.get('titles', ['Image'])
        return create_comparison_view(images, titles, **kwargs)
    elif view_type == 'histogram':
        return create_histogram_view(image, **kwargs)
    elif view_type == 'profile':
        point1 = kwargs.get('point1')
        point2 = kwargs.get('point2')
        if point1 is None or point2 is None:
            raise ValueError("Profile view requires point1 and point2 parameters")
        return create_profile_view(image, point1, point2)
    else:
        raise ValueError(f"Unknown viewer type: {view_type}")
