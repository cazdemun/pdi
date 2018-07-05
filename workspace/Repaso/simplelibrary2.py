import cv2
import base64
import numpy as np
import os, os.path


def areSimilar(countour1, countour2):
    x,y,w,h = cv2.boundingRect(countour1)
    x1,y1,w1,h1 = cv2.boundingRect(countour2)
    
    # Primer criterio
    if not h > 20:
        return False
    
    # Segundo criterio
    if not abs(y - y1) < 10:
        return False
    
    # Tercer criterio
    if abs(h - h1)/h < 0.1 and abs(w - w1)/w < 4:
        return True
    else:
        return False
    
def orderFromLeft(c):
    x,y,w,h = cv2.boundingRect(c)
    return x

def convertTo64String(img):
    _, buffer = cv2.imencode('.jpg', img)
    cnt = base64.b64encode(buffer)
    return cnt.decode("utf-8")
    
def isLetter(c):
    x,y,w,h = cv2.boundingRect(c)
    
    # Constantes de Ratio
    
    if not h > 20:
        return False
    else:
        return True
    