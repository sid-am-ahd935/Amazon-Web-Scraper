
import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
from PIL import Image
from subprocess import check_output
import cv2
import numpy as np

# def get_captcha(html): 
#    tree = lxml.html.fromstring(html) 
#    img_data = tree.cssselect('div.a-row.a-text-center')[0].get('src') 
#    img_data = img_data.partition(',')[-1] 
#    binary_img_data = img_data.decode('base64') 
#    file_like = BytesIO(binary_img_data) 
#    img = Image.open(file_like) 
#    return img 



# img = get_captcha(html_file.read())
# img.save('captcha_original.png') 
# gray = img.convert('L') 
# gray.save('captcha_gray.png') 
# bw = gray.point(lambda x: 0 if x < 1 else 255, '1') 
# bw.save('captcha_thresholded.png') 

# # print(pytesseract.image_to_string(bw))


# def resolve(path):
#     print("Resampling the Image")
#     check_output(['convert', path, '-resample', '600', path])
#     return pytesseract.image_to_string(Image.open(path))




def get_captcha(r : "requests.get"):
    text = r.content.decode('utf-8')

    img_src = re.search("https://images-na.ssl-images-amazon.com/captcha", text, re.I), re.search("\.jpg", text, re.I)
    
    print(img_src)
    img_url = text[img_src[0].start(): img_src[1].end() + 1]

    img_r = requests.get(img_url, stream= True)
    img_r.raw.decode_content = True

    with open("captcha.jpg", 'wb')as f:
        shutil.copyfileobj(img_r.raw, f)
    
    return 



def resolve_captcha(path):
    print("Resampling the Image")
    check_output(['convert', path, '-resample', '600', path])
    # Grayscale image
    img = Image.open(path).convert('L')
    ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)

    # Older versions of pytesseract need a pillow image
    # Convert back if needed
    img = Image.fromarray(img.astype(np.uint8))

    print(pytesseract.image_to_string(img, config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))

    # Creating a Grayscale image again in an attempt to refine the already greyscaled image
    ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)

    # Older versions of pytesseract need a pillow image
    # Convert back if needed
    img = Image.fromarray(img.astype(np.uint8))

    return pytesseract.image_to_string(img, config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
