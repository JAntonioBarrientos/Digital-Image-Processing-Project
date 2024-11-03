from PIL import Image
import numpy as np
from models.base_filter import BaseFilter
from models.filters.grayscale_filter import GrayscaleFilter

class ClusteredDitheringFilter(BaseFilter):

    def __init__(self, image):
        """
        Initializes the clustered dithering filter with a grayscale image.
        :param image: PIL Image object.
        """
        # Convert to grayscale using GrayscaleFilter
        im_gray = GrayscaleFilter(image)
        super().__init__(im_gray.apply_filter())  # Initialize base class with grayscale image

        self.width, self.height = self.image.size

        # Define the 3x3 clustered matrix
        self.cluster_matrix = np.array([
            [8, 3, 4],
            [6, 1, 2],
            [7, 5, 9]
        ])

        # Scale the matrix to match the pixel scaling (0-255)
        self.threshold_matrix = self.cluster_matrix * (255 / (self.cluster_matrix.max() + 1))

    def apply_filter(self):
        """
        Applies clustered dithering using a 3x3 matrix.
        :return: Dithered PIL Image.
        """
        # Convert image to NumPy array
        image_array = np.array(self.image.convert('L'), dtype=np.uint8)

        # Create a threshold map based on the position in the 3x3 matrix
        Y, X = np.indices((self.height, self.width))
        cluster_indices_x = X % 3
        cluster_indices_y = Y % 3
        threshold_map = self.threshold_matrix[cluster_indices_y, cluster_indices_x]

        # Create mask where pixel value is less than the threshold
        mask = image_array < threshold_map

        # Create the result array: 0 where mask is True, 255 otherwise
        result_array = np.where(mask, 0, 255).astype(np.uint8)

        # Convert result array to PIL Image
        result_image = Image.fromarray(result_array, mode='L')

        return result_image