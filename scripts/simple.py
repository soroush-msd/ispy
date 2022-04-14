#!/usr/bin/env python

import numpy as np
import cv2

# Load an color image in grayscale
img = cv2.imread('/home/soroush/Pictures/dog-puppy-on-garden-royalty-free-image-1586966191.jpg',0)

# show image

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
