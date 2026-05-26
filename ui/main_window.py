from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDialog,
    QMessageBox
)

from PyQt5.QtGui import QIcon

from core.stego_heatmap import generate_heatmap
from core.stego_logic import (
    hide_message,
    extract_message,
    hide_file,
    extract_file
)

from core.security_scan import (
    plot_histogram,
    show_bit_plane
)

from attacks.cracker import crack_caesar, best_candidate

from core.ml_model import predict_image
from core.ml_train import train_model

import os


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("CSA 🔐")
        self.setGeometry(100, 100, 950, 650)

        self.setWindowIcon(QIcon("icon.png"))

        self.image_path = None

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # --------------------------------
        # TABS
        # --------------------------------

        self.tabs.addTab(
            self.create_steganography_tab(),
            "Steganography"
        )

        self.tabs.addTab(
            self.create_ml_tab(),
            "ML Scanner"
        )

        self.tabs.addTab(
            self.create_analysis_tab(),
            "Image Analysis"
        )

        self.tabs.addTab(
            self.create_attack_tab(),
            "Attack Lab"
        )

        self.apply_styles()

    # ====================================
    # STYLES
    # ====================================

    def apply_styles(self):

        self.setStyleSheet("""

            QMainWindow {
                background-color: #1e1e2f;
            }

            QLabel {
                color: #f0f0f0;
                font-size: 14px;
                font-weight: bold;
            }

            QTextEdit {
                background-color: #2e2e3e;
                color: #f0f0f0;
                border: 1px solid #444;
                border-radius: 5px;
                font-size: 13px;
            }

            QPushButton {
                background-color: #4a76a8;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #5e8bc7;
            }

            QPushButton:pressed {
                background-color: #3a5f88;
            }

            QTabWidget::pane {
                border: 1px solid #444;
                border-radius: 5px;
                margin-top: 10px;
            }

            QTabBar::tab {
                background: #2e2e3e;
                color: #f0f0f0;
                padding: 10px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }

            QTabBar::tab:selected {
                background: #4a76a8;
                font-weight: bold;
            }

            QTableWidget {
                background-color: #2e2e3e;
                color: #f0f0f0;
                border: 1px solid #444;
                font-size: 13px;
            }

        """)

    # ====================================
    # STEGANOGRAPHY TAB
    # ====================================

    def create_steganography_tab(self):

        widget = QWidget()
        layout = QVBoxLayout()

        self.stego_label = QLabel("No image selected")

        select_btn = QPushButton("Select Image")
        select_btn.clicked.connect(self.select_image)

        self.stego_input = QTextEdit()
        self.stego_input.setPlaceholderText(
            "Enter hidden message..."
        )

        hide_btn = QPushButton("Hide Message")
        extract_btn = QPushButton("Extract Message")

        hide_btn.clicked.connect(self.hide_data)
        extract_btn.clicked.connect(self.extract_data)

        hide_file_btn = QPushButton("Hide File")
        extract_file_btn = QPushButton("Extract File")

        hide_file_btn.clicked.connect(self.hide_file_ui)
        extract_file_btn.clicked.connect(self.extract_file_ui)

        self.stego_output = QTextEdit()
        self.stego_output.setReadOnly(True)

        layout.addWidget(self.stego_label)
        layout.addWidget(select_btn)

        layout.addSpacing(10)

        layout.addWidget(QLabel("Secret Message"))
        layout.addWidget(self.stego_input)

        layout.addWidget(hide_btn)
        layout.addWidget(extract_btn)

        layout.addSpacing(15)

        layout.addWidget(QLabel("File Steganography"))

        layout.addWidget(hide_file_btn)
        layout.addWidget(extract_file_btn)

        layout.addSpacing(15)

        layout.addWidget(QLabel("Output"))
        layout.addWidget(self.stego_output)

        widget.setLayout(layout)

        return widget

    # ====================================
    # ML TAB
    # ====================================

    def create_ml_tab(self):

        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Machine Learning Security")

        scan_btn = QPushButton("Security Scan")
        train_btn = QPushButton("Train ML Model")
        risk_btn = QPushButton("Generate Risk Heatmap")

        scan_btn.clicked.connect(self.run_security_scan)
        train_btn.clicked.connect(self.train_ml_model)
        risk_btn.clicked.connect(self.show_risk_heatmap)

        layout.addWidget(title)

        layout.addSpacing(15)

        layout.addWidget(scan_btn)
        layout.addWidget(train_btn)
        layout.addWidget(risk_btn)

        widget.setLayout(layout)

        return widget

    # ====================================
    # IMAGE ANALYSIS TAB
    # ====================================

    def create_analysis_tab(self):

        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Image Forensics")

        histogram_btn = QPushButton("Histogram Analysis")
        bit_plane_btn = QPushButton("Bit Plane Analysis")
        heatmap_btn = QPushButton("Generate Heatmap")

        histogram_btn.clicked.connect(
            self.show_histogram_ui
        )

        bit_plane_btn.clicked.connect(
            self.show_bit_plane_ui
        )

        heatmap_btn.clicked.connect(
            self.generate_heatmap_ui
        )

        layout.addWidget(title)

        layout.addSpacing(15)

        layout.addWidget(histogram_btn)
        layout.addWidget(bit_plane_btn)
        layout.addWidget(heatmap_btn)

        widget.setLayout(layout)

        return widget

    # ====================================
    # ATTACK TAB
    # ====================================

    def create_attack_tab(self):

        widget = QWidget()
        layout = QVBoxLayout()

        self.attack_input = QTextEdit()
        self.attack_input.setPlaceholderText(
            "Enter encrypted text..."
        )

        crack_btn = QPushButton("Crack Caesar")
        crack_btn.clicked.connect(
            self.run_caesar_attack
        )

        self.attack_output = QTextEdit()
        self.attack_output.setReadOnly(True)

        layout.addWidget(QLabel("Caesar Cipher Attack"))
        layout.addWidget(self.attack_input)
        layout.addWidget(crack_btn)
        layout.addWidget(self.attack_output)

        widget.setLayout(layout)

        return widget

    # ====================================
    # SELECT IMAGE
    # ====================================

    def select_image(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:

            self.image_path = file_path

            self.stego_label.setText(
                f"Selected: {file_path}"
            )

    # ====================================
    # HIDE MESSAGE
    # ====================================

    def hide_data(self):

        if not self.image_path:

            self.stego_output.setText(
                "Select image first!"
            )

            return

        message = self.stego_input.toPlainText()

        if not message:

            self.stego_output.setText(
                "Enter message!"
            )

            return

        stego_dir = os.path.join(
            os.path.dirname(self.image_path),
            "stego"
        )

        os.makedirs(stego_dir, exist_ok=True)

        base_name = os.path.splitext(
            os.path.basename(self.image_path)
        )[0]

        output_path = os.path.join(
            stego_dir,
            base_name + "_secret.png"
        )

        hide_message(
            self.image_path,
            output_path,
            message
        )

        self.stego_output.setText(
            f"Saved:\n{output_path}"
        )

    # ====================================
    # EXTRACT MESSAGE
    # ====================================

    def extract_data(self):

        if not self.image_path:

            self.stego_output.setText(
                "Select image first!"
            )

            return

        try:

            message = extract_message(
                self.image_path
            )

            self.stego_output.setText(message)

        except Exception:

            self.stego_output.setText(
                "Error extracting message"
            )

    # ====================================
    # HIDE FILE
    # ====================================

    def hide_file_ui(self):

        if not self.image_path:

            self.stego_output.setText(
                "Select image first!"
            )

            return

        secret_file, _ = QFileDialog.getOpenFileName(
            self,
            "Select File"
        )

        if not secret_file:
            return

        output_path = self.image_path.replace(
            ".png",
            "_hidden.png"
        )

        try:

            hide_file(
                self.image_path,
                output_path,
                secret_file
            )

            self.stego_output.setText(
                f"File hidden:\n{output_path}"
            )

        except Exception as e:

            self.stego_output.setText(str(e))

    # ====================================
    # EXTRACT FILE
    # ====================================

    def extract_file_ui(self):

        if not self.image_path:

            self.stego_output.setText(
                "Select image first!"
            )

            return

        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Extracted File"
        )

        if not output_file:
            return

        try:

            extract_file(
                self.image_path,
                output_file
            )

            self.stego_output.setText(
                f"Extracted:\n{output_file}"
            )

        except Exception as e:

            self.stego_output.setText(str(e))

    # ====================================
    # SECURITY SCAN
    # ====================================

    def run_security_scan(self):

        if not self.image_path:
            return

        try:

            result = predict_image(
                self.image_path
            )

            dialog = SecurityScanDialog(result)

            dialog.exec_()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    # ====================================
    # TRAIN ML MODEL
    # ====================================

    def train_ml_model(self):

        try:

            report_data = train_model()

            dialog = MLReportDialog(
                report_data
            )

            dialog.exec_()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    # ====================================
    # HISTOGRAM
    # ====================================

    def show_histogram_ui(self):

        if not self.image_path:

            self.stego_output.setText(
                "Select image first!"
            )

            return

        plot_histogram(self.image_path)

    # ====================================
    # BIT PLANE
    # ====================================

    def show_bit_plane_ui(self):

        if not self.image_path:

            self.stego_output.setText(
                "Select image first!"
            )

            return

        try:

            output = show_bit_plane(
                self.image_path,
                0,
                "bit_plane.png"
            )

            self.stego_output.setText(
                f"Bit plane saved:\n{output}"
            )

        except Exception as e:

            self.stego_output.setText(str(e))

    # ====================================
    # HEATMAP
    # ====================================

    def generate_heatmap_ui(self):

        if not self.image_path:

            self.stego_output.setText(
                "Select original image first!"
            )

            return

        try:

            modified_path = self.image_path.replace(
                ".png",
                "_secret.png"
            )

            output = generate_heatmap(
                self.image_path,
                modified_path
            )

            self.stego_output.setText(
                f"Heatmap saved:\n{output}"
            )

        except Exception as e:

            self.stego_output.setText(str(e))

    # ====================================
    # RISK HEATMAP
    # ====================================

    def show_risk_heatmap(self):

        if not self.image_path:

            self.stego_output.setText(
                "Select image first!"
            )

            return

        try:

            output = block_risk_map(
                self.image_path
            )

            self.stego_output.setText(
                f"Risk heatmap saved:\n{output}"
            )

        except Exception as e:

            self.stego_output.setText(str(e))

    # ====================================
    # CAESAR ATTACK
    # ====================================

    def run_caesar_attack(self):

        text = self.attack_input.toPlainText()

        if not text:
            return

        results = crack_caesar(text)

        best = best_candidate(results)

        output = "=== All Variants ===\n\n"

        for shift, res in results:

            output += (
                f"Shift {shift}: {res}\n"
            )

        output += "\n=== Best Guess ===\n"

        output += (
            f"Shift {best[0]}: {best[1]}"
        )

        self.attack_output.setText(output)


# ========================================
# ML REPORT DIALOG
# ========================================

class MLReportDialog(QDialog):

    def __init__(self, report_data):

        super().__init__()

        self.setWindowTitle(
            "ML Evaluation Report"
        )

        self.setGeometry(
            200,
            200,
            700,
            500
        )

        layout = QVBoxLayout()

        accuracy = round(
            report_data["accuracy"] * 100,
            2
        )

        layout.addWidget(
            QLabel(
                f"Model Accuracy: {accuracy}%"
            )
        )

        metrics = report_data["metrics"]

        def get_metric(m, key):

            return m.get(
                key,
                {
                    "precision": 0,
                    "recall": 0,
                    "f1-score": 0,
                    "support": 0
                }
            )

        normal = get_metric(metrics, "0")
        stego = get_metric(metrics, "1")

        table = QTableWidget()

        table.setRowCount(2)
        table.setColumnCount(5)

        table.setHorizontalHeaderLabels([
            "Class",
            "Precision",
            "Recall",
            "F1-score",
            "Support"
        ])

        # NORMAL

        table.setItem(
            0,
            0,
            QTableWidgetItem("Normal")
        )

        table.setItem(
            0,
            1,
            QTableWidgetItem(
                str(round(
                    normal["precision"],
                    2
                ))
            )
        )

        table.setItem(
            0,
            2,
            QTableWidgetItem(
                str(round(
                    normal["recall"],
                    2
                ))
            )
        )

        table.setItem(
            0,
            3,
            QTableWidgetItem(
                str(round(
                    normal["f1-score"],
                    2
                ))
            )
        )

        table.setItem(
            0,
            4,
            QTableWidgetItem(
                str(normal["support"])
            )
        )

        # STEGO

        table.setItem(
            1,
            0,
            QTableWidgetItem("Stego")
        )

        table.setItem(
            1,
            1,
            QTableWidgetItem(
                str(round(
                    stego["precision"],
                    2
                ))
            )
        )

        table.setItem(
            1,
            2,
            QTableWidgetItem(
                str(round(
                    stego["recall"],
                    2
                ))
            )
        )

        table.setItem(
            1,
            3,
            QTableWidgetItem(
                str(round(
                    stego["f1-score"],
                    2
                ))
            )
        )

        table.setItem(
            1,
            4,
            QTableWidgetItem(
                str(stego["support"])
            )
        )

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(table)

        self.setLayout(layout)


# ========================================
# SECURITY SCAN DIALOG
# ========================================

class SecurityScanDialog(QDialog):

    def __init__(self, result):

        super().__init__()

        self.setWindowTitle(
            "Security Scan Report"
        )

        self.setGeometry(
            250,
            250,
            600,
            400
        )

        layout = QVBoxLayout()

        risk = result.get("risk", 0)

        decision = result.get(
            "decision",
            "Unknown"
        )

        title = QLabel(
            "ML Security Scan Result"
        )

        layout.addWidget(title)

        table = QTableWidget()

        table.setRowCount(2)
        table.setColumnCount(2)

        table.setHorizontalHeaderLabels([
            "Metric",
            "Value"
        ])

        table.setItem(
            0,
            0,
            QTableWidgetItem(
                "Risk Score"
            )
        )

        table.setItem(
            0,
            1,
            QTableWidgetItem(
                f"{risk}%"
            )
        )

        table.setItem(
            1,
            0,
            QTableWidgetItem(
                "Decision"
            )
        )

        table.setItem(
            1,
            1,
            QTableWidgetItem(
                str(decision)
            )
        )

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(table)

        self.setLayout(layout)