# import necessary libraries
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
import os

# import classes self-created
from Preprocessing import RotateImage, CropImage, WhitebalanceImage
from Bands import (
    ColourBands, GoldBand, BrownBands, BlackBands, GreenBands, YellowBands,
    BlueBands, OrangeBands, GreyBands, RedBands, VioletBands, WhiteBands
)
from Analysis import UniqueBands, SortBands, SortColours
from config import *


# calculates the resistance of the resistor
class ResistanceCalculation:
    # initialise with bands and colour values
    def __init__(self, band1, band2, band3, band4):
        self.__band1 = band1
        self.__band2 = band2
        self.__band3 = band3
        self.__band4 = band4

        # dictionaries with key-value pairs of colour representation

        # first two bands represent numeric digit values
        self.__colour_digits = {'black': '0',
                              'brown': '1',
                              'red': '2',
                              'orange': '3',
                              'yellow': '4',
                              'green': '5',
                              'blue': '6',
                              'violet': '7',
                              'gray': '8',
                              'white': '9'}

        # third band represents power of 10

        self.__multipliers = {'black': 1,
                            'brown': 10,
                            'red': 100,
                            'orange': 1000,
                            'yellow': 10000,
                            'green': 100000,
                            'blue': 1000000,
                            'violet': 10000000,
                            'gray': 100000000,
                            'white': 1000000000}

        # fourth band represents the deviation from calculated value

        self.__tolerances = {'brown': '+/- 1 %',
                           'red': '+/- 2 %',
                           'green': "+/- 0.5 %",
                           'blue': '+/- 0.25 %',
                           'violet': '+/- 0.1 %',
                           'gold': '+/- 5 %',
                           'silver': '+/- 10 %',
                           'none': '+/-20 %'}

    def findResistance(self):
        # calculate resistance
        if self.__band1 in self.__colour_digits and self.__band2 in self.__colour_digits and self.__band3 in self.__multipliers and self.__band4 in self.__tolerances:
            tensdigit = self.__colour_digits.get(self.__band1)
            onesdigit = self.__colour_digits.get(self.__band2)
            multiplier = self.__multipliers.get(self.__band3)
            tolerance = self.__tolerances.get(self.__band4)
            digits = int(tensdigit + onesdigit)
            resistance = str(digits * multiplier) + " Ohms " + tolerance

        return resistance


# creates user interface
class GUI:

    #  initialise with root window
    def __init__(self, root):
        # create widgets in root window

        self.__img = None
        self.__root = root
        self.__camera_label = None
        self.__gui_frame = tk.Frame(self.__root, bg='white')

        # Load GUI images if available
        self.__background_image = None
        self.__image = None
        
        try:
            if os.path.exists(BACKGROUND_IMAGE):
                self.__background_image = tk.PhotoImage(file=BACKGROUND_IMAGE)
        except Exception as e:
            print(f"Background image not found: {BACKGROUND_IMAGE}")
            
        try:
            if os.path.exists(LOGO_IMAGE):
                self.__image = tk.PhotoImage(file=LOGO_IMAGE)
        except Exception as e:
            print(f"Logo image not found: {LOGO_IMAGE}")

        # initialise style

        self.__style = ttk.Style()

        # define window size and camera feed size
        self.__window_width = WINDOW_WIDTH
        self.__window_height = WINDOW_HEIGHT
        self.__frame_width = FRAME_WIDTH
        self.__frame_height = FRAME_HEIGHT

    # configure the interface

    def interface(self):

        # set properties of main window

        self.__root.title("Resistor Recognition - Homepage")
        self.__root.geometry(f'{self.__window_width}x{self.__window_height}')
        self.__root.configure(bg='lightblue')

        # Setup GUI layout
        self.__gui_frame.place(relwidth=1, relheight=1)
        
        # Add background image or fallback
        if self.__background_image:
            background_label = tk.Label(self.__gui_frame, image=self.__background_image)
            background_label.place(x=0, y=0)
        else:
            self.__gui_frame.configure(bg='lightblue')
            title_label = tk.Label(self.__gui_frame, text="Resistor Recognition System", 
                                 font=("Helvetica", 20, "bold"), bg='lightblue', fg='darkblue')
            title_label.place(x=250, y=50)
        
        # Add logo image or fallback
        if self.__image:
            self.__image = self.__image.subsample(4, 4)
            image_label = tk.Label(self.__gui_frame, image=self.__image)
            image_label.place(x=250, y=10)
        elif not self.__background_image:
            subtitle_label = tk.Label(self.__gui_frame, text="Computer Vision Color Band Detection", 
                                    font=("Helvetica", 12), bg='lightblue', fg='darkblue')
            subtitle_label.place(x=280, y=90)

        # change button colours if hovering over it

        self.__style.configure("TButton", font=("Helvetica", 14), background='lightblue')
        self.__style.configure("TButton.Hover.TButton", font=("Helvetica", 14),
                               background='lightgreen')
        self.__style.map("TButton", background=[("active", "lightgreen")])

        # create and position buttons

        self.__start_button = ttk.Button(self.__gui_frame, text="Start",
                                         command=self.__start_clicked,
                                       width=10, style="TButton")

        self.__start_button.place(x=375, y=360)

        self.__exit_button = ttk.Button(self.__gui_frame, text="Exit",
                                        command=self.__exit_clicked,
                                      width=10, style="TButton")

        self.__exit_button.place(x=375, y=440)

        # identify if mouse on either button

        self.__start_button.bind("<Enter>", self.__on_enter)
        self.__start_button.bind("<Leave>", self.__on_leave)

        self.__set_window_size(self.__root, self.__window_width, self.__window_height)

    # entering region of button

    def __on_enter(self, event):

        self.__start_button.configure(style="TButton.TButton")

    # leaving region of button

    def __on_leave(self, event):
        self.__start_button.configure(style="TButton.TButton")

    # define size of the window screen being used

    def __set_window_size(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')

    # display live camera feed
    def __show_camera_feed(self):
        ret, camera_frame = cap.read()
        if ret:
            camera_frame = cv.cvtColor(camera_frame, cv.COLOR_BGR2RGB)

            # show camera feed using label on window at configured intervals
            photo = ImageTk.PhotoImage(image=Image.fromarray(camera_frame))
            self.__camera_label.config(image=photo)
            self.__camera_label.image = photo
            self.__camera_label.after(CAMERA_UPDATE_INTERVAL, self.__show_camera_feed)

    # state after clicking start button

    def __start_clicked(self):
        global camera_window
        # new window to show camera feed
        camera_window = tk.Toplevel()
        camera_window.title("Camera Feed")
        self.__set_window_size(camera_window, self.__window_width, self.__window_height)

        # creates frame
        gui_frame = tk.Frame(camera_window, bg='white')
        gui_frame.place(relwidth=1, relheight=1)

        # capture camera feed

        global cap
        cap = cv.VideoCapture(0)

        # camera feed via label in frame
        self.__camera_label = tk.Label(gui_frame)
        self.__camera_label.place(x=10, y=10, width=self.__frame_width, height=
                                  self.__frame_height)

        # calls method to display camera feed
        self.__show_camera_feed()

        # creates button for user to capture an image

        capture_button = ttk.Button(gui_frame, text="Capture Image", command=
                                    self.__capture_image, width=15,
                                    style="TButton")
        capture_button.place(x=330, y=self.__frame_height + 20)

    # captures specific frame after button pressed

    def __capture_image(self):
        if cap.isOpened():
            ret, frame = cap.read()

            # displays captured frame

            if ret:
                self.__show_captured_frame(frame)

    # closes window if exit button pressed

    def __exit_clicked(self):
        if 'cap' in globals():
            cap.release()
        self.__root.destroy()

    # rotates image using calls to RotateImage methods

    def __rotation(self, img):
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        _, thresh = cv.threshold(gray_img, 140, 255, cv.THRESH_BINARY_INV)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        img_to_rotate = RotateImage(img)
        img_to_rotate._set_bounding_rectangle(contours)
        img_to_rotate._set_rotation_angle()
        img_to_rotate._set_rotation_matrix()
        rotated_image = img_to_rotate._get_rotated_image()

        return rotated_image

    # crops resistor image using calls to CropImage methods

    def __cropping(self):
        template = cv.imread(TEMPLATE_IMAGE, 0)

        # uses results from rotation
        img_to_crop = CropImage(self.__rotation(self.__img), template)
        img_cropped = img_to_crop.get_cropped_image()

        return img_cropped

    # white balances image calling WhitebalanceImage methods

    def __whitebalancing(self):
        reference_image = cv.imread(REFERENCE_IMAGE)

        # uses results from cropping
        img_to_whitebalance = WhitebalanceImage(self.__cropping(), reference_image)
        img = img_to_whitebalance.final_whitebalanced()
        cv.imwrite(os.path.join(ASSETS_DIR, 'whitebalanced_image.jpg'), img)
        return img

    # attempts to find colour bands using ColourBand child class methods

    def __findbands(self):

        # analyses each colour, creates final image of all identified bands

        # uses whitebalancing

        combined_image = np.zeros_like(self.__whitebalancing())
        resistor_img = self.__whitebalancing()

        # adds to the previous combined image each time

        gold_band = GoldBand(resistor_img, combined_image)
        self.__gold_contours, combined_image = gold_band.colour_band_image()

        brown_band = BrownBands(resistor_img, combined_image)
        self.__brown_contours, combined_image = brown_band.colour_band_image()

        green_band = GreenBands(resistor_img, combined_image)
        self.__green_contours, combined_image = green_band.colour_band_image()

        violet_band = VioletBands(resistor_img, combined_image)
        self.__violet_contours, combined_image = violet_band.colour_band_image()

        yellow_band = YellowBands(resistor_img, combined_image)
        self.__yellow_contours, combined_image = yellow_band.colour_band_image()

        red_band = RedBands(resistor_img, combined_image)
        self.__red_contours, combined_image = red_band.colour_band_image()

        black_band = BlackBands(resistor_img, combined_image)
        self.__black_contours, combined_image = black_band.colour_band_image()

        orange_band = OrangeBands(resistor_img, combined_image)
        self.__orange_contours, combined_image = orange_band.colour_band_image()

        blue_band = BlueBands(resistor_img, combined_image)
        self.__blue_contours, combined_image = blue_band.colour_band_image()

        white_band = WhiteBands(resistor_img, combined_image)
        self.__white_contours, combined_image = white_band.colour_band_image()
        return combined_image

    # sorts these colour bands and returns the colours

    def __sorting(self):

        # uses findbands

        # finds contours of combined image using thresholding

        gray_combined = cv.cvtColor(self.__findbands(), cv.COLOR_BGR2GRAY)

        _, combined_threshold = cv.threshold(gray_combined, 1, 255, cv.THRESH_BINARY)

        # Find contours in the thresholded image
        contours, _ = cv.findContours(combined_threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # calls UniqueBands methods to ensure individual bands are not repeated

        select_unique_bands = UniqueBands(contours)
        selected_contours = select_unique_bands.find_unique_bands()
        print(len(selected_contours))
        combined_image = np.zeros_like(self.__findbands())
        cv.drawContours(combined_image, selected_contours, -1, (0, 255, 0), 2)

        # sorts bands based on x values
        sorted_bands = SortBands(selected_contours)
        sorted_contours = sorted_bands.merge_sort_contours()
        colour_sort = SortColours(sorted_contours, self.__orange_contours, self.__red_contours, self.__green_contours, self.__blue_contours,
                                  self.__yellow_contours, self.__black_contours, self.__brown_contours, self.__gold_contours, self.__white_contours, self.__violet_contours)

        # creates an array of the colours in the resistor

        sorted_contours_colours = colour_sort.colour_assignment()

        return sorted_contours_colours


    # finds the resistance value to be output

    def __processing(self, contours):
        if len(contours) > 0:
            # calls sorting method
            sorted_contours_colours = self.__sorting()

            # ensures gold band is always at the right end

            if sorted_contours_colours[0] == 'gold':
                sorted_contours_colours.reverse()

            print('Colours in order:', sorted_contours_colours)

            # finds resistance using ResistanceCalculation class method calls
            global text

            resistance = ResistanceCalculation(sorted_contours_colours[0],sorted_contours_colours[1],
                                               sorted_contours_colours[2],sorted_contours_colours[3])
            text = 'Resistance Value: ' + resistance.findResistance()

        else:

            # accounts for when there is no resistor presented (no contours detected)

            text = 'ERROR: No Resistor Detected!'
        print(text)
        return text

    # displays the captured frame with resistance

    def __show_captured_frame(self, captured_frame):

        try:
            # finds contours using thresholding and colour space conversion
            self.__img = captured_frame
            img = self.__img

            # Convert the image to grayscale
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Threshold the image
            ret, threshold = cv.threshold(gray, THRESHOLD_VALUE, 255, cv.THRESH_BINARY_INV)

            # Find contours
            contours, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            contours = [contour for contour in contours if cv.contourArea(contour) > MIN_CONTOUR_AREA]

            # uses call to processing to find resistance value

            self.__processing(contours)

            # creates new window displaying the captured frame and resistance output

            captured_frame = cv.cvtColor(captured_frame, cv.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(captured_frame))

            # creates new window
            captured_frame_window = tk.Toplevel()
            captured_frame_window.title("Resistance Value Output")


            # displays using a label

            image_label = tk.Label(captured_frame_window, image=photo)
            image_label.image = photo  # Reference to keep the image alive
            image_label.pack()

            text_label = tk.Label(captured_frame_window, text=text, font=("Helvetica", 12),
                                  bg='lightblue', fg='black')
            text_label.pack()

        except Exception as e:

            # If an error occurs, display a new window with the "Try Again" message
            captured_frame = cv.cvtColor(captured_frame, cv.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(captured_frame))

            # creates new window

            error_window = tk.Toplevel()
            error_window.title("Error")

            # displays using a label

            image_label = tk.Label(error_window, image=photo)
            image_label.image = photo
            image_label.pack()

            error_label = tk.Label(error_window, text="Oops, Please Try Again :)",
                                   font=("Helvetica", 12), bg='lightcoral', fg='black')
            error_label.pack()
