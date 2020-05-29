import pytesseract
from PIL import Image

#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

image = Image.open('C:\\Users\\YFZX\\Desktop\\target.jpg')
content = pytesseract.image_to_string(image, lang="chi_sim")   # 解析图片
print(content)

