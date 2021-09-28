Install PyTorch for Linux (1.8.2 LTS - cuda11)
pip3 install torch==1.8.2+cu111 torchvision==0.9.2+cu111 torchaudio==0.8.2 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html

Install psbody
On Enviroment folder:
git clone https://github.com/MPI-IS/mesh.git
sudo apt-get install libboost-dev
sudo apt-get install cmake

mesh/mesh/cmake/thirdparty.cmake
	:29 COMMAND ${PYTHON_EXECUTABLE} -c "import numpy; print(numpy.get_include())"

mesh/ make all


pyqt
sudo apt-get install --reinstall libxcb-xinerama0
env/lib/python3.9/site-packages/cv2/qt/ borrar carpeta plugins