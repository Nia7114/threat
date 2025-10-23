import tkinter as tk
from tkinter import messagebox
import os
import shutil
import time
import logging
from cryptography.fernet import Fernet
import threading
import random
import json
import datetime

# Configure logging
logging.basicConfig(filename="incident_response.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Incident Response Simulation in an ICS Environment
class ICSSimulation:
    def __init__(self, folder_path, backup_path):
        self.folder_path = folder_path
        self.backup_path = backup_path
        self.ics_files = ['valve_data.csv', 'sensor_data.csv', 'pressure_log.csv']

    def create_ics_files(self):
        """Create simulation files representing critical ICS files"""
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        for file in self.ics_files:
            file_path = os.path.join(self.folder_path, file)
            with open(file_path, 'w') as f:
                f.write(f"Important data or configurations\n")
        logging.info("ICS Files created successfully.")

    def backup_files(self):
        """Backup ICS files before ransomware attack."""
        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)

        for file in self.ics_files:
            src = os.path.join(self.folder_path, file)
            dest = os.path.join(self.backup_path, file)
            if os.path.exists(src):
                shutil.copy2(src, dest)
        logging.info("ICS Files backed up successfully.")

# Advanced Ransomware Attack Simulation
class RansomwareSimulation:
    def __init__(self, ics_simulation, key):
        self.ics_simulation = ics_simulation
        self.key = key
        self.cipher = Fernet(key)

    def attack(self):
        """Encrypt ICS files with Fernet encryption and simulate attack"""
        attack_report = []

        for file in self.ics_simulation.ics_files:
            file_path = os.path.join(self.ics_simulation.folder_path, file)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    data = f.read()
                encrypted_data = self.cipher.encrypt(data)
                with open(file_path + ".enc", 'wb') as f:
                    f.write(encrypted_data)
                os.remove(file_path)
                attack_report.append({"file": file, "status": "Encrypted"})

        # Save attack report
        with open("attack_report.json", "w") as report_file:
            json.dump(attack_report, report_file, indent=4)

        logging.warning("Ransomware Attack: ICS files encrypted!")

# GUI Application with Incident Response Features
class ICSRansomwareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ICS Incident Response Simulation")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e272e')

        self.key = Fernet.generate_key()
        self.ics_simulation = ICSSimulation(folder_path="ics_data", backup_path="backup_ics_data")
        self.ransomware_sim = RansomwareSimulation(self.ics_simulation, self.key)

        self.create_widgets()

    def create_widgets(self):
        self.status_label = tk.Label(self.root, text="ICS Incident Response Simulation", font=("Helvetica", 18, "bold"), bg='#1e272e', fg='white')
        self.status_label.pack(pady=20)

        self.create_files_button = tk.Button(self.root, text="Create ICS Files", command=self.create_files, bg='#0fbcf9', fg='white', font=("Arial", 14, "bold"), width=40, height=2)
        self.create_files_button.pack(pady=10)

        self.run_attack_button = tk.Button(self.root, text="Simulate Ransomware Attack", command=self.simulate_attack, bg='#ff3f34', fg='white', font=("Arial", 14, "bold"), width=40, height=2)
        self.run_attack_button.pack(pady=10)

        self.log_text = tk.Text(self.root, width=90, height=15, wrap="word", bg='#d2dae2', fg='black', font=("Courier", 10))
        self.log_text.pack(pady=20)
