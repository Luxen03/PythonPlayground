import pyforms
from pyforms.controls import ControlButton
from pyforms.controls import ControlImage
from pyforms.controls import ControlText
import cv2
import os
import shutil

from memory_profiler import profile
import requests


class Recognizer(pyforms.BaseWidget):
    def __init__(self):
        #initialize
        super(Recognizer, self).__init__("Recognizer")
        #self.model = YOLO("yolo11n-seg.pt")
        self.camera = cv2.VideoCapture(0)

        #memory
        self.identities = {}
        self.identityIndex = 0
        self.isTrained = False

        #cameraControls
        self.image = ControlImage()
        self.camButton = ControlButton("Start Camera Feed!")
        self.camButton.value = self.start
        self.textBox = ControlText("Place person's name here")
        
        #libraryControls
        self.libImage = ControlImage()
        self.prevButton = ControlButton("<<<")
        self.prevButton.value = self.prevFunc
        self.deleButton = ControlButton("No images found")
        self.deleButton.value = self.deleteIdentity
        self.nextButton = ControlButton(">>>")
        self.nextButton.value = self.nextFunc
        self.trainButton = ControlButton("Start training!")
        self.trainButton.value = self.train
        self.predButton = ControlButton("Start predicting!")
        self.predButton.value = self.predict
        
        #structure
        self.formset = [{
            "Camera" : ["image", "textBox", "camButton", "predButton"],
            "Library" : ["libImage", ("prevButton", "deleButton", "nextButton"), "trainButton"]
        }]

    #@profile
    def start(self):
        #change button to take picture
        self.camButton.label = "Take Picture!"
        self.camButton.value = self.takePicture
        #start cam
        self.isOpen, pic = self.camera.read()
        while self.isOpen:
            self.isOpen, pic = self.camera.read()
            self.image.value = pic
            #self.image.value = self.model.predict(pic)[0].plot()
            cv2.waitKey(20)

    #@profile
    def takePicture(self):
        #guard input
        name = self.textBox.value
        if (name == ""): return
        print("PICTURE TAKEN")
        #instantiate identity
        if (not name in self.identities.keys()):
            self.identities[name] = []
        self.identities[name].append(self.image.value)
        #update libImage
        self.libImage.value = self.identities[name]
        self.deleButton.label = f"delete {name}?"
        self.identityIndex = list(self.identities.keys()).index(name)

    def prevFunc(self):
        if (len(self.identities) <= 1): return
        self.identityIndex = (self.identityIndex - 1) % len(self.identities)
        self.libImage.value = self.identities[list(self.identities.keys())[self.identityIndex]]
        self.deleButton.label = f"delete {list(self.identities.keys())[self.identityIndex]}?"

    def deleteIdentity(self):
        if (len(self.identities) == 0): return
        del self.identities[list(self.identities.keys())[self.identityIndex]]
        if (len(self.identities) == 0):
            self.deleButton.label = "No images found"
            return
        self.prevFunc()

    def nextFunc(self):
        if (len(self.identities) <= 1): return
        self.identityIndex = (self.identityIndex + 1) % len(self.identities)
        self.libImage.value = self.identities[list(self.identities.keys())[self.identityIndex]]
        self.deleButton.label = f"delete {list(self.identities.keys())[self.identityIndex]}?"

    def train(self):
        self.isOpen = False
        if (os.path.exists("Datasets")): shutil.rmtree("Datasets")
        for identity in self.identities.keys():
            if (not os.path.exists(f"Datasets/{identity}")):
                os.makedirs(f"Datasets/{identity}")
            i = 0
            for image in self.identities[identity]:
                cv2.imwrite(f"Datasets/{identity}/{i:03}.jpg", image)
                i += 1
        self.isTrained = True
        #PLACE FACE TRAINING CODE HERE!!!

        #PLACE FACE TRAINING CODE HERE!!!

    def predict(self):
        if (not self.isTrained): return
        #PLACE FACE RECOG CODE HERE!!!
 
        #PLACE FACE RECOG CODE HERE!!!

if __name__ == "__main__":
    recognizer = pyforms.start_app(Recognizer, geometry = (500, 500, 1000, 700))
