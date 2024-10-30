from threading import Lock

class PreprocessingStatus:
    def __init__(self):
        self.lock = Lock()
        self.is_preprocessing = False

    def set_preprocessing(self, status: bool):
        with self.lock:
            self.is_preprocessing = status

    def get_preprocessing(self) -> bool:
        with self.lock:
            return self.is_preprocessing

# Instancia global para ser utilizada en toda la aplicación
preprocessing_status = PreprocessingStatus()
