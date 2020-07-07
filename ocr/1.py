import pytesseract
from PIL import Image

text = pytesseract.image_to_string(Image.open('test.png').convert('L'),lang="chi_sim")

print(text)