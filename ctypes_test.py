'''
Simple tester for the Motive API using ctypes
'''

import ctypes
import time
import os

# Load the Motive API DLL
full_dll_path = "C:\\Program Files\\OptiTrack\\Motive\\lib\\MotiveAPI.dll"

try:
    motive_api = ctypes.WinDLL(full_dll_path)
    print(f"Motive API DLL loaded successfully from full path: {full_dll_path}")

except OSError as e:
    print(f"Error loading Motive API DLL from full path: {e}")
    print("Attempting to load from project folder...")

    project_dll_path = os.path.join(os.getcwd(), "MotiveAPI.dll")
    
    try:
        motive_api = ctypes.WinDLL(project_dll_path)
        print(f"Motive API DLL loaded successfully from project folder: {project_dll_path}")

    except OSError as e:
        print(f"Error loading Motive API DLL from project folder: {e}")
        print("Failed to load Motive API DLL. Exiting...")
        exit(1)

# Do we need to load a Motive camera calibration file?

motive_api.Initialize()
print("motive API initialized")

motive_api.StartRecording()
print("recording started")

time.sleep(5) # wait 5 seconds

motive_api.StopRecording()
print("recording stopped")

# Shutdown Motive SDK
motive_api.Shutdown()
print("motive API shutdown")
