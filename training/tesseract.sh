#!/bin/bash
# have this script in the same folder as the .tiff and .box files
# call script by:
# bash tesseract.sh name_of_file_no_extension three_letter_code
# example:
# bash tesseract.sh eng.applechancery.exp0 icr
cur_path=`pwd`
echo $cur_path

#generating training file from box and tiff files
#box and tiff files have to be named exactly the same
tiff="$1.tiff"
`tesseract $tiff $1 box.train`

#extracting the unicharset from the box file
box="$1.box"
echo $box
`unicharset_extractor $box`

#generate the font_properties file
`echo "$2 0 0 0 0 0" > font_properties`

#cluster features that were generated
train="$1.tr"
`mftraining -F font_properties -U unicharset -O unicharset $train`
`cntraining $train`

#rename all resulting files
`mv normproto $2.normproto`
`mv shapetable $2.shapetable`
`mv pffmtable $2.pffmtable`
`mv inttemp $2.inttemp`
`mv unicharset $2.unicharset`

#now combine all of them into one file
`combine_tessdata $2.` || true

#move this into tesseract's folder
`mv $2.traineddata /usr/local/share/tessdata`
