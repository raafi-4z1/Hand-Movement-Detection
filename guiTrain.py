from tkinter import *
from tkinter import filedialog as fd
import train


class Gui_Train(Toplevel):
    def __init__(self, parent, dir_folder={}, p_title="Train"):
        Toplevel.__init__(self, parent)
        self.title(p_title)
        parent.withdraw()
        self.geometry("500x400")
        self.textDir = {}

        if dir_folder.get('yaml') and dir_folder.get('cfg'):
            self.dirYaml = dir_folder["yaml"]
            self.dirCfg = dir_folder["cfg"]

            for _, key in enumerate(dir_folder):
               self.textDir[key] =  dir_folder[key][-40:] if (len(dir_folder[key]) > 40) else dir_folder[key]
        else:
            for _, key in enumerate(['yaml', 'cfg']):
               self.textDir[key] = 'Belum Memilih'

            self.dirYaml = ''
            self.dirCfg = ''
        self.dirWeights = ''

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
        self.top_frame_weights = Frame(self.top_frame)
        self.top_frame_weights.pack(fill='both', padx=5, pady=5)

        self.mid_frame_input = Frame(self.mid_frame)
        self.mid_frame_input.pack(side='top', fill='both', padx=5, pady=5)
        self.mid_frame_btn = Frame(self.mid_frame)
        self.mid_frame_btn.pack(fill='both', padx=5, pady=5)

        self.lab = Label(self.mid_frame_input, width=11,
                         text='Learning Rate:', anchor='w')
        self.lab.pack(side=LEFT, padx=3)
        self.input_lr = Entry(self.mid_frame_input, width=11)
        self.input_lr.pack(side=LEFT, fill=X)

        self.lab = Label(self.mid_frame_input, width=7,
                         text='Epochs:', anchor='w')
        self.lab.pack(side=LEFT)
        self.input_epochs = Entry(self.mid_frame_input, width=11)
        self.input_epochs.pack(side=LEFT, fill=X, padx=2)

        # Label
        self.lbl_pilih_yaml = Label(self.top_frame_yaml, width=33, font=(
            'Times', 12, 'bold'), text=self.textDir['yaml'], anchor='w', bg='white')
        self.lbl_pilih_yaml.pack(side=LEFT, fill=X, padx=3)

        self.lbl_pilih_cfg = Label(self.top_frame_cfg, width=33, font=(
            'Times', 12, 'bold'), text=self.textDir['cfg'], anchor='w', bg='white')
        self.lbl_pilih_cfg.pack(side=LEFT, fill=X, padx=3)

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

        self.btn_open_weights = Button(self.top_frame_weights, text='Pilih bobot', font=(
            'Times', 12, 'bold'), width=10)
        self.btn_open_weights.config(command=self.openFileWeights)
        self.btn_open_weights.pack(side=RIGHT, fill=X, padx=3)

        self.btn_kembali = Button(self.mid_frame_btn, text='Kembali', font=(
            'Times', 12, 'bold'))
        self.btn_kembali.config(command=lambda: self.destroy())
        self.btn_kembali.pack(fill=X)

        self.btn_train = Button(self.mid_frame_btn, text='Mulai Train', font=(
            'Times', 12, 'bold'))
        self.btn_train.config(command=self.testBobot)
        self.btn_train.pack(fill=X, pady=5)

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
            if not self.input_lr.get():
                raise ValueError("Isi learning rate")
            if not self.input_epochs.get():
                raise ValueError("Isi Epochs")

            float(self.input_lr.get())
            int(self.input_epochs.get())

            if 0 > float(self.input_lr.get()) or float(self.input_lr.get()) > 1:
                raise ValueError(
                    "learning rate harus bernilai antara 0 sampai 1 (0.5)")

            train.mainTrain(
                self.dirYaml,
                self.dirCfg,
                self.dirWeights,
                float(self.input_lr.get()),
                epochs=int(self.input_epochs.get())
            )

        except Exception as err:
            self.file_contents.insert(END, "Cek input, epochs harus bernilai integer" if err.args[0].find(
                'invalid') == 0 else err)