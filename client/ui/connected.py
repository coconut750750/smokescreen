from tkinter import *
from tkinter.ttk import *

class Connected(Frame):
    def __init__(self, parent, connection_string, disconnect):
        Frame.__init__(self,parent)
        self.parent = parent
        self.disconnect = disconnect
        self.connection_string = connection_string
        self.pack()
        self.setup_widgets()

    def setup_widgets(self):
        self.winfo_toplevel().title("Smokescreen")

        self.connected_label = Label(self, text=f"Connected to {self.connection_string}") 
        self.connected_label.grid(row=0, column=0, sticky=W, pady=2)

        self.dc_button = Button(self, text="Disconnect", command=self.disconnect)
        self.dc_button.grid(row=1, column=0, pady=2)

if __name__ == '__main__':
    def disconnect():
        print('dc')
    root = Tk()
    main = Connected(root, 'localhost:1515', disconnect)
    root.mainloop()