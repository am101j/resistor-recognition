# import pre-built Tkinter library for GUI
import tkinter as tk

# import self-created classes from respective program files
from FrontEnd import GUI

# run main to launch user interface window and process image
def main():
    # main window
    root = tk.Tk()

    # create instance of GUI class as the front end
    frontend = GUI(root)

    # call class method to build home screen
    frontend.interface()

    # main loop for user interaction
    root.mainloop()


# if running script, initiate main
if __name__ == '__main__':
    main()
