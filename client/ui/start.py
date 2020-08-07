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

    def setup_connected(self, ip, port):
        self.ip_label.grid_forget()
        self.port_label.grid_forget()
        self.ip_entry.grid_forget()
        self.port_entry.grid_forget()
        self.submit_button.grid_forget()

        self.connected_label = Label(self, text=f"Connected to {ip}:{port}") 
        self.connected_label.grid(row=0, column=0, sticky=W, pady=2) 


    def on_submit(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        if port.isnumeric():
            self.connect(ip, int(port))
            self.setup_connected(ip, port)


if __name__ == '__main__':
    def connect(ip, port):
        print(ip, port)
    root = Tk()
    main = Main(root, connect)
    root.mainloop()