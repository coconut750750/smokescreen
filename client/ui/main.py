import wx

from client.ui.connection_form import ConnectionForm

WIDTH = 400
HEIGHT = 600

class MainWindow(wx.Frame):
    def __init__(self, start_connection):
        super().__init__(parent=None, title='Smokescreen', size=(WIDTH, -1))
        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.table = wx.ListCtrl(
            self, size=(-1, HEIGHT), 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.build_table()
        self.start_connection = start_connection
        connForm = ConnectionForm(self, self.on_submit)
        sizer.Add(connForm, 0, wx.EXPAND)
        sizer.Add(self.table, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.setup_shortcuts()
        self.Show()

    def setup_shortcuts(self):
        qid = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onQ, id=qid)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('Q'), qid)])
        self.SetAcceleratorTable(accel_tbl)

    def onQ(self, event):
        self.Close()

    def build_table(self):
        self.table.InsertColumn(0, 'Time', width=100)
        self.table.InsertColumn(1, 'Level', width=50)
        self.table.InsertColumn(2, 'Message', width=250)
    
    def add_log(self, time, levelname, log):
        self.table.InsertItem(0, time)
        self.table.SetItem(0, 1, levelname)
        self.table.SetItem(0, 2, log)

    def on_submit(self, server_ip, server_port):
        self.start_connection(self, server_ip, server_port)

if __name__ == '__main__':
    app = wx.App(False)
    window = MainWindow()
    app.MainLoop()
