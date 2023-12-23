import argparse
import os
import platform
import shutil
from tkinter import *
import time
import math
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from utils.google_utils import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords, xyxy2xywh, strip_optimizer)
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

from models.models import *
from utils.datasets import *
from utils.general import *

FONT_SCALE = 2e-3  # Adjust for larger font size in all images
THICKNESS_SCALE = 1e-3  # Adjust for larger thickness in all images

class Deteksi(Toplevel):
    def __init__(self, parent, p_title="Deteksi", source='0', cfg='file.cfg', names='file.names', weights=[], conf_thres=50, img_size=704, view_image=False):
        Toplevel.__init__(self, parent)
        parent.file_contents.delete('1.0', END)

        opt = argparse.Namespace(agnostic_nms=False,
                                 augment=False,
                                 cfg=cfg,
                                 classes= None, # [0, 1, 2], # None
                                 conf_thres=conf_thres/100,
                                 device='0',
                                 img_size=img_size,
                                 iou_thres=0.5,
                                 names=names,
                                 output='Hasil',
                                 save_txt=False,
                                 source=source,
                                 update=False,
                                 view_img=view_image,
                                 weights=weights)

        print(opt)

        with torch.no_grad():
            if opt.update:  # update all models (to fix SourceChangeWarning)
                #print(opt)
                for opt.weights in ['']:
                    self.detect(parent, opt=opt)
                    strip_optimizer(opt.weights)
            else:
                self.detect(parent, opt=opt)

        self.grab_set()
        self.wait_window()

    def load_classes(self, path):
        # Loads *.names file at 'path'
        with open(path, 'r') as f:
            names = f.read().split('\n')
        return list(filter(None, names))  # filter removes empty strings (such as last line)

    def detect(self, parent, save_img=False, opt=argparse.Namespace()):
        path_image, source, weights, view_img, save_txt, imgsz, cfg, names = \
            opt.output, opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size, opt.cfg, opt.names
        webcam = source == '0' or source.startswith('rtsp') or source.startswith('http') or source.endswith('.txt')

        # Initialize
        jumlah_terdeteksi = 0
        path_image = f"{path_image}/"
                        
        # membuat file penyimpanan
        folderHasil = os.path.join(path_image, time.strftime("%d-%m-%Y (%Hh, %Mm, %Ss)", time.localtime(time.time())))
        if not os.path.exists(folderHasil):
            os.makedirs(folderHasil)
        #out = folderHasil

        device = select_device(opt.device)
        half = device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        model = Darknet(cfg, imgsz).cuda()
        try:
            model.load_state_dict(torch.load(weights[0], map_location=device)['model'])
            #model = attempt_load(weights, map_location=device)  # load FP32 model
            #imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
        except:
            load_darknet_weights(model, weights[0])
        model.to(device).eval()
        if half:
            model.half()  # to FP16

        # Second-stage classifier
        classify = False
        if classify:
            modelc = load_classifier(name='resnet101', n=2)  # initialize
            modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model'])  # load weights
            modelc.to(device).eval()

        # Set Dataloader
        vid_path, vid_writer = None, None
        if webcam:
            view_img = True
            cudnn.benchmark = True  # set True to speed up constant image size inference
            self.dataset = LoadStreams(source, img_size=imgsz)
            test_parameter = True
        else:
            save_img = True
            self.dataset = LoadImages(source, img_size=imgsz, auto_size=64)

        # Get names and colors
        names = self.load_classes(names)
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
        #print(f"BGR: {colors}")

        # Run inference
        t0 = time.time()
        img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
        _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once
        for path, img, im0s, vid_cap in self.dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            t1 = time_synchronized()
            pred = model(img, augment=opt.augment)[0]

            # Apply NMS
            pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
            t2 = time_synchronized()

            # Apply Classifier
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                if webcam:  # batch_size >= 1
                    p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
                    save_path = str(Path(folderHasil) / 'live.avi')
                else:
                    p, s, im0 = path, '', im0s
                    save_path = str(Path(folderHasil) / Path(p).name)
            
                txt_path = str(Path(folderHasil) / Path(p).stem) + ('_%g' % self.dataset.frame if self.dataset.mode == 'video' else '')
                s += '%gx%g ' % img.shape[2:]  # print string

                height, width, _ = im0.shape
                # https://stackoverflow.com/questions/52846474/how-to-resize-text-for-cv2-puttext-according-to-the-image-size-in-opencv-python
                font_scale = min(width, height) * FONT_SCALE
                thickness = math.ceil(min(width, height) * THICKNESS_SCALE)
            
                timee = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(time.time()))

                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if det is not None and len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += '%g %s, ' % (n, names[int(c)])  # add to string
                        jumlah_terdeteksi += n

                    # Write results
                    for *xyxy, conf, cls in det:
                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                            with open(txt_path + '.txt', 'a') as f:
                                f.write(('%g ' * 5 + '\n') % (cls, *xywh))  # label format

                        if save_img or view_img:  # Add bbox to image
                            label = '%s %.2f' % (names[int(cls)], conf)
                            plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=thickness*2) # 3

                # Print time (inference + NMS)
                print('%sDone. (%.3fs)' % (s, t2 - t1))
                parent.file_contents.insert(END, '%sDone. (%.3fs)\n' % (s, t2 - t1))
                text_color = (255,255,255)

                # https://stackoverflow.com/questions/60674501/how-to-make-black-background-in-cv2-puttext-with-python-opencv
                in_putText = im0.copy()
                bg_color = (0,0,0)
                y_putText = int(height / 25)

                if width < 600:
                    x_putText = int(width/74)
                elif (round(width/height, 3) < 1.477) or (width == height and width < 1000):
                    x_putText = int(width/83)
                else:
                    x_putText = int(width/188)

                # Draw black background dan rentang untuk background text
                black_bg = np.full((im0.shape), bg_color, dtype=np.uint8)
                z = int(round(font_scale + thickness, 0) * 2)

                cv2.putText(black_bg, f'Time: {timee}', (x_putText, y_putText), cv2.FONT_HERSHEY_COMPLEX_SMALL, font_scale, text_color, thickness)
                i,j,w,h = cv2.boundingRect(black_bg[:,:,2])

                # copy bounding box region from black_bg to img/in_putText
                in_putText[j - z:j + h + z, i - z:i + w + z] = black_bg[j - z:j + h + z, i - z:i + w + z]
                black_bg = np.full((im0.shape), bg_color, dtype=np.uint8)

                cv2.putText(black_bg, f'Detected objects: {jumlah_terdeteksi}', (x_putText, int(y_putText * 2.2)), cv2.FONT_HERSHEY_COMPLEX_SMALL, font_scale, text_color, thickness)
                i,j,w,h = 0,0,0,0
                i,j,w,h = cv2.boundingRect(black_bg[:,:,2])
                in_putText[j - z:j + h + z, i - z:i + w + z] = black_bg[j - z:j + h + z, i - z:i + w + z]

                #### alpha, the 4th channel of the image
                alpha = 0.4
                cv2.addWeighted(in_putText, alpha, im0, 1 - alpha, 0, im0)
                jumlah_terdeteksi = 0

                # Stream results
                if view_img:
                    im_res = im0.copy()
                    im_res = cv2.resize(im_res, (800, 600))

                    if webcam: # save video
                        #im_res = cv2.resize(im_res, (800, 600)) # w, h  1024, 768 || 960, 540
                        cv2.imshow(p, im_res)

                        if vid_path != save_path:  # new video
                            vid_path = save_path
                            if isinstance(vid_writer, cv2.VideoWriter):
                                vid_writer.release()

                            fourcc = 'MJPG'  # output video codec
                            fps = 15 # 12 || 10
                            vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (800, 600)) # 1024, 768 || 800, 600
                        vid_writer.write(im_res)
                    else:
                        #im_res = cv2.resize(im_res, (1024, 768)) # w, h  1024, 768 || 960, 540
                        cv2.imshow(p, im_res)

                    if cv2.waitKey(1) == ord('q'):  # q to quit, 10/15
                        #vid_writer.release()
                        break

                # Save results (image with detections)
                if save_img:
                    if self.dataset.mode == 'images':
                        cv2.imwrite(save_path, im0)
                    else:
                        if vid_path != save_path:  # new video
                            vid_path = save_path
                            if isinstance(vid_writer, cv2.VideoWriter):
                                vid_writer.release()  # release previous video writer

                            fourcc = 'mp4v'  # output video codec
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
                        vid_writer.write(im0)

        if save_txt or save_img:
            print('Results saved to %s' % Path(folderHasil))
            parent.file_contents.insert(END, 'Results saved to %s\n' % Path(folderHasil))
            if platform == 'darwin' and not opt.update:  # MacOS
                os.system('open ' + save_path)

        print('Done. (%.3fs)' % (time.time() - t0))
        parent.file_contents.insert(END, 'Done. (%.3fs)\n' % (time.time() - t0))
        self.destroy()