#include <windows.h>
#include<tchar.h>
#include <iostream>
#include <chrono>
#include <thread>

#include "MotiveAPI.h"

typedef void (*InitializeFunc)();  // Define a function pointer type for 'Initialize'
typedef void (*StartRecordingFunc)();
typedef void (*StopRecordingFunc)();

int main() {
    // Load the DLL
    HMODULE hMotiveAPI = LoadLibrary(_T("MotiveAPI.dll"));
    if (hMotiveAPI == NULL) {
        std::cerr << "Failed to load MotiveAPI.dll" << std::endl;
        return 1;
    }

    std::cout << "Motive API loaded successfully." << std::endl;

    // Get the address of 'Initialize' function
    InitializeFunc Initialize = (InitializeFunc)GetProcAddress(hMotiveAPI, "Initialize");
    if (!Initialize) {
        std::cerr << "'Initialize' function not found in the Motive API." << std::endl;
        FreeLibrary(hMotiveAPI);
        return 1;
    }

    // Get the address of 'StartRecording' function
    StartRecordingFunc StartRecording = (StartRecordingFunc)GetProcAddress(hMotiveAPI, "StartRecording");
    if (!StartRecording) {
        std::cerr << "'StartRecording' function not found in the Motive API." << std::endl;
        FreeLibrary(hMotiveAPI);
        return 1;
    }

    // Get the address of 'StopRecording' function
    StopRecordingFunc StopRecording = (StopRecordingFunc)GetProcAddress(hMotiveAPI, "StopRecording");
    if (!StopRecording) {
        std::cerr << "'StopRecording' function not found in the Motive API." << std::endl;
        FreeLibrary(hMotiveAPI);
        return 1;
    }

    // Call Initialize
    Initialize();
    std::cout << "Motive API initialized." << std::endl;

    // Start recording
    StartRecording();
    std::cout << "Recording started." << std::endl;

    // Wait for 5 seconds
    std::this_thread::sleep_for(std::chrono::seconds(5));

    // Stop recording
    StopRecording();
    std::cout << "Recording stopped." << std::endl;

    // Free the DLL when done
    FreeLibrary(hMotiveAPI);

    return 0;
}