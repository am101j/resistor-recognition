# import libraries
import numpy as np
import cv2 as cv


# perform white balancing on the image
class WhitebalanceImage:

    # initialise with attributes of image and the reference images

    def __init__(self, image_to_whitebalance, reference_image):
        self.__img = cv.resize(image_to_whitebalance, (450, 350))
        self.__reference_image = cv.resize(reference_image, (450, 350))

    # extract a patch of the white background common in both images

    def extract_white_patch(self, image):
        result_patch = cv.resize(image, None, fx=20, fy=20)
        return result_patch[60: 75, 300: 315]

    # perform ground truth whitebalancing using a patch on the image

    def ground_truth_whitebalancing(self):
        # assume the patch is the 'ideal' true white
        true_white_patch = self.extract_white_patch(self.__img)

        # normalise each channel of entire image using patch max channel values

        max_value_whitebalancing = (self.__img * 1.0 /
                                    true_white_patch.max(axis=(0, 1))).clip(0, 1)

        # convert BGR to RGB
        ground_truth_whitebalanced_img = max_value_whitebalancing[:, :, ::-1]

        cv.waitKey(0)
        cv.destroyAllWindows()

        return ground_truth_whitebalanced_img

    # different type of whitebalancing using Euclidian distance
    def deviation_whitebalancing(self):
        reference_patch = self.extract_white_patch(self.__reference_image)
        current_patch = self.extract_white_patch(self.__img)

        reference_patch_mean = np.mean(reference_patch)
        current_patch_mean = np.mean(current_patch)

        # finds the Euclidian distance between patches
        deviation = np.linalg.norm(reference_patch - current_patch)

        # using combination (in different ratios) of deviation and ratio of means to white balance

        scale1 = (reference_patch_mean / current_patch_mean)
        whitebalanced_deviation_img1 = self.__img * scale1
        scale2 = 0.03 * deviation
        whitebalanced_deviation_img2 = self.__img + scale2

        whitebalanced_deviation_img = cv.addWeighted(whitebalanced_deviation_img1, 0.6, whitebalanced_deviation_img2,
                                                     0.4, 0)
        # converts to 8-bit integer

        whitebalanced_deviation_img = np.clip(whitebalanced_deviation_img, 0, 255).astype(np.uint8)

        return np.clip(whitebalanced_deviation_img, 0, 255).astype(np.uint8)

    # uses two whitebalancing methods to perform a combination of both
    def final_whitebalanced(self):
        # calls both whitebalancing methods
        whitebalance1 = self.deviation_whitebalancing()
        whitebalance2 = cv.resize(self.ground_truth_whitebalancing(), (450, 350))

        # uses different percentages of both methods

        final_whitebalanced_img = cv.addWeighted(whitebalance1, 0.3, (whitebalance2 * 255).astype(np.uint8), 0.7, 0)

        return final_whitebalanced_img


# crops captured frame

class CropImage:

    def __init__(self, img_to_crop, template_img):
        # adds attributes of image and template

        self.__img = img_to_crop
        self.__template = template_img

    # uses template matching to crop

    def get_cropped_image(self):
        template_width, template_height = self.__template.shape[::-1]
        img_gray = cv.cvtColor(self.__img, cv.COLOR_BGR2GRAY)

        # detects the location of the resistor

        method = eval('cv.TM_CCOEFF')
        resistor_detection = cv.matchTemplate(img_gray, self.__template, method)

        # finds max and min locations where there is a match to crop

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(resistor_detection)
        top_left = max_loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)


        cropped_region = self.__img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # resizes and enhances the cropped image

        resize_image = cv.resize(cropped_region, None, fx=2, fy=3)
        cropped_image = cv.filter2D(resize_image, -1, np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]))
        cropped_image = cropped_image[:, :, ::-1]

        return cropped_image


# rotates image

class RotateImage:

    # initialise object with necessary attributes

    def __init__(self, img):
        self.__img = img
        self.__bounding_rectangle = None
        self.__rotation_angle = None
        self.__rotation_matrix = None
        self.__rotated_image = None
        self.__height, self.__width = img.shape[:2]
        self.__orientation_angle = None

    # finds a rectangle encompassing the resistor

    # setter
    def _set_bounding_rectangle(self, frame_contours):

        if len(frame_contours) > 0:
            # form rectangle using largest contour

            largest_contour_index = max(range(len(frame_contours)), key=lambda i: cv.contourArea(frame_contours[i]))
            bounding_rectangle = cv.minAreaRect(frame_contours[largest_contour_index])
            self.__bounding_rectangle = bounding_rectangle

    # getter
    def _get_bounding_rectangle(self):
        return self.__bounding_rectangle

    # find angle to rotate by

    # setter
    def _set_rotation_angle(self):

        # calls getter method for the bounding rectangle

        bounding_rectangle = self._get_bounding_rectangle()
        self.__orientation_angle = bounding_rectangle[-1]

        # find corners of rectangle  as integers

        resistor_bounding_box = cv.boxPoints(bounding_rectangle)
        resistor_bounding_box = np.intp(resistor_bounding_box)

        # find vertices on opposite sides of rectangle
        rectangle_vertex_1 = tuple(resistor_bounding_box[1]) if resistor_bounding_box[0][1] > resistor_bounding_box[1][
            1] else tuple(resistor_bounding_box[0])
        rectangle_vertex_2 = tuple(resistor_bounding_box[3]) if resistor_bounding_box[2][1] < resistor_bounding_box[3][
            1] else tuple(resistor_bounding_box[2])

        # retrieve angle using bounding rectangle

        if self.__orientation_angle == 90:
            self.__orientation_angle = 0

        elif self.__orientation_angle != 90:
            # if already horizontally placed, do not rotate
            if 0 < self.__orientation_angle < 5:
                self.__orientation_angle = 0

            # add to angle based on the way resistor is slanting
            if rectangle_vertex_1[0] > rectangle_vertex_2[0]:
                self.__orientation_angle += 90

        self.__rotation_angle = self.__orientation_angle

    # getter
    def _get_rotation_angle(self):
        return self.__rotation_angle

    # matrix to perform rotation

    # setter
    def _set_rotation_matrix(self):
        center = ((self.__width - 1) // 2, (self.__height - 1) // 2)
        # use rotation angle method to convert to radians
        angle_rad = self._get_rotation_angle() * np.pi / 180.0

        # use trigonometry
        alpha = np.cos(angle_rad)
        beta = np.sin(angle_rad)

        # create 2x3 rotation matrix
        element1 = alpha
        element2 = beta
        element3 = (1 - alpha) * center[0] - beta * center[1]
        element4 = -beta
        element5 = alpha
        element6 = beta * center[0] + (1 - alpha) * center[1]

        # represent array to represent matrix
        self.__rotation_matrix = np.array([[element1, element2, element3], [element4, element5, element6]],
                                         dtype=np.float64)

    # getter
    def _get_rotation_matrix(self):
        return self.__rotation_matrix

    # rotates the image

    def _get_rotated_image(self):

        #  rotated_image = cv.warpAffine(self.__img, self._get_rotation_matrix(), (self.width, self.height))
        rotated_image = np.zeros_like(self.__img)

        # nested for loop to apply matrix and rotate every pixel
        for y in range(self.__img.shape[0]):
            for x in range(self.__img.shape[1]):
                new_x, new_y = np.dot(self.__rotation_matrix, [x, y, 1])
                new_x, new_y = int(new_x), int(new_y)
                if 0 <= new_x < self.__img.shape[1] and 0 <= new_y < self.__img.shape[0]:

                    # assign pixel value of original to new position
                    rotated_image[new_y, new_x] = self.__img[y, x]

        self.__rotated_image = rotated_image

        return self.__rotated_image
