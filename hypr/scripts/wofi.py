#!/usr/bin/env python3

import gi
import os
import json
import re

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def resolveIconPath(iconName):
    iconTheme = Gtk.IconTheme.get_default()
    iconFile = iconTheme.lookup_icon(iconName.lower(), 32, 0)
    if iconFile:
        return iconFile.get_filename()
    else:
        return ""

def mapWindow(w):
    w["class"] = w["class"].replace(" ", "_").title()
    return "img:%s:text:%s"%(resolveIconPath(w["class"]), "%s - %s (%s)"%(w["workspace"]["id"], w["class"], w["title"][0:30]))
    # return "img:%s:text:%s"%(resolveIconPath(w["class"]), w["class"])

windows = json.loads(os.popen("hyprctl -j clients").read())
filtered_windows = list(filter(lambda w: w["workspace"]["id"] != -1, windows))
mapped_windows = list(map(mapWindow, filtered_windows))

print(mapped_windows)

selected_window = os.popen("echo \"%s\" | wofi -I -S dmenu"%("\n".join(mapped_windows))).read()

print("selected_window: %s"%(selected_window))

if (selected_window):
    match = re.search(r"\((\w+)\)$", selected_window)
    addr = match.group(1).split("_")[0]
    os.system("hyprctl dispatch focuswindow address:%s"%(addr))
else:
    print("no selected_window")