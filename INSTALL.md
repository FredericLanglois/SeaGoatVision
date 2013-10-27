SeaGoatVision
=============
SeaGoatVision is a vision server to develop and execute filter on different media.
This Vision Serveur is tested on OpenCV 2.4.5 with Python 2.7 on Fedora 18, Ubuntu 12.04 and Arch Linux.

Requirements
------------

 - Python 2.7
 - PyQt4
 - Glade 3
 - OpenCV 2.4 w/ Python/Numpy bindings
 - Numpy
 - Scipy

Until OpenCV 2.4 is fully supported, the preferred way is to compile OpenCV manually:
http://opencv.willowgarage.com/wiki/InstallGuide

Installation
------------
### A. Download the project ###
    git clone git://github.com/Octets/SeaGoatVision.git

###B. Install dependencies###
#### Ubuntu : ####
	sudo apt-get install python python-numpy python-scipy python-opencv python-protobuf protobuf-compiler python-pyside python-qt4 python-imaging libopencv-dev

#### Fedora : ####
	sudo yum install python numpy scipy opencv-python protobuf-python protobuf protobuf-compiler python-pyside PyQT4 python-imaging opencv-devel

#### Arch Linux : ####
Don't forget to active the "community" repositorie. See https://wiki.archlinux.org/index.php/Pacman

	pacman -S python2 python2-numpy python2-scipy opencv protobuf protobuf-python python2-pyside python2-pyqt python2-imaging

#### Windows : ####
Install the following dependencies:

 - Python:	http://python.org/ftp/python/2.7.3/python-2.7.3.msi
 - Numpy:	http://sourceforge.net/projects/numpy/files/NumPy/	# Choose the installer
 - Scipy:	http://sourceforge.net/projects/scipy/files/scipy/	# Choose the installer
 - PyQt4:	http://www.riverbankcomputing.co.uk/software/pyqt/download
 - PySide:	http://qt-project.org/wiki/PySide_Binaries_Windows
 - PIL:		http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe
 - OpenCV:	http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv	# OpenCV installer for Windows.

### C. Install OpenCV 2.4 ###
If your package management has opencv 2.4, it's not necessary to follow this section.

To check if your package management have opencv 2.4;

###Try i.e. with Ubuntu###
	apt-cache search opencv

###If the output is showing something like opencv 2.4, install it and go to step D.###

###1. Install required OpenCV dependencies###
	sudo apt-get install cmake cmake-gui gcc pkg-config libavformat-dev libswscale-dev

###2. Download the archive manually###
	From here: http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.5/opencv-2.4.5.tar.gz
	Go to directory containing downloaded file with a command line.

###3. Extract the archive###
	tar -xvf OpenCV-2.4.5.tar.gz && cd OpenCV-2.4.5

###4. Configure###
	mkdir release
	cd release
	cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON ..

###5. Compile (replace # by the number of processor core)###
	make -j#

###6. Install###
	sudo make install

###7. Do crazy stuff!###

More information is available here: http://opencv.willowgarage.com/wiki/InstallGuide

### D. Compile the project ###
Note: The third-party pydc1394 is dependant of cython 0.19. Be sure you have it, else install it with easy_install from his website.
On the root of the project:

	git submodule init
	git submodule update
	make
