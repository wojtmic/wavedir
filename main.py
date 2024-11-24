import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject 

path = os.path.expanduser("~")

def gen_file_widget(name):
    item = Gtk.FlowBoxChild()
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    item.add(box)
    icon = Gtk.Image.new_from_icon_name("document-open", Gtk.IconSize.DIALOG)
    label = Gtk.Label(name)
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)

    item.set_hexpand(False)
    item.set_vexpand(False)
    item.set_valign(Gtk.Align.START)

    item.set_margin_bottom(0)
    item.set_margin_top(0)

    return item

class Handler:
    def on_window_destroy(self, *args):
        Gtk.main_quit()
    def path_change(self):
        pass

builder = Gtk.Builder()
builder.add_from_file("ui/main.glade")
builder.connect_signals(Handler())

fileview1 = builder.get_object("View1")

for i in range(10):
    fileview1.add(gen_file_widget("File %d" % i))

window = builder.get_object("Window")
window.show_all()
Gtk.main()