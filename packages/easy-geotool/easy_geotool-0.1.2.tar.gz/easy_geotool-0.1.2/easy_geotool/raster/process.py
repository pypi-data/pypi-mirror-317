import numpy as np
from skimage.exposure import equalize_hist

def histogram_equalize(image_array, mask):
    """
    Perform histogram equalization for all bands in the image array, ignoring masked regions.

    Parameters:
    -----------
    image_array : numpy.ndarray
        The multi-band raster data array, shape (height, width, bands) or (height, width).
    mask : numpy.ndarray
        Mask array with the same height and width as `image_array`. Masked regions have a value of True.

    Returns:
    --------
    equalized_array : numpy.ndarray
        The histogram-equalized image array, with the same shape as the input `image_array`.
    """
    # Handle single-band images by adding a dummy third dimension
    if image_array.ndim == 2:
        image_array = image_array[:, :, None]

    # Initialize variables
    height, width, bands = image_array.shape
    equalized_array = np.zeros_like(image_array, dtype=np.float32)

    # Process each band separately
    for band in range(bands):
        band_data = image_array[:, :, band]
        # Extract non-masked values
        non_masked_values = band_data[~mask]
        equalized_band = np.zeros_like(band_data, dtype=np.float32)

        if len(non_masked_values) > 0:
            # Perform histogram equalization on non-masked values
            equalized_values = equalize_hist(non_masked_values)
            equalized_band[~mask] = equalized_values

        equalized_array[:, :, band] = equalized_band

    # Remove the dummy third dimension for single-band images
    return equalized_array.squeeze()
