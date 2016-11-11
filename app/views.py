

#Now let's add more functionality like buttons to our web application


import os
from flask import render_template, request
from app import app
import subprocess
import re
from PIL import Image



APP_ROOT= os.path.dirname(os.path.abspath(__file__))

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
    button_title = {'title1': 'Upload Image', 'title2':'Convert to text','title3':'Get text orientation',
    'title4':'Get all coordinates','title5':'Get its coordinates', 'title6':'Crop out this text', 'title7': 'Detect checkmark'}
    return render_template('index.html',
                           button_title=button_title)

                           

def get_orientation(linktoimage):
    orientationdata = subprocess.check_output(["tesseract", linktoimage, "stdout", "-psm", "0"], stderr=subprocess.STDOUT)
    orientpattre = re.compile('Orientation in degrees: (\d+)')
    degrees = orientpattre.findall(orientationdata)
    degrees = degrees[0]
    return degrees


def findcoordinates(word,text,boxdata):
    nowhitespacetext="".join(e for e in text if e.isalnum())
    coordinates={}
    newword="".join(e for e in word if e.isalnum())
    wordindex=nowhitespacetext.find(newword)
    coordata=boxdata.splitlines()
    coordinates['start']=coordata[wordindex+1]
    coordinates['end']=coordata[wordindex+len(newword)]
    return coordinates                   

def find_checkmark(image, leftwards, radius, distance, coordinates):
    if not coordinates:
        return 0
    if type(coordinates) == list:
        coordinates = coordinates[0]
    coorarray = coordinates.split(" ")
    img = Image.open(image)
    height = img.size[1]
    
    xstart = int(coorarray[1])
    ystart = int(coorarray[2])
    xend = int(coorarray[3])
    yend = int(coorarray[4])
    
    ycenter = int((ystart + yend)/2)
    print ycenter
    
    if leftwards:
        xcenter = xstart - distance
    else:
        xcenter = xend + distance
    #print xcenter
    cropdim = (xcenter - radius, height - ycenter - radius/1.5, xcenter + radius-10, height - ycenter + radius/1.5)
    cropdim = tuple([int(x) for x in cropdim])
    crop = img.crop(cropdim)
    #crop.save("./mycrop"+ str(ystart) + ".jpg")
    
    cropheight = crop.size[1]
    cropwidth = crop.size[0]
    
    numofpixels = 0
    numofdarkpixels = 0
    pix = crop.load()
    for x in range(cropwidth):
        for y in range(cropheight):
            color = pix[x,y]
            if sum(color) < 1020:
                numofdarkpixels += 1
            numofpixels += 1
            print color
    ratio = float(numofdarkpixels) / float(numofpixels)
    print numofdarkpixels
    print numofpixels
    crop.close()
    return ratio

@app.route('/submissionsuccess',methods=['GET','POST'])
def success():
    
    target=os.path.join(APP_ROOT,'images')
    
    if not os.path.isdir(target):
        os.mkdir(target)
    destination1="/".join([target,'file1.tif'])  
    file1 = request.files['file1']
    file1.save(destination1)

    if request.method == 'POST':
        if request.form['submit'] == 'Convert to text':
            text1=subprocess.check_output(['tesseract',destination1,"stdout","-l","eng","-psm","4"])
            return text1
        elif request.form['submit'] == 'Get orientation':
            orientation1=get_orientation(destination1)
            return orientation1
        elif request.form['submit'] == 'Get all coordinates':
            box1=subprocess.check_output(['tesseract',destination1,"stdout","-l","eng","-psm","4","makebox"])
            mytext = "<br />".join(box1.split("\n"))
            return mytext
        elif request.form['submit'] == 'Get its coordinates':
            word = request.form['coortext']
            text1=subprocess.check_output(['tesseract',destination1,"stdout","-l","eng","-psm","4"])
            box1=subprocess.check_output(['tesseract',destination1,"stdout","-l","eng","-psm","4","makebox"])
            PatternCoor=findcoordinates(word,text1,box1)
            return PatternCoor['start']+" "+PatternCoor['end']
        elif request.form['submit'] == 'Crop out this text':
            #return request.form['croptext']
            
            target=os.path.join(APP_ROOT,'images')
            word = request.form['croptext']
            text1=subprocess.check_output(['tesseract',destination1,"stdout","-l","eng","-psm","4"])
            box1=subprocess.check_output(['tesseract',destination1,"stdout","-l","eng","-psm","4","makebox"])
            PatternCoor=findcoordinates(word,text1,box1)
            img = Image.open(destination1)
            height = img.size[1]
            cropdim = (int(list(PatternCoor['start'].split())[1]), height- int(list(PatternCoor['end'].split())[4]), int(list(PatternCoor['end'].split())[3]), height - int(list(PatternCoor['end'].split())[2]))
            cropdim = tuple([int(x) for x in cropdim])
            crop = img.crop(cropdim)
            cropdestination1="/".join([target,'crop1.png'])
            crop.save(cropdestination1)            
            return "Done. Please check the images folder"
        elif request.form['submit'] == 'Detect checkmark':
            #return request.form['croptext']
            word = request.form['croptext']
            text1=subprocess.check_output(['tesseract',destination1,"stdout","-l","eng","-psm","4"])
            box1=subprocess.check_output(['tesseract',destination1,"stdout","-l","eng","-psm","4","makebox"])
            OptionACoor=findcoordinates('Python',text1,box1)
            OptionBCoor=findcoordinates('Java',text1,box1)
            OptionCCoor=findcoordinates('Objective',text1,box1)
            
            OptionARatio=find_checkmark(destination1,True , 15, 17,OptionACoor['start'] )
            OptionBRatio=find_checkmark(destination1,True , 15, 17,OptionBCoor['start'] )
            OptionCRatio=find_checkmark(destination1,True , 15, 17,OptionCCoor['start'] )
            
            return "Python is "+str(OptionARatio)+"<br>"+"Java is "+str(OptionBRatio)+"<br>"+"Objective C is "+str(OptionCRatio)
        else:
            pass # unknown
    
    
    

