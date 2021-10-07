# ControllerPy

A python script to use a controller as mouse and keyboard.

Currently only working on linux (test on ubuntu 20).

For keyboard input, an on screen keyboarded name [onboard](https://launchpad.net/onboard) is used.


## Note

This is a personal project under development. All feature requests and issues and appreciated.


## Comments
1. "Xlib.threaded" is imported but never used. The import is to fix an issues xlib has with multi-threaded usage.
2. You can change **sensitivty** and **dead-zone** parameters in the **config.yaml** file.


## Installation
```bash
sudo apt install onboard

python3 -m pip install git+https://github.com/sandstorm12/ControllerPy.git
```


## Run
```bash
controllerpy
```


## Urgent issues and futures
1. Add a list of used libraries to the main readme


## Issues and futures
1. Add Windows support
2. Make config file custom and createable from cli
3. Add cli interface
4. Add version cli option
5. List controllers using cli options


## Contributors
1. Hamid Mohammadi: <sandstormeatwo@gmail.com>
