import cv2
import numpy
from PIL import Image, ImageTk
from fileutils import FilesFinder


class ImageLoader:
    def __init__(self, folder) -> None:
        self.proc_folder = folder   

    def load_all_image_from_folder(self):
        return FilesFinder(self.proc_folder).by_extension(".jpeg")