import numpy as np
import cv2 as cv


# sorts bands by x coordinates

class SortBands:

    # initialises object with attributes contours and empty list
    def __init__(self, contours):
        self.__contours = contours
        self.__sorted_contours = []

    # find x centre value of contour centroid

    def __calculate_cx(self, moment):

        if moment['m00'] != 0:
            cx = int(moment['m10'] / moment['m00'])
        else:
            cx = 0

        return cx

    # sort two lists based on x
    def __sort_two_lists(self, left_half, right_half):

        # initialise index as 0

        left_index = 0
        right_index = 0

        # compare x values in left and right halves and sort
        while left_index < len(left_half.contours) and right_index < len(right_half.contours):

            left_moment = cv.moments(left_half.contours[left_index])
            right_moment = cv.moments(right_half.contours[right_index])
            left_cx = left_half.__calculate_cx(left_moment)
            right_cx = right_half.__calculate_cx(right_moment)

            if left_cx < right_cx:
                self.__sorted_contours.append(left_half.contours[left_index])
                left_index += 1
            else:
                self.__sorted_contours.append(right_half.contours[right_index])
                right_index += 1

        # sort remaining contours
        while left_index < len(left_half.contours):
            self.__sorted_contours.append(left_half.contours[left_index])
            left_index += 1

        while right_index < len(right_half.contours):
            self.__sorted_contours.append(right_half.contours[right_index])
            right_index += 1

        return self.__sorted_contours

    # perform merge sort
    def merge_sort_contours(self):
        # base case
        if len(self.__contours) <= 1:
            return self.__contours

        # divide contours list in half
        middle = len(self.__contours) // 2

        # create instances of SortBands with half the values
        left_half = SortBands(self.__contours[:middle])
        right_half = SortBands(self.__contours[middle:])

        # recursively call merge sort until every list is just one element
        left_half.contours = left_half.merge_sort_contours()
        right_half.contours = right_half.merge_sort_contours()

        # sort final two halves
        return self.__sort_two_lists(left_half, right_half)


# identify bands uniquely
class UniqueBands:

    # contours, empty array for unique contours as attribute to instantiated object
    def __init__(self, contours):
        self.__selected_contours = []
        self.__contours = contours

    # ensures the same band is not recognised twice or more

    def find_unique_bands(self):

        # analyse area occupied by every contour
        for contour in self.__contours:
            contour_x, _, contour_width, _ = cv.boundingRect(contour)

            # specify x area occupied by current contour
            x_min = contour_x + 0.5
            x_max = contour_x + contour_width - 0.5

            if not self.__selected_contours:

                # If the list is empty, add the first contour
                self.__selected_contours.append(contour)

            else:
                overlapping = False

                # nested for loop to check if any band (contour) has an x range overlapping with current contour
                for selected_contour in self.__selected_contours:
                    # repeat process for x ranges
                    selected_x, _, selected_w, _ = cv.boundingRect(selected_contour)
                    selected_x_min = selected_x - 0.5
                    selected_x_max = selected_x + selected_w + 0.5

                    # check if these overlap
                    if ((selected_x_min <= x_min <= selected_x_max) or (
                            selected_x_min <= x_max <= selected_x_max)):
                        overlapping = True
                        break
                if not overlapping:
                    # add band as unique
                    self.__selected_contours.append(contour)

        return self.__selected_contours


class SortColours:

    # initialise with all contours and colour contours
    def __init__(self, sorted_contours, orange_contours, red_contours, green_contours, blue_contours,
                 yellow_contours, black_contours, brown_contours, gold_contours, white_contours, violet_contours):
        self.__sorted_contours = sorted_contours
        self.__orange_contours = orange_contours
        self.__red_contours = red_contours
        self.__green_contours = green_contours
        self.__blue_contours = blue_contours
        self.__yellow_contours = yellow_contours
        self.__black_contours = black_contours
        self.__brown_contours = brown_contours
        self.__gold_contours = gold_contours
        self.__violet_contours = violet_contours
        self.__white_contours = white_contours

    # finds what colour the band associates with
    def __match_contours(self, current_contour, colour_contours):
        for contour_reference in colour_contours:
            # check if there is a similarity in shape of contours from colour contours
            ret = cv.matchShapes(contour_reference, current_contour, 1, 0)
            current_moment = cv.moments(current_contour)
            cx_current = int(current_moment['m10'] / current_moment['m00']) if current_moment['m00'] != 0 else 0
            reference_moment = cv.moments(contour_reference)
            cx_reference = int(reference_moment['m10'] / reference_moment['m00']) if reference_moment['m00'] != 0 else 0
            # Set a threshold for shape similarity and centroid x-value range
            thresh_shape = 0.1
            thresh_centre_x = 10
            # Check if there is similarity in both shape and centroid x-value
            if ret <= thresh_shape and abs(cx_current - cx_reference) <= thresh_centre_x:
                return True

        return False

    def colour_assignment(self):
        sorted_contours_colours = []
        count = 0
        # loop to ensure correct number of bands identified in reasonable time
        while len(sorted_contours_colours) != 4 and count < 20 and 'gold' not in sorted_contours_colours:
            for contour in self.__sorted_contours:
                count += 1

                # calls match_contours to add associated colour to a new list
                if self.__match_contours(contour, self.__orange_contours):
                    sorted_contours_colours.append('orange')
                elif self.__match_contours(contour, self.__red_contours):
                    sorted_contours_colours.append('red')
                elif self.__match_contours(contour, self.__green_contours):
                    sorted_contours_colours.append('green')
                elif self.__match_contours(contour, self.__blue_contours):
                    sorted_contours_colours.append('blue')
                elif self.__match_contours(contour, self.__yellow_contours):
                    sorted_contours_colours.append('yellow')
                elif self.__match_contours(contour, self.__black_contours):
                    sorted_contours_colours.append('black')
                elif self.__match_contours(contour, self.__brown_contours):
                    sorted_contours_colours.append('brown')
                elif self.__match_contours(contour, self.__gold_contours):
                    sorted_contours_colours.append('gold')
                elif self.__match_contours(contour, self.__violet_contours):
                    sorted_contours_colours.append('violet')
                elif self.__match_contours(contour, self.__white_contours):
                    sorted_contours_colours.append('white')
        return sorted_contours_colours
