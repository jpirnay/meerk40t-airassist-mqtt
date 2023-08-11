import wx

class ConfigDialog(wx.Dialog):

    # from meerk40t.gui.wxutils import TextCtrl

    def __init__(self, context, coolid, *args, **kwds):
        self.context = context
        _ = context._
        self._coolid = coolid
        # begin wxGlade: RefAlign.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle(_("Manage MQTT-Interfaces"))
        mainsizer = wx.BoxSizer(wx.VERTICAL)


        self.SetSizer(mainsizer)
        mainsizer.Fit(self)
