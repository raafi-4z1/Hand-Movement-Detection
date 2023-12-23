from tkinter import *
from tkinter import filedialog as fd
import detect

class Gui_Deteksi(Toplevel):
    def __init__(self, parent, dir_folder={}, p_title="Deteksi"):
        Toplevel.__init__(self, parent)
        self.title(p_title)
        parent.withdraw()
        self.geometry("500x400")
        self.textDir = {}

        if dir_folder.get('cfg') and dir_folder.get('names'):
            self.dirCfg = dir_folder["cfg"]
            self.dirNames = dir_folder["names"]

            for _, key in enumerate(dir_folder):
               self.textDir[key] =  dir_folder[key][-40:] if (len(dir_folder[key]) > 40) else dir_folder[key]
        else:
            for _, key in enumerate(['cfg', 'names']):
               self.textDir[key] = 'Belum Memilih'

            self.dirCfg = ''
            self.dirNames = ''
        self.dirSource = ''
        self.dirWeights = []

        self.view_image = IntVar()
        self.folder_referen = "D:\\Program"
        self.aturKomponen()

        # self.transient(parent)
        self.grab_set()
        self.wait_window()

    def aturKomponen(self):
        # Membagi Frame
        self.top_frame = Frame(self)
        self.top_frame.pack(side='top', pady=5)
        self.mid_frame = Frame(self)
        self.mid_frame.pack(padx=5, pady=5)
        self.bottom_frame = Frame(self)
        self.bottom_frame.pack(padx=15, pady=5)

        self.top_frame_source = Frame(self.top_frame)
        self.top_frame_source.pack(side='top', fill='both', padx=5, pady=5)
        self.top_frame_cfg = Frame(self.top_frame)
        self.top_frame_cfg.pack(fill='both', padx=5, pady=5)
        self.top_frame_names = Frame(self.top_frame)
        self.top_frame_names.pack(fill='both', padx=5, pady=5)
        self.top_frame_weights = Frame(self.top_frame)
        self.top_frame_weights.pack(fill='both', padx=5, pady=5)

        self.mid_frame_input = Frame(self.mid_frame)
        self.mid_frame_input.pack(side='top', fill='both', padx=5, pady=5)
        self.mid_frame_btn = Frame(self.mid_frame)
        self.mid_frame_btn.pack(fill='both', padx=5, pady=5)

        # Checkbutton
        Checkbutton(self.mid_frame_input, text='Tampilkan Hasil,', variable=self.view_image, onvalue=1, offvalue=0).pack(side=LEFT, fill=X)

        # Input/Entry Label
        Label(self.mid_frame_input, width=11,
              text='Threshold (%):', anchor='w').pack(side=LEFT, padx=3)
        self.input_thl = Entry(self.mid_frame_input, width=11)
        self.input_thl.pack(side=LEFT, fill=X)

        # Label
        self.lbl_pilih_source = Label(self.top_frame_source, width=33, font=(
            'Times', 12, 'bold'), text='Belum Memilih', anchor='w', bg='white')
        self.lbl_pilih_source.pack(side=LEFT, fill=X, padx=3)

        self.lbl_pilih_cfg = Label(self.top_frame_cfg, width=33, font=(
            'Times', 12, 'bold'), text=self.textDir['cfg'], anchor='w', bg='white')
        self.lbl_pilih_cfg.pack(side=LEFT, fill=X, padx=3)

        self.lbl_pilih_names = Label(self.top_frame_names, width=33, font=(
            'Times', 12, 'bold'), text=self.textDir['names'], anchor='w', bg='white')
        self.lbl_pilih_names.pack(side=LEFT, fill=X, padx=3)

        self.lbl_pilih_weights = Label(self.top_frame_weights, width=33, font=(
            'Times', 12, 'bold'), text='Belum Memilih', anchor='w', bg='white')
        self.lbl_pilih_weights.pack(side=LEFT, fill=X, padx=3)

        # Button
        self.btn_open_source = Button(self.top_frame_source, text='File', font=(
            'Times', 12, 'bold'), width=3)
        self.btn_open_source.config(command=self.openFileSource)
        self.btn_open_source.pack(side=RIGHT, fill=X, padx=2)

        self.btn_open_source = Button(self.top_frame_source, text='Camera', font=(
            'Times', 12, 'bold'), width=6)
        self.btn_open_source.config(
            command=lambda: self.setVideo("0"))
        self.btn_open_source.pack(side=RIGHT, fill=X)

        self.btn_open_cfg = Button(self.top_frame_cfg, text='Pilih cfg', font=(
            'Times', 12, 'bold'), width=10)
        self.btn_open_cfg.config(command=self.openFileCfg)
        self.btn_open_cfg.pack(side=RIGHT, fill=X, padx=3)

        self.btn_open_names = Button(self.top_frame_names, text='Pilih names', font=(
            'Times', 12, 'bold'), width=10)
        self.btn_open_names.config(command=self.openFileNames)
        self.btn_open_names.pack(side=RIGHT, fill=X, padx=3)

        self.btn_open_weights = Button(self.top_frame_weights, text='Pilih bobot', font=(
            'Times', 12, 'bold'), width=10)
        self.btn_open_weights.config(command=self.openFileWeights)
        self.btn_open_weights.pack(side=RIGHT, fill=X, padx=3)

        self.btn_kembali = Button(self.mid_frame_btn, text='Kembali', font=(
            'Times', 12, 'bold'))
        self.btn_kembali.config(command=lambda: self.destroy())
        self.btn_kembali.pack(fill=X, pady=2)

        self.btn_deteksi = Button(self.mid_frame_btn, text='Mulai Deteksi', font=(
            'Times', 12, 'bold'))
        self.btn_deteksi.config(command=self.funDeteksi)
        self.btn_deteksi.pack(fill=X, pady=3)

        # Create a blank text area.
        self.file_contents = Text(self.bottom_frame)
        self.file_contents.pack(fill=BOTH, expand=True)

    def openFileSource(self):
        open_file_name = fd.askopenfilename(title="Open File Untuk Deteksi",
            initialdir="D:\\Program", filetypes=[("Video", '*.mp4'), ("Video", '*.avi'), ("Gambar", '*.jpg'), ("Gambar", '*.png')])

        if open_file_name:
            self.dirSource = open_file_name
            self.lbl_pilih_source.config(
                text=(open_file_name[-40:] if (len(open_file_name) > 40) else open_file_name))

    def setVideo(self, inp):
        self.lbl_pilih_source.config(text=inp)
        self.dirSource = inp

    def openFileCfg(self):
        open_file_name = fd.askopenfilename(title="Open File cfg",
            initialdir=self.folder_referen, filetypes=[("cfg", '*.cfg')])

        if open_file_name:
            self.dirCfg = open_file_name
            self.lbl_pilih_cfg.config(
                text=(open_file_name[-40:] if (len(open_file_name) > 40) else open_file_name))

    def openFileNames(self):
        open_file_name = fd.askopenfilename(title="Open File names",
            initialdir=self.folder_referen, filetypes=[("names", '*.names')])

        if open_file_name:
            self.dirNames = open_file_name
            self.lbl_pilih_names.config(
                text=(open_file_name[-40:] if (len(open_file_name) > 40) else open_file_name))

    def openFileWeights(self):
        open_file_name = fd.askopenfilenames(title="Open File Bobot atau weight",
            initialdir=self.folder_referen, filetypes=[("Bobot", '*.weights'), ("Bobot", '*.pt')])

        if open_file_name:
            self.dirWeights = []
            text = ''

            for dir in open_file_name:
                self.dirWeights.append(dir)

                if len(open_file_name) == 1:
                    text = (dir[-40:] + '  ' if (len(dir) > 40)
                            else dir + '  ')
                else:
                    text += dir.replace('/', ' ').split()[-1] + ', '
            self.lbl_pilih_weights.config(text=text[:-2])

    def funDeteksi(self):
        self.file_contents.delete('1.0', END)
        #size_img = 0

        try:
            if not self.dirSource:
                raise ValueError("Pilih File source")
            if not self.dirCfg:
                raise ValueError("Pilih File cfg")
            if not self.dirNames:
                raise ValueError("Pilih File names")
            if not self.dirWeights:
                raise ValueError("Pilih File bobot")
            if not self.input_thl.get():
                raise ValueError("Isi Threshold")

            int(self.input_thl.get())

            dtc = detect.Deteksi(
                self,
                "Deteksi",
                self.dirSource,
                self.dirCfg,
                self.dirNames,
                self.dirWeights,
                int(self.input_thl.get()),
                view_image=bool(self.view_image.get())
            )

        except Exception as err:
            self.file_contents.insert(END, "Cek input, Threshold harus bernilai integer" if err.args[0].find(
                'invalid') == 0 else err)