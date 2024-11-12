'''
Simple tester for the Motive API using ctypes
'''

import ctypes
import time

# Load the Motive API DLL
try:
    motive_api = ctypes.CDLL("C:\\Program Files\\OptiTrack\\Motive\\lib\\MotiveAPI.dll")
    print("Motive API DLL loaded successfully.")
except OSError as e:
    print(f"Error loading Motive API DLL: {e}")
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
