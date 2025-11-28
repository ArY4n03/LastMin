import customtkinter as ctk
from tkinter import filedialog
import utils
import threading

class Main:
    def __init__(self,master):
        master.geometry("1200x800")
        master.title("LastMin")
        self.db = None
        self.document = None
        self.retriveval_chain = None
        self.font = (None,35)
        self.mode = None
        self.source = None
        #Main Frame
        self.mainFrame = ctk.CTkFrame(master)
        self.mainFrame.place(relheight=1,relwidth=1)

        #
        self.WorkingFrame = ctk.CTkFrame(master)
        self.WorkingFrame.place(relheight=1,relwidth=1)

        self.mainFrame.tkraise()

        #contents of main frame
        self.pdfBtn = ctk.CTkButton(master=self.mainFrame,text="PDF FILE",font=self.font,command= lambda: self.raiseFrame('pdf'))
        self.pdfBtn.place(relx=0.4,rely=0.2)

        self.webBtn = ctk.CTkButton(master=self.mainFrame,text="Websites",font=self.font,command= lambda: self.raiseFrame('web'))
        self.webBtn.place(relx=0.4,rely=0.4)

        self.txtBtn = ctk.CTkButton(master=self.mainFrame,text="Text File",font=self.font,command= lambda: self.raiseFrame('text'))
        self.txtBtn.place(relx=0.4,rely=0.6)


        self.SourceEntry= ctk.CTkEntry(self.WorkingFrame,font=self.font,state='disabled')
        self.SourceEntry.place(relx=0.25,rely=0.1,relwidth=0.4)

        self.BrowseBtn = ctk.CTkButton(self.WorkingFrame,font=self.font,text='Browse File',command= self.browse_source)
        self.BrowseBtn.place(relx=0.7,rely=0.1)

        self.responseArea = ctk.CTkTextbox(self.WorkingFrame,font=self.font)
        self.responseArea.place(relx=0.15,rely=0.2,relheight=0.55,relwidth=0.7)

        self.queryArea = ctk.CTkTextbox(self.WorkingFrame,font=self.font)
        self.queryArea.place(relx=0.15,rely=0.8,relheight=0.1,relwidth=0.7)

        self.AskBtn = ctk.CTkButton(self.WorkingFrame,font=self.font,text='Ask',command=self.ask)
        self.AskBtn.place(relx=0.45,rely=0.93)

    def raiseFrame(self,mode):
        self.mode = mode
        self.WorkingFrame.tkraise()

    def browse_source(self):
        
        if self.mode:
            match self.mode:
                case "pdf":
                    self.source = filedialog.askopenfilename(defaultextension="*.pdf",filetypes=(("PDF File","*.pdf"),))

                    print(self.source)
                case "web":
                    self.source = filedialog.askopenfilename(defaultextension="*.pdf",filetypes=(("PDF File","*.pdf"),))

                    print(self.source)
                case "text":
                    self.source = filedialog.askopenfilename(defaultextension="*.txt",filetypes=(("Text File","*.txt"),))
                    print(self.source)
        
        if self.source:
            self.show_loading()
            threading.Thread(target=self.process_file,daemon=True).start()

    def process_file(self):
        try:
            self.SourceEntry.configure(state='normal')
            self.SourceEntry.delete(0, "end")
            self.SourceEntry.insert(0, self.source)
            self.SourceEntry.configure(state="normal")

            self.document = utils.load_document(self.source,self.mode)
            self.retriveval_chain = utils.create_retrieval_chain_(self.document)
        except:
            pass
        finally:
            self.hide_loading()

    def ask(self):
        if self.retriveval_chain:
            #invoking query from retriveal chain
            self.show_loading()

            threading.Thread(target=self.generate_response,daemon=True).start()

    def generate_response(self):
            
        response = self.retriveval_chain.invoke({'input':self.queryArea.get('1.0','end').strip()})['answer']
            
        if response:

            self.responseArea.insert("end", "Question: " + self.queryArea.get('1.0','end').strip())
            self.responseArea.insert("end","\nResponse : " + response)
        

        self.hide_loading()
    
    def show_loading(self, text="Processing..."):
        self.loader = ctk.CTkToplevel()          # popup window
        self.loader.geometry("300x120")
        self.loader.title("Please wait")
        self.loader.resizable(False, False)
        self.loader.attributes("-topmost",True)
        label = ctk.CTkLabel(self.loader, text=text, font=(None, 20))
        label.pack(pady=15)

        progress = ctk.CTkProgressBar(self.loader, mode="indeterminate")
        progress.pack(pady=10, fill="x", padx=20)
        progress.start()
    
    def hide_loading(self):
        print('entered function')
        if hasattr(self,"loader"):
            print("entered if statement")
            self.loader.destroy()

if __name__ == "__main__":
    window = ctk.CTk()
    main = Main(window)
    window.mainloop()
