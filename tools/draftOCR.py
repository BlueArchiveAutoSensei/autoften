import pytesseract
from PIL import Image
import timeit

# 先加载图像，作为全局变量
img = Image.open(r'c:\Users\Vickko\Pictures\Image21.png')

# 定义一个函数来执行OCR操作
def ocr_image():
    # 这里只进行OCR识别，不再加载图像
    text = pytesseract.image_to_string(img, config='--psm 10')
    #print(text)

# 使用timeit运行这个函数100次，并获取总的运行时间
total_time = timeit.timeit('ocr_image()', setup='from __main__ import ocr_image', number=100)

# 打印平均每次运行的时间（毫秒）
average_time = total_time / 100 * 1000
print(f'Average time per recognition: {average_time} ms')
