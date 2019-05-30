import tkinter as tk
from tkinter import *

import Capture
import Classifier

#tk.Frame = tk.LabelFrame

class Viewer(tk.Frame):

    def __init__(self, parent):
        #initiating the classifier
        self.cls = Classifier.Classifier()
        
        tk.Frame.__init__(self, parent)
        self.parent = parent # there is self.master which keeps parent

        self.parent.protocol('WM_DELETE_WINDOW', self.parent.destroy)

        self.screen_width = parent.winfo_screenwidth()
        self.screen_height = parent.winfo_screenheight()

        self.embed = tk.Frame(self.parent, width=640, height=480)
        self.embed.pack()

        self.buttonFrame = tk.Frame(self.parent, width=640, height=480)
        self.buttonFrame.pack()

        self.parent.update() # need it to get embed.winfo_id() in Capture

        self.c = Capture.Capture(self)

        self.checkButton = tk.Button(self.buttonFrame,
                                 text='Check',
                                 command=self.refresh)
        self.checkButton.config( height = 2, width = 40 )
        self.checkButton.pack()

        self.label = Label(self.parent, text="Ready", bg="white", fg="black")
        self.label.pack(fill=X)

        self.imageTaken = False

        

    def refresh(self):
        #self.label.config(text = "Please wait")
        print("now here")
        if self.imageTaken:
            self.checkButton.config(text = "Check")
            self.label.config(text = "Ready")
            self.c.reset()
            self.imageTaken = False
        else:
            self.c.click()
            self.checkButton.config(text = "Check another picture?")
            self.imageTaken = True
            self.label.config(text = self.cls.classify())


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Leaf Classifier")
    run = Viewer(root)
    root.resizable(False, False)
    root.mainloop()
