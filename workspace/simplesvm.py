import numpy as np
import cv2
import os, os.path
import skimage
from  skimage.feature import hog

percentage = 0.8 # Porcentaje de imágenes usadas
ppc = 5 # Pixels per cell

# Construccion de base de datos

labels = []
dic = {}

imageDir = os.getcwd()

file_list = os.listdir(imageDir + '/entrenamiento')
    
for folder in file_list:
    labels.append(ord(folder))
    dic[ord(folder)] = []

    for file in os.listdir(imageDir + '/entrenamiento/' + folder):
        dic[ord(folder)].append(folder + "/" + file)
            
D=[] # Descriptores
L=[] # Etiquetas

# Construir dataset de entrenamiento (cálculo del HOG)

for label in labels:
    size = len(dic[label])
    for im in dic[label][:int(size * percentage)]:
        auxIm = cv2.imread(imageDir + '/entrenamiento/'+ im, 0)
        auxIm = cv2.resize(auxIm, (20, 20))
        fd=skimage.feature.hog(auxIm, orientations = 8, pixels_per_cell = (ppc, ppc), cells_per_block = (1, 1))
        
        D.append(fd)
        L.append(label)

D = np.vstack(D)
D = np.float32(D)

L = np.vstack(L)

# Creamos máquina de aprendizaje
svm = cv2.ml.SVM_create()

svm.setKernel(cv2.ml.SVM_LINEAR)
svm.setType(cv2.ml.SVM_C_SVC)
svm.setC(2.67)
svm.setGamma(5.383)

svm.train(D, cv2.ml.ROW_SAMPLE, L)