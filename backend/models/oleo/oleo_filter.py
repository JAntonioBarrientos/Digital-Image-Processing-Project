import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter
from models.convolutionFilters.filters.blur_filter import BlurFilter

class OleoFilter(BaseFilter):
    @staticmethod
    def process_pixel_row(args):
        image_array_padded, i, width, block_size = args
        pad_size = block_size // 2
        row_result = []
        for j in range(width):
            # Extract the block centered at (i, j)
            block = image_array_padded[i:i+block_size, j:j+block_size, :]
            block_flat = block.reshape(-1, block.shape[2])
            # Convert RGB colors to single integers for easy counting
            colors = (block_flat[:, 0].astype(np.int32) << 16) + \
                     (block_flat[:, 1].astype(np.int32) << 8) + \
                      block_flat[:, 2].astype(np.int32)
            unique, counts = np.unique(colors, return_counts=True)
            most_common_color = unique[np.argmax(counts)]
            # Convert back to RGB
            r = (most_common_color >> 16) & 0xFF
            g = (most_common_color >> 8) & 0xFF
            b = most_common_color & 0xFF
            row_result.append((r, g, b))
        return row_result

    def apply_filter(self, color, blur, block_size):
        """
        Applies the filter by assigning to each pixel the most frequent color in its block of block_size x block_size pixels.
        """
        if not color:
            grayscale_filter = GrayscaleFilter(self.image)
            self.image = grayscale_filter.apply_filter()
        
        # Convert the image to a NumPy array
        image_array = np.array(self.image, dtype=np.uint8)
        height, width = image_array.shape[:2]
        
        # Pad the image to handle borders
        pad_size = block_size // 2
        image_array_padded = np.pad(
            image_array,
            ((pad_size, pad_size), (pad_size, pad_size), (0, 0)),
            mode='edge'
        )
        
        # Prepare arguments for multiprocessing
        args_list = []
        for i in range(height):
            args_list.append((image_array_padded, i, width, block_size))
        
        # Process rows with multiprocessing
        num_workers = min(cpu_count(), len(args_list))
        print(f"Using {num_workers} CPU cores for multiprocessing.")
        
        output_array = np.zeros_like(image_array)
        
        with Pool(processes=num_workers) as pool:
            for i, row_result in enumerate(pool.imap_unordered(OleoFilter.process_pixel_row, args_list)):
                output_array[i, :, :] = row_result
        
        # Convert the NumPy array back to a PIL image
        processed_image = Image.fromarray(output_array, mode='RGB')
        
        if blur:
            blur_filter = BlurFilter(processed_image)
            processed_image = blur_filter.apply_filter(2)
        
        return processed_image

