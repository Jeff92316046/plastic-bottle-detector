from __future__ import print_function
from imutils import paths
from scipy.io import loadmat
from skimage import io
from dlib import cuda as cuda
import dlib
import json
import sys
import cv2

dlib.DLIB_USE_CUDA = True
# handle Python 3 compatibility
if sys.version_info > (3,):
    long = int
# construct the argument parse and parse the arguments
config_file = open("src/test/config.json")
args = json.load(config_file)
# grab the default training options for our HOG + Linear SVM detector initializethe
# list of images and bounding boxes used to train the classifier
print("[INFO] gathering images and bounding boxes...")
options = dlib.simple_object_detector_training_options()
images = []
boxes = []
boxes_ar = {}
# loop over the image paths

cnt = 300
color = (255, 0, 0)
for imagePath in paths.list_images(args["class"]):
    # extract the image ID from the image path and load the annotations file
    cnt -= 1
    if cnt == 0:
        break
    # image_file_id = imagePath[imagePath.rfind("/") + 1:].split("_")[1]
    # image_file_id = image_file_id.replace(".jpg", "")
    # p = "{}/annotation_{}.mat".format(args["annotations"], image_file_id)
    # annotations = loadmat(p)["box_coord"]
    # print(imagePath[imagePath.rfind("\\") + 1:][:-4])
    image_file_label =args["annotations"] + "/" + imagePath[imagePath.rfind("\\") + 1:][:-4] + ".txt"
    # print(image_file_label)
    img = cv2.imread(imagePath)
    h,w,_ = img.shape
    with open(image_file_label,"r") as annotations :
        for line in annotations.readlines():
            try :
                _,x_center, y_center, width, height = map(float,line.strip().split())
                width = width * w
                height = height * h
                if height*width < 400:
                    continue
                if boxes_ar.get(height//width,-1) != -1:
                    boxes_ar[height//width] += 1
                else :
                     boxes_ar[height//width] = 1
                if not(height/width > 2 and height/width < 4):
                    continue
                print(height/width)
                x_center = x_center * w
                y_center = y_center * h  
                (x1,y1,x2,y2) = (int(x_center-width/2),int(y_center-height/2),int(x_center+width/2),int(y_center+height/2))
                # print(x1,y1,x2,y2)
                # cv2.rectangle(img, (x1,y1), (x2,y2), color,1)
                bb = [dlib.rectangle(left=long(int(x_center-width/2)), top=long(int(y_center-height/2)), right=long(x_center+width/2), bottom=long(y_center+height/2))]
                # print(bb)
                boxes.append(bb)
                # add the image to the list of images
                images.append(io.imread(imagePath))
            except:
                continue
    # cv2.imshow("test",img)
    # cv2.waitKey()
    # loop over the annotations and add each annotation to the list of bounding
    # boxes
for k,v in sorted(boxes_ar.items()):
    print(k,v)
print(boxes)
# train the object detector
print("[INFO] training detector...")
detector = dlib.train_simple_object_detector(images, boxes, options)
# dump the classifier to file
print("[INFO] dumping classifier to file...")
detector.save(args["output"])
# visualize the results of the detector
win = dlib.image_window()
win.set_image(detector)
dlib.hit_enter_to_continue()
