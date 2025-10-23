# main_window.py

# Set platform to offscreen if no display is available (must be before PyQt6 import)
import os
if 'DISPLAY' not in os.environ:
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'

import sys, threading, queue, time
from PyQt6 import QtCore, QtWidgets, QtGui

from detection.anomaly_model import SimpleAnomalyModel
from mitigation.actions import MitigationEngine
from monitor.process_monitor import ProcessMonitor
from monitor.network_monitor import NetworkMonitor
from utils.report_export import export_report
from detection.ttp_infer import infer_ttps


class ThreatApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Threat Prediction & Mitigation")
        self.resize(900, 600)

        # Shared objects
        self.queue = queue.Queue()
        self.running_flag = threading.Event()
        self.model = SimpleAnomalyModel()
        self.mitigator = MitigationEngine()
        self.logs = []

        # ---- Toolbar ----
        toolbar = self.addToolBar("Controls")

        start_btn = QtGui.QAction("▶ Start Monitoring", self)
        start_btn.triggered.connect(self.start)
        toolbar.addAction(start_btn)

        stop_btn = QtGui.QAction("⏹ Stop Monitoring", self)
        stop_btn.triggered.connect(self.stop)
        toolbar.addAction(stop_btn)

        extract_btn = QtGui.QAction("📄 Extract TTPs", self)
        extract_btn.triggered.connect(self.extract_ttps)
        toolbar.addAction(extract_btn)

        report_btn = QtGui.QAction("💾 Export Report", self)
        report_btn.triggered.connect(self.export_pdf)
        toolbar.addAction(report_btn)

        # ---- Central log widget ----
        self.text = QtWidgets.QTextEdit()
        self.text.setReadOnly(True)
        self.setCentralWidget(self.text)

        # ---- Timer for UI refresh ----
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1500)

    # ---------------- CORE FUNCTIONS ----------------

    def start(self):
        try:
            self.running_flag.set()
            self.text.append("▶ Monitoring started")

            # Start monitoring threads
            self.proc = ProcessMonitor(self.queue, self.running_flag)
            self.net = NetworkMonitor(self.queue, self.running_flag)

            threading.Thread(target=self._safe_run, args=(self.proc.run,), daemon=True).start()
            threading.Thread(target=self._safe_run, args=(self.net.run,), daemon=True).start()
            threading.Thread(target=self.consume, daemon=True).start()
        except Exception as e:
            error_msg = f"[ERROR] Failed to start monitoring: {e}"
            self.text.append(error_msg)
            print(error_msg)

    def _safe_run(self, target_func):
        """Wrapper to safely run monitoring functions with error handling"""
        try:
            target_func()
        except Exception as e:
            error_msg = f"[ERROR] Monitor thread crashed: {e}"
            self.logs.append(error_msg)
            print(error_msg)

    def stop(self):
        self.running_flag.clear()
        self.text.append("⏹ Monitoring stopped")

    def consume(self):
        while self.running_flag.is_set():
            try:
                features = self.queue.get(timeout=1)

                # Safely predict and score
                try:
                    label = self.model.predict(features)
                    score = self.model.score(features)
                except Exception as e:
                    print(f"[ERROR] Model prediction failed: {e}")
                    label = 1  # Assume normal
                    score = 0.0

                log_msg = f"[ALERT] {features} → {label}, score={score:.3f}"
                self.logs.append(log_msg)
                self.text.append(log_msg)

                if label == -1:  # anomaly
                    try:
                        self.mitigator.apply(features)
                    except Exception as e:
                        error_msg = f"[ERROR] Mitigation failed: {e}"
                        self.logs.append(error_msg)
                        self.text.append(error_msg)

            except queue.Empty:
                continue
            except Exception as e:
                error_msg = f"[ERROR] Consumer error: {e}"
                self.logs.append(error_msg)
                self.text.append(error_msg)

    def refresh(self):
        # could later add system stats refresh here
        pass

    def extract_ttps(self):
        try:
            fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Threat Report", "", "PDF Files (*.pdf)")
            if fname:
                try:
                    ttps = infer_ttps(fname)
                    self.logs.append(f"[TTP Extracted] {ttps}")
                    self.text.append(f"[TTP Extracted] {ttps}")
                    self.last_ttps = ttps
                except Exception as e:
                    error_msg = f"[ERROR] TTP extraction failed: {e}"
                    self.logs.append(error_msg)
                    self.text.append(error_msg)
                    self.last_ttps = []
            else:
                self.last_ttps = []
        except Exception as e:
            error_msg = f"[ERROR] File dialog failed: {e}"
            self.text.append(error_msg)
            print(error_msg)

    def export_pdf(self):
        try:
            fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Report", "report.pdf", "PDF Files (*.pdf)")
            if fname:
                try:
                    ttps = getattr(self, "last_ttps", [])
                    export_report(self.logs, ttps, fname)
                    self.text.append(f"✅ Report saved to {fname}")
                except Exception as e:
                    error_msg = f"[ERROR] Report export failed: {e}"
                    self.logs.append(error_msg)
                    self.text.append(error_msg)
        except Exception as e:
            error_msg = f"[ERROR] Export dialog failed: {e}"
            self.text.append(error_msg)
            print(error_msg)


# ---------------- MAIN ENTRY ----------------
def main():
    app = QtWidgets.QApplication(sys.argv)
    w = ThreatApp()

    # Only show window if display is available
    if 'DISPLAY' in os.environ:
        w.show()
    else:
        print("Running in headless mode - GUI not displayed")
        print("Application is running. Press Ctrl+C to stop.")
        # Run for a short time in headless mode for testing
        QtCore.QTimer.singleShot(5000, app.quit)

    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
