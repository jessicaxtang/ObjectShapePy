//======================================================================================================
// Overwriting NaturalPoint Motive API Sample: with Experiment API
//======================================================================================================
#include <conio.h>
#include <thread>
#include <mutex>

#include <MotiveAPI.h>
#include "inputmanager.h"
#include "apilistener.h"
#include "transformmatrix.h"
#include "support.h"

#include "LabJackUD.h"

using namespace MotiveAPI;

LJ_HANDLE lngHandle = 0;

// Function to check Plato goggles transparency state (input pin DIO1)
bool readPlatoGogglesStatus() {
	long lngErrorcode;
	double transparencyValue = 0;

	// Read from digital input pin DIO1 for Plato Goggles status (transparent or opaque)
	lngErrorcode = AddRequest(lngHandle, LJ_ioGET_DIGITAL_BIT, 1, 0, 0, 0);  // DIO1 pin as input
	ErrorHandler(lngErrorcode, __LINE__, 0);

	// Execute the requests
	lngErrorcode = GoOne(lngHandle);
	ErrorHandler(lngErrorcode, __LINE__, 0);

	// Read the transparency value (0 or 1)
	lngErrorcode = GetFirstResult(lngHandle, &lngIOType, &lngChannel, &transparencyValue, NULL, NULL);
	ErrorHandler(lngErrorcode, __LINE__, 0);

	return (transparencyValue > 0.5); // Return true if goggles are transparent (1)
}

// Function to toggle Plato goggles transparency using LabJack (DIO1 pin)
void togglePlatoGogglesTransparency() {
	static bool transparent = false; // Initial state: opaque
	long lngErrorcode;

	// Toggle the transparency state (transparent or opaque)
	transparent = !transparent;

	// Set DIO0 pin to high (transparent) or low (opaque)
	lngErrorcode = AddRequest(lngHandle, LJ_ioPUT_DIGITAL_BIT, 1, transparent ? 1 : 0, 0, 0);  // DIO0 pin as output
	ErrorHandler(lngErrorcode, __LINE__, 0);

	// Execute the requests to apply the state change
	lngErrorcode = GoOne(lngHandle);
	ErrorHandler(lngErrorcode, __LINE__, 0);

	printf("Plato goggles are now %s.\n", transparent ? "transparent" : "opaque");
}

// Function to trigger Motive recording with Motive API
void triggerCameraRecording(bool start) {
	if (start) {
		// Start recording
		printf("Starting camera recording...\n");
		StartRecording();
	}
	else {
		// Stop recording
		printf("Stopping camera recording...\n");
		StopRecording();
	}
}

int ProcessFrame(int frameCounter) {
	float   yaw, pitch, roll;
	float   x, y, z;
	float   qx, qy, qz, qw;

	printf("running ProcessFrame now");
	printf("\rFrame #%d: %d Markers", frameCounter, MarkerCount());

	// If calibrating, print out some state information.
	eCalibrationState state = CalibrationState();
	if (state == eCalibrationState::Wanding) {
		std::vector<int> neededCameras(CalibrationCamerasLackingSamples());
		if (!neededCameras.empty())
		{
			printf("\nNeed more samples for %d cameras:", (int)neededCameras.size());
			for (int cameraIndex : neededCameras)
			{
				int cameraSamples = CameraCalibrationSamples(cameraIndex);
				printf("\n%d (%d)", CameraID(cameraIndex), cameraSamples);
			}
			printf("\n");
		}
	}
	else if (state >= eCalibrationState::PreparingSolver && state <= eCalibrationState::Complete) {
		PrintCalibrationQuality();
	}

	// Check LabJack's status here (e.g., monitor a digital input pin to sync events)
	bool cameraTriggered = readLabJackTrigger();

	if (cameraTriggered) {
		// If the trigger is active, start recording in Motive if not already started
		printf("Pluto Goggles turned on! Starting camera recording...\n");
		triggerCameraRecording(true);  // Trigger the camera recording
	}
	else {
		// If the trigger is not active, stop recording in Motive
		printf("Plato Goggles turned off! Stopping camera recording...\n");
		triggerCameraRecording(false); // Stop the camera recording
	}

	// Continue processing frames as usual
	return frameCounter;
}

// LabJack error handling function called after every UD function call. 
void ErrorHandler(LJ_ERROR lngErrorcode, long lngLineNumber, long lngIteration)
{
	char err[255];

	if (lngErrorcode != LJE_NOERROR) {
		ErrorToString(lngErrorcode, err);
		printf("Error number = %d\n", lngErrorcode);
		printf("Error string = %s\n", err);
		printf("Source line number = %d\n", lngLineNumber);
		printf("Iteration = %d\n\n", lngIteration);
		if (lngErrorcode > LJE_MIN_GROUP_ERROR)
		{
			//Quit if this is a group error.
			getchar();
			exit(0);
		}
	}
}



int main(int argc, char* argv[])
{
	const wchar_t* calibrationFile = L"C:\\ProgramData\\OptiTrack\\Motive\\System Calibration.cal";
	const wchar_t* profileFile = L"C:\\ProgramData\\OptiTrack\\MotiveProfile.motive";

	if (Initialize() != kApiResult_Success) {
		printf("Unable to license Motive API\n");
		return 1;
	}

	// Attach listener for frame notifications
	APIListener listener;
	AttachListener(&listener);

	// Automatically Load a current camera calibration and profiles saved by Motive.
	int cameraCount = LoadCalibrationAndProfile(calibrationFile, profileFile);

	printf("Initializing NaturalPoint Devices...\n\n");

	WaitForCameraDiscovery(cameraCount);
	PrintConnectedCameras();
	PrintRigidBodies();

	FlushCameraQueues();

	// Initialize LabJack device
	LJ_ERROR lngErrorcode;
	long lngGetNextIteration;
	long lngIOType = 0, lngChannel = 0;
	double dblValue = 0;

	//Open LabJack U3
	lngErrorcode = OpenLabJack(LJ_dtU3, LJ_ctUSB, "1", 1, &lngHandle);
	ErrorHandler(lngErrorcode, __LINE__, 0);

	//Plato Goggles is FIO1
	// did we?: Set DIO0 pin to high (start signal)
	lngErrorcode = AddRequest(lngHandle, LJ_ioPUT_CONFIG, LJ_chI2C_SDA_PIN_NUM, 1, 0, 0);
	ErrorHandler(lngErrorcode, __LINE__, 0);

	//Execute the requests on a single LabJack.
	lngErrorcode = GoOne(lngHandle);
	ErrorHandler(lngErrorcode, __LINE__, 0);

	// User input for toggling Plato goggles transparency (space bar)
	printf("Press Space to toggle Plato goggles transparency.\n");

	// Wait for user input to toggle goggles transparency
	while (true) {
		if (_kbhit()) {
			char ch = _getch();
			if (ch == ' ') {  // Space bar pressed
				togglePlatoGogglesTransparency(); // Toggle goggles transparency
			}
		}
	}

	// hookup commands for user input
	InputManager inputManager;

	// set function to be called for each frame during ProcessFrames();
	inputManager.RegisterProcessFrameFunction(&ProcessFrame);

	// start processing frames
	inputManager.ProcessFrames(listener);

	if (inputManager.Save()) {
		CheckResult(SaveProfile(profileFile));
		CheckResult(SaveCalibration(calibrationFile));
	}

	inputManager.Shutdown();

	return 0;
}