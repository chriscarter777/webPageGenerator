# Step 73 drill:
# use VS and Python3
# create a webpage
# use tkinter to make a GUI
# let user set the body text
# or select from prior entries (displayed)
# using sqlite to stare and retrieve prior entries
# let user publish the page
# open the page in web browser upon publishing
#
import os
import os.path
import sys
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import webbrowser
import sqlite3
import datetime
import time


class Webform:
    
    def __init__(self, master):

        # DEFINE FORM ACTIONS
        def changeFile():
            self.fileName = filedialog.asksaveasfilename()
            enterFilepath.delete(0, END)
            enterFilepath.insert(0, self.fileName)
    
        def selectPrior():
            pn = self.priorNum.get()-1
            print(pn, self.priorNum, type(self.priorNum))

            self.fileName = self.priorVals[pn][0]
            self.pageTitle = self.priorVals[pn][1]
            self.pageContent = self.priorVals[pn][2]
            enterFilepath.delete(0, END)
            enterFilepath.insert(0, self.fileName)
            enterTitle.delete(0, END)
            enterTitle.insert(0, self.pageTitle)
            enterContent.delete("1.0", END)
            enterContent.insert(END, self.pageContent)

        def onQuit():
            master.destroy()
            connection.close()
    
        def publish():
            #---->GET DATA
            self.fileName = enterFilepath.get()
            self.pageTitle = enterTitle.get()
            self.pageContent = enterContent.get("1.0", "end")

            #---->WRITE DATA TO DATABASE
            c.execute("INSERT INTO submissions (date, pathname, title, contents) VALUES (?,?,?,?)", (time.time(), self.fileName, self.pageTitle, self.pageContent))
            connection.commit()

            
            #---->OPEN FILE FOR WRITING
            print("Writing file...")
            print(self.fileName, "\n  ",self.pageTitle, "\n  ",self.pageContent)
            f= open(self.fileName, "w")

            #---->WRITE THE HTML
            f.write("<html>\n")
            f.write("<head><title>" + self.pageTitle + "</title>\n")
            f.write("<body>\n")
            f.write(self.pageContent + "\n")
            f.write("</body>\n")
            f.write("</html>\n")

            #---->CLOSE THE FILE
            f.close()

            #====>OPEN IT IN THE WEB BROWSER
            url = self.fileName
            webbrowser.open(url,2)

        # SET UP DATABASE CONNECTION
        connection=sqlite3.connect("webPages.db")
        c=connection.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS submissions (id INTEGER PRIMARY KEY, date DATE, pathname VARCHAR(60), title VARCHAR(60), contents VARCHAR(600))")
        priors = c.execute("SELECT * FROM submissions")

        # SET UP THE WINDOW
        master.title("Publish Web Page")
        master.geometry("800x800+200+200")
        topFrame=ttk.Frame(master, width=800, height=300)
        middleFrame=ttk.Frame(master, width=800, height=300)
        bottomFrame=ttk.Frame(master, width=800, height=300)
        topFrame.pack()
        middleFrame.pack()
        bottomFrame.pack()

        # SET UP MENUS
        master.option_add("*tearOff", False)

        menuBar = Menu(master)
        master.config(menu = menuBar)

        fileMenu = Menu(menuBar)
        exitMenu = Menu(menuBar)
        menuBar.add_cascade(menu = fileMenu, label = "File")
        menuBar.add_cascade(menu = exitMenu, label = "Exit")

        fileMenu.add_command(label = "Change filename", command = changeFile)
        exitMenu.add_command(label = "Quit", command = onQuit)
 
        # SET UP PATHNAME ENTRY, WITH DEFAULT VALUES
        self.fileName = "C:\\Users\Owner\Desktop\PythonStep72Page.html"
        
        filepathPrompt = ttk.Label(topFrame, text = "File pathname:", justify=RIGHT)
        filepathPrompt.grid(column=0, row=0, sticky="e", padx=15, pady=5)
        
        enterFilepath = ttk.Entry(topFrame, width = 60)
        enterFilepath.insert(0, self.fileName)
        enterFilepath.grid(column=1, row=0, sticky="w", pady=5)

        # SET UP TITLE ENTRY, WITH DEFAULT VALUES
        self.pageTitle = "Summer Sale"
        
        titlePrompt = ttk.Label(topFrame, text = "Enter title for web page:", justify=RIGHT)
        titlePrompt.grid(column=0, row=1, sticky="e", padx=15, pady=5)
        
        enterTitle = ttk.Entry(topFrame, width = 60)
        enterTitle.insert(0, self.pageTitle)
        enterTitle.grid(column=1, row=1, sticky="w", pady=5)

        # SET UP BODY TEXT ENTRY, WITH DEFAULT VALUES
        self.pageContent = "Stay tuned for our amazing summer sale!"
        
        contentPrompt = ttk.Label(topFrame, text = "Enter content for web page body:", justify=RIGHT)
        contentPrompt.grid(column=0, row=2, sticky="e", padx=15, pady=5)
        
        enterContent = Text(topFrame, width = 60, height = 6, wrap="word")
        #self.pageContent = enterContent.get()
        enterContent.insert("1.0", self.pageContent)
        enterContent.grid(column=1, row=2, sticky="w", pady=5)

        # SET UP THE PRIORS
        priorIdLabel=ttk.Label(middleFrame, text="Id")
        priorDateLabel=ttk.Label(middleFrame, text="Date")
        priorFileLabel=ttk.Label(middleFrame, text="Filepath")
        priorTitleLabel=ttk.Label(middleFrame, text="Page Title")
        priorContentLabel=ttk.Label(middleFrame, text="Body text")
        priorIdLabel.grid(column=0, row=0, sticky="n", pady=20)
        priorDateLabel.grid(column=1, row=0, sticky="n", pady=20)
        priorFileLabel.grid(column=2, row=0, sticky="n", pady=20)
        priorTitleLabel.grid(column=3, row=0, sticky="n", pady=20)
        priorContentLabel.grid(column=4, row=0, sticky="n", pady=20)
        counter = 0
        self.priorVals = []

        for prior in priors:
            counter += 1
            self.priorVals.append([prior[2], prior[3], prior[4]])

            ttk.Label(middleFrame, text=counter, width=4).grid(column=0, row=counter, padx=5)
            ttk.Label(middleFrame, text=prior[1], width=18).grid(column=1, row=counter, padx=5)
            ttk.Label(middleFrame, text=prior[2], width=25).grid(column=2, row=counter, padx=5)
            ttk.Label(middleFrame, text=prior[3], width=20).grid(column=3, row=counter, padx=5)
            ttk.Label(middleFrame, text=prior[4], width=40).grid(column=4, row=counter, padx=5)
        
        # SET UP THE SELECTION OF PRIOR DATA
        ttk.Label(middleFrame, text="Select a prior dataset if desired.").grid(column=0, row=counter+1, columnspan=5)
        
        self.priorNum = IntVar()
        Spinbox(middleFrame, from_ =0, to= counter, textvariable=self.priorNum).grid(column=0, row=counter+2, columnspan=2)
        
        priorSel = ttk.Button(middleFrame, text="Select Dataset")
        priorSel.grid(column=4, row=counter+2, columnspan=2)
        priorSel.config(command=selectPrior)
        
        # SET UP THE ACTION BUTTON
        go = ttk.Button(bottomFrame, text = "Publish Web Page")
        go.pack(pady=30)
        go.config(command=publish)





def main():
    root = Tk()
    form1 = Webform(root)
    root.mainloop()

if __name__ == "__main__": main()
