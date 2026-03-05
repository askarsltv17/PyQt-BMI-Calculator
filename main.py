import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt

class BMICalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI Calculator Pro")
        self.setFixedSize(350, 450)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)

        self.create_menu()

        # Title
        title = QLabel("BMI Calculator")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Unit Selection
        layout.addWidget(QLabel("Select Unit System:"))
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Metric (kg, m/cm)", "Imperial (lb, in)"])
        layout.addWidget(self.unit_combo)

        # Weight Input
        layout.addWidget(QLabel("Weight:"))
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("e.g. 80")
        layout.addWidget(self.weight_input)

        # Height Input
        layout.addWidget(QLabel("Height:"))
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("e.g. 1.90 or 190")
        layout.addWidget(self.height_input)

        # Calculate Button
        self.calc_button = QPushButton("Calculate BMI")
        self.calc_button.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; font-weight: bold; padding: 10px; border-radius: 5px; }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.calc_button.clicked.connect(self.calculate_bmi)
        layout.addWidget(self.calc_button)

        # Result Labels
        self.result_label = QLabel("BMI: --")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.result_label)

        self.status_label = QLabel("Status: --")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.status_label)

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        
        clear_action = file_menu.addAction("Clear")
        clear_action.triggered.connect(self.clear_fields)
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        help_menu = menu_bar.addMenu("&Help")
        help_action = help_menu.addAction("How to use")
        help_action.triggered.connect(self.show_help)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_input.text().replace(',', '.'))
            height = float(self.height_input.text().replace(',', '.'))
            
            if self.unit_combo.currentIndex() == 0:  # Metric
                # Logic to handle cm instead of m automatically
                if height > 3: 
                    height = height / 100
                bmi = weight / (height ** 2)
            else:  # Imperial
                bmi = (weight / (height ** 2)) * 703

            self.update_result(round(bmi, 2))
        except (ValueError, ZeroDivisionError):
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers.")

    def update_result(self, bmi):
        self.result_label.setText(f"BMI: {bmi}")
        
        if bmi < 18.5:
            status, color = "Underweight", "#3498db"
        elif 18.5 <= bmi < 25:
            status, color = "Normal Weight", "#27ae60"
        elif 25 <= bmi < 30:
            status, color = "Overweight", "#f39c12"
        else:
            status, color = "Obese", "#e74c3c"
            
        self.status_label.setText(f"Status: {status}")
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")

    def clear_fields(self):
        self.weight_input.clear()
        self.height_input.clear()
        self.result_label.setText("BMI: --")
        self.status_label.setText("Status: --")
        self.status_label.setStyleSheet("color: black;")

    def show_help(self):
        QMessageBox.information(self, "Help", "Enter weight and height.\nNote: In Metric, 1.90 and 190 are both accepted.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BMICalculator()
    window.show()
    sys.exit(app.exec())