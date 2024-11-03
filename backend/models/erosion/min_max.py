import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter

def process_chunk(args):
    """
    Process a chunk of rows in the image.

    :param args: Tuple containing padded_array, y_start, y_end, width, radius, operation
    :return: Tuple of y_start and the processed chunk array
    """
    padded_array, y_start, y_end, width, radius, operation = args
    chunk_height = y_end - y_start
    chunk_result = np.zeros((chunk_height, width), dtype=np.uint8)
    for idx, y in enumerate(range(y_start, y_end)):
        for x in range(width):
            # Extract the kernel
            kernel = padded_array[y : y + 2*radius + 1, x : x + 2*radius + 1]
            if operation == 'max':
                value = np.max(kernel)
            else:
                value = np.min(kernel)
            chunk_result[idx, x] = value
    return y_start, chunk_result

class MinMaxKernelFilter(BaseFilter):
    def apply_filter(self, radius, operation='max'):
        """
        Applies a filter that replaces each pixel with the maximum or minimum value found in its kernel.

        :param radius: Radius of the kernel (positive integer).
        :param operation: 'max' for maximum, 'min' for minimum.
        :return: Processed image (PIL Image).
        """
        if radius <= 0:
            raise ValueError("El radio debe ser un entero positivo.")
        if operation not in ['max', 'min']:
            raise ValueError("La operación debe ser 'max' o 'min'.")

        # Convert the image to grayscale if not already
        gray_convert = GrayscaleFilter(self.image)
        gray_image = gray_convert.apply_filter().convert('L')

        # Convert the image to a NumPy array
        image_array = np.array(gray_image, dtype=np.uint8)

        # Get the image dimensions
        height, width = image_array.shape

        # Padding to handle the borders
        pad_width = radius
        padded_array = np.pad(image_array, pad_width, mode='edge')

        # Prepare arguments for multiprocessing
        num_workers = cpu_count()
        print(f"Using {num_workers} CPU cores for multiprocessing.")

        # Determine chunk size
        chunk_size = max(1, height // (num_workers * 4))  # Adjust factor as needed
        args_list = []
        for y_start in range(0, height, chunk_size):
            y_end = min(y_start + chunk_size, height)
            args = (padded_array, y_start, y_end, width, radius, operation)
            args_list.append(args)

        # Initialize the processed array
        processed_array = np.zeros_like(image_array)

        # Process chunks in parallel
        with Pool(processes=num_workers) as pool:
            results = pool.map(process_chunk, args_list)

        # Collect results
        for y_start, chunk_result in results:
            y_end = y_start + chunk_result.shape[0]
            processed_array[y_start:y_end, :] = chunk_result

        # Convert the processed array back to a PIL image
        processed_image = Image.fromarray(processed_array, mode='L')

        return processed_image