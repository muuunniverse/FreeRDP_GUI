#!/usr/bin/env python3

import base64
import subprocess
import configparser
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
from os import path

freerdp_conn_str = "xfreerdp /cert:ignore /v:"

conf_file = path.expanduser("~") + '/.config/FreeRDP_GUI.conf'

class Table(Gtk.Window):
    def Connect(self, widget, data=None):
        conn_deets = connection_entry.get_text()
        name = login_entry.get_text()
        password = password_entry.get_text()
        if ( data == "conn_init"):
            string = freerdp_conn_str + conn_deets + " /u:" + name + " /p:" + password
            
        if fullscreen_check.get_active():
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
                status_entry_label.set_markup('<b><span color="red">Error: wrong login or password</span></b>');
            else:
                status_entry_label.set_markup('<b><span color="red">Error: check your connection</span></b>');
        print("Error code", rc)

    def DescriptionEnterPressed(self, widget, event):
        if Gdk.keyval_name(event.keyval) == 'Return':
            connection_entry.grab_focus()
            return True
        return False

    def ConnectionEnterPressed(self, widget, event):
        if Gdk.keyval_name(event.keyval) == 'Return':
            login_entry.grab_focus()
            return True
        return False

    def LoginEnterPressed(self, widget, event):
        if Gdk.keyval_name(event.keyval) == 'Return':
            password_entry.grab_focus()
            return True
        return False

    def PasswordEnterPressed(self, widget, event):
        if Gdk.keyval_name(event.keyval) == 'Return':
            profile_entry.grab_focus()
            return True
        return False

    def ProfileAppend(self, widget, btn1, btn2, btn3, btn4, event):
        description = description_entry.get_text()
        conn_deets = connection_entry.get_text()
        name = login_entry.get_text()
        password = password_entry.get_text()
        profilesel = profile_entry.get_text()
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
            return error # review specific
        SaveLogin(description, conn_deets, profilesel, name, password)
        return False

    def load_quicksave(self, widget, slot): #Load profile details to quicksave buttons
        if conf.has_option(slot, "description"):
            quicksave = conf.get(slot, "description")
        else:
            quicksave = f"Empty Profile {slot}"
        return quicksave

    def load_fields(self, widget, prof, descr, conn, nm):
        if prof == "1":
            description_entry.set_text(descr)
            connection_entry.set_text(conn)
            login_entry.set_text(nm)
            if conf.has_option(prof, "fullscreen") == True:
                fullscreen_check.set_active(True)
            else:
                fullscreen_check.set_active(False)
            if conf.has_option(prof, "savepassword") == True:
                password_check.set_active(True)
            else:
                password_check.set_active(False)
            if conf.has_option(prof, "password"):
                password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(conf.get(prof, "password")))).decode('utf-8'))
        elif prof == "2":
            description_entry.set_text(descr)
            connection_entry.set_text(conn)
            login_entry.set_text(nm)
            if conf.has_option(prof, "fullscreen") == True:
                fullscreen_check.set_active(True)
            else:
                fullscreen_check.set_active(False)
            if conf.has_option(prof, "savepassword") == True:
                password_check.set_active(True)
            else:
                password_check.set_active(False)
            if conf.has_option(prof, "password"):
                password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(conf.get(prof, "password")))).decode('utf-8'))
        elif prof == "3":
            description_entry.set_text(descr)
            connection_entry.set_text(conn)
            login_entry.set_text(nm)
            if conf.has_option(prof, "fullscreen") == True:
                fullscreen_check.set_active(True)
            else:
                fullscreen_check.set_active(False)
            if conf.has_option(prof, "savepassword") == True:
                password_check.set_active(True)
            else:
                password_check.set_active(False)
            if conf.has_option(prof, "password"):
                password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(conf.get(prof, "password")))).decode('utf-8'))
        elif prof == "4":
            description_entry.set_text(descr)
            connection_entry.set_text(conn)
            login_entry.set_text(nm)
            if conf.has_option(prof, "fullscreen") == True:
                fullscreen_check.set_active(True)
            else:
                fullscreen_check.set_active(False)
            if conf.has_option(prof, "savepassword") == True:
                password_check.set_active(True)
            else:
                password_check.set_active(False)
            if conf.has_option(prof, "password"):
                password_entry.set_text(base64.b32decode(base64.b16decode(base64.b64decode(conf.get(prof, "password")))).decode('utf-8'))
        else:
            return error # review specific

    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()
        return False

    def __init__(self):
        super().__init__(title="pyGtkRDP")
        self.window = Gtk.Window()
        self.window.set_title("FreeRDP Connection")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(10)
        table = Gtk.Table(n_rows=17, n_columns=4, homogeneous=True)
        self.window.add(table)

        #Connection Details
        description_entry_label = Gtk.Label (label="Connection Description:")
        table.attach(description_entry_label, 0, 4, 0, 1)
        description_entry_label.show()
        description_entry.set_max_length(20)
        table.attach(description_entry, 0, 4, 1, 2)
        description_entry.show()
        description_entry.connect('key-press-event', self.DescriptionEnterPressed)

        connection_entry_label = Gtk.Label (label="IP/ Domain:")
        table.attach(connection_entry_label, 0, 4, 2, 3)
        connection_entry_label.show()
        connection_entry.set_max_length(100)
        table.attach(connection_entry, 0, 4, 3, 4)
        connection_entry.show()
        connection_entry.connect('key-press-event', self.ConnectionEnterPressed)
        
        #Login User
        login_entry_label = Gtk.Label (label="Username:")
        table.attach(login_entry_label, 0, 4, 4, 5)
        login_entry_label.show()
        login_entry.set_max_length(20)
        table.attach(login_entry, 0, 4, 5, 6)
        login_entry.show()
        login_entry.connect('key-press-event', self.LoginEnterPressed)

        #Password Capture
        password_entry_label = Gtk.Label (label="Password:")
        table.attach(password_entry_label, 0, 4, 6, 7)
        password_entry_label.show()
        password_entry.set_max_length(30)
        password_entry.set_visibility(False)
        table.attach(password_entry, 0, 4, 7, 8)
        password_entry.show()
        password_entry.connect('key-press-event', self.PasswordEnterPressed)
        table.attach(status_entry_label, 0, 2, 8, 9)
        status_entry_label.show()

        fullscreen_check.set_tooltip_text("If checked – remote connection will be fullscreen, if no – windowed. Press CTRL+ALT+ENTER to toggle fullscreen.")
        fullscreen_check.set_active(True)
        table.attach(fullscreen_check, 2, 4, 8, 9)
        fullscreen_check.show()

        password_check.set_tooltip_text("If checked – password will be saved in file. It's unsafe feature, please, be careful.")
        password_check.set_active(False)
        table.attach(password_check, 0, 1, 11, 12)
        password_check.show()

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
        profile_entry.set_max_length(30)
        profile_entry.set_visibility(True)
        table.attach(profile_entry, 1, 2, 11, 12)
        profile_entry.show()
        button = Gtk.Button(label="Save to Profile")
        button.connect("clicked", self.ProfileAppend, save_button1, save_button2, save_button3, save_button4, profile_entry.get_text()) #pass variable captured to function to save the data for the connection
        table.attach(button, 2, 4, 11, 12)
        button.show()

        button = Gtk.Button(label="Connect")
        button.connect("clicked", self.Connect, "conn_init")
        table.attach(button, 0, 4, 14, 16)
        button.show()

        button = Gtk.Button(label="Exit")
        button.connect("clicked", lambda w: Gtk.main_quit())
        table.attach(button, 0, 4, 16, 17)
        button.show()

        table.show()
        self.window.show()

def SaveLogin(description, connection, profileselection, login, password):
    if not conf.has_section(profileselection):
        conf.add_section(profileselection) 
    conf.set(profileselection, "description", description)
    conf.set(profileselection, "Address/Domain", connection)
    conf.set(profileselection, "User", login)
    conf.set(profileselection, "fullscreen", fullscreen_check.get_active())
    conf.set(profileselection, "savepassword", password_check.get_active())
    if password_check.get_active():
        password = password.encode()
        password = base64.b64encode(base64.b16encode(
                                  base64.b32encode(password)))
        password = password.decode('utf-8')
        conf.set(profileselection, "password", password)
    else:
        conf.remove_option(profileselection, "password")
    conf.write(open(conf_file, "w"))

def main():
    Gtk.main()
    return 0

description_entry = Gtk.Entry()
profile_entry = Gtk.Entry()
connection_entry = Gtk.Entry()
login_entry = Gtk.Entry()
password_entry = Gtk.Entry()
profile_entry = Gtk.Entry()
status_entry_label = Gtk.Label (label="CTRL+ALT+ENTER - toggle fullscreen")
fullscreen_check = Gtk.CheckButton (label="Fullscreen mode")
password_check = Gtk.CheckButton (label="Save password (unsafe)")

if __name__ == "__main__":
    conf = configparser.RawConfigParser()
    if not path.exists(conf_file):
        open(conf_file, 'w')
    conf.read(conf_file)
    Table()
    main()