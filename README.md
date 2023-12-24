# Hand-Movement-Detection
Human Body Hand Movement Detection Using the YOLOv4

## Abstrak
Setiap hari kita pasti melakukan aktivitas baik di dalam maupun di luar ruangan. Ketika melakukan hal tersebut, kita akan melakukan gerakan pada tubuh seperti menggerakkan tangan. Gerakan tangan merupakan gerakan yang dapat dikenali oleh penglihatan manusia, dan gerakan tangan dapat diaplikasikan untuk mengendalikan robot atau hal lainnya, dengan demikian peneliti ingin mengetahui potensi algoritma You Only Look Once (YOLO) Versi 4 dalam mendeteksi gerak tangan manusia.

Algoritma You Only Look Once (YOLO) versi 4 memiliki tingkat akurasi yang tinggi dan identifikasi yang cepat, algoritma ini juga merupakan algoritma yang mendeteksi suatu objek secara real-time. Pada penelitian ini, gerak tangan yang akan dideteksi meliputi gerak tangan kanan, tangan kiri, atau kedua tangan. Gerakan tersebut dilakukan dengan posisi orang menghadap atau membelakangi kamera. Penelitian menggunakan data awal sebanyak 600 dan menjadi 1440 setelah dilakukan pre-processing dan augmentation dari website Roboflow. 

Train dilakukan dengan skema learning rate (0.1; 0.01; 0.001; 0.00261) dan maximal epoch (100; 200; sampai 1000) yang menghasilkan bobot dengan nilai F1-Score, threshold (50%), dan threshold (50%-95%) tertinggi masing-masing sebesar 0.913; 0.981; 0.873. Hasil dari penelitian ini dapat disimpulkan bahwa YOLOv4 dapat mendeteksi dan mengidentifikasi dengan cukup baik terhadap gerak tangan “kanan”, “kiri”, maupun “keduanya”. 

Saran untuk penelitian berikutnya adalah memiliki data yang lebih banyak termasuk dari kelas objek yang hampir berkaitan dengan yang diteliti sehingga meminimalkan kesalahan yang terjadi. Memiliki bervariasi sisi pengambilan, dalam proses pelabelan pada data, lakukanlah dengan lebih teliti karena menentukan hasil terutama dalam memilih kelas untuk data yang dilabelkan. Gunakanlah versi terbaru dari beberapa versi YOLO yang ada sesuai kebutuhan

## Dataset
### Data Preprocessing
  1. Auto-Orient
  2. Resize (448x448)
  3. Filter Null

### Data Augmentation
  1. Rotation
  2. Hue
  3. Brightness
  4. Exposure
  5. Blur
  6. Cutout
  7. Mosaic
  

## Alat
  1. [Google Colaboratory](https://colab.research.google.com/)
  2. [Roboflow](https://app.roboflow.com/login)

## Hasil
![Gambar1](https://github.com/raafi-4z1/Hand-Movement-Detection/assets/80319631/1d0af7f7-7610-43b5-8a58-a2e0e13c6ada)
![Gambar2](https://github.com/raafi-4z1/Hand-Movement-Detection/assets/80319631/4018c462-94b3-4cf6-9df0-9c4cddc2a044)
![Gambar3](https://github.com/raafi-4z1/Hand-Movement-Detection/assets/80319631/7a2b498e-ab97-4998-bb0a-0e90c20d1233)
![Gambar4](https://github.com/raafi-4z1/Hand-Movement-Detection/assets/80319631/b88dc1e2-0d2e-471c-9488-3443d8f91f17)
![Gambar5](https://github.com/raafi-4z1/Hand-Movement-Detection/assets/80319631/71b849fb-3a5c-44a1-9bff-2b90ade16bc1)


## Sumber & Data
 - https://github.com/WongKinYiu/PyTorch_YOLOv4.git
 - https://drive.google.com/drive/folders/1_so9lbs4ZsjCwkdZgPPtzeodDM3epcDh?usp=sharing
