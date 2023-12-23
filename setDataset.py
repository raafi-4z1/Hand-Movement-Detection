from tkinter import *
from tkinter import filedialog as fd
import os
import cv2


class Set_Dataset(Toplevel):
    def __init__(self, parent, p_title):
        Toplevel.__init__(self, parent)
        self.title(p_title)
        parent.withdraw()
        self.geometry("500x400")
        self.parent = parent

        # setting default
        self.ukuran_gambar = [416, 416]  # [width, height]
        self.n_classes = 2
        self.folder_referen = "D:\\Program"

        self.parent.df_names = ''
        self.parent.df_yaml = ''
        self.parent.df_cfg = ''

        self.aturKomponen()

        self.grab_set()
        self.wait_window()

    def aturKomponen(self):
        # Membagi Frame
        self.top_frame = Frame(self)
        self.top_frame.pack(side='top', fill=X, pady=8, padx=2, expand=YES)
        self.bottom_frame = Frame(self)
        self.bottom_frame.pack(fill=X, pady=8, padx=8, expand=YES)

        self.frame_yaml = Frame(self.top_frame)
        self.frame_yaml.pack(side='top', fill=BOTH, padx=3, pady=5)
        self.frame_cfg = Frame(self.top_frame)
        self.frame_cfg.pack(side='bottom', fill=BOTH, padx=3, pady=5)

        # Label
        self.lbl_pilih_yaml = Label(self.frame_yaml, width=38, font=(
            'Times', 12, 'bold'), text='Belum Memilih', anchor='w', bg='white')
        self.lbl_pilih_yaml.pack(side=LEFT, fill=Y, padx=3)

        self.lbl_pilih_cfg = Label(self.frame_cfg, width=38, font=(
            'Times', 12, 'bold'), text='Belum Memilih', anchor='w', bg='white')
        self.lbl_pilih_cfg.pack(side=LEFT, fill=Y, padx=3)

        # Button
        self.btn_open_yaml = Button(self.frame_yaml, text='Open File YAML', font=(
            'Times', 12, 'bold'), width=13)
        self.btn_open_yaml.config(command=self.openFileYaml)
        self.btn_open_yaml.pack(side=RIGHT, fill=Y, padx=3)

        self.btn_open_cfg = Button(self.frame_cfg, text='Open File cfg', font=(
            'Times', 12, 'bold'), width=13)
        self.btn_open_cfg.config(command=self.openFileCfg)
        self.btn_open_cfg.pack(side=RIGHT, fill=Y, padx=3)

        self.btn_kembali = Button(self.bottom_frame, text='Kembali', font=(
            'Times', 12, 'bold'))
        self.btn_kembali.config(command=lambda: self.destroy())
        self.btn_kembali.pack(side=TOP, fill=X, expand=True)

        # Create a blank text area.
        self.file_contents = Text(self.bottom_frame)
        self.file_contents.pack(fill=BOTH, expand=True, pady=5)

    def openFileYaml(self):
        open_file_name = fd.askopenfilename(title="File yaml",
            initialdir=self.folder_referen, filetypes=[("YAML", '*.yaml')])
        if open_file_name:
            dir_name, _ = os.path.split(open_file_name)
            self.lbl_pilih_yaml.config(
                text=(open_file_name[-38:] if (len(open_file_name) > 38) else open_file_name))
            
            str = '############### yaml ###############\n'
            str_file = ''

            ############### yaml ###############
            with open(open_file_name, 'r+') as file_yaml:
                for i, str_f in enumerate(file_yaml):
                    if i < 3:
                        str_file += str_f.replace('..', dir_name)
                        if str_f.find('train:') != -1:
                            _, cek_gambar = str_file.split()
                    else:
                        str_file += str_f

                        if str_f.find('nc:') != -1:
                            _, n_classes = str_f.split()
                        elif str_f.find('names:') != -1:
                            classes_name = str_f[str_f.find(
                                '[')+1:str_f.find(']')]
                file_yaml.seek(0)
                file_yaml.write(str_file)
                str += str_file
                str_file = ''

            cek_gambar = f'{cek_gambar}/{os.listdir(cek_gambar)[0]}'
            self.n_classes = n_classes
            classes_name = classes_name.replace('\'', '').replace(', ', '\n')

            ############### data.names ###############
            with open(f"{dir_name}/data.names", 'w') as file_names:
                file_names.write(classes_name)

            self.parent.df_names = f'{dir_name}/data.names'
            self.parent.df_yaml = open_file_name

            self.file_contents.insert(END, str)

            im_read = cv2.imread(cek_gambar)
            height, width, _ = im_read.shape
            self.ukuran_gambar = [width, height]

    def openFileCfg(self):
        open_file_name = fd.askopenfilename(title="File cfg",
            initialdir=self.folder_referen, filetypes=[("CFG", '*.cfg')])
        # dir_name, _ = os.path.split(open_file_name)
        if open_file_name:
            self.lbl_pilih_cfg.config(
                text=(open_file_name[-38:] if (len(open_file_name) > 38) else open_file_name))
            # self.dir_folder_cfg = open_file_name
            filter_cls = (int(self.n_classes) + 5) * 3
            
            str = '\n\n############### cfg ###############\n'
            str_file = ''

            ############### cfg ###############
            with open(open_file_name, 'r+') as file_cfg:
                for i, str_c in enumerate(file_cfg):
                    if 6 < i < 9:
                        if str_c.find('width=') != -1:
                            str_file += "{}{}\n".format(
                                str_c[:(str_c.find('=')+1)], self.ukuran_gambar[0])
                        elif str_c.find('height=') != -1:
                            str_file += "{}{}\n".format(
                                str_c[:(str_c.find('=')+1)], self.ukuran_gambar[1])
                        else:
                            str_file += str_c
                    elif 1438 < i < 1446 or 1476 < i < 1484 or 1514 < i < 1522:
                        if str_c.find('filters=') != -1:
                            str_file += "{}{}\n".format(
                                str_c[:(str_c.find('=')+1)], filter_cls)
                        elif str_c.find('classes=') != -1:
                            str_file += "{}{}\n".format(
                                str_c[:(str_c.find('=')+1)], self.n_classes)
                        else:
                            str_file += str_c
                    else:
                        str_file += str_c

                file_cfg.seek(0)
                file_cfg.write(str_file)
                str += str_file
                str_file = ''

                self.parent.df_cfg = open_file_name
                self.file_contents.insert(END, str)