# mapBurning

> The program was prepared for the subject Script Languages and their usages. 
## Table of contents
* [About The Project](#about-the-project)
* [Technologies](#technologies)
* [Getting Started with PyQt](#getting-started-with-PyQt)
* [Getting Started with PyGtk](#getting-started-with-PyGtk)
* [Contact](#contact)
## About The Project
The purpose of the project was to implement "Map Burning" ("Wypalanie mapy") game.

## Technologies
* Python 3.9
* PyQt5
* PyGtk3
* Windows OS

## Getting Started with PyQt
* Clone the repository  `git clone https://github.com/matibob333/mapBurning.git`  
* Game can be run using e.g. PyCharm IDE - starting file is `main.py`

## Getting Started with PyGtk
* Firstly prepare environment https://pygobject.readthedocs.io/en/latest/getting_started.html?fbclid=IwAR2y0CjddfN8CNG0evEtnhLUkgiJrYZV6y1NjUBm1cUlnZURiQ4DsLA_isk#windows-getting-started
* Go to http://www.msys2.org/ and download the x86_64 installer
* Follow the instructions on the page for setting up the basic environment
* Run `C:\msys64\mingw64.exe` - a terminal window should pop up
* Execute `pacman -Suy`
* Execute `pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3 mingw-w64-x86_64-python3-gobject`
* To test that GTK 3 is working you can run gtk3-demo
* Clone the repository  `git clone https://github.com/matibob333/mapBurning.git` 
* Copy the `mapBurningPyGTK.py` script and `saves` folder to C:\msys64\home\<username>
* In the mingw64 terminal execute `python3 mapBurningPyGTK.py` - a window should appear.

## Contact
Mateusz Nieścier - `mateusz.niescier@gmail.com`
