from tkinter import *
from tkinter.ttk import *

class Main(Frame):
    def __init__(self, parent, connect):
        Frame.__init__(self,parent)
        self.parent = parent
        self.connect = connect
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        self.winfo_toplevel().title("Smokescreen")

        ip_label = Label(self, text="Server IP:") 
        port_label = Label(self, text="Server Port:") 
        ip_label.grid(row=0, column=0, sticky=W, pady=2) 
        port_label.grid(row=1, column=0, sticky=W, pady=2) 

        self.ip_entry = Entry(self)
        self.port_entry = Entry(self)

        self.ip_entry.grid(row=0, column=1, pady=2) 
        self.port_entry.grid(row=1, column=1, pady=2) 

        submit_button = Button(self, text="Connect", command=self.on_submit)
        submit_button.grid(row=2, column=1, pady=2) 

    def on_submit(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())
        self.connect(ip, port)


if __name__ == '__main__':
    def connect(ip, port):
        print(ip, port)
    root = Tk()
    main = Main(root, connect)
    root.mainloop()