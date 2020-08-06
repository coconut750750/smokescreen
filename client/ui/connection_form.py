import wx

def text_input_sizer(parent, label):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    label = wx.StaticText(parent, wx.ID_ANY, label)
    text_ctrl = wx.TextCtrl(parent, wx.ID_ANY)

    sizer.Add(label, 0, wx.EXPAND)
    sizer.Add(text_ctrl, 0, wx.EXPAND)
    return sizer, label, text_ctrl

class ConnectionForm(wx.Panel):
    def __init__(self, parent, onSubmit):
        wx.Panel.__init__(self, parent, size=(-1, -1))
        connect_button = wx.Button(self, wx.ID_ANY, 'Connect')
        self.Bind(wx.EVT_BUTTON, self.submit, connect_button)

        server_sizer, server_label, self.server_input = text_input_sizer(self, "Server IP:")
        port_sizer, port_label, self.port_input = text_input_sizer(self, "Server Port:")

        sizer = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(connect_button, 0, wx.EXPAND)
        sizer.Add(server_sizer, 0, wx.EXPAND)
        sizer.Add(port_sizer, 0, wx.EXPAND)
        sizer.Add(hsizer, 0, wx.EXPAND)

        self.onSubmit = onSubmit

        self.SetSizer(sizer)
        self.Show()

    def submit(self, event):
        ip = self.server_input.GetValue()
        port = int(self.port_input.GetValue())
        self.onSubmit(ip, port)

if __name__ == '__main__':
    app = wx.App()
    frame = ConnectionForm(None)
    app.MainLoop()
