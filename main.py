import time
import pandas as pd
import numpy as np
import sounddevice as sd
import tkinter as tk
import u3

'''
NOTES TO CHANGE
- PLATO goggles controlled through labjack io pin, set on or off
'''

# --- Experiment Class to handle the core experiment functions ---
class EEGExperiment:
    def __init__(self):
        self.data = []
        self.participant_id = None
        self.goggles_state = "opaque"
        self.lj = u3.U3()  # Initialize LabJack
        self.lj.configU3()  # Configure LabJack
        self.sound_duration = 0.5  # Duration of the beep sound (seconds)

        # PLATO goggles initialization - Add specific initialization code here
        
    def play_beep(self):
        """Play a beep sound using the LabJack U3-LV connected speaker."""
        frequency = 1000  # 1000 Hz beep
        sample_rate = 44100  # Samples per second
        
        # Generate a beep sound
        t = np.linspace(0, self.sound_duration, int(sample_rate * self.sound_duration), False)
        beep = np.sin(frequency * 2 * np.pi * t)  # Sine wave at 1000 Hz
        sd.play(beep, samplerate=sample_rate)
        
        # Mark the beep time
        beep_time = time.time()
        self.data.append({'event': 'beep', 'timestamp': beep_time})
        sd.wait()

    def check_goggles(self):
        """Check the status of the PLATO goggles."""
        goggle_state = self.lj.getFIOState(1) # read FIO1 sensor
        return goggle_state
        
    def control_goggles(self, state):
        """Control the PLATO goggles."""
        if state == "transparent":
            # Add code to set goggles to transparent
            self.goggles_state = "transparent"
        else:
            # Add code to set goggles to opaque
            self.goggles_state = "opaque"
        
        # Mark the time of goggles change
        event_time = time.time()
        self.data.append({'event': f'goggles_{state}', 'timestamp': event_time})
    
    def check_infrared_sensor(self):
        """Check the infrared sensor status from LabJack."""
        # Replace with actual infrared sensor reading code using the LabJack library
        sensor_state = self.lj.getFIOState(0) # example pin for reading FIO0 sensor
        return sensor_state
    
    def run_experiment(self):
        """Run the core experiment routine."""
        # Set goggles to opaque
        self.control_goggles("opaque")
        
        # Wait for participant to be ready (place fingers on sensor)
        while not self.check_infrared_sensor():
            time.sleep(0.1)
        
        # Play the beep sound cue
        self.play_beep()
        
        # Make goggles transparent
        self.control_goggles("transparent")
        
        # Wait for the infrared sensor to detect finger lift
        while self.check_infrared_sensor():
            time.sleep(0.01)
        lift_time = time.time()
        self.data.append({'event': 'finger_lift', 'timestamp': lift_time})
        
        # Wait for the participant to return fingers to the sensor
        while not self.check_infrared_sensor():
            time.sleep(0.01)
        return_time = time.time()
        self.data.append({'event': 'finger_return', 'timestamp': return_time})
        
        # Set goggles back to opaque
        self.control_goggles("opaque")
    
    def save_data(self):
        """Save collected data to a file."""
        df = pd.DataFrame(self.data)
        filename = f"participant_{self.participant_id}_data.csv"
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

# --- GUI Class for the user interface ---
class ExperimentGUI:
    def __init__(self, root):
        self.experiment = EEGExperiment()
        self.root = root
        self.root.title('EEG Grasping Experiment')
        
        # Participant ID label and entry
        self.participant_label = tk.Label(root, text='Enter Participant ID:')
        self.participant_label.pack()
        
        self.participant_entry = tk.Entry(root)
        self.participant_entry.pack()
        
        # Start experiment button
        self.start_button = tk.Button(root, text='Start Experiment', command=self.start_experiment)
        self.start_button.pack()

        # End experiment button
        self.end_button = tk.Button(root, text='End Experiment', command=self.end_experiment)
        self.end_button.pack()
    
    def start_experiment(self):
        participant_id = self.participant_entry.get()
        if participant_id:
            self.experiment.participant_id = participant_id
            self.experiment.run_experiment()
            self.experiment.save_data()
        else:
            print("Please enter a valid participant ID.")

    def end_experiment(self):
        # save data and close the program
        self.experiment.lj_handle.close()
        self.experiment.save_data()

# --- Main Function to run the program ---
def main():
    root = tk.Tk()
    gui = ExperimentGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
