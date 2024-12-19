# import packages
from nms import non_max_suppression
from object_detector import ObjectDetector
from hog_c import HOG
from conf_c import Conf
import numpy as np
import imutils
import argparse
import pickle
import cv2
from imutils import paths

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required = True, help = "Path to the configuration file")
args = vars(ap.parse_args())

# load the configuration file
conf = Conf(args["conf"])

# load the classifier, then initialize the Histogram of Oriented Gradients descriptor
# and the object detector
model = pickle.loads(open(conf["classifier_path"], "rb").read())
hog = HOG(orientations = conf["orientations"], pixelsPerCell = tuple(conf["pixels_per_cell"]),
	cellsPerBlock = tuple(conf["cells_per_block"]), normalize = conf["normalize"], block_norm = "L1")
od = ObjectDetector(model, hog)
trnPaths = list(paths.list_images(conf["test_dataset"]))
for (i, trnPath) in enumerate(trnPaths):
	print(i)
	# load the image and convert it to grayscales
	image = cv2.imread(trnPath)
	image = imutils.resize(image, width = min(260, image.shape[1]))
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# detect objects in the image and apply non-maxima suppression to the bounding boxes
	(boxes, probs) = od.detect(gray, conf["window_dim"], winStep = conf["window_step"],
		pyramidScale = conf["pyramid_scale"], minProb = conf["min_probability"])
	pick = non_max_suppression(np.array(boxes), probs, conf["overlap_thresh"])
	orig = image.copy()

	# loop over the original bounding boxes and draw them
	for (startX, startY, endX, endY) in boxes:
		cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 0, 255), 2)

	# loop over the allowed bounding boxes and draw them
	for (startX, startY, endX, endY) in pick:
		cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

	# show the output images
	cv2.imshow("Original", orig)
	cv2.imshow("Image", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()