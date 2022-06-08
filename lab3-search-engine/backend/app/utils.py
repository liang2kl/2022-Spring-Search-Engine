import math
import numpy as np
import cv2
from sklearn.cluster import KMeans

def chi2_distance(histA, histB, eps=1e-10):
    if histB is None:
        histB = np.zeros(len(histA), dtype=float)
    # compute chi-squared distance
    d = 0.5 * np.sum([((a-b)**2)/(a+b+eps)
        for (a,b) in zip(histA, histB)])

    # return the chi-squared distance
    return d

class ColorDescriptor:
	def __init__(self, bins):
		# store the number of bins for the 3D histogram
		self.bins = bins

	def describe(self, image):
		# convert the image to the HSV color space and initialize
		# the features used to quantify the image
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		features = []

		# grab the dimensions and compute the center of the image
		(h, w) = image.shape[:2]
		(cX, cY) = (int(w * 0.5), int(h * 0.5))

		# divide the image into four rectangles/segments (top-left,
		# top-right, bottom-right, bottom-left)
		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
			(0, cX, cY, h)]
 
		# construct an elliptical mask representing the center of the
		# image
		(axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
		ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
		cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
 
		# loop over the segments
		for (startX, endX, startY, endY) in segments:
			# construct a mask for each corner of the image, subtracting
			# the elliptical center from it
			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
			cornerMask = cv2.subtract(cornerMask, ellipMask)
 
			# extract a color histogram from the image, then update the
			# feature vector
			hist = self.histogram(image, cornerMask)
			features.extend(hist)
 
		# extract a color histogram from the elliptical region and
		# update the feature vector
		hist = self.histogram(image, ellipMask)
		features.extend(hist)
 
		# return the feature vector
		return features

	def histogram(self, image, mask):
		# extract a 3D color histogram from the masked region of the
		# image, using the supplied number of bins per channel; then
		# normalize the histogram
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
			[0, 180, 0, 256, 0, 256])
		cv2.normalize(hist,hist)
		hist = hist.flatten()
 
		# return the histogram
		return hist

# The following code is extracted from
# https://github.com/srijannnd/Dominant-Color-Extraction-Dominance-and-Recoloring

def get_prominant_colors(image):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	r, c = image.shape[:2]
	out_r = 120
	image = cv2.resize(image, (int(out_r*float(c)/r), out_r))
	pixels = image.reshape((-1, 3))
	km = KMeans(n_clusters=8)
	km.fit(pixels)
	colors = np.asarray(km.cluster_centers_, dtype='uint8')
	percentage = np.asarray(np.unique(km.labels_, return_counts = True)[1], dtype='float32')
	percentage = percentage / pixels.shape[0]
	dom = [[float(percentage[ix]), (colors[ix]).tolist()] for ix in range(km.n_clusters)]
	dominance = sorted(dom, key=lambda x:x[0], reverse=True)
	return [d[1] for d in dominance]

def distance_of_colors(c1, c2):
	c1 = [int(x) for x in c1]
	c2 = [int(x) for x in c2]
	d = math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)
	print(d)
	return d
