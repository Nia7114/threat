import time
import os
import random

def simulate_high_cpu():
    print("[*] Simulating high CPU usage...")
    # Burn CPU artificially
    start = time.time()
    while time.time() - start < 5:
        _ = [x**2 for x in range(10000)]
    print("[+] High CPU load simulation complete.")

def simulate_suspicious_process():
    print("[*] Simulating suspicious process: evil.exe")
    # Just create a fake process indicator file
    with open("evil_process.log", "w") as f:
        f.write("Process: evil.exe running...\n")
    print("[+] Suspicious process simulated as 'evil.exe'.")

def simulate_malicious_action():
    print("[*] Simulating malicious action: deleting system files...")
    # Instead of deleting real files, write a fake log
    os.makedirs("quarantine", exist_ok=True)
    with open("quarantine/fake_delete.log", "w") as f:
        f.write("Attempted to delete C:\\Windows\\System32\n")
    print("[+] Malicious action simulation complete.")

if __name__ == "__main__":
    print("[*] Dummy Threat Script Running...")
    simulate_high_cpu()
    time.sleep(2)
    simulate_suspicious_process()
    time.sleep(2)
    simulate_malicious_action()
    print("[*] Dummy threat simulation finished.")

