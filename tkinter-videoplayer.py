"""A very simple example for VLC python bindings using tkinter.
Requires Python 3.4 or later.
Author: Vincent Guigui
Based on: https://git.videolan.org/?p=vlc/bindings/python.git;a=blob_plain;f=examples/tkvlc.py;hb=HEAD
    by Patrick Fay 
Date: 08/09/2020
"""
import tkinter as tk
from PIL import Image, ImageTk
import vlc
import platform

class VideoPlayer:  
    def start_video(self, canvas, video_path, angle):
        self.isMacOS   = platform.system().lower().startswith('darwin')
        self.isWindows = platform.system().lower().startswith('win')
        self.isLinux   = platform.system().lower().startswith('linux')
        self.canvas = canvas

        print(f'Starting VLC on Mac:{self.isMacOS} Windows:{self.isWindows} Linux:{self.isLinux}')

        # VLC player options
        args = [f'--video-filter=transform{{type={angle}}}']
        if self.isLinux:
            args.append('--no-xlib')
        self.Instance = vlc.Instance(args)
        self.player = self.Instance.media_player_new()

        m = self.Instance.media_new(str(video_path))  # Path, unicode
        self.player.set_media(m)

        # set the window id where to render VLC's video output
        h = self.canvas.winfo_id()
        if self.isWindows:
            self.player.set_hwnd(h)
        elif self.isMacOS:
            v = _GetNSView(h)
            if v:
                self.player.set_nsobject(v)
            else:
                self.player.set_xwindow(h)  # plays audio, no video
        else:
            self.player.set_xwindow(h) 
        self.player.play()
        
root = tk.Tk()
canvas1 = tk.Canvas(root, width=500, height=500)
canvas1.pack(side=tk.LEFT)
canvas2 = tk.Canvas(root, width=500, height=500)
canvas2.pack(side=tk.LEFT)
player = VideoPlayer()
player.start_video(canvas1, '../../media/60 seconds to understand artificial intelligence.mp4', 90)
player.start_video(canvas2, '../../media/60 seconds to understand artificial intelligence.mp4', 270)
root.mainloop()