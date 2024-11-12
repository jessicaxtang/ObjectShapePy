import time
import pandas as pd
import tkinter as tk
import u3

# EEGExperiment handles experiment functions
class EEGExperiment:
    def __init__(self):
        self.data = []
        self.participant_id = None
        self.goggles_state = "opaque"
        self.lj = u3.U3()  # Initialize LabJack
        self.lj.configU3()  # Configure LabJack
        self.lj.configIO(FIOAnalog=0)  # Set FIOs to digital

        # FIO1: PLATO goggles initialized to opaque
        self.lj.setFIOState(1, 0)
        self.lj.setFIOState(0, 0)

    def check_goggles(self):
        """Returns status of PLATO goggles: 'Opaque' or 'Transparent'"""
        return self.goggle_state
    
    def control_goggles(self, desired_state):
        """Control the PLATO goggles using FIO1"""
        # to do: may add a parameter to specify pin number
        # to do: check if time.time() gives ok output/what is EEG data time format ?? 
            # is it time in ms since start of experiment ?
        if desired_state == "transparent":
            self.lj.setFIOState(1, 1)  # Set FIO1 to 1 (transparent goggles)
            self.lj.setFIOState(0, 1)
            self.goggles_state = "transparent"
        else:
            self.lj.setFIOState(1, 0)  # Set FIO1 to 0 (opaque goggles)
            self.lj.setFIOState(0, 0)
            self.goggles_state = "opaque"
        
        self.data.append({'event': f'goggles_{desired_state}', 'timestamp': time.time()})

    def run_experiment(self):
        """Run the core experiment"""
        # to do: LOTS. (just checking plato goggles rn. will need to add sound, IR sensors, cameras, etc.)

        self.control_goggles("opaque")
        print("Goggles are opaque") # print statements just for testing
        time.sleep(3) # Wait for 3 seconds
        self.control_goggles("transparent")  
        print("Goggles are transparent")      
        time.sleep(3) # Wait for 3 seconds
        self.control_goggles("opaque")
        print("Goggles are opaque")
    
    def save_data(self):
        """Save data to participant file"""
        # to do: make a folder for each participant/block/session?
            # to do: check if folder exists/need to make new
        # to do: confirm formatting of file
        # to do: confirm file name convention

        df = pd.DataFrame(self.data)
        filename = f"participant_{self.participant_id}_data.csv"
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

# ExperimentGUI handles the graphical user interface
class ExperimentGUI:
    # to do: make window size bigger
    # to do: add more buttons for different parts of experiment
    # to do: add "save data" button and more buttons and key presses for different commands
    # to do: show some indication of experiment state
        # show time elapsed, current block, session, partiicpant, etc.
        # maybe indicate w green/red "light" for experiment status (or just use text for "running", "paused", "stopped")
    # to do: just make it look nicer too.

    # to check: im pretty sure closing window also saves data

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
        self.end_button = tk.Button(root, text='Save Data & End Experiment', command=self.end_experiment)
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
        self.experiment.save_data()
        self.root.destroy() # close tkinter window

def main():
    root = tk.Tk()
    gui = ExperimentGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
