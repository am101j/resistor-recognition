# import necessary libraries

import numpy as np
import cv2 as cv
import random


# define parent class to identify colours

class ColourBands:

    # initialise with image and combined_image

    def __init__(self, image, combined_image):
        self._image = image
        self._combined_image = combined_image
        self._min_area_threshold = None

    # find mask that detects colour

    def _colour_mask(self):
        # convert to HSV
        img_hsv = cv.cvtColor(self._image, cv.COLOR_BGR2HSV)
        # find pixels in HSV range
        initial_mask = cv.inRange(img_hsv, self._lower_hsv, self._upper_hsv)
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(initial_mask, connectivity=8)
        refined_mask = np.zeros_like(initial_mask)
        # filter based on area of mask components
        for label in range(1, num_labels):
            if self._min_area_threshold < stats[label, cv.CC_STAT_AREA] < 1300:
                refined_mask[labels == label] = 255

        return cv.cvtColor(refined_mask, cv.COLOR_GRAY2BGR)

    def colour_band_image(self):
        # new image showing only the identified colour band
        mask = cv.resize(self._colour_mask(), (self._image.shape[1], self._image.shape[0]))
        band_img = cv.bitwise_and(mask, self._image)
        # band_img = cv.medianBlur(band_img, 5)
        band_img_gray = cv.cvtColor(band_img, cv.COLOR_BGR2GRAY)
        _, threshold = cv.threshold(band_img_gray, 1, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        self._combined_image = cv.resize(self._combined_image, (self._image.shape[1], self._image.shape[0]))
        # add bands to combined image
        self._combined_image = cv.bitwise_or(self._combined_image, band_img)
        return contours, self._combined_image


# child classes inherit from ColourBands

class GoldBand(ColourBands):

    def __init__(self, image, combined_image):
        # call from superclass
        super().__init__(image, combined_image)
        self._lower_hsv = np.array([11, 32, 54])
        self._upper_hsv = np.array([22, 53, 141])

    # override method from superclass

    def _colour_mask(self):
        img_hsv = cv.cvtColor(self._image, cv.COLOR_BGR2HSV)
        initial_mask = cv.inRange(img_hsv, self._lower_hsv, self._upper_hsv)
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(initial_mask, connectivity=8)
        # only detect largest label for gold
        largest_gold_label = np.argmax(stats[1:, cv.CC_STAT_AREA]) + 1
        refined_mask = np.zeros_like(initial_mask)

        refined_mask[labels == largest_gold_label] = 255
        return cv.cvtColor(refined_mask, cv.COLOR_GRAY2BGR)

    def colour_band_image(self):
        # new image showing only the identified colour band
        mask = cv.resize(self._colour_mask(), (self._image.shape[1], self._image.shape[0]))
        band_img = cv.bitwise_and(mask, self._image)
        band_img = cv.medianBlur(band_img, 5)
        band_img_gray = cv.cvtColor(band_img, cv.COLOR_BGR2GRAY)
        _, threshold = cv.threshold(band_img_gray, 1, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        self._combined_image = cv.resize(self._combined_image, (self._image.shape[1], self._image.shape[0]))
        # add bands to combined image
        self._combined_image = cv.bitwise_or(self._combined_image, band_img)
        return contours, self._combined_image


# similar for other subclasses for other colours

class BrownBands(ColourBands):
    def __init__(self, image, combined_image):
        super().__init__(image, combined_image)
        self._lower_hsv = np.array([0, 50, 50])
        self._upper_hsv = np.array([180, 76, 120])
        self._min_area_threshold = 200

    # overriding default to include blurring
    def colour_band_image(self):
        # new image showing only the identified colour band
        mask = cv.resize(self._colour_mask(), (self._image.shape[1], self._image.shape[0]))
        band_img = cv.bitwise_and(mask, self._image)
        band_img = cv.medianBlur(band_img, 5)
        band_img_gray = cv.cvtColor(band_img, cv.COLOR_BGR2GRAY)
        _, threshold = cv.threshold(band_img_gray, 1, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        self._combined_image = cv.resize(self._combined_image, (self._image.shape[1], self._image.shape[0]))
        # add bands to combined image
        self._combined_image = cv.bitwise_or(self._combined_image, band_img)
        return contours, self._combined_image


class BlackBands(ColourBands):
    def __init__(self, image, combined_image):
        super().__init__(image, combined_image)
        self._lower_hsv = np.array([25, 0, 20])
        self._upper_hsv = np.array([150, 90, 86])
        self._min_area_threshold = 2000

    def _colour_mask(self):
        # convert to HSV
        img_hsv = cv.cvtColor(self._image, cv.COLOR_BGR2HSV)
        # find pixels in HSV range
        initial_mask = cv.inRange(img_hsv, self._lower_hsv, self._upper_hsv)
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(initial_mask, connectivity=8)
        refined_mask = np.zeros_like(initial_mask)
        # filter based on area of mask components
        for label in range(1, num_labels):
            if self._min_area_threshold < stats[label, cv.CC_STAT_AREA] < 1300:
                refined_mask[labels == label] = 255

        return cv.cvtColor(refined_mask, cv.COLOR_GRAY2BGR)


class GreenBands(ColourBands):
    def __init__(self, image, combined_image):
        super().__init__(image, combined_image)
        self._lower_hsv = np.array([40, 130, 62])
        self._upper_hsv = np.array([74, 180, 115])
        self._min_area_threshold = 60


class YellowBands(ColourBands):
    def __init__(self, image, combined_image):
        super().__init__(image, combined_image)
        self._lower_hsv = np.array([23, 98, 138])
        self._upper_hsv = np.array([53, 190, 240])
        self._min_area_threshold = 20

    def _colour_mask(self):
        # convert to HSV
        img_hsv = cv.cvtColor(self._image, cv.COLOR_BGR2HSV)
        # find pixels in HSV range
        initial_mask = cv.inRange(img_hsv, self._lower_hsv, self._upper_hsv)
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(initial_mask, connectivity=8)
        refined_mask = np.zeros_like(initial_mask)
        # filter based on area of mask components
        for label in range(1, num_labels):
            if self._min_area_threshold < stats[label, cv.CC_STAT_AREA] < 1300:
                refined_mask[labels == label] = 255

        return cv.cvtColor(refined_mask, cv.COLOR_GRAY2BGR)


class RedBands(ColourBands):
    def __init__(self, image, combined_image):
        super().__init__(image, combined_image)
        self._lower_hsv = np.array([150, 110, 90])
        self._upper_hsv = np.array([180, 180, 210])
        self._min_area_threshold = 50


class VioletBands(ColourBands):
    def __init__(self, image, combined_image):
        super().__init__(image, combined_image)
        self._lower_hsv = np.array([125, 50, 100])
        self._upper_hsv = np.array([167, 125, 160])
        self._min_area_threshold = 100

    def _colour_mask(self):
        # convert to HSV
        img_hsv = cv.cvtColor(self._image, cv.COLOR_BGR2HSV)
        # find pixels in HSV range
        initial_mask = cv.inRange(img_hsv, self._lower_hsv, self._upper_hsv)
        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(initial_mask, connectivity=8)
        refined_mask = np.zeros_like(initial_mask)
        # filter based on area of mask components
        for label in range(1, num_labels):
            if self._min_area_threshold < stats[label, cv.CC_STAT_AREA] < 1300:
                refined_mask[labels == label] = 255

        return cv.cvtColor(refined_mask, cv.COLOR_GRAY2BGR)


class BlueBands(ColourBands):
    def __init__(self, image, combined_image):
        super().__init__(image, combined_image)
        self._lower_hsv = np.array([90, 94, 79])
        self._upper_hsv = np.array([120, 148, 138])
        self._min_area_threshold = 50


class OrangeBands(ColourBands):
    def __init__(self, image, combined_image):
        super().__init__(image, combined_image)
        self._lower_hsv = np.array([0, 110, 145])
        self._upper_hsv = np.array([30, 174, 205])
        self._min_area_threshold = 100


class WhiteBands(ColourBands):
    def __init__(self, image, combined_image):
        super().__init__(image, combined_image)
        self._lower_hsv = np.array([20, 12, 134])
        self._upper_hsv = np.array([30, 40, 170])
        self._min_area_threshold = 2000


class GreyBands(ColourBands):
    def __init__(self, image, combined_image):
        super().__init__(image, combined_image)
        self._lower_hsv = np.array([44, 0, 46])
        self._upper_hsv = np.array([180, 20, 90])
        self._min_area_threshold = 50
