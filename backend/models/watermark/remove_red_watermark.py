# models/remove_red_watermark_filter.py

import numpy as np
from PIL import Image
import cv2
from models.base_filter import BaseFilter

class RemoveRedWatermarkFilter(BaseFilter):
    def __init__(self, image, sensitivity, iterations=10):
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
        
        # Iterar según el número de iteraciones
        for _ in range(self.iterations):
            # Convertir la imagen de BGR a HSV
            img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            
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
            img_bgr = cv2.inpaint(img_bgr, mask, inpaint_radius, cv2.INPAINT_TELEA)
        
        # Convertir la imagen de inpainted de BGR a RGB
        img_inpaint_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        # Convertir el arreglo NumPy de vuelta a una imagen PIL
        processed_image = Image.fromarray(img_inpaint_rgb)
        
        return processed_image
