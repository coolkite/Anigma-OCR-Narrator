import cv2
import numpy as np
import pytesseract 
from pytesseract import Output
import googletrans
from googletrans import Translator
from gtts import gTTS
from pygame import mixer
import os
img = cv2.imread('download.jpg')

# This function converts a given image into grayscale 
def get_grayscale(image):
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale

#This function rotates the image and deskews it
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (height, width) = image.shape[:2]
    center = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (width, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#This function removes the irregularity of pixel contrast
def remove_noise(image):
    return cv2.medianBlur(image,5)
 

#This function adds pixels to boundary of objects in image
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#This function removes the boundary pixels from the objects
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)
#This function makes the threshold of the image
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#opening. Basically, erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#Used to detect a variety of edges
def canny(image):
    return cv2.Canny(image, 100, 200)
# translates a given text into another text
def translator(text, initiallanguage, language):
    ilan = initiallanguage
    lan = language
    translator = Translator()
    translated = translator.translate(text, src = ilan, dest=lan)
    return translated
# converts text to speech
def text_to_speech(text,  language):
    t=text.text
    l=language
    output = gTTS(text = t, lang=l, slow=False)
    output.save("output.mp3")
    mixer.init()
    mixer.music.load("output.mp3")
    mixer.music.play()
"""
#implementing the methods on a picture
gray = get_grayscale(img)
thresh = thresholding(gray)
opening = opening(gray)
canny = canny(gray)
#group the words in the picture and extract the text
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
d = pytesseract.image_to_data(img, output_type=Output.DICT)

# set the language of the extracted text
custom_config = r'-l eng --psm 6'

#Print the text from the image
print(pytesseract.image_to_string(img, config=custom_config))
#Speak the translated text
text_to_speech(translator(pytesseract.image_to_string(img, config=custom_config), "en", "es"), "es")
"""
