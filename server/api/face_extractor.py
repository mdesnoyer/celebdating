import cv2

class FaceCropper:
    def __init__(self, model_file):
        self.haarParams = {'minNeighbors': 5,
                           'minSize': (50, 50),
                           'scaleFactor': 1.1}
        self.face_cascade = cv2.CascadeClassifier()
        self.face_cascade.load(self.model_file)

    def extract_faces(self, image):
        # Get the greyscale
        gimage = image
        if len(image.shape) == 3 and image.shape[2] > 1:
            gimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        coords = self.face_cascade.detectMultiScale(gimage, **self.haarParams)

        faces = []
        for x, y, w, h in coords:
            faces.append(image[y:(y+h), x:(x+w), :])

        return faces
        
