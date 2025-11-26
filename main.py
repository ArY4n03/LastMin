import customtkinter as ctk
import utils

 
class Main:
    def __init__(self,master):
        window.geometry("1200x600")
        self.db = None
        self.document = None
        self.retrival_chain = None
        self.font = (None,35)
        #Main Frame
        self.mainFrame = ctk.CTkFrame(master)
        self.mainFrame.place(relheight=1,relwidth=1)

        #Frame used when using pdf file
        self.PdfFrame = ctk.CTkFrame(master)
        self.PdfFrame.place(relheight=1,relwidth=1)

        #Frame Used when using websites
        self.WebFrame = ctk.CTkFrame(master,bg_color="Green")
        self.WebFrame.place(relheight=1,relwidth=1)

        #frame used when using text files
        self.TextFrame = ctk.CTkFrame(master)
        self.TextFrame.place(relheight=1,relwidth=1)

        self.mainFrame.tkraise()

        #contents of main frame
        self.pdfBtn = ctk.CTkButton(master=self.mainFrame,text="PDF FILE",font=self.font,command= lambda: self.raiseFrame(1))
        self.pdfBtn.place(relx=0.4,rely=0.2)

        self.webBtn = ctk.CTkButton(master=self.mainFrame,text="Websites",font=self.font,command= lambda: self.raiseFrame(2))
        self.webBtn.place(relx=0.4,rely=0.4)

        self.txtBtn = ctk.CTkButton(master=self.mainFrame,text="Text File",font=self.font,command= lambda: self.raiseFrame(3))
        self.txtBtn.place(relx=0.4,rely=0.6)


        self.textFile = ctk.CTkEntry(self.TextFrame,font=self.font)
        self.textFile.place(relx=0.25,rely=0.1,relwidth=0.4)

        self.BrowseBtn = ctk.CTkButton(self.TextFrame,font=self.font,text='browse',command= self.browse_text_File)
        self.BrowseBtn.place(relx=0.7,rely=0.1)

        self.responseArea = ctk.CTkTextbox(self.TextFrame,font=self.font)
        self.responseArea.place(relx=0.15,rely=0.3,relheight=0.65,relwidth=0.7)

    def raiseFrame(self,frame=1):
        match frame:
            case 1:
                self.PdfFrame.tkraise()
                print('pdf')
            case 2:
                self.WebFrame.tkraise()
                print('web')
            case 3:
                self.TextFrame.tkraise()
                print('text')

    def browse_text_File(self):
        self.filename = ""
        self.document = None
        
if __name__ == "__main__":
    window = ctk.CTk()
    main = Main(window)
    window.mainloop()
