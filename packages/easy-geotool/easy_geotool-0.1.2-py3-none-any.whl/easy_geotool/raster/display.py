import numpy as np
import matplotlib.pyplot as plt
from skimage.exposure import equalize_hist
from easy_geotool.raster.process import *

def display_raster_image(image_array, rgb_bands=None, single_band=None, nodata_value=None, equalize=True):
    """
    Display a raster image as either a single band or an RGB composite. Supports histogram equalization and masking.

    Parameters:
    -----------
    image_array : numpy.ndarray
        The multi-dimensional raster data array, shape (height, width) or (height, width, bands).
    rgb_bands : list or tuple, optional
        Indices of the bands to be displayed as RGB (e.g., [3, 2, 1]). Indices start from 0.
    single_band : int, optional
        Index of the single band to be displayed (e.g., 3). Index starts from 0.
    nodata_value : int, float, or list, optional
        Value(s) representing NoData. If None, no masking is applied.
    equalize : bool, optional
        Whether to apply histogram equalization to all bands. Default is False.

    Returns:
    --------
    None
    """
    # Check image dimensions
    if image_array.ndim == 2 or (image_array.ndim == 3 and image_array.shape[2] == 1):  # Single-band image
        print("Detected single-band image, ignoring single_band and rgb_bands parameters...")
        single_band = 0  # Force single-band mode
    
    elif image_array.ndim == 3:  # Multi-band image
        num_bands = image_array.shape[2]
        if single_band is not None:  # Validate single_band
            if single_band >= num_bands or single_band < 0:
                raise ValueError(f"single_band parameter is invalid. Band index should be in [0, {num_bands - 1}]!")
        elif rgb_bands is not None:  # Validate rgb_bands
            if len(rgb_bands) != 3:
                raise ValueError("rgb_bands parameter must contain exactly 3 band indices!")
            if max(rgb_bands) >= num_bands or min(rgb_bands) < 0:
                raise ValueError(f"rgb_bands parameter is invalid. Band indices should be in [0, {num_bands - 1}]!")
        else:
            raise ValueError("Either single_band or rgb_bands must be specified!")
    else:
        raise ValueError("Invalid dimensions for image_array. Must be 2D or 3D array!")

    # Create mask for NoData values
    if nodata_value is not None:
        if isinstance(nodata_value, (list, tuple)):  # Multiple NoData values
            mask = np.isin(image_array, nodata_value).all(axis=-1) if image_array.ndim == 3 else np.isin(image_array, nodata_value)
        else:  # Single NoData value
            mask = (image_array == nodata_value).all(axis=-1) if image_array.ndim == 3 else (image_array == nodata_value)
    else:
        mask = np.zeros(image_array.shape[:2], dtype=bool)  # No mask applied

    # Apply histogram equalization if required
    if equalize:
        image_array = histogram_equalize(image_array, mask)
    else:
        # Normalize the data to [0, 1] for all bands, ignoring mask
        if image_array.ndim == 2 or (image_array.ndim == 3 and image_array.shape[2] == 1):  # Single band
            image_array = (image_array - image_array.min()) / (image_array.max() - image_array.min() + 1e-10)
        elif image_array.ndim == 3:  # Multi-band
            for band in range(image_array.shape[2]):
                band_data = image_array[:, :, band]
                # Normalize the band to [0, 1]
                band_data = (band_data - band_data.min()) / (band_data.max() - band_data.min() + 1e-10)
                image_array[:, :, band] = band_data

    # Single-band display
    if single_band is not None:
        band_data = image_array[:, :, single_band] if image_array.ndim == 3 else image_array.squeeze()

        # Mask NoData regions
        band_data = np.ma.masked_array(band_data, mask=mask)

        # Display single-band image
        plt.figure(figsize=(8, 8))
        plt.imshow(band_data, cmap='gray')
        plt.colorbar(label="Pixel Value")
        plt.title(f"Band {single_band + 1 if image_array.ndim == 3 else 1} (Single Band Display)", fontsize=16)
        plt.axis("off")
        plt.show()

    # RGB composite display
    elif rgb_bands is not None:
        # Initialize RGB image
        rgb_image = np.zeros((image_array.shape[0], image_array.shape[1], 3), dtype=np.float32)

        # Process and combine RGB bands
        for i, band in enumerate(rgb_bands):
            band_data = image_array[:, :, band]
            rgb_image[:, :, i] = band_data

        # Mask NoData regions with white color
        rgb_image[mask] = [1.0, 1.0, 1.0]  # White

        # Display RGB composite image
        plt.figure(figsize=(8, 8))
        plt.imshow(rgb_image)
        plt.title("RGB Composite Image", fontsize=16)
        plt.axis("off")
        plt.show()
    
    return image_array