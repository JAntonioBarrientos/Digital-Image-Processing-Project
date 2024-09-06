class BaseFilter:
    def __init__(self, image):
        self.image = image

    def apply_filter(self):
        raise NotImplementedError("Subclasses must implement this method")
