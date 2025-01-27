# FreeRDP_GUI
A FreeRDP GUI for linux distributions PyGTK4 based

# Overview

A simple FreeRDP GUI that allows for connection to four pre-configured presets or add connections to a drop down box

Main testing platform is Arch-based distributions however being PyGTK4 based it should be somewhat cross-platform compatible.

Steps:
1. Enter Connection Data - You can progress straight to connect if you don't want to save to a profile
2. Select Profile (1-4 for Quicksave), or other values for drop down list.
3. Hit Save Profile (This will lock the file)
4. Hit Connect

## Resolution

Default resolution is set to 1920x1080 however with the fullscreen box ticked it will adjust to the current screen resolution

## Save

Insecure Save function

## Work in Progress

I'm continuing to work on this as a fun side project. Looking at testing launching multiple concurrent connections, better error codes, full and correct unified packaging and deployment with a PKGBUILD for AUR. Looking to add encryption for saved passwords.

## Updates

v0.2

- Removed Icon (You can drag the desktop connection directly to the taskbar in KDE anyway)
- Major code refactoring to meet GTK 4
- Overall Major tidy-up
- style.css added to give the App a unique look. 
