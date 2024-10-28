import time
import pandas as pd
import tkinter as tk

# EEGExperiment handles experiment functions
class EEGExperiment:
    def __init__(self):
        self.data = []
        self.participant_id = None
        self.goggles_state = "opaque"

    def check_goggles(self):
        """Check the status of the PLATO goggles."""
        return self.goggle_state
    
    def control_goggles(self, desired_state):
        """Control the PLATO goggles using FIO1."""
        if desired_state == "transparent":
            self.goggles_state = "transparent"
        else:
            self.goggles_state = "opaque"
        
        # Mark the time of goggles state change
        event_time = time.time()
        self.data.append({'event': f'goggles_{desired_state}', 'timestamp': event_time})

    def run_experiment(self):
        """Run the core experiment routine."""

        self.control_goggles("opaque")

        time.sleep(3) # Wait for 3 seconds
   
        self.control_goggles("transparent")
        
        time.sleep(3) # Wait for 1 seconds

        self.control_goggles("opaque")
    
    def save_data(self):
        """Save collected data to a file."""
        df = pd.DataFrame(self.data)
        filename = f"participant_{self.participant_id}_data.csv"
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

# ExperimentGUI handles the graphical user interface
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
        self.experiment.save_data()
        self.root.destroy() # close tkinter window

def main():
    root = tk.Tk()
    gui = ExperimentGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
