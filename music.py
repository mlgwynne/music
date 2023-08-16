import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from pygame import mixer

mixer.init()
import eyed3

UI_FILE = "music.ui"


class Run(Gtk.ApplicationWindow):
    def __init__(self):
        self.f = "0"
        self.mfile = "0"
        self.load = "0"
        self.foo = "0"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window")
        self.window.set_resizable(False)

        self.window.show_all()
        self.menub = self.builder.get_object("menub")

        self.window.connect("destroy", Gtk.main_quit)
        self.playimg = self.builder.get_object("playimg")
        self.play = self.builder.get_object("play")
        self.pauseimg = self.builder.get_object("pauseimg")
        self.header = self.builder.get_object("header")
        self.prog = self.builder.get_object("prog")

        if mixer.music.get_busy():
            print("test")

    def aboutbutton_clicked_cb(self, button):
        self.about = self.builder.get_object("about")
        self.about.show_all()

    def aboutok_clicked_cb(self, button):
        self.about.hide()

    def play_clicked_cb(self, button):

        if self.mfile == "0":
            print("*does nothing*")
        else:
            if mixer.music.get_busy() == True:
                mixer.music.pause()
                self.play.set_image(self.playimg)
            else:
                if self.load == "1":
                    mixer.music.unpause()
                    self.play.set_image(self.pauseimg)
                else:
                    print("not test")
                    self.play.set_image(self.pauseimg)
                    print(self.mfile)
                    mixer.music.load(self.mfile)
                    mixer.music.play()
                    print(mixer.music.get_busy())
                    self.load = "1"

    def rewind_clicked_cb(self, button):
        mixer.music.set_pos(0)
        print("rewind")

    def file_clicked_cb(self, dialog):
        if self.mfile == "0":
            print("*file dialog opens*")
        else:
            self.play.set_image(self.playimg)
            mixer.music.pause()

        self.dialog = self.builder.get_object("filedialog")
        self.dialog.show_all()
        if self.f == "0":
            self.add_filters(self.dialog)
            self.f = "1"

    def cancel_clicked_cb(self, button):
        self.dialog.hide()

    def add_filters(self, dialog):
        filter_music_all = Gtk.FileFilter()
        filter_music_all.set_name("All Supported Files (mp3, flac, ogg...)")
        filter_music_all.add_mime_type("audio/mpeg")
        filter_music_all.add_mime_type("audio/flac")
        filter_music_all.add_mime_type("audio/ogg")
        dialog.add_filter(filter_music_all)
        filter_music_mpeg = Gtk.FileFilter()
        filter_music_mpeg.set_name("mpeg (mp3, mp2...)")
        filter_music_mpeg.add_mime_type("audio/mpeg")
        dialog.add_filter(filter_music_mpeg)
        filter_music_flac = Gtk.FileFilter()
        filter_music_flac.set_name("flac")
        filter_music_flac.add_mime_type("audio/flac")
        dialog.add_filter(filter_music_flac)
        filter_music_ogg = Gtk.FileFilter()
        filter_music_ogg.set_name("ogg")
        filter_music_ogg.add_mime_type("audio/ogg")
        dialog.add_filter(filter_music_ogg)

    def choose_clicked_cb(self, widget):
        print("File selected: " + self.dialog.get_filename())
        self.mfile = self.dialog.get_filename()
        self.dialog.hide()
        self.load = "0"
        self.audio = eyed3.load(self.mfile)
        try:
            self.window.set_title(self.audio.tag.title)
        except AttributeError:
            self.window.set_title("Unknown Song Name")

        try:
            self.header.set_subtitle(self.audio.tag.artist)
        except AttributeError:
            self.header.set_subtitle("Unknown Artist")


def main():
    app = Run()
    Gtk.main()


if __name__ == "__main__":
    main()
