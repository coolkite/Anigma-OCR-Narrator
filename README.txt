This is an OCR program that helps visually-impaired or those with a language barrier access literature by reading and translating text in a book. 

This program is intended to be used on a mobile device, but for prototyping, a simulated version of the program is being used.

This program loads an image of a page, extracts text using machine learning, and uses an API to translate the text to a wide range of desired languages. It then displays and narrates the translated text.

To run, execute app.py

There are included packages to make running this program easier. cv2, googletrans, gtts, gtts_token, pydub, and pytesseract, pygame_gui are all third-party libraries included in the directory that are not created by the initial owners. These aid in OCR, narration, and translation. Other third-party libaries include numpy and pygame for processing. 

orlib is our own program.

By Henry Zhang, Divyansh Shivashok, Ryan Weiner