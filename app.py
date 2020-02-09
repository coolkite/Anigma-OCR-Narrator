import orlib
import tkinter as tk
import pygame
import cv2
import pygame_gui
import pytesseract
from pytesseract import Output
from gtts import gTTS
from pydub import AudioSegment
from tkinter.filedialog import askopenfilename
from googletrans import Translator
from pygame import mixer

pygame.init()
mixer.init()
root = tk.Tk()
root.withdraw()

def open_file_dialog():
    f = askopenfilename()
    return f

pygame.init()

def speak(filename, language):
    string = getText(filename)
    mp3 = gTTS(text = string, language = l, slow = False)
    mp3.save("audio.mp3")
    src = mp3
    dst = "waveFile.wav"
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format='wav')

    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(0)
    pygame.mixer.music.stop()

"""

back = tk.Frame(master, bg = 'black')

label = tk.Label(master, text = "enter image path name").grid(row = 0)
label2 = tk.Label(master, text = "language:").grid(row = 1)

path = tk.Entry(master).grid(row = 0, col = 1)
lang = tk.Entry(master).grid(row = 1, col = 1)


getPathButton = tk.Button(master, text = "Start", command = speak(path.get(), lang.get()))
getPathButton.grid(row = 2, col = 0)

master.mainloop()

"""

def animate():

    screen.fill((255, 255, 255))
    manager.draw_ui(screen)
    pygame.display.flip()

screen = pygame.display.set_mode((400, 600))
manager = pygame_gui.UIManager((400, 600))         # Main screen

home = pygame_gui.core.UIContainer(relative_rect=pygame.Rect((0, 0), (400, 600)),
                                   manager=manager)
bluprint = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (400, 30)),
                                          text="MIT | blueprint", parent_element=home, container=home, manager=manager)
title_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 35), (400, 100)),
                                         text="Anigma", parent_element=home, container=home, manager=manager)
from_dropdown = pygame_gui.elements.UIDropDownMenu(["English", "Spanish", "Chinese", "Hindi", "Japanese", "French"], "Select language...",
                                                   relative_rect=pygame.Rect((200, 155), (175, 50)),
                                                   parent_element=home, container=home, manager=manager)
from_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((25, 155), (150, 50)), text="Original language",
                                        parent_element=home, container=home, manager=manager)

to_dropdown = pygame_gui.elements.UIDropDownMenu(["English", "Spanish", "Chinese", "Hindi", "Japanese", "French"], "Select language...",
                                                   relative_rect=pygame.Rect((200, 220), (175, 50)),
                                                   parent_element=home, container=home, manager=manager)
to_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((25, 220), (150, 50)), text="Translate to",
                                        parent_element=home, container=home, manager=manager)

upload_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 300), (175, 50)),
                                             text="Choose a picture", parent_element=home, container=home, manager=manager)
upload_file = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((25, 300), (150, 50)),
                                          text="Chosen file", parent_element=home, container=home, manager=manager)
label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20, 390), (200, 30)),
                                    text="Extracted text", parent_element=home, container=home, manager=manager)
extracted_text = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((20, 420), (360, 160)),
                                               html_text="", parent_element=home, container=home, manager=manager)

key_dict = {
    "English" : "en",
    "Spanish" : "es",
    "Chinese" : "zh-CN",
    "Hindi" : "hi",
    "Japanese" : "ja",
    "French" : "fr"
}

clock = pygame.time.Clock()
running = True
filep = None
image = None
while running:
    delta = clock.tick(60)/1000.0
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        elif e.type == pygame.USEREVENT:
            if e.user_type == 'ui_button_pressed':
                if e.ui_element == upload_button:
                    filep = open_file_dialog()
                    upload_file.text = filep.split("/")[-1]
                    upload_file.rebuild()
                    upload_button.set_text("Processing...")
                    #upload_button.rebuild()
                    
        manager.process_events(e)

    manager.update(delta)

    animate()
    if filep:
        # Load image from filep
        image = cv2.imread(filep)
        filep = False
        # Load text
        gray = orlib.get_grayscale(image)
        thresh = orlib.thresholding(gray)
        opening = orlib.opening(thresh)

        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
        custom_config = r'-l eng --psm 6'

        string = pytesseract.image_to_string(image, config=custom_config)
        trans = orlib.translator(string, key_dict[from_dropdown.selected_option], key_dict[to_dropdown.selected_option])
        extracted_text.html_text = trans.text
        extracted_text.rebuild()
        # Play the text
        orlib.text_to_speech(trans, key_dict[to_dropdown.selected_option])

        upload_button.set_text("Choose a picture")
        #upload_button.rebuild()
    
pygame.quit()
root.destroy()
