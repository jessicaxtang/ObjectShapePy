### NOTES FROM JESS ON JAN 11, 2025

## 1. Under motivepy folder

__try running:__
```python setup.py build_ext --inplace```
or
```python setup.py install```

__the current error:__
```
running build_ext
building 'motive.native' extension
"C:\Pr...
...motive\native.cpp(3700): error C2065: 'kApiResult_Success': undeclared identifier
...
...
...
error: command 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Tools\\MSVC\\14.42.34433\\bin\\HostX86\\x64\\cl.exe' failed with exit code 2
```

__note__: i installed build tools for VS C++
__motivepy documentation__: https://ratcave.github.io/motivepy/
__note__: THIS REPO WAS MADE FOR PYTHON2 and an older version of motive. BUT in general it *should* work.

## 2. I made a motive_test.cpp to try using motive directly in c++.
- IT STILL SAYS THE FUNCTIONS DON"T EXIST IN DLL
- I printed all the exported functions of the dll in ctypes_test.py AND NONE OF THE FUNCTIONS IN THE MotiveAPI.h ARE LISTED??



THANK YOU FOR HELPING DEBUG I hope this has been some use for u :,)