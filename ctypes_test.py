# '''
# Simple tester for the Motive API using ctypes
# '''

import ctypes
import time
import os

dll_path = os.path.join(os.getcwd(), "MotiveAPI.dll")
# Load the DLL
try:
    motive_api = ctypes.WinDLL(dll_path)
    print("Motive API loaded successfully.")
except OSError as e:
    print(f"Failed to load Motive API: {e}")
    exit(1)

# Do we need to load a Motive camera calibration file? IDK
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
# import ctypes
# import time
# import os

# # Path to the MotiveAPI.dll
# dll_path = os.path.join(os.getcwd(), "MotiveAPI.dll")
# # Load the DLL
# try:
#     motive_api = ctypes.WinDLL(dll_path)
#     print("Motive API loaded successfully.")
# except OSError as e:
#     print(f"Failed to load Motive API: {e}")
#     exit(1)

# # Initialize the API
# if motive_api.TT_Initialize() != 0:  # TT_Initialize should return 0 on success
#     print("Failed to initialize Motive API.")
#     exit(1)

# print("Motive API initialized.")

# if motive_api.TT_LoadProfile(b"C:\\Path\\To\\Profile.motive") != 0:
#     print("Failed to load profile.")
# if motive_api.TT_LoadCalibration(b"C:\\Path\\To\\Calibration.cal") != 0:
#     print("Failed to load calibration.")

# # Start Recording
# if motive_api.TT_StartRecording() != 0:
#     print("Failed to start recording.")
# else:
#     print("Recording started.")
#     time.sleep(5)  # Record for 5 seconds

# # Stop Recording
# if motive_api.TT_StopRecording() != 0:
#     print("Failed to stop recording.")
# else:
#     print("Recording stopped.")

# # Shutdown the API
# if motive_api.TT_Shutdown() != 0:
#     print("Failed to shut down Motive API.")
# else:
#     print("Motive API shut down successfully.")
