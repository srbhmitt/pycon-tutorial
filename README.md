# pycon-tutorial

- [Installations and setup](#setup)
- [Training Tesseract for new fonts](#training)

## <a name="setup"></a>Installations and setup
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

# For Windows:

Download and install this: https://github.com/UB-Mannheim/tesseract/wiki

Open the views tab and create a new variable to point to the install. For example:

pt2='C:\\Users\\GMZ094\\AppData\\Local\\Tesseract-OCR\\tesseract'

then update the subprocess calls in views.py. For example from:

text1=subprocess.check_output(['tesseract',destination1,"stdout","-l","eng","-psm","4"])

to:

text1=subprocess.check_output([pt2,destination1,"stdout","-l","eng","-psm","4"])


## <a name="training"></a>Training a new font with Tesseract
Tesseract allows [training of new fonts and even new languages](https://github.com/tesseract-ocr/tesseract/wiki/Training-Tesseract), which requires installing Tesseract with this command:
```
brew install --with-training-tools tesseract
```

You'll need to `brew uninstall tesseract` first if you already have it installed.

Try to run Tesseract on the current image example in the training folder:

```
tesseract eng.icr.exp0.tiff before_training
```

The resulting `before_training.txt` file gives us an idea of what the results would be on a new untrained font.  Now we can use this image to train and see what the results would be after training. Typically, this is a [manual process](http://pp19dd.com/tesseract-ocr-chopper/) involving a human to manually go through each character and dictating whether the guessed output is correct or not, and provide the correct character if it's incorrect. In the interest of time, we've done this for you already, and the results are in the .box file.

To train on the new font, you'd need both the original .tiff and the .box file, with their names **exactly** the same. In the training folder, you can use the following command that trains on this new font:

```
bash tesseract.sh eng.icr.exp0 icr
```

Now to see the new results after training, use the following command:

```
tesseract eng.icr.exp0.tiff after_training -l icr
```

Check `after_training.txt` and compare it to `before_training.txt` to see the difference!

Usually, you would want to train with more text, we've minimized the text here for the sake of time.
