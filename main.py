from tkinter import *
from tkinter import filedialog
import foto
import video
import setDataset
import guiTrain
import guiTest
import guiDeteksi


class WindowUtama:
    def __init__(self, parent, title):
        self.parent = parent
        # print("self.parent: {}, self: {}, parent: {}, title: {} ".format(self.parent, self, parent, title))

        self.parent.geometry("500x400")
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.onTutup)
        self.parent.resizable(False, False)

        self.dir_folder = dict(yaml='', cfg='', names='')
        self.aturKomponen()

    def aturKomponen(self):
        mainFrame = Frame(self.parent, bd=10)
        mainFrame.pack(fill=BOTH, expand=YES, padx=5)

        # label window Utama
        # Label(mainFrame, text="WINDOW UTAMA").pack(expand=YES)

        # komponen atas
        topFrame = Frame(mainFrame)
        topFrame.pack(fill=X, pady=8)
        Label(topFrame, text=f"{'-'*38} Buka File {'-'*38}", font=(
            'Times', 14, 'bold')).pack(expand=YES, side=TOP, pady=4)

        btn_video = Button(topFrame, text='Buka File Video', font=(
            'Times', 12, 'bold'))
        btn_video.config(command=self.bukaVideo)
        btn_video.pack(side=LEFT, padx=3, expand=YES, fill=X)

        btn_foto = Button(topFrame, text='Buka File Gambar', font=(
            'Times', 12, 'bold'))
        btn_foto.config(command=self.bukaFoto)
        btn_foto.pack(side=LEFT, padx=3, expand=YES, fill=X)

        # komponen tengah
        midFrame = Frame(mainFrame)
        midFrame.pack(fill=X, pady=8)
        Label(midFrame, text=f"{'-'*37} Konfigurasi {'-'*37}", font=(
            'Times', 14, 'bold')).pack(expand=YES, side=TOP, pady=4)

        btn_dataset = Button(midFrame, text='Pilih Dataset', font=(
            'Times', 12, 'bold'))
        btn_dataset.config(command=self.pilihDataset)
        btn_dataset.pack(side=BOTTOM, padx=3, expand=YES, fill=X)

        # komponen bawah
        bottomFrame = Frame(mainFrame)
        bottomFrame.pack(fill=X, pady=8)
        Label(bottomFrame, text=f"{'-'*37} YOLO versi 4 {'-'*37}", font=(
            'Times', 14, 'bold')).pack(expand=YES, side=TOP, pady=4)

        btn_train = Button(bottomFrame, text='Train Dataset', font=(
            'Times', 12, 'bold'))
        btn_train.config(command=self.trainData)
        btn_train.pack(side=LEFT, padx=3, expand=YES, fill=X)

        btn_test = Button(bottomFrame, text='Test Bobot', font=(
            'Times', 12, 'bold'))
        btn_test.config(command=self.testBobot)
        btn_test.pack(side=LEFT, padx=3, expand=YES, fill=X)

        btn_deteksi = Button(bottomFrame, text='Deteksi', font=(
            'Times', 12, 'bold'))
        btn_deteksi.config(command=self.funDeteksi)
        btn_deteksi.pack(side=RIGHT, padx=3, expand=YES, fill=X)

        # buat menu
        menuBar = Menu(self.parent)

        menuUtama = Menu(menuBar, tearoff=1)
        menuUtama.add_command(label="Keluar", command=self.onTutup)
        menuBar.add_cascade(label="Menu", menu=menuUtama)

        self.parent.config(menu=menuBar)

    def bukaVideo(self, event=None):
        self.file_video = filedialog.askopenfilename(title="Open File Video", initialdir="D:\\Program", filetypes=[("MP4", '*.mp4'), ("AVI", '*.avi')])
        while True:
            if self.file_video:
                app_video = video.App_Video(
                    self.parent, "Video", self.file_video)
                if self.parent.openfile == False:
                    self.parent.deiconify()
                    break
                else:
                    self.file_video = self.parent.file_video
            else:
                break

    def bukaFoto(self, event=None):
        self.file_foto = filedialog.askopenfilenames(title="Open File Foto atau Gambar", initialdir="D:\\Program", filetypes=[("Gambar", '*.png'), ("Gambar", '*.jpeg'), ("Gambar", '*.jpg')])

        if self.file_foto:
            app_foto = foto.App_Foto(self.parent, "Foto", self.file_foto)
            self.parent.deiconify()

    def pilihDataset(self, event=None):
        app_dataset = setDataset.Set_Dataset(self.parent, "Setting Dataset")
        self.parent.deiconify()

        self.dir_folder["yaml"] = self.parent.df_yaml
        self.dir_folder["cfg"] = self.parent.df_cfg
        self.dir_folder["names"] = self.parent.df_names

    def trainData(self, event=None):
        app_data = guiTrain.Gui_Train(self.parent, dir_folder=self.dir_folder, p_title="Train")
        self.parent.deiconify()

    def testBobot(self, event=None):
        app_test = guiTest.Gui_Test(self.parent, dir_folder=self.dir_folder, p_title="Test")
        self.parent.deiconify()

    def funDeteksi(self, event=None):
        app_deteksi = guiDeteksi.Gui_Deteksi(self.parent, dir_folder=self.dir_folder, p_title="Deteksi")
        self.parent.deiconify()

    def onTutup(self, event=None):
        self.parent.destroy()


if __name__ == '__main__':
    root = Tk()

    app = WindowUtama(root, "Tugas Akhir (YOLOv4)")

    root.mainloop()
