# pycon-tutorial

This is the repo which contains the code for the pycon-tutorial Capital One is sponsoring in 2016. This tutorial teaches
how to create a simple web application to do OCR.

To run the code on your Mac. Please follow the steps below to install the required libraries.

To follow along, attendees will require a laptop with Python (>=2.7) and the Python packages Flask and Pillow installed.

Run following command in terminal:

- brew install automake libtool jpeg libtiff libpng leptonica tesseract ghostscript
- Ensure the following path exists first: /usr/local/Cellar/tesseract/3.04.01_2/share
- Add the below line to your .bash_profile:
  - export TESSDATA_PREFIX="/usr/local/Cellar/tesseract/3.04.01_2/share"
- Run “tesseract - v” to ensure that Tesseract installed successfully

Then just run python run.py from your terminal.
