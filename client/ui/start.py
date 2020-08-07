from tkinter import *
from tkinter.ttk import *

class Start(Frame):
    def __init__(self, parent, connect):
        Frame.__init__(self,parent)
        self.parent = parent
        self.connect = connect
        self.setup_widgets()

    def setup_widgets(self):
        self.ip_label = Label(self, text="Server IP:") 
        self.port_label = Label(self, text="Server Port:") 
        self.ip_label.grid(row=0, column=0, sticky=W, pady=2) 
        self.port_label.grid(row=1, column=0, sticky=W, pady=2) 

        self.ip_entry = Entry(self)
        self.port_entry = Entry(self)

        self.ip_entry.grid(row=0, column=1, pady=2) 
        self.port_entry.grid(row=1, column=1, pady=2) 

        self.submit_button = Button(self, text="Connect", command=self.on_submit)
        self.submit_button.grid(row=2, column=1, pady=2)
        self.parent.bind('<Return>', self.on_submit)

    def on_submit(self, event=None):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        if port.isnumeric():
            self.connect(ip, int(port))

if __name__ == '__main__':
    def connect(ip, port):
        print(ip, port)
    root = Tk()
    main = Main(root, connect)
    root.mainloop()