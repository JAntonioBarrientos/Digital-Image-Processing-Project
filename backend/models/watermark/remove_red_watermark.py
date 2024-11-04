import numpy as np
from PIL import Image
import cv2
from models.base_filter import BaseFilter

import numpy as np

def inpaint_iterative(img: np.ndarray, mask: np.ndarray, max_iterations: int) -> np.ndarray:
    """
    Rellena los píxeles enmascarados en una imagen de manera iterativa usando el promedio de los vecinos.

    :param img: Arreglo NumPy de la imagen en formato BGR.
    :param mask: Arreglo NumPy de la máscara binaria (255 para áreas a rellenar).
    :param max_iterations: Número máximo de iteraciones para el proceso de inpainting.
    :return: Arreglo NumPy de la imagen con inpainting aplicado.
    """
    # Crear una copia de la imagen para evitar modificar la original
    inpainted_img = img.copy()
    
    # Crear una máscara booleana donde True indica píxeles a rellenar
    mask_bool = mask == 255
    
    # Definir un kernel para los 8 vecinos
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]], dtype=np.float32)
    
    for iteration in range(max_iterations):
        print(f"Inpainting Iteración {iteration + 1}/{max_iterations}")
        updated = False
        
        # Iterar sobre cada píxel enmascarado
        ys, xs = np.where(mask_bool)
        for y, x in zip(ys, xs):
            # Definir los límites de la ventana de vecinos
            y_min = max(y - 1, 0)
            y_max = min(y + 2, inpainted_img.shape[0])
            x_min = max(x - 1, 0)
            x_max = min(x + 2, inpainted_img.shape[1])
            
            # Extraer la ventana de vecinos
            window = inpainted_img[y_min:y_max, x_min:x_max]
            window_mask = mask_bool[y_min:y_max, x_min:x_max]
            
            # Extraer los valores de los vecinos que no están enmascarados
            neighbors = window[~window_mask]
            
            if neighbors.size > 0:
                # Calcular el promedio de los vecinos
                mean_color = neighbors.mean(axis=0)
                # Actualizar el píxel en la imagen
                inpainted_img[y, x] = mean_color
                # Marcar el píxel como ya procesado
                mask_bool[y, x] = False
                updated = True
        
        if not updated:
            print("No se realizaron actualizaciones en esta iteración. Finalizando inpainting.")
            break
    
    return inpainted_img


class RemoveRedWatermarkFilter(BaseFilter):
    def __init__(self, image, sensitivity, iterations=5):
        """
        Inicializa el filtro para eliminar marcas de agua rojas.

        :param image: Objeto de imagen (PIL Image).
        :param sensitivity: Umbral para la detección de rojo (valor entre 0 y 255). 
                            Un valor más bajo detecta más tonos de rojo.
        :param iterations: Número de veces que se aplicará el filtro.
        """
        super().__init__(image)
        
        # Validar la sensibilidad
        if not (0 <= sensitivity <= 255):
            raise ValueError("La sensibilidad debe estar entre 0 y 255.")
        
        # Validar el número de iteraciones
        if iterations < 1:
            raise ValueError("El número de iteraciones debe ser al menos 1.")
        
        self.sensitivity = sensitivity
        self.iterations = iterations

    def apply_filter(self):
        """
        Aplica el filtro para eliminar marcas de agua rojas en la imagen.

        :return: Imagen procesada sin marcas de agua rojas (PIL Image).
        """
        # Convertir la imagen PIL a un arreglo NumPy en formato RGB
        img_rgb = np.array(self.image.convert('RGB'))
        
        # Convertir la imagen de RGB a BGR (formato usado por OpenCV)
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        
        # Convertir la imagen de BGR a HSV
        img_hsv = self.bgr_to_hsv(img_bgr)
        
        # Definir los rangos de color rojo en HSV
        # El rojo se encuentra en dos rangos en el espacio HSV
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([15, 255, 255])
        lower_red2 = np.array([165, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        
        # Crear máscaras para los dos rangos de rojo
        mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
        
        # Combinar ambas máscaras
        mask = cv2.bitwise_or(mask1, mask2)
        
        # Ajustar la máscara según la sensibilidad
        if self.sensitivity > 0:
            _, mask = cv2.threshold(mask, self.sensitivity, 255, cv2.THRESH_BINARY)
        
        # Dilatar la máscara para cubrir mejor las marcas de agua
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)
        
        # Aplicar inpainting para rellenar las áreas rojas detectadas
        # Usar el método Telea para un buen equilibrio entre velocidad y calidad
        inpaint_radius = 3  # Radio para el inpainting
        img_bgr = inpaint_iterative(img_bgr, mask, self.iterations)
        
        # Convertir la imagen de inpainted de BGR a RGB
        img_inpaint_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        # Convertir el arreglo NumPy de vuelta a una imagen PIL
        processed_image = Image.fromarray(img_inpaint_rgb)
        
        return processed_image

    def bgr_to_hsv(self, img_bgr: np.ndarray) -> np.ndarray:
        """
        Convierte una imagen de BGR a HSV utilizando operaciones vectorizadas de NumPy.

        :param img_bgr: Arreglo NumPy de la imagen en formato BGR.
        :return: Arreglo NumPy de la imagen en formato HSV.
        """
        img_bgr = img_bgr.astype('float32') / 255.0
        B = img_bgr[:, :, 0]
        G = img_bgr[:, :, 1]
        R = img_bgr[:, :, 2]

        Cmax = np.maximum.reduce([R, G, B])
        Cmin = np.minimum.reduce([R, G, B])
        Delta = Cmax - Cmin

        # Hue calculation
        Hue = np.zeros_like(Cmax)
        mask = Delta != 0
        # When Cmax == R
        idx = (Cmax == R) & mask
        Hue[idx] = ((60 * ((G[idx] - B[idx]) / Delta[idx])) % 360)
        # When Cmax == G
        idx = (Cmax == G) & mask
        Hue[idx] = (60 * ((B[idx] - R[idx]) / Delta[idx]) + 120) % 360
        # When Cmax == B
        idx = (Cmax == B) & mask
        Hue[idx] = (60 * ((R[idx] - G[idx]) / Delta[idx]) + 240) % 360

        # Escalar Hue a [0,179] para coincidir con OpenCV
        Hue = Hue / 2

        # Saturation calculation
        Saturation = np.zeros_like(Cmax)
        Saturation[Cmax != 0] = Delta[Cmax != 0] / Cmax[Cmax != 0]

        # Escalar Saturation a [0,255]
        Saturation = Saturation * 255

        # Value calculation
        Value = Cmax * 255

        # Combine into HSV image
        img_hsv = np.stack([Hue, Saturation, Value], axis=2).astype('uint8')

        return img_hsv
