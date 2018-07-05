from flask import Flask, make_response, render_template, Response
import cv2
import base64
import numpy as np
import os, os.path

app = Flask(__name__)

@app.route('/gallery', defaults={'name' : 'P6070001'})
@app.route('/gallery/<name>')
def get_gallery(name):
    
    imageslist = getImagesList()
    
    im_names = []
    
    img = cv2.imread('070603/' + name + '.jpg')

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    retval, buffer = cv2.imencode('.jpg', img)
    cnt = base64.b64encode(buffer)
    im_names.append(cnt.decode("utf-8"))
        
    try:
        white = np.uint8([[[255,255,255]]])
        white_hsv = cv2.cvtColor(white, cv2.COLOR_RGB2HSV)
        
        lower_white = np.array([0, 0, 230])
        upper_white = np.array([10, 255, 255])
        
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(img_hsv, lower_white, upper_white)
        mask = cv2.GaussianBlur(mask, (3,3), 0)
        
        res = cv2.bitwise_and(img_rgb, img_rgb, mask = mask)
        res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
        #res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
        
        retval, buffer = cv2.imencode('.jpg', res)
        cnt = base64.b64encode(buffer)
        im_names.append(cnt.decode("utf-8"))
        
        row, col, _ = img.shape
        pad = col - row
        
        x = cv2.getGaussianKernel(row, 100)
        gaussian = x * x.T
        superGaussian = gaussian
        
        for i in range(0, row):
            for j in range(0, row):
                if gaussian[i][j] < 0.000005:
                    superGaussian[i][j] = 0
                else:
                    superGaussian[i][j] = 1
        
        mask = np.zeros((row, col))
        mask[:row,pad//2:pad//2+row] = superGaussian
        
        # Applying filters
        img_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        img_gray = img_gray * mask
        # Printing
        retval, buffer = cv2.imencode('.jpg', img_gray)
        cnt = base64.b64encode(buffer)
        im_names.append(cnt.decode("utf-8"))
        
        c0, c1 = col, 0
        r0, r1 = row, 0
        
        for i in range(0, row):
            for j in range(0, col):
                if j < c0 and img_gray[i][j] != 0:
                    c0 = j
                if j > c1 and img_gray[i][j] != 0:
                    c1 = j
                if i < r0 and img_gray[i][j] != 0:
                    r0 = i
                if i > r1 and img_gray[i][j] != 0:
                    r1 = i
        
        recortado = img[r0:r1,c0:c1]
        
        retval, buffer = cv2.imencode('.jpg', recortado)
        cnt = base64.b64encode(buffer)
        im_names.append(cnt.decode("utf-8"))
    
        return render_template("gallery.html", image_names=im_names, img_names=imageslist)
    except:
        print("ESTO ES UN ERROR PERO NO ENTRA")
        return render_template("gallery.html", image_names=im_names, img_names=imageslist)

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