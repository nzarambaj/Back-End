"""
DICOM Viewer - Medical Image Viewer
View and analyze DICOM files with Python
"""

import pydicom
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from tkinter import Tk, filedialog, Button, Label, Frame, messagebox
from PIL import Image, ImageTk
import threading

class DICOMViewer:
    """Interactive DICOM file viewer"""
    
    def __init__(self):
        self.current_file = None
        self.ds = None
        self.image_data = None
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI interface"""
        self.root = Tk()
        self.root.title("DICOM Medical Image Viewer")
        self.root.geometry("800x600")
        
        # Create frames
        control_frame = Frame(self.root)
        control_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        info_frame = Frame(self.root)
        info_frame.pack(side="top", fill="x", padx=10, pady=5)
        
        image_frame = Frame(self.root)
        image_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        
        # Control buttons
        Button(control_frame, text="Open DICOM File", command=self.open_file).pack(side="left", padx=5)
        Button(control_frame, text="View Metadata", command=self.show_metadata).pack(side="left", padx=5)
        Button(control_frame, text="Adjust Window", command=self.adjust_window).pack(side="left", padx=5)
        Button(control_frame, text="Save Image", command=self.save_image).pack(side="left", padx=5)
        
        # Info labels
        self.info_label = Label(info_frame, text="No file loaded", anchor="w")
        self.info_label.pack(fill="x")
        
        self.metadata_label = Label(info_frame, text="", anchor="w", justify="left")
        self.metadata_label.pack(fill="x")
        
        # Image display
        self.image_label = Label(image_frame, text="Open a DICOM file to view", bg="black", fg="white")
        self.image_label.pack(fill="both", expand=True)
    
    def open_file(self):
        """Open and display DICOM file"""
        file_path = filedialog.askopenfilename(
            title="Select DICOM File",
            filetypes=[("DICOM files", "*.dcm *.dicom"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.load_dicom_file(file_path)
                self.display_image()
                self.update_info()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load DICOM file: {str(e)}")
    
    def load_dicom_file(self, file_path):
        """Load DICOM file"""
        self.current_file = file_path
        self.ds = pydicom.dcmread(file_path)
        
        # Get pixel data
        if hasattr(self.ds, 'pixel_array'):
            self.image_data = self.ds.pixel_array
        else:
            raise ValueError("No pixel data found in DICOM file")
    
    def display_image(self):
        """Display the DICOM image"""
        if self.image_data is None:
            return
        
        # Apply window/level if available
        display_image = self.apply_window_level(self.image_data)
        
        # Normalize for display
        if display_image.max() > display_image.min():
            display_image = ((display_image - display_image.min()) / 
                           (display_image.max() - display_image.min()) * 255).astype(np.uint8)
        
        # Create PIL image
        if len(display_image.shape) == 2:
            pil_image = Image.fromarray(display_image, mode='L')
        else:
            pil_image = Image.fromarray(display_image)
        
        # Resize for display
        pil_image = pil_image.resize((600, 400), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(pil_image)
        self.image_label.config(image=photo, text="")
        self.image_label.image = photo  # Keep a reference
    
    def apply_window_level(self, image):
        """Apply window/level settings"""
        if hasattr(self.ds, 'WindowCenter') and hasattr(self.ds, 'WindowWidth'):
            try:
                window_center = self.ds.WindowCenter
                window_width = self.ds.WindowWidth
                
                if isinstance(window_center, list):
                    window_center = window_center[0]
                if isinstance(window_width, list):
                    window_width = window_width[0]
                
                # Apply window/level
                min_val = window_center - window_width // 2
                max_val = window_center + window_width // 2
                
                return np.clip(image, min_val, max_val)
            except:
                pass
        
        return image
    
    def update_info(self):
        """Update file information"""
        if self.ds is None:
            return
        
        info_text = f"File: {os.path.basename(self.current_file)} | "
        info_text += f"Size: {self.image_data.shape[1]}x{self.image_data.shape[0]} | "
        info_text += f"Modality: {getattr(self.ds, 'Modality', 'Unknown')} | "
        info_text += f"Patient: {getattr(self.ds, 'PatientID', 'Unknown')}"
        
        self.info_label.config(text=info_text)
        
        # Show key metadata
        metadata_text = f"Study: {getattr(self.ds, 'StudyDescription', 'Unknown')} | "
        metadata_text += f"Date: {getattr(self.ds, 'StudyDate', 'Unknown')} | "
        metadata_text += f"Institution: {getattr(self.ds, 'InstitutionName', 'Unknown')}"
        
        self.metadata_label.config(text=metadata_text)
    
    def show_metadata(self):
        """Show detailed DICOM metadata"""
        if self.ds is None:
            messagebox.showinfo("Info", "No DICOM file loaded")
            return
        
        # Create metadata window
        metadata_window = Tk()
        metadata_window.title("DICOM Metadata")
        metadata_window.geometry("600x400")
        
        # Create text widget
        from tkinter import scrolledtext
        text_widget = scrolledtext.ScrolledText(metadata_window, wrap="word")
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add metadata
        text_widget.insert("1.0", "DICOM Metadata\n" + "="*50 + "\n\n")
        
        for elem in self.ds:
            if elem.VR != "SQ":  # Skip sequences for simplicity
                text_widget.insert("end", f"{elem.keyword}: {elem.value}\n")
        
        text_widget.config(state="disabled")
        metadata_window.mainloop()
    
    def adjust_window(self):
        """Adjust window/level settings"""
        if self.ds is None:
            messagebox.showinfo("Info", "No DICOM file loaded")
            return
        
        # Create adjustment window
        adjust_window = Tk()
        adjust_window.title("Window/Level Adjustment")
        adjust_window.geometry("300x200")
        
        # Add sliders
        from tkinter import Scale, DoubleVar
        
        window_center = DoubleVar(value=getattr(self.ds, 'WindowCenter', 128))
        window_width = DoubleVar(value=getattr(self.ds, 'WindowWidth', 256))
        
        Scale(adjust_window, from_=0, to=4000, variable=window_center, 
              orient="horizontal", label="Window Center").pack(pady=10)
        Scale(adjust_window, from_=1, to=4000, variable=window_width, 
              orient="horizontal", label="Window Width").pack(pady=10)
        
        def apply_changes():
            # Temporarily modify window/level
            self.ds.WindowCenter = int(window_center.get())
            self.ds.WindowWidth = int(window_width.get())
            self.display_image()
        
        Button(adjust_window, text="Apply", command=apply_changes).pack(pady=10)
        adjust_window.mainloop()
    
    def save_image(self):
        """Save current image as PNG"""
        if self.image_data is None:
            messagebox.showinfo("Info", "No DICOM file loaded")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Apply window/level
                display_image = self.apply_window_level(self.image_data)
                
                # Normalize
                if display_image.max() > display_image.min():
                    display_image = ((display_image - display_image.min()) / 
                                   (display_image.max() - display_image.min()) * 255).astype(np.uint8)
                
                # Save image
                pil_image = Image.fromarray(display_image)
                pil_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

def view_dicom_file(file_path):
    """Quick view a single DICOM file"""
    try:
        ds = pydicom.dcmread(file_path)
        
        # Get pixel data
        if hasattr(ds, 'pixel_array'):
            image_data = ds.pixel_array
        else:
            print("No pixel data found in DICOM file")
            return
        
        # Display image
        plt.figure(figsize=(10, 8))
        plt.imshow(image_data, cmap='gray')
        plt.title(f"DICOM Image\n{os.path.basename(file_path)}")
        plt.colorbar(label='Pixel Intensity')
        plt.axis('off')
        
        # Add metadata
        metadata_text = f"Patient ID: {getattr(ds, 'PatientID', 'Unknown')}\n"
        metadata_text += f"Modality: {getattr(ds, 'Modality', 'Unknown')}\n"
        metadata_text += f"Study Date: {getattr(ds, 'StudyDate', 'Unknown')}\n"
        metadata_text += f"Image Size: {image_data.shape[1]}x{image_data.shape[0]}"
        
        plt.figtext(0.02, 0.02, metadata_text, fontsize=10, 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Error viewing DICOM file: {str(e)}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Command line mode - view specific file
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            print(f"Viewing DICOM file: {file_path}")
            view_dicom_file(file_path)
        else:
            print(f"File not found: {file_path}")
    else:
        # GUI mode
        print("Starting DICOM Viewer GUI...")
        viewer = DICOMViewer()
        viewer.run()

if __name__ == "__main__":
    main()
