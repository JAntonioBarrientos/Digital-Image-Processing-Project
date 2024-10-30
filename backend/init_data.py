from models.mosaico.mosaic_filter import MosaicFilter
from PIL import Image

def initialize_csv():
    # Aquí asumimos que tienes una imagen de inicio o puedes pasar None si el constructor maneja eso
    dummy_image = Image.new('RGB', (1, 1))
    mosaic_filter = MosaicFilter(image=dummy_image)
    # Ejecutar el método que crea el CSV
    # Asumiendo que la inicialización ya crea el CSV si no existe
    print("Inicialización del CSV completada.")

if __name__ == "__main__":
    initialize_csv()
