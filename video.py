from tkinter import *
from tkinter import filedialog
import cv2
import PIL.Image
import PIL.ImageTk
import time


class App_Video(Toplevel):
    def __init__(self, parent, p_title="Video", video_source=0):
        Toplevel.__init__(self, parent)
        self.title(p_title)
        parent.withdraw()

        self.parent = parent
        self.parent.openfile = False # keadaan untuk membuka video dari frame ini

        self.aturKomponen()
        self.settingVideo(video_source)
        self.resizable(False, False)
        # self.transient(parent) # membuat frame parent tidak bisa tutup, dan tidak bisa menggunakan withdraw
        self.grab_set()
        self.wait_window()

    def aturKomponen(self):
        # membagi frame
        self.left_frame = Frame(self, bg='gray')
        self.left_frame.pack(side='left', fill='both', padx=5, pady=5)
        self.right_frame = Frame(self)
        self.right_frame.pack(side='right', fill='both', padx=5, pady=5)

        # Button
        self.btn_open = Button(self.left_frame, text="Open", font=(
            'Times', 12, 'bold'), width=20, command=self.funOpen)
        self.btn_open.pack(padx=3, pady=4)

        self.btn_pp = Button(self.left_frame, text="Pause/Play", font=(
            'Times', 12, 'bold'), width=20, command=self.funPP)
        self.btn_pp.pack(padx=3, pady=4)

        self.btn_stop = Button(self.left_frame, text="Stop", font=(
            'Times', 12, 'bold'), width=20, command=lambda: self.destroy())
        self.btn_stop.pack(padx=3, pady=4)

    def settingVideo(self, video_source):
        # open video source (by default this will try to open the computer webcam)
        self.pp = False  # pause(True)/play(False) video
        self.vid = MyVideoCapture(video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = Canvas( 
            self.right_frame, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10
        self.update()

    def update(self):
        if self.pp:
            self.after(800, self.update)  # 3000 ~= 3 detik
        else:
            # Get a frame from the video source
            ret, frame = self.vid.get_frame()
            # print(frame)

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(
                    image=PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
                self.after(self.delay, self.update)
            else:
                self.destroy()

    def funOpen(self):
        self.pp = True
        self.file_video = filedialog.askopenfilename(initialdir="D:\\Program", filetypes=[
                                                     ("MP4", '*.mp4'), ("AVI", '*.avi')])
        if self.file_video:
            self.parent.openfile = True
            self.parent.file_video = self.file_video
            self.destroy()
            # self.canvas.forget()  # destroy?menghapus canvas sebelumnya
            # self.settingVideo(self.file_video)
        else:
            self.pp = False

    def funPP(self):
        if self.pp:
            self.pp = False
        else:
            self.pp = True


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        # self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # 720p: 1280x720
        # 480p: 854x480
        self.width = 854
        self.height = 480

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.resize(frame, (self.width, self.height))
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)