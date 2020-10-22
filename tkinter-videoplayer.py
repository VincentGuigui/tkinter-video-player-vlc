"""A very simple example for VLC python bindings using tkinter.
Requires Python 3.4 or later.
Author: Vincent Guigui
Based on: https://git.videolan.org/?p=vlc/bindings/python.git;a=blob_plain;f=examples/tkvlc.py;hb=HEAD
    by Patrick Fay 
Date: 08/09/2020

Description:
Here is a short sample on how to use VLC video player on Python with tKinter.
It should work on Windows, Linux, MacOS

In this sample:
- the same video is played independently on 2 different Tkinter canvas
- each video has a video transform filter applied: 90° or 270° rotation
- one of the video is muted
- one of the video has an inverted color filter

"""
import tkinter as tk
from PIL import Image, ImageTk
import vlc
import platform

class VideoPlayer:  
    def start_video(self, canvas, video_path, angle, mute, invert):
        self.isMacOS   = platform.system().lower().startswith('darwin')
        self.isWindows = platform.system().lower().startswith('win')
        self.isLinux   = platform.system().lower().startswith('linux')
        self.canvas = canvas

        if self.isMacOS:
            from ctypes import c_void_p, cdll
            # libtk = cdll.LoadLibrary(ctypes.util.find_library('tk'))
            # returns the tk library /usr/lib/libtk.dylib from macOS,
            # but we need the tkX.Y library bundled with Python 3+,
            # to match the version number of tkinter, _tkinter, etc.
            try:
                libtk = 'libtk%s.dylib' % (Tk.TkVersion,)
                prefix = getattr(sys, 'base_prefix', sys.prefix)
                libtk = joined(prefix, 'lib', libtk)
                dylib = cdll.LoadLibrary(libtk)
                # getNSView = dylib.TkMacOSXDrawableView is the
                # proper function to call, but that is non-public
                # (in Tk source file macosx/TkMacOSXSubwindows.c)
                # and dylib.TkMacOSXGetRootControl happens to call
                # dylib.TkMacOSXDrawableView and return the NSView
                _GetNSView = dylib.TkMacOSXGetRootControl
                # C signature: void *_GetNSView(void *drawable) to get
                # the Cocoa/Obj-C NSWindow.contentView attribute, the
                # drawable NSView object of the (drawable) NSWindow
                _GetNSView.restype = c_void_p
                _GetNSView.argtypes = c_void_p,
                del dylib

            except (NameError, OSError):  # image or symbol not found
                def _GetNSView(unused):
                    return None

        print(f'Starting VLC on Mac:{self.isMacOS} Windows:{self.isWindows} Linux:{self.isLinux}')

        # VLC player options
        if invert:
            args = [f'--video-filter=transform{{type={angle}}}:invert']
        else:
            args = [f'--video-filter=transform{{type={angle}}}']
        if mute:
            args.append('--noaudio')
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
        # set_mute will mute all VLC instance
        #   self.player.audio_set_mute(mute)
        # it is better/more efficient to disable the audio track (see Instance constructor)
        self.player.play()

root = tk.Tk()
canvas1 = tk.Canvas(root, width=500, height=500)
canvas1.pack(side=tk.LEFT)
canvas2 = tk.Canvas(root, width=500, height=500)
canvas2.pack(side=tk.LEFT)
player = VideoPlayer()
# Audio, 90° rotation, inverted color
player.start_video(canvas1, 'sample.mp4', 90, False, True)
# No Audio, 270°/-90° rotation, normal color
player.start_video(canvas2, 'sample.mp4', 270, True, False)
root.mainloop()