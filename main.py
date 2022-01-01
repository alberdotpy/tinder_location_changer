## Python 3.8
## by alber.py

import sys, os
import wx
from db import insert_into_table
from session import TinderBot

baseFolder = os.path.dirname(os.path.abspath('__file__'))


class Robot(wx.Frame):
    def __init__(self, parent, title):
        super(Robot, self).__init__(parent, title=title, size=(700, 450))
        self.init_ui()
        self.Centre()
        self.SetTitle("Tinder Location Changer")
        self.Maximize(False)
        try:
            icon = wx.EmptyIcon()
            icon.CopyFromBitmap(wx.Bitmap("img\\logo.ico", wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)
        except Exception as e:
            print("The favicon was not found, please save the favicon in the img directory as icon.png")

    def init_ui(self):
        nb = wx.Notebook(self)
        nb.AddPage(Panel1(nb), "Location Changer")
        self.Show(True)


class Panel1(wx.Panel):
    def __init__(self, parent):

        super(Panel1, self).__init__(parent)
        sizer = wx.GridBagSizer(5, 5)

        # Header
        try:
            imageFile = "img\\logo.png"
            png = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            png = scale_bitmap(png, 80, 80)
            logo = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
            sizer.Add(logo, pos=(0, 0), span=(3, 6), flag=wx.BOTTOM | wx.ALIGN_CENTER | wx.TOP, border=10)
        except Exception as e:
            print("The logo file was not found, please save the logo file in the img directory as logo.png")
            print(e)

        # Logo

        # Prices & Promotions
        lbl_city = wx.StaticText(self, label="City", style=wx.ALIGN_LEFT)
        sizer.Add(lbl_city, pos=(3, 0), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        lbl_lat = wx.StaticText(self, label="Latitude", style=wx.ALIGN_LEFT)
        sizer.Add(lbl_lat, pos=(3, 1), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        lbl_lon = wx.StaticText(self, label="Longitude", style=wx.ALIGN_LEFT)
        sizer.Add(lbl_lon, pos=(3, 2), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)

        btn_add = wx.Button(self, label="Add Location")
        sizer.Add(btn_add, pos=(4, 3), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)
        self.Bind(wx.EVT_BUTTON, self.onAdd, btn_add)
        self.city_to_add = wx.TextCtrl(self, value="Paris")
        sizer.Add(self.city_to_add, pos=(4, 0), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)
        self.lat_to_add = wx.TextCtrl(self, value="48.8874318")
        sizer.Add(self.lat_to_add, pos=(4, 1), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)
        self.lon_to_add = wx.TextCtrl(self, value="2.2875198")
        sizer.Add(self.lon_to_add, pos=(4, 2), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)

        line = wx.StaticLine(self)
        sizer.Add(line, pos=(5, 0), span=(1, 6), flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        lbl_select_loc = wx.StaticText(self, label="Selected location : ", style=wx.ALIGN_LEFT)
        sizer.Add(lbl_select_loc, pos=(6, 0), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        self.selected_location = wx.TextCtrl(self, value="Buenos Aires")
        sizer.Add(self.selected_location, pos=(6, 1), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)
        btn_gen = wx.Button(self, label="Launch")
        sizer.Add(btn_gen, pos=(6, 2), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)
        self.Bind(wx.EVT_BUTTON, self.onLaunch, btn_gen)

        # Result Box
        lbl_rbox = wx.StaticText(self, label="Logs :")
        sizer.Add(lbl_rbox, pos=(7, 0), flag=wx.LEFT | wx.ALIGN_LEFT, border=15)
        self.ResultBox = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        sizer.Add(self.ResultBox, pos=(8, 0), span=(3, 6), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)

        # Footer
        titre = wx.StaticText(self, label="© 2022 - alber.py")
        font = wx.Font(7, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        titre.SetFont(font)
        sizer.Add(titre, pos=(12, 0), span=(1, 6), flag=wx.BOTTOM | wx.ALIGN_CENTER | wx.TOP, border=5)

        # Sizer
        sizer.AddGrowableCol(5, 0)
        sizer.AddGrowableRow(9, 0)
        self.SetSizer(sizer)
        sizer.Fit(self)
        sys.stdout = self.ResultBox

    def onAdd(self, event):
        try:
            insert_into_table(table="locations", dict_location={"location": self.city_to_add.GetValue(),
                                                                "longitude": self.lon_to_add.GetValue(),
                                                                "latitude": self.lat_to_add.GetValue()}
                              )
        except Exception as e:
            print("[-] An error has occurred :(")
            print("Please, see the details below: ")
            print(e)
            raise
        print(f"[+] Location {self.city_to_add.GetValue()} successfully.")
        print()

    def onLaunch(self, event):
        print(f"[+] Starting session...")
        try:
            tindersession = TinderBot(location=self.selected_location.GetValue())
            tindersession.start()
        except Exception as e:
            print("[-] An error has occurred :(")
            print("Please, see the details below: ")
            print(e)
            raise
        print(f"[+] Sleeping 99 999 seconds...")


def main():
    app = wx.App()
    Robot(None, 'Robot').Show()
    app.MainLoop()


def scale_bitmap(bitmap, width, height):
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.BitmapFromImage(image)
    return result


if __name__ == '__main__':
    main()