from command.command import Command
from sniff.pcap_investigator import PcapInvestigator
from utils.utils import press_enter_and_clear_screen
import os
import time
from tabulate import tabulate

class PcapInvestigation(Command):
    """
    Command to investigate captured PCAP files.
    Allows selecting a file and generating a forensic report.
    """
    def execute(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n--- PCAP Forensic Investigation ---")
            
            pcap_dir = "threads"
            if not os.path.exists(pcap_dir):
                print("[-] No captures found (threads/ directory missing).")
                press_enter_and_clear_screen()
                break

            pcap_files = [f for f in os.listdir(pcap_dir) if f.endswith(".pcap")]
            
            if not pcap_files:
                print("[-] No .pcap files found in threads/ directory.")
                press_enter_and_clear_screen()
                break

            table_data = []
            for idx, f in enumerate(pcap_files, 1):
                fpath = os.path.join(pcap_dir, f)
                size = os.path.getsize(fpath) / 1024 # KB
                mtime = time.ctime(os.path.getmtime(fpath))
                table_data.append([idx, f, f"{size:.2f} KB", mtime])

            headers = ["#", "File Name", "Size", "Captured At"]
            print(tabulate(table_data, headers, tablefmt="fancy_grid"))
            
            print("\nOptions: [Number] to analyze, [q] to quit")
            choice = input(">> ").lower()

            if choice == 'q':
                break
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(pcap_files):
                    selected_file = os.path.join(pcap_dir, pcap_files[idx])
                    result = PcapInvestigator.analyze(selected_file)
                    print("\n" + result)
                    input("\nPress Enter to return to file list...")
                else:
                    print("[-] Invalid selection.")
                    time.sleep(1)
            else:
                print("[-] Invalid input.")
                time.sleep(1)

    def set_configuration(self, value):
        pass # Not needed for this command
