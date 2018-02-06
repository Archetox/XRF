
import tkinter as tk
import tkFileDialog
import sys
import glob, os
import bin.h5conversion_v1 as h5conv

############################################################################################
####		Gui to convert CLS files to h5 files for PyXRF analysis			####
####		Calls h5conversion_v1 script to do the actual converstion		####
############################################################################################

class App(tk.Tk):

##### GUI set up ##############################
    def __init__(self):                                   #Sets up GUI layout and formatting
        tk.Tk.__init__(self)
        self.roifile = "" 				  #Initialize empty roi file name
        self.datafile = ""				  #Initialize empty data file name
        self.fname = ""					  #Initialize empyt generic file name 
							  # variable

        self.title("h5 Conversion v1.0")
        self.grid()					  #Sets up menu grid (table format)
        self.rowconfigure(5, weight=1)			  #First row has 5 columns
        self.rowconfigure(5, weight=1)                    #Second row has 5 columns
        
        self.label1 = tk.Label(self, text="ROI File:")   #Labels for files needed and h5 file
        self.label1.grid(row=1, column=1, sticky=tk.W)   # that will be created
        self.label2 = tk.Label(self, text="Data File:")
        self.label2.grid(row=2, column=1, sticky=tk.W)
        self.label3 = tk.Label(self, text="Output File:")
        self.label3.grid(row=3, column=1, sticky=tk.W)
        self.e1 = tk.Entry(self, bg="white", width=27)   #Entry that stores file names to be
        self.e1.grid(row=1, column=3, sticky=tk.W)       # used and created
        self.e2 = tk.Entry(self, bg="white", width=27)
        self.e2.grid(row=2, column=3, sticky=tk.W)
        self.e3 = tk.Entry(self, relief="flat", width=41)
        self.e3.grid(row=3, column=2, columnspan=3, sticky=tk.W)
        self.e4 = tk.Entry(self, relief="flat", highlightbackground="gray80", width=55)
        self.e4.grid(row=4, column=0, columnspan=4, sticky=tk.W) #Error message entry

        self.button1 = tk.Button(self, text="Browse",   #Button to load roi file
                                 command=self.loadroifile, width=10)
        self.button1.grid(row=1, column=2, sticky=tk.W)
        self.button2 = tk.Button(self, text="Browse",   #Button to load data file
                                 command=self.loaddatafile, width=10)
        self.button2.grid(row=2, column=2, sticky=tk.W)

        self.runbutton = tk.Button(self, text="Convert\n\nto\n\nh5file", justify=tk.CENTER, 
                                   command=self.fileconvert) # Button to initiate conversion
        self.runbutton.grid(row=1, column = 0, rowspan=3,  sticky=tk.W)
        self.runbutton.configure(background="IndianRed1")
        self.clearbutton = tk.Button(self, text="Clear", command=self.clearcontents)
        self.clearbutton.grid(row=4, column = 3, sticky=tk.E) #Button to clear files that have
                                                              # been loaded  
        self.exitbutton = tk.Button(self, text="Exit", command=self.quit) # Exit button
        self.exitbutton.grid(row=4, column = 4, sticky=tk.W)

        tk.mainloop()

    def loadroifile(self):                                #Function that selects roi filename

        self.e4.delete(0, tk.END)                         #Removes error message (prevents 
                                                          # concatenation of sequential text)

        self.runbutton.configure(background="IndianRed1") #Ensures red button colour is produced 
                                                          # if selection that previously gave a
                                                          # green color is changed.
        currentdir = os.chdir("./")
        self.fname = tkFileDialog.askopenfilename(initialdir=currentdir,
                                                  filetypes=( ("Dat files", "*.dat"), ("All files", "*.*") ))
        if self.fname:                                    #Ensures file is actually selected and 
                                                          # code does not run if "browse" cancelled 

            self.e1.delete(0, tk.END)                     #Previous file name is removed from entry
            self.e1.insert(0, self.fname)                 #New file selection stored in entry

            chars = len(self.fname)                       #Length of file/path determined to set
            self.e1.config(width=chars)                   # correct width of entry box

            self.outfile = self.fname.replace(".dat",".h5") #Output file/path created
            self.e3.delete(0, tk.END)                     #Previous output file name is removed
            self.e3.insert(0, self.outfile)               #New output file name is stored
            self.e3.config(width=chars)                   #Entry box width is set

        f1 = ( self.e1.get() )                            #Store roi file name in variable
        f2 = ( self.e2.get() )                            #Store data file name in variable

        self.colourbutton(f1, f2)                         #Sets color of button based on 
                                                          # authentisity of selected files 
              
    def loaddatafile(self):                               #Function that selects data filename
							  #See comments above
        self.e4.delete(0, tk.END)
        self.runbutton.configure(background="IndianRed1")

        currentdir = os.chdir("./")
        self.fname = tkFileDialog.askopenfilename(initialdir=currentdir,
                                                  filetypes=( ("Dat files", "*.dat"), ("All files", "*.*") ))

        if self.fname:
            chars = len(self.fname) 
            self.e2.delete(0, tk.END)
            self.e2.insert(0, self.fname)
            self.e2.config(width=chars)

        f1 = ( self.e1.get() )
        f2 = ( self.e2.get() )

        self.colourbutton(f1, f2)    

    def clearcontents(self):                             #Function to restore GUI to default

        self.e1.delete(0, tk.END)                        #Deletes stored roi file name and 
        self.e1.config(width=27)                         # resets entry width
        self.e2.delete(0, tk.END)                        #Deletes stored data file name and
        self.e2.config(width=27)                         # resets entry width
        self.e3.delete(0, tk.END)                        #Deletes stored output file name and
        self.e3.config(width=41)                         # resets entry width
        self.e4.delete(0, tk.END)                        #Deletes error messages and resets
        self.e4.config(width=48)                         # entry width

        self.runbutton.configure(background="IndianRed1") #Colours run button red

    def colourbutton(self, f1, f2):                      #Sets run button color
   							 # Green = good input, red = bad input
        if f1 and f2 and (f1 != f2):
            self.runbutton.configure(background="pale green")
        else:
            self.runbutton.configure(background="IndianRed1")

    def fileconvert(self):				 #Function to convert files to h5 format
  
        self.roifile = ( self.e1.get() )		 #Gets roi file name from selected file
        self.datafile = ( self.e2.get() )                #Gets data file name from selected file


        if self.roifile and self.datafile and (self.roifile != self.datafile):
							 #Ensures roi and data file are selected
							 # and aren't the same name before running
							 # conversion code 
            self.e4.delete(0, tk.END)			 #Removes previous error messages

            msg = h5conv.h5convert(self.roifile, self.datafile) #CODE TO CONVERT FILES!!
							 # Calls function from h5convert_v1.0.py
    							 #Outputs completion message
            chars = len(msg)   				 #Determines message length
            self.e4.delete(0, tk.END)                    #Removes previous error messages
            self.e4.config(width=chars)                  #Sets message box the length of msg
            self.e4.insert(0, msg)                       #Prints completion message

        elif (self.roifile == self.datafile) and (self.roifile or self.datafile != ""):
                                                         #Error if files are not selected or
            self.e4.delete(0, tk.END)                    # are the same name
            self.e4.insert(0, "ROI file can not be the same as Data file!")
        elif self.roifile or self.datafile == "":        #Error if one file is not selected

            self.e4.delete(0, tk.END)
            self.e4.insert(0, "Please select both ROI and Data files to convert")

    def quit(self):
        sys.exit(0)            

##########################################################################################

if __name__ == '__main__':
    App()






