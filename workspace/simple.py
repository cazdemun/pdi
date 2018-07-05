from flask import Flask, make_response, render_template, Response
import cv2
import base64
import numpy as np
import os, os.path
from simplelibrary import *
from simplesvm import *

app = Flask(__name__)

@app.route('/gallery', defaults={'name' : 'P6070001'})
@app.route('/gallery/<name>')
def get_gallery(name):
    
    imageslist = getImagesList()
    
    im_names = []
    
    plaqueta = ''
    
    
    img = cv2.imread('070603/' + name + '.jpg')
    im_names.append(convertTo64String(img))
    height, width, numChannels = img.shape
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    im_names.append(convertTo64String(img_gray))
    
    _, img_bw = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    im_names.append(convertTo64String(img_bw))
    
    _, contours, _ = cv2.findContours(img_bw.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    img_c = cv2.drawContours(np.zeros((height, width, 3), np.uint8), contours, -1, (255,255,255), 1)
    im_names.append(convertTo64String(img_c))
    
    contours = [x for x in contours if cv2.boundingRect(x)[3] > 20]
    img_allC = cv2.drawContours(np.zeros((height, width, 3), np.uint8), contours, -1, (255,255,255), 1)
    
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(img_allC,(x,y),(x+w,y+h),(0,255,0),1)
        
    im_names.append(convertTo64String(img_allC))
    
    
    
    possiblePlates = []
    
    for c in contours:
        possiblePlate = []
        for c1 in contours:
            if areSimilar(c, c1):
                possiblePlate.append(c1)
        possiblePlates.append(possiblePlate)
            
    possiblePlates.sort(key=len)
    
    mainPlate = possiblePlates[-1]
    mainPlate.sort(key=lambda x: orderFromLeft(x))
    
    #img_mainC = cv2.drawContours(np.zeros((height, width, 3), np.uint8), mainPlate, -1, (255,255,255), 1)
    img_mainC = cv2.drawContours(img_c.copy(), mainPlate, -1, (255,255,255), 1)
    
    for letter in mainPlate:
        x,y,w,h = cv2.boundingRect(letter)
        cv2.rectangle(img_mainC,(x,y),(x+w,y+h),(0,255,0),1)
    
    im_names.append(convertTo64String(img_mainC))
    
    
    letterImageArray = []

    for letter in mainPlate:
        x,y,w,h = cv2.boundingRect(letter)
        img_letter = img_rgb[y:y+h,x:x+w]
        letterImageArray.append(img_letter)
    
    P = []
    
    for letter in letterImageArray:
        auxl = cv2.resize(letter, (20, 20))
        fd=hog(auxl, orientations = 8, pixels_per_cell = (ppc, ppc), cells_per_block = (1, 1))
        P.append(fd)
    
    P = np.vstack(P)
    P = np.float32(P)

    
    result = svm.predict(P)[1]
    mask = result
    correct = np.count_nonzero(mask)
    plate = [ chr(c) for c in result ]
    plaqueta = ''.join(plate)
    
    return render_template("gallery.html", image_names=im_names, img_names=imageslist, placa=plaqueta)

def getImagesList():
    lista  = []
    imageDir = os.getcwd()
    #print(imageDir +'/070603')

    
    file_list = os.listdir(imageDir + '/070603')
        
    for folder in file_list:
        if not os.path.isdir(folder) and folder.endswith('.jpg'):
            lista.append(os.path.splitext(folder)[0])
                
    #print(lista)
    
    return sorted(lista)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)