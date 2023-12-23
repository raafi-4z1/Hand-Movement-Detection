from tkinter import *
from tkinter import filedialog as fd
import test


class Gui_Test(Toplevel):
    def __init__(self, parent, dir_folder={}, p_title="Test"):
        Toplevel.__init__(self, parent)
        self.title(p_title)
        parent.withdraw()
        self.geometry("500x400")
        self.textDir= {}

        if dir_folder.get('yaml') and dir_folder.get('cfg') and dir_folder.get('names'):
            self.dirYaml = dir_folder["yaml"]
            self.dirCfg = dir_folder["cfg"]
            self.dirNames = dir_folder["names"]

            for _, key in enumerate(dir_folder):
               self.textDir[key] =  dir_folder[key][-40:] if (len(dir_folder[key]) > 40) else dir_folder[key]
        else:
            for _, key in enumerate(['yaml', 'cfg', 'names']):
               self.textDir[key] = 'Belum Memilih'

            self.dirYaml = ''
            self.dirCfg = ''
            self.dirNames = ''
        self.dirWeights = []

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

        self.top_frame_yaml = Frame(self.top_frame)
        self.top_frame_yaml.pack(side='top', fill='both', padx=5, pady=5)
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

        self.lab = Label(self.mid_frame_input, width=10,
                         text='Threshold:', anchor='w')
        self.lab.pack(side=LEFT, padx=3)
        self.input_thl = Entry(self.mid_frame_input, width=11)
        self.input_thl.pack(side=LEFT, fill=X)

        self.lab = Label(self.mid_frame_input, width=8,
                         text='IOU T (%):', anchor='w')
        self.lab.pack(side=LEFT)
        self.input_iou_thres = Entry(self.mid_frame_input, width=11)
        self.input_iou_thres.pack(side=LEFT, fill=X, padx=2)
        
        self.input_iou_thres.delete(0, END)
        self.input_iou_thres.insert(0, 60)

        # Label
        self.lbl_pilih_yaml = Label(self.top_frame_yaml, width=33, font=(
            'Times', 12, 'bold'), text=self.textDir['yaml'], anchor='w', bg='white')
        self.lbl_pilih_yaml.pack(side=LEFT, fill=X, padx=3)

        self.lbl_pilih_cfg = Label(self.top_frame_cfg, width=33, font=(
            'Times', 12, 'bold'), text=self.textDir['cfg'], anchor='w', bg='white')
        self.lbl_pilih_cfg.pack(side=LEFT, fill=X, padx=3)

        self.lbl_pilih_names = Label(self.top_frame_names, width=33, font=(
            'Times', 12, 'bold'), text=self.textDir['names'], anchor='w', bg='white')
        self.lbl_pilih_names.pack(side=LEFT, fill=X, padx=3)

        self.lbl_pilih_weights = Label(self.top_frame_weights, width=33, font=(
            'Times', 12, 'bold'), anchor='w', bg='white')
        self.lbl_pilih_weights.pack(side=LEFT, fill=X, padx=3)

        # Button
        self.btn_open_yaml = Button(self.top_frame_yaml, text='Pilih yaml', font=(
            'Times', 12, 'bold'), width=10)
        self.btn_open_yaml.config(command=self.openFileYaml)
        self.btn_open_yaml.pack(side=RIGHT, fill=X, padx=3)

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
        self.btn_kembali.pack(fill=X)

        self.btn_test = Button(self.mid_frame_btn, text='Mulai Test', font=(
            'Times', 12, 'bold'))
        self.btn_test.config(command=self.testBobot)
        self.btn_test.pack(fill=X, pady=5)

        # Create a blank text area.
        self.file_contents = Text(self.bottom_frame)
        self.file_contents.pack(fill=BOTH, expand=True)

    def openFileYaml(self):
        open_file_name = fd.askopenfilename(title="Open File yaml",
            initialdir=self.folder_referen, filetypes=[("yaml", '*.yaml')])

        if open_file_name:
            self.dirYaml = open_file_name
            self.lbl_pilih_yaml.config(
                text=(open_file_name[-40:] if (len(open_file_name) > 40) else open_file_name))

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

    def testBobot(self):
        self.file_contents.delete('1.0', END)
        try:
            if not self.dirYaml:
                raise ValueError("Pilih File yaml")
            if not self.dirCfg:
                raise ValueError("Pilih File cfg")
            if not self.dirNames:
                raise ValueError("Pilih File names")
            if not self.dirWeights:
                raise ValueError("Pilih File bobot")
            if not self.input_thl.get():
                raise ValueError("Isi Threshold")
            if not self.input_iou_thres.get():
                iou_thres = 60
            else:
                iou_thres = self.input_iou_thres.get()

            float(self.input_thl.get())

            if 0 > float(self.input_thl.get()) or float(self.input_thl.get()) > 1:
                raise ValueError(
                    "Threshold bernilai antara 0 sampai 1 (0.5)")

            test.mainTest(
                self.dirYaml,
                self.dirCfg,
                self.dirNames,
                self.dirWeights,
                conf_thres=float(self.input_thl.get()),
                iou_thres=int(iou_thres)
            )

        except Exception as err:
            self.file_contents.insert(END, "Cek input, IOU Threshold harus bernilai integer" if err.args[0].find(
                'invalid') == 0 else err)
