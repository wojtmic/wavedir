import gi
import os
import json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject 

fm_path = os.path.expanduser("~")
show_hidden = True

def decide_icon(path):
    """Determine appropriate icon name for file/folder"""
    if os.path.isdir(path):
        # Check for .directory file
        directory_file = os.path.join(path, ".directory")
        if os.path.exists(directory_file):
            try:
                with open(directory_file, 'r') as f:
                    for line in f:
                        if line.startswith("Icon="):
                            return line.split("=")[1].strip()
            except:
                pass
        return "folder"
    
    # Handle regular files
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    
    # Common file type mappings
    with open("icon_map.json", "r") as f:
        icon_map = json.load(f)
    
    return icon_map.get(ext, "text-x-generic")

def gen_file_widget(path):
    global fm_path
    name = os.path.basename(path)

    item = Gtk.FlowBoxChild()
    button = Gtk.Button()
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    button.add(box)

    icon = Gtk.Image.new_from_icon_name(decide_icon(path), Gtk.IconSize.DIALOG)
    label = Gtk.Label(label=name)

    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)

    if os.path.isdir(path):
        def on_click(button):
            global fm_path
            fm_path = path
            list_path(path)
            button.get_toplevel().queue_draw()  # Refresh window
        button.connect("clicked", on_click)
    else:
        def on_click(button):
            try:
                quoted_path = f"'{path}'"  # Handle paths with spaces
                os.system(f"xdg-open {quoted_path}")
            except Exception as e:
                print(f"Error opening file: {e}")
        button.connect("clicked", on_click)

    item.add(button)
    return item

def list_path(path):
    global show_hidden
    print(f"Listing path: {path}")
    for child in fileview1.get_children():
        fileview1.remove(child)

    files = os.listdir(path)
    hidden_dirs = []
    dirs = []
    hidden_files = []
    files_list = []

    for item in files:
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            if item.startswith('.'):
                hidden_dirs.append(item)
            else:
                dirs.append(item)
        else:
            if item.startswith('.'):
                hidden_files.append(item)
            else:
                files_list.append(item)

    if not show_hidden:
        hidden_dirs = []
        hidden_files = []
    
    hidden_dirs.sort()
    dirs.sort()
    hidden_files.sort()
    files_list.sort()

    files = hidden_dirs + dirs + hidden_files + files_list

    for item in files:
        fileview1.add(gen_file_widget(os.path.join(path, item)))
    
    path_entry.set_text(path)

    if fm_path == "/":
        builder.get_object("BackButton").set_sensitive(False)
    else:
        builder.get_object("BackButton").set_sensitive(True)

    window.show_all()
    window.set_title(f"WaveDir - {path.replace(os.path.expanduser('~'), '~')}")

class Handler:
    def on_window_destroy(self, *args):
        Gtk.main_quit()
    def path_change(self, _=None):
        if os.path.exists(path_entry.get_text()):
            fm_path = path_entry.get_text()
            list_path(fm_path)
        else:
            list_path(fm_path)
    def go_back(self, _=None):
        global fm_path
        parent_path = os.path.dirname(fm_path)
        print(f"Going back to {parent_path}")
        if os.path.exists(parent_path):
            fm_path = parent_path
            list_path(fm_path)

builder = Gtk.Builder()
builder.add_from_file("ui/main.glade")
builder.connect_signals(Handler())

fileview1 = builder.get_object("View1")

path_entry = builder.get_object("PathEntry")

window = builder.get_object("Window")

list_path(fm_path)

window.show_all()
Gtk.main()