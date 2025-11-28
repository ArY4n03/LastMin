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

        #this frame will be used for all the work like asking questions and stuff
        self.WorkingFrame = ctk.CTkFrame(master)
        self.WorkingFrame.place(relheight=1,relwidth=1)

        self.mainFrame.tkraise()

        #contents of main frame

        self.label = ctk.CTkLabel(master=self.mainFrame,text="LastMin",font=(None,200))
        self.label.place(relx=0.3,rely=0.1)
        self.pdfBtn = ctk.CTkButton(master=self.mainFrame,text="PDF FILE",font=self.font,command= lambda: self.raiseFrame('pdf'))
        self.pdfBtn.place(relx=0.45,rely=0.4)

        self.txtBtn = ctk.CTkButton(master=self.mainFrame,text="Text File",font=self.font,command= lambda: self.raiseFrame('text'))
        self.txtBtn.place(relx=0.453,rely=0.5)


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


        self.BackBtn = ctk.CTkButton(self.WorkingFrame,font=self.font,text="back",command=self.clear_all)
        self.BackBtn.place(relx=0.05,rely=0.1)

        self.saveas_txt = ctk.CTkButton(self.WorkingFrame,text="save as text")
        self.saveas_txt.place(relx=0.87,rely=0.3)

        self.saveas_pdf = ctk.CTkButton(self.WorkingFrame,text="save as pdf")
        self.saveas_pdf.place(relx=0.87,rely=0.5)

    def raiseFrame(self,mode):
        self.mode = mode
        self.WorkingFrame.tkraise()

    def browse_source(self):
        
        if self.mode:
            match self.mode:
                case "pdf":
                    self.source = filedialog.askopenfilename(defaultextension="*.pdf",filetypes=(("PDF File","*.pdf"),))
                case "text":
                    self.source = filedialog.askopenfilename(defaultextension="*.txt",filetypes=(("Text File","*.txt"),))
        
        if self.source:
            self.show_loading()
            threading.Thread(target=self.process_file,daemon=True).start()

    def process_file(self):
        try:
            self.SourceEntry.configure(state='normal')
            self.SourceEntry.delete(0, "end")
            self.SourceEntry.insert(0, self.source)
            self.SourceEntry.configure(state="disabled")

            self.document = utils.load_document(self.source,self.mode)
            self.retriveval_chain = utils.create_retrieval_chain_(self.document)
        except:
            pass
        finally:
            self.hide_loading()

    def ask(self):
        if self.retriveval_chain:
            #invoking query from retriveal chain
            self.show_loading(text="Generating Response")

            threading.Thread(target=self.generate_response,daemon=True).start()

    def generate_response(self):
            
        response = self.retriveval_chain.invoke({'input':self.queryArea.get('1.0','end').strip()})['answer']
            
        if response:
            self.responseArea.configure(state='normal')
            self.responseArea.insert("end", "Question: " + self.queryArea.get('1.0','end').strip())
            self.responseArea.insert("end","\nResponse : " + response + "\n")
            self.responseArea.configure(state='disabled')

        self.hide_loading()
    
    def show_loading(self, text="Processing..."):
        self.loader = ctk.CTkToplevel()# popup window
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
        if hasattr(self,"loader"):
            self.loader.destroy()
    
    def clear_all(self):
        self.clear_text(self.SourceEntry)
        self.clear_text(self.responseArea)
        self.document = None
        self.retriveval_chain = None
        self.mainFrame.tkraise()

    
    def clear_text(self,widget):
        widget.configure(state='normal')
        widget.delete(0,'end')
        widget.configure(state='disabled')
if __name__ == "__main__":
    window = ctk.CTk()
    main = Main(window)
    window.mainloop()
