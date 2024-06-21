from PIL import ImageFont
import os

from api.src.const import BASE_PATH


def find_ttf_file(name, folder_path='/all_fonts'):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.ttf') and name in file:
                return os.path.join(root, file)
    return os.path.join(BASE_PATH, "src/create_diploma/all_fonts/times new roman.ttf")


class ElementFont:
    def __init__(self, name, size) -> None:
        self.font_path = find_ttf_file(name, ".venv\\src\\create_diploma\\all_fonts")
        self.size = size
    
    def get_font(self):
        return ImageFont.truetype(self.font_path, self.size)
    

    
# element_font = ElementFont("times new roman", 14)
# print(element_font.getFont())