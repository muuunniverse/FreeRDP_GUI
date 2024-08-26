#! python3

import base64
import subprocess
import configparser
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from os import path
import os

class Table(Gtk.Window):

    description_entry = Gtk.Entry()
    profile_entry = Gtk.Entry()
    connection_entry = Gtk.Entry()
    login_entry = Gtk.Entry()
    password_entry = Gtk.Entry()
    profile_entry = Gtk.Entry()
    status_entry_label = Gtk.Label (label="CTRL+ALT+ENTER - toggle fullscreen")
    fullscreen_check = Gtk.CheckButton (label="Fullscreen mode")
    password_check = Gtk.CheckButton (label="Save password (unsafe)")

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

        p = subprocess.Popen(string, shell=True, stderr=subprocess.PIPE, )
        streamdata = p.communicate()[0]
        rc = p.returncode
        
        if ( (rc == 0) or (rc == 62)):
            Gtk.main_quit()
        else:
            if (rc == 132):
                self.status_entry_label.set_markup('<b><span color="red">Error: wrong login or password</span></b>');
            else:
                self.status_entry_label.set_markup('<b><span color="red">Error: check your connection</span></b>');
        print("Error code", rc)

    def DescriptionEnterPressed(self, widget, event):
        if Gdk.keyval_name(event.keyval) == 'Return':
            self.connection_entry.grab_focus()
            return True
        return False

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

    def ProfileAppend(self, widget, btn1, btn2, btn3, btn4, event):
        description = self.description_entry.get_text()
        conn_deets = self.connection_entry.get_text()
        name = self.login_entry.get_text()
        password = self.password_entry.get_text()
        profilesel = self.profile_entry.get_text()
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
            return OSError
        self.SaveLogin(description, conn_deets, profilesel, name, password)
        return False

    def load_quicksave(self, widget, slot):
        conf_file = path.expanduser("~") + '/.config/FreeRDP_GUI.conf'
        conf = configparser.RawConfigParser()
        if not path.exists(conf_file):
            open(conf_file, 'w')
        conf.read(conf_file)
        if conf.has_option(slot, "description"):
            quicksave = conf.get(slot, "description")
        else:
            quicksave = f"Empty Profile {slot}"
        return quicksave

    def load_fields(self, widget, prof, descr, conn, nm):
        conf_file = path.expanduser("~") + '/.config/FreeRDP_GUI.conf'
        conf = configparser.RawConfigParser()
        if not path.exists(conf_file):
            open(conf_file, 'w')
        conf.read(conf_file)
        if prof == "1":
            self.description_entry.set_text(descr)
            self.connection_entry.set_text(conn)
            self.login_entry.set_text(nm)
            if conf.has_option(prof, "fullscreen") == True:
                self.fullscreen_check.set_active(True)
            else:
                self.fullscreen_check.set_active(False)
            if conf.has_option(prof, "savepassword") == True:
                self.password_check.set_active(True)
            else:
                self.password_check.set_active(False)
            if conf.has_option(prof, "password"):
                self.password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(conf.get(prof, "password")))).decode('utf-8'))
        elif prof == "2":
            self.description_entry.set_text(descr)
            self.connection_entry.set_text(conn)
            self.login_entry.set_text(nm)
            if conf.has_option(prof, "fullscreen") == True:
                self.fullscreen_check.set_active(True)
            else:
                self.fullscreen_check.set_active(False)
            if conf.has_option(prof, "savepassword") == True:
                self.password_check.set_active(True)
            else:
                self.password_check.set_active(False)
            if conf.has_option(prof, "password"):
                self.password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(conf.get(prof, "password")))).decode('utf-8'))
        elif prof == "3":
            self.description_entry.set_text(descr)
            self.connection_entry.set_text(conn)
            self.login_entry.set_text(nm)
            if conf.has_option(prof, "fullscreen") == True:
                self.fullscreen_check.set_active(True)
            else:
                self.fullscreen_check.set_active(False)
            if conf.has_option(prof, "savepassword") == True:
                self.password_check.set_active(True)
            else:
                self.password_check.set_active(False)
            if conf.has_option(prof, "password"):
                self.password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(conf.get(prof, "password")))).decode('utf-8'))
        elif prof == "4":
            self.description_entry.set_text(descr)
            self.connection_entry.set_text(conn)
            self.login_entry.set_text(nm)
            if conf.has_option(prof, "fullscreen") == True:
                self.fullscreen_check.set_active(True)
            else:
                self.fullscreen_check.set_active(False)
            if conf.has_option(prof, "savepassword") == True:
                self.password_check.set_active(True)
            else:
                self.password_check.set_active(False)
            if conf.has_option(prof, "password"):
                self.password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(conf.get(prof, "password")))).decode('utf-8'))
        else:
            return error
    
    def SaveLogin(self, description, connection, profileselection, login, password):
        conf_file = path.expanduser("~") + '/.config/FreeRDP_GUI.conf'
        conf = configparser.RawConfigParser()
        if not path.exists(conf_file):
            open(conf_file, 'w')
        conf.read(conf_file)
        if not conf.has_section(profileselection):
            conf.add_section(profileselection) 
        conf.set(profileselection, "description", description)
        conf.set(profileselection, "Address/Domain", connection)
        conf.set(profileselection, "User", login)
        conf.set(profileselection, "fullscreen", self.fullscreen_check.get_active())
        conf.set(profileselection, "savepassword", self.password_check.get_active())
        if self.password_check.get_active():
            password = password.encode()
            password = base64.b64encode(base64.b16encode(
                                      base64.b32encode(password)))
            password = password.decode('utf-8')
            conf.set(profileselection, "password", password)
        else:
            conf.remove_option(profileselection, "password")
        conf.write(open(conf_file, "w"))

    def __init__(self):
        super().__init__(title="pyGtkRDP")
        self.window = Gtk.Window()
        self.window.set_title("FreeRDP Connection")
        self.window.set_border_width(10)
        table = Gtk.Table(n_rows=17, n_columns=4, homogeneous=True)
        self.window.add(table)

        def Destroy(self, obj):
            Gtk.main_quit()
        
        conf_file = path.expanduser("~") + '/.config/FreeRDP_GUI.conf'
        conf = configparser.RawConfigParser()
        if not path.exists(conf_file):
            open(conf_file, 'w')
        conf.read(conf_file)

        self.description_entry = Gtk.Entry()
        self.profile_entry = Gtk.Entry()
        self.connection_entry = Gtk.Entry()
        self.login_entry = Gtk.Entry()
        self.password_entry = Gtk.Entry()
        self.profile_entry = Gtk.Entry()
        self.status_entry_label = Gtk.Label (label="CTRL+ALT+ENTER - toggle fullscreen")
        self.fullscreen_check = Gtk.CheckButton (label="Fullscreen mode")
        self.password_check = Gtk.CheckButton (label="Save password (unsafe)")

        #Connection Details
        description_entry_label = Gtk.Label (label="Connection Description:")
        table.attach(description_entry_label, 0, 4, 0, 1)
        description_entry_label.show()
        self.description_entry.set_max_length(40)
        table.attach(self.description_entry, 0, 4, 1, 2)
        self.description_entry.show()
        self.description_entry.connect('key-press-event', self.DescriptionEnterPressed)

        connection_entry_label = Gtk.Label (label="IP/ Domain:")
        table.attach(connection_entry_label, 0, 4, 2, 3)
        connection_entry_label.show()
        self.connection_entry.set_max_length(100)
        table.attach(self.connection_entry, 0, 4, 3, 4)
        self.connection_entry.show()
        self.connection_entry.connect('key-press-event', self.ConnectionEnterPressed)
        
        #Login User
        login_entry_label = Gtk.Label (label="Username:")
        table.attach(login_entry_label, 0, 4, 4, 5)
        login_entry_label.show()
        self.login_entry.set_max_length(30)
        table.attach(self.login_entry, 0, 4, 5, 6)
        self.login_entry.show()
        self.login_entry.connect('key-press-event', self.LoginEnterPressed)

        #Password Capture
        password_entry_label = Gtk.Label (label="Password:")
        table.attach(password_entry_label, 0, 4, 6, 7)
        password_entry_label.show()
        self.password_entry.set_max_length(30)
        self.password_entry.set_visibility(False)
        table.attach(self.password_entry, 0, 4, 7, 8)
        self.password_entry.show()
        self.password_entry.connect('key-press-event', self.PasswordEnterPressed)
        table.attach(self.status_entry_label, 0, 2, 8, 9)
        self.status_entry_label.show()

        self.fullscreen_check.set_tooltip_text("If checked – remote connection will be fullscreen, if no – windowed. Press CTRL+ALT+ENTER to toggle fullscreen.")
        self.fullscreen_check.set_active(True)
        table.attach(self.fullscreen_check, 2, 4, 8, 9)
        self.fullscreen_check.show()

        self.password_check.set_tooltip_text("If checked – password will be saved in file. It's unsafe feature, please, be careful.")
        self.password_check.set_active(False)
        table.attach(self.password_check, 0, 1, 11, 12)
        self.password_check.show()

        save_button1 = Gtk.Button(label=f"{self.load_quicksave(self, "1")}")
        save_button1.set_tooltip_text(f"This is your first saved connection")
        prof = "1"
        if conf.has_option("1", "description"):
            description = conf.get("1", "description")
            conn_deets = conf.get("1", "Address/Domain")
            name = conf.get("1", "User")
        else:
            description = ""
            conn_deets = ""
            name = ""
        save_button1.connect("clicked", self.load_fields, prof, description, conn_deets, name)
        table.attach(save_button1, 0, 2, 12, 13)
        save_button1.show()

        save_button2 = Gtk.Button(label=f"{self.load_quicksave(self, "2")}")
        save_button2.set_tooltip_text(f"This is your second saved connection")
        prof = "2"
        if conf.has_option("2", "description"):
            description = conf.get("2", "description")
            conn_deets = conf.get("2", "Address/Domain")
            name = conf.get("2", "User")
        else:
            description = ""
            conn_deets = ""
            name = ""
        save_button2.connect("clicked", self.load_fields, prof, description, conn_deets, name)
        table.attach(save_button2, 2, 4, 12, 13)
        save_button2.show()
        
        save_button3= Gtk.Button(label=f"{self.load_quicksave(self, "3")}")
        save_button3.set_tooltip_text(f"This is your third saved connection")
        prof = "3"
        if conf.has_option("3", "description"):
            description = conf.get("3", "description")
            conn_deets = conf.get("3", "Address/Domain")
            name = conf.get("3", "User")
            prof = "3"
        else:
            description = ""
            conn_deets = ""
            name = ""
        save_button3.connect("clicked", self.load_fields, prof, description, conn_deets, name)
        table.attach(save_button3, 0, 2, 13, 14)
        save_button3.show()

        save_button4 = Gtk.Button(label=f"{self.load_quicksave(self, "4")}")
        save_button4.set_tooltip_text(f"This is your fourth saved connection")
        prof = "4"
        if conf.has_option("4", "description"):
            description = conf.get("4", "description")
            conn_deets = conf.get("4", "Address/Domain")
            name = conf.get("4", "User")
        else:
            description = ""
            conn_deets = ""
            name = ""
        save_button4.connect("clicked", self.load_fields, prof, description, conn_deets, name)
        table.attach(save_button4, 2, 4, 13, 14)
        save_button4.show()

        #Save Information to Profile
        self.profile_entry.set_max_length(30)
        self.profile_entry.set_visibility(True)
        table.attach(self.profile_entry, 1, 2, 11, 12)
        self.profile_entry.show()
        button = Gtk.Button(label="Save to Profile")
        button.connect("clicked", self.ProfileAppend, save_button1, save_button2, save_button3, save_button4, self.profile_entry.get_text()) #pass variable captured to function to save the data for the connection
        table.attach(button, 2, 4, 11, 12)
        button.show()

        button = Gtk.Button(label="Connect")
        button.connect("clicked", self.Connect, "conn_init")
        table.attach(button, 0, 4, 14, 16)
        button.show()

        table.show()
        self.window.show()

def main():
    Table()
    Gtk.main()
    return 0

if __name__ == "__main__":
    main()