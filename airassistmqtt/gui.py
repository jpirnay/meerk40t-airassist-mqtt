import wx
import paho.mqtt.client as mqtt

_ = wx.GetTranslation

class ConfigDialog(wx.Dialog):

    # from meerk40t.gui.wxutils import TextCtrl

    def __init__(self, context, coolid, *args, **kwds):
        # begin wxGlade: RefAlign.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE

        self.context = context
        self.coolid = coolid
        if context is not None and hasattr(context, "root"):
            self.storage = context.root.settings
        else:
            self.storage = None
        self.entries = {}
        self.identifier = "airassist-mqtt"

        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1, client_id="meerk40t", )

        wx.Dialog.__init__(self, *args, **kwds)

        self.SetTitle(_("Manage MQTT-Interfaces"))
        sizer_main = wx.BoxSizer(wx.HORIZONTAL)

        vsizer_left = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(vsizer_left, 1, wx.EXPAND, 0)

        sizer_id = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Identifier")), wx.VERTICAL)
        vsizer_left.Add(sizer_id, 0, wx.EXPAND, 0)

        hsizer_id = wx.BoxSizer(wx.HORIZONTAL)
        sizer_id.Add(hsizer_id, 1, wx.EXPAND, 0)

        lbl_id = wx.StaticText(self, wx.ID_ANY, _("Id"))
        lbl_id.SetMinSize((70, -1))
        hsizer_id.Add(lbl_id, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.text_id = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_id.SetToolTip(_("Define a unique identifier to refer to within MeerK40t"))
        hsizer_id.Add(self.text_id, 1, wx.EXPAND, 0)

        sizer_server = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Broker")), wx.VERTICAL)
        vsizer_left.Add(sizer_server, 0, wx.EXPAND, 0)

        hsizer_address = wx.BoxSizer(wx.HORIZONTAL)
        sizer_server.Add(hsizer_address, 1, wx.EXPAND, 0)

        lbl_server = wx.StaticText(self, wx.ID_ANY, _("Address"))
        lbl_server.SetMinSize((70, -1))
        hsizer_address.Add(lbl_server, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.text_address = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_address.SetToolTip(_("Address of the MQTT-Broker"))
        hsizer_address.Add(self.text_address, 1, wx.EXPAND, 0)

        hsizer_port = wx.BoxSizer(wx.HORIZONTAL)
        sizer_server.Add(hsizer_port, 1, wx.EXPAND, 0)

        lbl_port = wx.StaticText(self, wx.ID_ANY, _("Port"))
        lbl_port.SetMinSize((70, -1))
        hsizer_port.Add(lbl_port, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.text_port = wx.TextCtrl(self, wx.ID_ANY, "1883")
        self.text_port.SetToolTip(_("Port to connect to (default 1883)"))
        hsizer_port.Add(self.text_port, 0, wx.EXPAND, 0)

        sizer_server_copy = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Authentication")), wx.VERTICAL)
        vsizer_left.Add(sizer_server_copy, 0, wx.EXPAND, 0)

        hsizer_user = wx.BoxSizer(wx.HORIZONTAL)
        sizer_server_copy.Add(hsizer_user, 1, wx.EXPAND, 0)

        lbl_username = wx.StaticText(self, wx.ID_ANY, _("Username"))
        lbl_username.SetMinSize((70, -1))
        hsizer_user.Add(lbl_username, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.text_username = wx.TextCtrl(self, wx.ID_ANY, "")
        self.text_username.SetToolTip(_("(Optional) Username to identify"))
        hsizer_user.Add(self.text_username, 1, wx.EXPAND, 0)

        hsizer_pass = wx.BoxSizer(wx.HORIZONTAL)
        sizer_server_copy.Add(hsizer_pass, 1, wx.EXPAND, 0)

        lbl_pass = wx.StaticText(self, wx.ID_ANY, _("Password"))
        lbl_pass.SetMinSize((70, -1))
        hsizer_pass.Add(lbl_pass, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.text_password = wx.TextCtrl(self, wx.ID_ANY)
        self.text_password.SetToolTip(_("(Optional) Password to identify"))
        hsizer_pass.Add(self.text_password, 1, wx.EXPAND, 0)

        sizer_on = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Command to turn on")), wx.VERTICAL)
        vsizer_left.Add(sizer_on, 0, wx.EXPAND, 0)

        hsizer_topic_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_on.Add(hsizer_topic_1, 1, wx.EXPAND, 0)

        lbl_subject_on = wx.StaticText(self, wx.ID_ANY, _("Topic"))
        lbl_subject_on.SetMinSize((70, -1))
        hsizer_topic_1.Add(lbl_subject_on, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.text_subject_on = wx.TextCtrl(self, wx.ID_ANY, "")
        hsizer_topic_1.Add(self.text_subject_on, 1, wx.EXPAND, 0)

        hsizer_payload_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_on.Add(hsizer_payload_1, 1, wx.EXPAND, 0)

        lbl_payload_on = wx.StaticText(self, wx.ID_ANY, _("Message"))
        lbl_payload_on.SetMinSize((70, -1))
        hsizer_payload_1.Add(lbl_payload_on, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.text_payload_on = wx.TextCtrl(self, wx.ID_ANY, _("ON"))
        self.text_payload_on.SetToolTip(_("What is the payload to send?"))
        hsizer_payload_1.Add(self.text_payload_on, 1, wx.EXPAND, 0)
        self.btn_test_on = wx.Button(self, wx.ID_ANY, _("Test"))
        self.btn_test_on.SetToolTip(_("Test it out and send the command"))
        hsizer_payload_1.Add(self.btn_test_on, 0, wx.EXPAND, 0)

        sizer_off = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Command to turn off")), wx.VERTICAL)
        vsizer_left.Add(sizer_off, 0, wx.EXPAND, 0)

        hsizer_topic_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_off.Add(hsizer_topic_2, 1, wx.EXPAND, 0)

        lbl_subject_off = wx.StaticText(self, wx.ID_ANY, _("Topic"))
        lbl_subject_off.SetMinSize((70, -1))
        hsizer_topic_2.Add(lbl_subject_off, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.text_subject_off = wx.TextCtrl(self, wx.ID_ANY, "")
        hsizer_topic_2.Add(self.text_subject_off, 1, wx.EXPAND, 0)

        hsizer_payload_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_off.Add(hsizer_payload_2, 1, wx.EXPAND, 0)

        lbl_payload_off = wx.StaticText(self, wx.ID_ANY, _("Message"))
        lbl_payload_off.SetMinSize((70, -1))
        hsizer_payload_2.Add(lbl_payload_off, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.text_payload_off = wx.TextCtrl(self, wx.ID_ANY, _("OFF"))
        self.text_payload_off.SetToolTip(_("What is the payload to send?"))
        hsizer_payload_2.Add(self.text_payload_off, 1, wx.EXPAND, 0)
        self.btn_test_off = wx.Button(self, wx.ID_ANY, _("Test"))
        self.btn_test_off.SetToolTip(_("Test it out and send the command"))
        hsizer_payload_2.Add(self.btn_test_off, 0, wx.EXPAND, 0)

        self.btn_apply = wx.Button(self, wx.ID_ANY, _("Apply"))
        vsizer_left.Add(self.btn_apply, 0, wx.ALIGN_RIGHT, 0)

        vsizer_right = wx.BoxSizer(wx.VERTICAL)
        sizer_main.Add(vsizer_right, 1, wx.EXPAND, 0)

        self.list_entries = wx.ListBox(self, wx.ID_ANY)
        self.list_entries.SetToolTip(_("Select the entry to edit"))
        vsizer_right.Add(self.list_entries, 1, wx.EXPAND, 0)

        hsizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        vsizer_right.Add(hsizer_buttons, 0, wx.EXPAND, 0)

        self.btn_ok = wx.Button(self, wx.ID_ANY, _("OK"))
        self.btn_ok.SetToolTip(_("We are done"))
        hsizer_buttons.Add(self.btn_ok, 0, 0, 0)

        hsizer_buttons.Add((0, 0), 0, 0, 0)

        self.btn_add = wx.Button(self, wx.ID_ANY, _("Add another"))
        self.btn_add.SetToolTip(_("Add another entry"))
        hsizer_buttons.Add(self.btn_add, 0, 0, 0)

        self.btn_remove = wx.Button(self, wx.ID_ANY, _("Remove"))
        self.btn_remove.SetToolTip(_("Remove the currently selected entry"))
        hsizer_buttons.Add(self.btn_remove, 0, 0, 0)

        self.SetSizer(sizer_main)
        sizer_main.Fit(self)

        self.Layout()

        self.fill_data(True)

        self.text_id.Bind(wx.EVT_TEXT, self.on_changes)
        self.text_address.Bind(wx.EVT_TEXT, self.on_changes)
        self.text_port.Bind(wx.EVT_TEXT, self.on_changes)
        self.text_subject_on.Bind(wx.EVT_TEXT, self.on_changes)
        self.text_payload_on.Bind(wx.EVT_TEXT, self.on_changes)
        self.text_subject_off.Bind(wx.EVT_TEXT, self.on_changes)
        self.text_payload_off.Bind(wx.EVT_TEXT, self.on_changes)
        self.btn_apply.Bind(wx.EVT_BUTTON, self.on_button_apply)
        self.list_entries.Bind(wx.EVT_LISTBOX, self.on_list_select)
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_button_okay)
        self.btn_add.Bind(wx.EVT_BUTTON, self.on_button_add)
        self.btn_remove.Bind(wx.EVT_BUTTON, self.on_button_remove)
        self.btn_test_on.Bind(wx.EVT_BUTTON, self.on_button_test_on)
        self.btn_test_off.Bind(wx.EVT_BUTTON, self.on_button_test_off)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.on_changes(None)

    def on_close(self, event):
        if self.client and self.client.is_connected():
            self.client.disconnect()
        del self.client
        event.Skip()

    def on_changes(self, event):
        flag = True
        flag = flag and len(self.text_address.GetValue()) > 0
        flag = flag and len(self.text_subject_on.GetValue()) > 0
        flag = flag and len(self.text_subject_off.GetValue()) > 0
        self.btn_apply.Enable(flag)
        flag1 = True
        flag1 = flag1 and len(self.text_address.GetValue()) > 0
        flag1 = flag1 and len(self.text_subject_on.GetValue()) > 0
        flag1 = flag1 and len(self.text_payload_on.GetValue()) > 0
        self.btn_test_on.Enable(flag1)
        flag2 = True
        flag2 = flag2 and len(self.text_address.GetValue()) > 0
        flag2 = flag2 and len(self.text_subject_off.GetValue()) > 0
        flag2 = flag2 and len(self.text_payload_off.GetValue()) > 0
        self.btn_test_off.Enable(flag2)

    def fill_data(self, clearit=False):
        if clearit:
            self.entries.clear()
            section = self.identifier
            if self.storage is not None:
                info = self.storage.read_persistent_string_dict(section)
                if info is not None and len(info) > 0:
                    print (info)
                    for key in info:
                        secs = key.split("/")
                        if len(secs) > 0:
                            skey = secs[-1]
                            entry = self.storage.read_persistent(tuple, section, skey, None)
                            print (f"Reading {skey}: {entry}")
                            if entry is not None:
                                self.entries[skey] = entry
        choices = list(self.entries.keys())
        self.list_entries.Set(choices)
        if len(choices):
            self.list_entries.SetSelection(0)
            self.on_list_select(None)

    def store_data(self):
        section = self.identifier
        if self.storage is not None:
            self.storage.clear_persistent(section)
            for key, entry in self.entries.items():
                self.storage.write_persistent(section, key, entry)

    def execute(self, subject, payload):
        if self.client.is_connected():
            self.client.disconnect()
        server = self.text_address.GetValue()
        pp = self.text_port.GetValue()
        port = 1883
        if pp:
            try:
                port = int(pp)
            except ValueError:
                pass
        usr_name = self.text_username.GetValue()
        usr_pass = self.text_password.GetValue()
        self.client.username_pw_set(usr_name, usr_pass)
        try:
            self.client.connect(server, port)
        except:
            wx.MessageBox(_("Could not connect to the mqtt broker"), "Error", style = wx.OK | wx.ICON_ERROR)
            return
        try:
            self.client.publish(subject, payload)
            self.client.loop()
        except:
            wx.MessageBox(_("Could not send {subject}/{payload}").format(subject=subject, payload=payload), "Error", style = wx.OK | wx.ICON_ERROR)
            return
        wx.MessageBox(_("Sucessfully sent {subject}/{payload}\nNow look at the result.").format(subject=subject, payload=payload), "Success", style = wx.OK | wx.ICON_INFORMATION)

    def on_button_test_on(self, event):
        subj = self.text_subject_on.GetValue()
        msg = self.text_payload_on.GetValue()
        self.execute(subj, msg)

    def on_button_test_off(self, event):
        subj = self.text_subject_off.GetValue()
        msg = self.text_payload_off.GetValue()
        self.execute(subj, msg)

    def on_button_apply(self, event):  # wxGlade: MQTTOptionPanel.<event_handler>
        this_id = self.text_id.GetValue()
        reload_needed = False
        if self.coolid is None:
            if len(this_id) == 0:
                return
            self.coolid = this_id
            reload_needed = True
        newentry = [
            self.text_address.GetValue(),
            self.text_port.GetValue(),
            self.text_username.GetValue(),
            self.text_password.GetValue(),
            self.text_subject_on.GetValue(),
            self.text_payload_on.GetValue(),
            self.text_subject_off.GetValue(),
            self.text_payload_off.GetValue(),
        ]
        if this_id != self.coolid:
            answer = wx.MessageDialog(
                self,
                message=_("This id has changed. Do you want to create a new entry?"),
                caption=_("New Id recognized"),
                style=wx.YES_NO | wx.ICON_QUESTION,
            )
            if answer == wx.ID_YES:
                self.coolid = this_id
                reload_needed = True
        self.entries[self.coolid] = newentry
        self.store_data()
        if reload_needed:
            self.fill_data(False)

    def on_list_select(self, event):
        if self.client.is_connected():
            self.client.disconnect()
        idx = self.list_entries.GetSelection()
        if idx < 0:
            return
        try:
            self.coolid = list(self.entries.keys())[idx]
        except IndexError:
            return
        try:
            entry = self.entries[self.coolid]
        except IndexError:
            return
        self.text_id.SetValue(self.coolid)
        self.text_address.SetValue(entry[0])
        self.text_port.SetValue(entry[1])
        self.text_username.SetValue(entry[2])
        self.text_password.SetValue(entry[3])
        self.text_subject_on.SetValue(entry[4])
        self.text_payload_on.SetValue(entry[5])
        self.text_subject_off.SetValue(entry[6])
        self.text_payload_off.SetValue(entry[7])

    def on_button_okay(self, event):
        self.Close()

    def on_button_add(self, event):
        # Save the current entry
        self.on_button_apply(None)
        if self.coolid is not None:
            newid = self.coolid
            newentry = self.entries[self.coolid]
        else:
            newid = "mqtt-airassist"
            newentry = ["192.168.0.38", "1883", "", "", "cmnd/airassist/POWER", "ON", "cmnd/airassist/POWER", "OFF"]
        newcounter = 0
        while newid in self.entries:
            newcounter += 1
            # Look for the last opening bracket
            if newid.endswith(")"):
                idx1 = newid.find("(")
                idx2 = idx1
                while idx2 >= 0:
                    idx2 = newid.find("(", idx1 + 1)
                    if idx2 > 0:
                        idx1 = idx2
                if idx1 >= 0:
                    newid = newid[:idx1]
            newid += f"({newcounter})"
        try:
            self.entries[newid] = newentry
        except IndexError:
            wx.MessageDialog(self, message=_("Something went wrong!") + f"\nnewid={newid}", caption=_("Error"), style=wx.OK | wx.ICON_ERROR)
            return
        self.store_data()
        self.coolid = newid
        self.fill_data(False)
        self.text_id.SetFocus()

    def on_button_remove(self, event):
        if self.coolid is None:
            return
        try:
            del self.entries[self.coolid]
        except KeyError:
            return
        self.store_data()
        self.coolid = None
        if len(self.entries):
            self.coolid = list(self.entries.keys())[0]
        self.fill_data(False)

    def submenu():
        return "Air-Assist", "MQTT-Interface"
