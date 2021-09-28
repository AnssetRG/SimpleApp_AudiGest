AudiGest Desktop Application for Linux OS
=========================================
For instalation use the requirements.txt on a new Virtual Enviroment with Python 3.9.6

```
$ pip install -r requirements.txt
```

Installing Other Dependencies
=============================

PyTorch for Linux (1.8.2 LTS - cuda11)
-------------------------------------
The application was developed using this version of PyTorch installed with the instructions from https://pytorch.org/get-started/locally/.

```
$ pip3 install torch==1.8.2+cu111 torchvision==0.9.2+cu111 torchaudio==0.8.2 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
```


PSBody - Mesh
-------------------------------------
On Enviroment folder:
```
$ git clone https://github.com/MPI-IS/mesh.git
$ sudo apt-get install libboost-dev
$ sudo apt-get install cmake
```

Then inmesh/mesh/cmake/thirdparty.cmake, fixed line 29 by writing "()" for "print":
```
COMMAND ${PYTHON_EXECUTABLE} -c "import numpy; print(numpy.get_include())"
```

Finally on mesh/ run the below command:
```
$ make all
```

PyQT5
-------------------------------------
If when running the main window **AudiGest_terminado.pyw** appears some errors, try the follow solutions:

```
$ sudo apt-get install --reinstall libxcb-xinerama0
```

Then go to env/lib/python3.9/site-packages/cv2/qt/ and delete **Plugins** folder.


FFMPEG
======================================
Install FFMPEG:
```
$ sudo apt install ffmpeg
```