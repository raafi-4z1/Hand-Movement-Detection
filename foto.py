# https://elektrocode2018.wordpress.com/2019/11/23/menampilkan-gambar-pada-tkinter-window-menggunakan-python-opencv/
from tkinter import *
from tkinter import filedialog
import cv2
import PIL.Image
import PIL.ImageTk


class App_Foto(Toplevel):
    def __init__(self, parent, p_title, image_path=["FhnNHwkUoAAWZxI.jpg"]):
        Toplevel.__init__(self, parent)
        self.title(p_title)
        parent.withdraw()

        self.aturKomponen()
        self.cv_img = []
        self.settingGambar(image_path)

        # self.transient(parent) # membuat frame parent tidak bisa tutup, dan tidak bisa menggunakan withdraw
        self.grab_set()
        self.wait_window()

    def aturKomponen(self):
        # Membagi Frame
        self.left_frame = Frame(self, bg='gray')
        self.left_frame.pack(side='left', fill='both', padx=5, pady=5)
        self.right_frame = Frame(self)
        self.right_frame.pack(side='right', fill='both', padx=5, pady=5)

        # Button
        self.btn_open = Button(self.left_frame, text="Open", font=(
            'Times', 12, 'bold'), width=20, command=self.funOpen)
        self.btn_open.pack(side=TOP, padx=3, pady=4)

        self.btn_next = Button(self.left_frame, text="Next", font=(
            'Times', 12, 'bold'), width=20, command=self.funNext)
        self.btn_next.pack(padx=3, pady=4)

        self.btn_preview = Button(self.left_frame, text="Preview", font=(
            'Times', 12, 'bold'), width=20, command=self.funPreview)
        self.btn_preview.pack(padx=3, pady=4)

        self.btn_stop = Button(self.left_frame, text="Stop", font=(
            'Times', 12, 'bold'), width=20, command=lambda: self.destroy())
        self.btn_stop.pack(padx=3, pady=4)

    def settingGambar(self, image_path):
        # Load an image using OpenCV
        for item in image_path:
            self.cv_img.append(cv2.cvtColor(
                cv2.imread(item), cv2.COLOR_BGR2RGB))

        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        # self.height, self.width, no_channels = self.cv_img.shape
        self.width = 640
        self.height = 640
        dim = (self.width, self.height)
        # print(image_path)
        # print(self.cv_img[0].shape[0] > 200 and self.cv_img[0].shape[1] > 200)

        # jumlah array dan indek untuk ganti-ganti gambar
        self.len_imgs = len(self.cv_img)
        self.index_img = 0

        # resize image
        for i in range(self.len_imgs):
            self.cv_img[i] = cv2.resize(
                self.cv_img[i], dim, interpolation=cv2.INTER_AREA)

        # Create a canvas that can fit the above image
        self.canvas = Canvas(
            self.right_frame, width=self.width, height=self.height)
        self.canvas.pack()

        self.ndarrayPhotoImage()

    def funOpen(self):
        image_path = filedialog.askopenfilenames(initialdir="D:\\Program", filetypes=[
            ("PNG", '*.png'), ("JPEG", '*.jpeg'), ("JPEG", '*.jpg')])
        if image_path:
            self.canvas.destroy()  # menghapus canvas sebelumnya
            self.settingGambar(image_path)

    def funNext(self):
        if self.len_imgs == 1:
            pass
        elif (self.index_img+1 == self.len_imgs):
            self.index_img = 0
            self.ndarrayPhotoImage()
        else:
            self.index_img += 1
            self.ndarrayPhotoImage(self.index_img)

    def funPreview(self):
        if self.len_imgs == 1:
            pass
        elif self.index_img == 0:
            self.index_img = self.len_imgs - 1
            self.ndarrayPhotoImage(self.index_img)
        else:
            self.index_img -= 1
            self.ndarrayPhotoImage(self.index_img)

    def ndarrayPhotoImage(self, i=0):
        print("i= {}, self.len_imgs= {}, self.index_img= {}".format(
            i, self.len_imgs, self.index_img))
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(self.cv_img[i]))

        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
