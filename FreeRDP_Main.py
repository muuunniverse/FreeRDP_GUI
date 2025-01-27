#! python3

import base64
import subprocess
import configparser
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, Gdk
from os import path
import os

image_file = "FreeRDP-image.png"
css_file = "style.css"
current_dir = os.path.dirname(os.path.abspath(__file__))

def find_file(start_dir, target_file):
    for root, dirs, files in os.walk(start_dir):
        #print(root, dirs, files) Testing
        if target_file in files:
            #print(os.path.join(root, target_file))
            return os.path.join(root, target_file)
    return None

css_path = find_file(current_dir, css_file)
icon_path = find_file(current_dir, image_file)

class FreeRDP_Connect(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='com.example.Gtk4Example', flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = FreeRDP_GUI_Window(application=self)
        win.present()

### Here is where we differentiate the Window from the Application for conversion to Gtk 4.0

class FreeRDP_GUI_Window(Gtk.ApplicationWindow):
    def __init__(self, application=None):
        super().__init__(application=application)

        self.conf_file = path.expanduser("~") + '/.config/FreeRDP_GUI.conf'
        self.conf = configparser.RawConfigParser()
        if not path.exists(self.conf_file):
            open(self.conf_file, 'w')
        self.conf.read(self.conf_file)
        #Create Dictionary Reference
        self.config = configparser.ConfigParser()
        self.config.read(self.conf_file)
        self.config_dict = {section: dict(self.config.items(section)) for section in self.config.sections()}
        #print(config_dict) Testing

        self.set_title("FreeRDP")
        self.set_default_size(430, 450)
        self.set_css_classes(["window"])

        # Load the CSS file
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(css_path)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.grid = Gtk.Grid()
        num_rows = 35
        num_columns = 35
        for i in range(num_rows):
            self.grid.insert_row(i)  
        for j in range(num_columns):
            self.grid.insert_column(j)
        self.set_child(self.grid)

        self.description_entry = Gtk.Entry()
        self.profile_entry = Gtk.Entry()
        self.connection_entry = Gtk.Entry()
        self.login_entry = Gtk.Entry()
        self.password_entry = Gtk.Entry()
        self.profile_entry = Gtk.Entry()
        self.fullscreen_check = Gtk.CheckButton (label="Fullscreen mode")
        self.fullscreen_check.set_css_classes(["label"])
        self.password_check = Gtk.CheckButton (label="Save password (unsafe)")
        self.password_check.set_css_classes(["label"])

        # Load an icon file (e.g., "icon.png")
        image_path = Gio.File.new_for_path(icon_path)
        if not image_path:
            print("Icon path not found.")
            return
        # Create a Gtk.Image widget
        image_widget = Gtk.Image()
        try:
            # Load the icon file into the image widget
            image_widget.set_from_file(image_path.get_path())
        except Exception as e:
            print(f"Error loading icon: {e}")
            return
        # Add the image to the grid (e.g., at position 0, 0)
        self.grid.attach(image_widget, 30, 6, 14, 14)

        #Row 1
        empty_row_label = Gtk.Label()
        empty_row_label.set_visible(True)
        self.grid.attach(empty_row_label, 0, 0, 3, 1)

        #Row2
        #Connection Details
        description_entry_label = Gtk.Label (label="Connection Description:")
        description_entry_label.set_css_classes(["label"])
        self.grid.attach(description_entry_label, 3, 1, 6, 1)
        self.description_entry.set_max_length(40)
        self.description_entry.set_css_classes(["button"])
        self.grid.attach(self.description_entry, 10, 1, 35, 1)
        self.description_entry_trig = Gtk.EventControllerKey()
        self.description_entry_trig.connect('key-pressed', self.DescriptionEnterPressed)

        #Row 3
        connection_entry_label = Gtk.Label (label="IP/ Domain:")
        connection_entry_label.set_css_classes(["label"])
        self.grid.attach(connection_entry_label, 3, 2, 6, 1)
        self.connection_entry.set_max_length(100)
        self.connection_entry.set_css_classes(["button"])
        self.grid.attach(self.connection_entry, 10, 2, 35, 1)
        self.connection_entry_trig = Gtk.EventControllerKey()
        self.connection_entry_trig.connect('key-pressed', self.ConnectionEnterPressed)
        
        #Row 4
        #Login User
        login_entry_label = Gtk.Label (label="Username:")
        login_entry_label.set_css_classes(["label"])
        self.grid.attach(login_entry_label, 3, 3, 6, 1)
        self.login_entry.set_max_length(30)
        self.login_entry.set_css_classes(["button"])
        self.grid.attach(self.login_entry, 10, 3, 35, 1)
        self.login_entry_trig = Gtk.EventControllerKey()
        self.login_entry_trig.connect('key-pressed', self.LoginEnterPressed)

        #Row 5
        #Password Capture
        password_entry_label = Gtk.Label (label="Password:")
        password_entry_label.set_css_classes(["label"])
        self.grid.attach(password_entry_label, 3, 4, 6, 1)
        self.password_entry.set_max_length(30)
        self.password_entry.set_visibility(False)
        self.password_entry.set_css_classes(["button"])
        self.grid.attach(self.password_entry, 10, 4, 35, 1)
        self.password_entry_trig = Gtk.EventControllerKey()
        self.password_entry_trig.connect('key-pressed', self.PasswordEnterPressed)

        #Row 6
        #Status Label
        self.status_entry_label = Gtk.Label()
        self.status_entry_label.set_visible(True)
        self.grid.attach(self.status_entry_label, 0, 5, 35, 1)

        #Row 7
        self.fullscreen_check.set_active(True)
        self.grid.attach(self.fullscreen_check, 2, 6, 6, 1)
        self.password_check.set_tooltip_text("If checked – password will be saved in file. It's unsafe feature, please, be careful.")
        self.password_check.set_active(False)
        self.grid.attach(self.password_check, 8, 6, 30, 1)

        #Row 8
        empty_row_label = Gtk.Label()
        empty_row_label.set_visible(True)
        self.grid.attach(empty_row_label, 0, 7, 4, 1)

        #Row 10
        empty_row_label = Gtk.Label()
        empty_row_label.set_visible(True)
        self.grid.attach(empty_row_label, 0, 9, 4, 1)

        #Row 11
        self.save_label = Gtk.Label(label="(Slots 1-4 Quicksave/ >5 Drop Menu Slots)", halign=Gtk.Align.CENTER, margin_start=10, margin_end=10)
        self.save_label.set_visible(True)
        self.save_label.set_css_classes(["subtext"])
        self.grid.attach(self.save_label, 0, 10, 30, 1)

        #Row 12
        empty_row_label = Gtk.Label()
        empty_row_label.set_visible(True)
        self.grid.attach(empty_row_label, 0, 11, 4, 1)

        #Row 13
        save_button1 = Gtk.Button(label=f"{self.load_quicksave(self, "1")}", halign=Gtk.Align.CENTER, margin_start=10, margin_end=10)
        save_button1.set_tooltip_text(f"This is your first saved connection")
        prof = "1"
        if self.conf.has_option("1", "description"):
            description = self.conf.get("1", "description")
            conn_deets = self.conf.get("1", "Address/Domain")
            name = self.conf.get("1", "User")
        else:
            description = ""
            conn_deets = ""
            name = ""
        save_button1.connect("clicked", self.load_fields, prof, description, conn_deets, name)
        save_button1.set_css_classes(["button"])
        self.grid.attach(save_button1, 0, 12, 10, 1)

        save_button2 = Gtk.Button(label=f"{self.load_quicksave(self, "2")}", halign=Gtk.Align.CENTER, margin_start=10, margin_end=10)
        save_button2.set_tooltip_text(f"This is your second saved connection")
        prof = "2"
        if self.conf.has_option("2", "description"):
            description = self.conf.get("2", "description")
            conn_deets = self.conf.get("2", "Address/Domain")
            name = self.conf.get("2", "User")
        else:
            description = ""
            conn_deets = ""
            name = ""
        save_button2.connect("clicked", self.load_fields, prof, description, conn_deets, name)
        save_button2.set_css_classes(["button"])
        self.grid.attach(save_button2, 10, 12, 20, 1)

        #Row 14
        empty_row_label = Gtk.Label()
        empty_row_label.set_visible(True)
        self.grid.attach(empty_row_label, 0, 13, 1, 1)

        #Row 15
        save_button3= Gtk.Button(label=f"{self.load_quicksave(self, "3")}", halign=Gtk.Align.CENTER, margin_start=10, margin_end=10)
        save_button3.set_tooltip_text(f"This is your third saved connection")
        prof = "3"
        if self.conf.has_option("3", "description"):
            description = self.conf.get("3", "description")
            conn_deets = self.conf.get("3", "Address/Domain")
            name = self.conf.get("3", "User")
            prof = "3"
        else:
            description = ""
            conn_deets = ""
            name = ""
        save_button3.connect("clicked", self.load_fields, prof, description, conn_deets, name)
        save_button3.set_css_classes(["button"])
        self.grid.attach(save_button3, 0, 14, 10, 1)

        save_button4 = Gtk.Button(label=f"{self.load_quicksave(self, "4")}", halign=Gtk.Align.CENTER, margin_start=10, margin_end=10)
        save_button4.set_tooltip_text(f"This is your fourth saved connection")
        prof = "4"
        if self.conf.has_option("4", "description"):
            description = self.conf.get("4", "description")
            conn_deets = self.conf.get("4", "Address/Domain")
            name = self.conf.get("4", "User")
        else:
            description = ""
            conn_deets = ""
            name = ""
        save_button4.connect("clicked", self.load_fields, prof, description, conn_deets, name)
        save_button4.set_css_classes(["button"])
        self.grid.attach(save_button4, 10, 14, 20, 1)

        #Row 9
        #Save Information to Profile
        self.profile_entry.set_max_length(10)
        self.profile_entry.set_visibility(True)
        self.profile_entry.set_css_classes(["button"])
        self.grid.attach(self.profile_entry, 15, 8, 15, 1)
        save_button = Gtk.Button(label="Save")
        save_button.connect("clicked", self.ProfileAppend, save_button1, save_button2, save_button3, save_button4, self.profile_entry.get_text()) #pass variable captured to function to save the data for the connection
        save_button.set_css_classes(["button"])
        self.grid.attach(save_button, 5, 8, 6, 1)

        #Row 16
        empty_row_label = Gtk.Label()
        empty_row_label.set_visible(True)
        self.grid.attach(empty_row_label, 1, 15, 12, 1)

        #Row 17
        self.combobox_label = Gtk.Label(label="Or Select Other Below:", halign=Gtk.Align.CENTER, margin_start=10, margin_end=10)
        self.combobox_label.set_css_classes(["label"])
        self.combobox_label.set_visible(True)
        self.grid.attach(self.combobox_label, 1, 16, 40, 1)

        #Row 18
        self.combo_box_text = Gtk.ComboBoxText()
        for key in self.config_dict.keys():
            value = self.config_dict[key]
            self.combo_box_text.append(key, value['description'])
        self.combo_box_text.connect("changed", self.on_combo_changed)
        self.grid.attach(self.combo_box_text, 0, 17, 45, 1)

        #Row 19
        empty_row_label = Gtk.Label()
        empty_row_label.set_visible(True)
        self.grid.attach(empty_row_label, 1, 18, 12, 1)

        #Row 20
        connect_button = Gtk.Button(label="Connect", halign=Gtk.Align.CENTER, margin_start=10, margin_end=10)
        connect_button.connect("clicked", self.Connect, "conn_init")
        connect_button.set_css_classes(["crit_button"])
        self.grid.attach(connect_button, 1, 19, 35, 1)

        #Row 21
        login_entry_label = Gtk.Label (label="Adrian Wallace (2025) v0.2", halign=Gtk.Align.END)
        login_entry_label.set_css_classes(["subtest"])
        self.grid.attach(login_entry_label, 1, 20, 45, 1)

    def on_combo_changed(self, widget):
        active = widget.get_active()
        active_mod =int(widget.get_active() + 1) #Key Selection is offset - May be because of file format - validation??
        if active_mod:
            combo_desc = self.config_dict[str(active_mod)]['description']
            combo_addr = self.config_dict[str(active_mod)]['address/domain']
            combo_login = self.config_dict[str(active_mod)]['user']
            combo_pass = self.config_dict[str(active_mod)]['password']
            self.description_entry.set_text(combo_desc)
            self.connection_entry.set_text(combo_addr)
            self.login_entry.set_text(combo_login)
            if self.config_dict[str(active_mod)]['savepassword'] == 'True':
                self.password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(combo_pass))).decode('utf-8'))
        
    def check_freerdp_version(self):
        commands = ['xfreerdp', 'xfreerdp3']
        for cmd in commands:
            try:
                subprocess.check_output(['which', cmd], shell=False)
                return cmd  # Return the existing command name
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        return None

    def Connect(self, widget, data=None):
        freerdp_version = self.check_freerdp_version()
        freerdp_conn_str = f"{freerdp_version} /cert:ignore /v:"
        conn_deets = self.connection_entry.get_text()
        name = self.login_entry.get_text()
        password = self.password_entry.get_text()
        if ( data == "conn_init"):
            string = freerdp_conn_str + conn_deets + " /u:" + name + " /p:" + password
            
        if self.fullscreen_check.get_active():
            string += " /f"
        else:
            string += " /w:1920 /h:1080"
        #print(string) #Testing Security Risk

        p = subprocess.Popen(string, shell=True, stderr=subprocess.PIPE, )
        streamdata = p.communicate()[0]
        rc = p.returncode
        
        if ( (rc == 0) or (rc == 62)):
            Gtk.main_quit()
        else:
            if (rc == 132):
                self.status_entry_label.set_markup('<b><span color="red">Error: wrong login or password</span></b>');
            else:
                markup_text=f"<b><span color='red'>Error {rc}: check your connection</span></b>"
                self.status_entry_label.set_markup(markup_text);
        print("Error code", rc)

    def ConnectionEnterPressed(self, widget, event):
        if Gdk.keyval_name(event.keyval) == 'Return':
            self.login_entry.grab_focus()
            return True
        return False

    def LoginEnterPressed(self, widget, event):
        if Gdk.keyval_name(event.keyval) == 'Return':
            self.password_entry.grab_focus()
            return True
        return False

    def PasswordEnterPressed(self, widget, event):
        if Gdk.keyval_name(event.keyval) == 'Return':
            self.profile_entry.grab_focus()
            return True
        return False

    def SaveLogin(self, widget, description, connection, profileselection, login, password):
        print(description, connection, profileselection, login, password)
        self.conf_file = path.expanduser("~") + '/.config/FreeRDP_GUI.conf'
        self.conf = configparser.RawConfigParser()
        if not path.exists(self.conf_file):
            open(self.conf_file, 'w')
        self.conf.read(self.conf_file)
        if not self.conf.has_section(profileselection):
            self.conf.add_section(profileselection) 
        self.conf.set(profileselection, "description", description)
        self.conf.set(profileselection, "Address/Domain", connection)
        self.conf.set(profileselection, "User", login)
        self.conf.set(profileselection, "fullscreen", self.fullscreen_check.get_active())
        self.conf.set(profileselection, "savepassword", self.password_check.get_active())
        if self.password_check.get_active():
            password = password.encode()
            password = base64.b64encode(base64.b16encode(
                                    base64.b32encode(password)))
            password = password.decode('utf-8')
            self.conf.set(profileselection, "password", password)
        else:
            self.conf.remove_option(profileselection, "password")
        self.conf.write(open(self.conf_file, "w"))

    def ProfileAppend(self, widget, btn1, btn2, btn3, btn4, event):
        description = self.description_entry.get_text()
        conn_deets = self.connection_entry.get_text()
        name = self.login_entry.get_text()
        password = self.password_entry.get_text()
        profilesel = self.profile_entry.get_text()
        print(description, conn_deets, name, password, profilesel) #testing profile numbers - Worked
        if profilesel == "1":
            btn1.get_child()
            btn1.set_label(description)
            btn1.set_sensitive(False)
        elif profilesel == "2":
            btn2.get_child()
            btn2.set_label(description)
            btn2.set_sensitive(False)
        elif profilesel == "3":
            btn3.get_child()
            btn3.set_label(description)
            btn3.set_sensitive(False)
        elif profilesel == "4":
            btn4.get_child()
            btn4.set_label(description)
            btn4.set_sensitive(False)
        else:
            #return OSError #stopping progression if profile is not 1-4? Verified
            pass
        self.SaveLogin(self, description, conn_deets, profilesel, name, password)
        return False

    def load_quicksave(self, widget, slot):
        self.conf_file = path.expanduser("~") + '/.config/FreeRDP_GUI.conf'
        self.conf = configparser.RawConfigParser()
        if not path.exists(self.conf_file):
            open(self.conf_file, 'w')
        self.conf.read(self.conf_file)
        if self.conf.has_option(slot, "description"):
            quicksave = self.conf.get(slot, "description")
        else:
            quicksave = f"Empty Profile {slot}"
        return quicksave

    def load_fields(self, widget, prof, descr, conn, nm):
        self.conf_file = path.expanduser("~") + '/.config/FreeRDP_GUI.conf'
        self.conf = configparser.RawConfigParser()
        if not path.exists(self.conf_file):
            open(self.conf_file, 'w')
        self.conf.read(self.conf_file)
        if prof == "1":
            self.description_entry.set_text(descr)
            self.connection_entry.set_text(conn)
            self.login_entry.set_text(nm)
            if self.conf.has_option(prof, "fullscreen") == True:
                self.fullscreen_check.set_active(True)
            else:
                self.fullscreen_check.set_active(False)
            if self.conf.has_option(prof, "savepassword") == True:
                self.password_check.set_active(True)
            else:
                self.password_check.set_active(False)
            if self.conf.has_option(prof, "password"):
                self.password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(self.conf.get(prof, "password")))).decode('utf-8'))
        elif prof == "2":
            self.description_entry.set_text(descr)
            self.connection_entry.set_text(conn)
            self.login_entry.set_text(nm)
            if self.conf.has_option(prof, "fullscreen") == True:
                self.fullscreen_check.set_active(True)
            else:
                self.fullscreen_check.set_active(False)
            if self.conf.has_option(prof, "savepassword") == True:
                self.password_check.set_active(True)
            else:
                self.password_check.set_active(False)
            if self.conf.has_option(prof, "password"):
                self.password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(self.conf.get(prof, "password")))).decode('utf-8'))
        elif prof == "3":
            self.description_entry.set_text(descr)
            self.connection_entry.set_text(conn)
            self.login_entry.set_text(nm)
            if self.conf.has_option(prof, "fullscreen") == True:
                self.fullscreen_check.set_active(True)
            else:
                self.fullscreen_check.set_active(False)
            if self.conf.has_option(prof, "savepassword") == True:
                self.password_check.set_active(True)
            else:
                self.password_check.set_active(False)
            if self.conf.has_option(prof, "password"):
                self.password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(self.conf.get(prof, "password")))).decode('utf-8'))
        elif prof == "4":
            self.description_entry.set_text(descr)
            self.connection_entry.set_text(conn)
            self.login_entry.set_text(nm)
            if self.conf.has_option(prof, "fullscreen") == True:
                self.fullscreen_check.set_active(True)
            else:
                self.fullscreen_check.set_active(False)
            if self.conf.has_option(prof, "savepassword") == True:
                self.password_check.set_active(True)
            else:
                self.password_check.set_active(False)
            if self.conf.has_option(prof, "password"):
                self.password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(self.conf.get(prof, "password")))).decode('utf-8'))
        else:
            return error

    def DescriptionEnterPressed(self, widget, event):
        if Gdk.keyval_name(event.keyval) == 'Return':
            self.connection_entry.grab_focus()
            return True
        return False

    def Destroy(self, obj):
        Gtk.main_quit()

def main():
    app = FreeRDP_Connect()
    
    def on_activate(app):
        win = FreeRDP_GUI_Window(application=app)
        win.present()
    
    return app.run(None)

if __name__ == "__main__":
    main()