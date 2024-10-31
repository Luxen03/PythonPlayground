import pyforms
from pyforms.controls import ControlButton
from pyforms.controls import ControlImage
from pyforms.controls import ControlText
import cv2
from ultralytics import YOLO


class Recognizer(pyforms.BaseWidget):
    def __init__(self):
        #initialize
        super(Recognizer, self).__init__("Recognizer")
        self.model = YOLO("yolo11n-seg.pt")
        self.camera = cv2.VideoCapture(0)

        #memory
        self.identities = {}
        self.identityIndex = 0

        #cameraControls
        self.image = ControlImage()
        self.camButton = ControlButton("Start Camera Feed!")
        self.camButton.value = self.start
        self.textBox = ControlText("Place person's name here")
        
        #libraryControls
        self.libImage = ControlImage()
        self.prevButton = ControlButton("<<<")
        self.deleButton = ControlButton("No images found")
        self.nextButton = ControlButton(">>>")
        
        #structure
        self.formset = [{
            "Camera" : ["image", "textBox", "camButton"],
            "Library" : ["libImage", ("prevButton", "deleButton", "nextButton")]
        }]


    def start(self):
        #change button to take picture
        self.camButton.label = "Take Picture!"
        self.camButton.value = self.takePicture
        #start cam
        isOpen, pic = self.camera.read()
        while isOpen:
            isOpen, pic = self.camera.read()
            #self.image.value = pic
            self.image.value = self.model.predict(pic)[0].plot()
            cv2.waitKey(20)


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

    def deleteIdentity(self):
        "Put delete identity here"






if __name__ == "__main__":
    recognizer = pyforms.start_app(Recognizer, geometry = (500, 500, 1000, 700))
