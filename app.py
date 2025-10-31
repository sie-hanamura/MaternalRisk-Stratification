"""
MATERNAL RISK ASSESSMENT SYSTEM - Desktop Application
PyQt5 Version - DUAL MODEL SUPPORT
Supports both Full Model (with lab) and Basic Model (without lab)
Municipal Health Office Bay, Laguna
"""

import sys
import os
import pickle
import json
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QDoubleSpinBox, QSpinBox, QTextEdit, QTabWidget,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QGroupBox, QGridLayout, QFrame, QScrollArea,
                             QHeaderView, QFileDialog, QCheckBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QPixmap
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import numpy as np

class MaternalRiskApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maternal Risk Assessment System - Bay, Laguna")
        self.setGeometry(100, 100, 1200, 800)
        
        # Load BOTH models
        self.load_models()
        
        # Setup UI
        self.init_ui()
        
        # Apply styling
        self.apply_styles()
        
    def load_models(self):
        """Load BOTH trained ML models and scalers"""
        try:
            # Load FULL model (Model A)
            with open('model_BEST_for_deployment.pkl', 'rb') as f:
                self.model_full = pickle.load(f)
            
            with open('scaler.pkl', 'rb') as f:
                self.scaler_full = pickle.load(f)
            
            with open('model_config.json', 'r') as f:
                self.config_full = json.load(f)
            
            print("✓ Full Model (Model A) loaded successfully")
            
            # Load BASIC model (Model B)
            with open('model_BASIC_for_deployment.pkl', 'rb') as f:
                self.model_basic = pickle.load(f)
            
            with open('scaler_BASIC.pkl', 'rb') as f:
                self.scaler_basic = pickle.load(f)
            
            with open('model_config_BASIC.json', 'r') as f:
                self.config_basic = json.load(f)
            
            print("✓ Basic Model (Model B) loaded successfully")
            
            self.risk_labels = {0: 'Low', 1: 'Moderate', 2: 'High'}
            
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                f"Failed to load models: {e}\n\n" +
                "Make sure these files exist:\n" +
                "- model_BEST_for_deployment.pkl\n" +
                "- scaler.pkl\n" +
                "- model_config.json\n" +
                "- model_BASIC_for_deployment.pkl\n" +
                "- scaler_BASIC.pkl\n" +
                "- model_config_BASIC.json")
            sys.exit(1)
    
    def init_ui(self):
        """Initialize the user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget for different sections
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(False)
        
        # Create tabs
        self.assessment_tab = self.create_assessment_tab()
        self.history_tab = self.create_history_tab()
        self.about_tab = self.create_about_tab()
        
        self.tabs.addTab(self.assessment_tab, "🏥 New Assessment")
        self.tabs.addTab(self.history_tab, "📊 History")
        self.tabs.addTab(self.about_tab, "ℹ️ About")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage("Ready | Dual Model System: Full (90.6%) | Basic (85.2%)")
    
    def create_header(self):
        """Create application header"""
        header = QFrame()
        header.setFrameStyle(QFrame.Box | QFrame.Raised)
        header.setLineWidth(2)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("🤰 MATERNAL RISK ASSESSMENT SYSTEM")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1f77b4; padding: 15px;")
        
        # Subtitle
        subtitle = QLabel("Municipal Health Office Bay, Laguna | AI-Assisted Screening Tool")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; padding-bottom: 10px;")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        header.setLayout(layout)
        
        return header
    
    def create_assessment_tab(self):
        """Create the patient assessment tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Patient Information Section
        patient_group = self.create_patient_info_section()
        scroll_layout.addWidget(patient_group)
        
        # Clinical Measurements Section
        clinical_group = self.create_clinical_section()
        scroll_layout.addWidget(clinical_group)
        
        # Assess Button
        self.assess_btn = QPushButton("🔍 ASSESS RISK")
        self.assess_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.assess_btn.setMinimumHeight(60)
        self.assess_btn.clicked.connect(self.assess_risk)
        scroll_layout.addWidget(self.assess_btn)
        
        # Results Section
        self.results_group = self.create_results_section()
        self.results_group.setVisible(False)
        scroll_layout.addWidget(self.results_group)
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        layout.addWidget(scroll)
        tab.setLayout(layout)
        
        return tab
    
    def create_patient_info_section(self):
        """Create patient information input section"""
        group = QGroupBox("👤 Patient Information")
        group.setFont(QFont("Arial", 12, QFont.Bold))
        layout = QGridLayout()
        
        # Patient ID
        layout.addWidget(QLabel("Patient ID:"), 0, 0)
        self.patient_id = QLineEdit()
        self.patient_id.setPlaceholderText("e.g., P-2024-001")
        layout.addWidget(self.patient_id, 0, 1)
        
        # Health Worker
        layout.addWidget(QLabel("Health Worker:"), 0, 2)
        self.health_worker = QLineEdit()
        self.health_worker.setPlaceholderText("Your name")
        layout.addWidget(self.health_worker, 0, 3)
        
        # Date
        layout.addWidget(QLabel("Date:"), 1, 0)
        date_label = QLabel(datetime.now().strftime("%Y-%m-%d"))
        date_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(date_label, 1, 1)
        
        group.setLayout(layout)
        return group
    
    def create_clinical_section(self):
        """Create clinical measurements input section"""
        group = QGroupBox("🩺 Clinical Measurements")
        group.setFont(QFont("Arial", 12, QFont.Bold))
        layout = QGridLayout()
        
        row = 0
        
        # Age
        layout.addWidget(QLabel("Age (years):"), row, 0)
        self.age_input = QSpinBox()
        self.age_input.setRange(15, 49)
        self.age_input.setValue(25)
        self.age_input.setSuffix(" years")
        layout.addWidget(self.age_input, row, 1)
        layout.addWidget(QLabel("Normal: 18-35"), row, 2)
        row += 1
        
        # Weight
        layout.addWidget(QLabel("Weight (kg):"), row, 0)
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(30.0, 150.0)
        self.weight_input.setValue(60.0)
        self.weight_input.setSuffix(" kg")
        self.weight_input.valueChanged.connect(self.calculate_bmi)
        layout.addWidget(self.weight_input, row, 1)
        layout.addWidget(QLabel(""), row, 2)
        row += 1
        
        # Height
        layout.addWidget(QLabel("Height (cm):"), row, 0)
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(130.0, 200.0)
        self.height_input.setValue(160.0)
        self.height_input.setSuffix(" cm")
        self.height_input.valueChanged.connect(self.calculate_bmi)
        layout.addWidget(self.height_input, row, 1)
        layout.addWidget(QLabel(""), row, 2)
        row += 1
        
        # BMI (calculated)
        layout.addWidget(QLabel("BMI:"), row, 0)
        self.bmi_label = QLabel("23.4")
        self.bmi_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.bmi_label.setStyleSheet("color: green;")
        layout.addWidget(self.bmi_label, row, 1)
        self.bmi_status = QLabel("Normal")
        layout.addWidget(self.bmi_status, row, 2)
        row += 1
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        layout.addWidget(separator, row, 0, 1, 3)
        row += 1
        
        # Systolic BP
        layout.addWidget(QLabel("Systolic BP (mmHg):"), row, 0)
        self.systolic_input = QSpinBox()
        self.systolic_input.setRange(90, 180)
        self.systolic_input.setValue(120)
        self.systolic_input.setSuffix(" mmHg")
        layout.addWidget(self.systolic_input, row, 1)
        layout.addWidget(QLabel("Normal: 90-120"), row, 2)
        row += 1
        
        # Diastolic BP
        layout.addWidget(QLabel("Diastolic BP (mmHg):"), row, 0)
        self.diastolic_input = QSpinBox()
        self.diastolic_input.setRange(60, 120)
        self.diastolic_input.setValue(80)
        self.diastolic_input.setSuffix(" mmHg")
        layout.addWidget(self.diastolic_input, row, 1)
        layout.addWidget(QLabel("Normal: 60-80"), row, 2)
        row += 1
        
        # LAB AVAILABILITY CHECKBOX
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        layout.addWidget(separator2, row, 0, 1, 3)
        row += 1
        
        lab_label = QLabel("📋 Laboratory Test Results:")
        lab_label.setFont(QFont("Arial", 11, QFont.Bold))
        lab_label.setStyleSheet("color: #1f77b4;")
        layout.addWidget(lab_label, row, 0, 1, 3)
        row += 1
        
        self.lab_available = QCheckBox("✓ Laboratory results are available")
        self.lab_available.setFont(QFont("Arial", 10))
        self.lab_available.setChecked(False)  # Default: NOT available
        self.lab_available.stateChanged.connect(self.toggle_lab_fields)
        layout.addWidget(self.lab_available, row, 0, 1, 3)
        row += 1
        
        # Blood Sugar (initially disabled)
        layout.addWidget(QLabel("Blood Sugar (mmol/L):"), row, 0)
        self.blood_sugar_input = QDoubleSpinBox()
        self.blood_sugar_input.setRange(4.0, 18.0)
        self.blood_sugar_input.setValue(5.5)
        self.blood_sugar_input.setSingleStep(0.1)
        self.blood_sugar_input.setSuffix(" mmol/L")
        self.blood_sugar_input.setEnabled(False)  # Disabled by default
        layout.addWidget(self.blood_sugar_input, row, 1)
        self.blood_sugar_note = QLabel("Normal: 4.0-7.0")
        layout.addWidget(self.blood_sugar_note, row, 2)
        row += 1
        
        # Hemoglobin (initially disabled)
        layout.addWidget(QLabel("Hemoglobin (g/dL):"), row, 0)
        self.hemoglobin_input = QDoubleSpinBox()
        self.hemoglobin_input.setRange(9.5, 14.0)
        self.hemoglobin_input.setValue(12.0)
        self.hemoglobin_input.setSingleStep(0.1)
        self.hemoglobin_input.setSuffix(" g/dL")
        self.hemoglobin_input.setEnabled(False)  # Disabled by default
        layout.addWidget(self.hemoglobin_input, row, 1)
        self.hemoglobin_note = QLabel("Normal: 11.0-14.0")
        layout.addWidget(self.hemoglobin_note, row, 2)
        row += 1
        
        # Model selection indicator
        self.model_indicator = QLabel()
        self.model_indicator.setFont(QFont("Arial", 9))
        self.model_indicator.setStyleSheet("color: #666; font-style: italic; padding: 5px;")
        self.update_model_indicator()
        layout.addWidget(self.model_indicator, row, 0, 1, 3)
        
        group.setLayout(layout)
        return group
    
    def toggle_lab_fields(self):
        """Enable/disable lab fields based on checkbox"""
        is_available = self.lab_available.isChecked()
        
        self.blood_sugar_input.setEnabled(is_available)
        self.hemoglobin_input.setEnabled(is_available)
        
        if is_available:
            # Reset styling to normal
            self.blood_sugar_input.setStyleSheet("")
            self.hemoglobin_input.setStyleSheet("")
        else:
            # Gray out disabled fields
            self.blood_sugar_input.setStyleSheet("background-color: #f0f0f0;")
            self.hemoglobin_input.setStyleSheet("background-color: #f0f0f0;")
        
        self.update_model_indicator()
    
    def update_model_indicator(self):
        """Update which model will be used"""
        if self.lab_available.isChecked():
            self.model_indicator.setText(
                "🤖 Using: Full Model (5 features) - Higher Accuracy (90.6%)"
            )
            self.model_indicator.setStyleSheet("color: #28a745; font-style: italic; padding: 5px;")
        else:
            self.model_indicator.setText(
                "🤖 Using: Basic Model (3 features) - Preliminary Screening (85.2%)"
            )
            self.model_indicator.setStyleSheet("color: #856404; font-style: italic; padding: 5px;")
    
    def create_results_section(self):
        """Create results display section"""
        group = QGroupBox("📊 Assessment Results")
        group.setFont(QFont("Arial", 12, QFont.Bold))
        layout = QVBoxLayout()
        
        # Risk Level Display
        self.risk_display = QLabel()
        self.risk_display.setAlignment(Qt.AlignCenter)
        self.risk_display.setFont(QFont("Arial", 24, QFont.Bold))
        self.risk_display.setMinimumHeight(100)
        layout.addWidget(self.risk_display)
        
        # Confidence
        self.confidence_label = QLabel()
        self.confidence_label.setAlignment(Qt.AlignCenter)
        self.confidence_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.confidence_label)
        
        # Model Used Indicator
        self.model_used_label = QLabel()
        self.model_used_label.setAlignment(Qt.AlignCenter)
        self.model_used_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.model_used_label)
        
        # Recommendations
        self.recommendations = QTextEdit()
        self.recommendations.setReadOnly(True)
        self.recommendations.setMinimumHeight(250)
        layout.addWidget(self.recommendations)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Save Assessment")
        self.save_btn.clicked.connect(self.save_assessment)
        btn_layout.addWidget(self.save_btn)
        
        self.print_btn = QPushButton("🖨️ Print Report")
        self.print_btn.clicked.connect(self.print_report)
        btn_layout.addWidget(self.print_btn)
        
        self.new_btn = QPushButton("📝 New Assessment")
        self.new_btn.clicked.connect(self.new_assessment)
        btn_layout.addWidget(self.new_btn)
        
        layout.addLayout(btn_layout)
        
        group.setLayout(layout)
        return group
    
    def create_history_tab(self):
        """Create history viewing tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header with export button
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("📊 Assessment History"))
        
        export_btn = QPushButton("📥 Export to CSV")
        export_btn.clicked.connect(self.export_history)
        header_layout.addWidget(export_btn)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(10)
        self.history_table.setHorizontalHeaderLabels([
            "Date/Time", "Patient ID", "Age", "BMI", "Risk Level", 
            "Confidence", "Model Used", "Health Worker", "Lab Available", "Action"
        ])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.history_table)
        
        tab.setLayout(layout)
        return tab
    
    def create_about_tab(self):
        """Create about/info tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setHtml("""
        <h2>🤰 Maternal Risk Assessment System</h2>
        <h3>Municipal Health Office Bay, Laguna</h3>
        
        <p><b>Version:</b> 2.0 (Dual Model System)</p>
        <p><b>Training Data:</b> 986 maternal health records (2019-2025)</p>
        
        <hr>
        
        <h3>🤖 Dual Model System</h3>
        
        <h4>Model A - Full Model (5 Features)</h4>
        <p><b>Accuracy:</b> 90.6% (Balanced Accuracy: 90.58%)</p>
        <p><b>Model Type:</b> Logistic Regression</p>
        <p><b>Features Used:</b></p>
        <ol>
            <li>BMI - Body Mass Index</li>
            <li>Systolic BP - Blood Pressure (Upper)</li>
            <li>Blood Sugar Level - Glucose Measurement ⚗️</li>
            <li>Hemoglobin Level - Anemia Indicator ⚗️</li>
            <li>Diastolic BP - Blood Pressure (Lower)</li>
        </ol>
        <p><b>Use When:</b> Laboratory test results are available</p>
        
        <h4>Model B - Basic Model (3 Features)</h4>
        <p><b>Accuracy:</b> ~85% (varies by test set)</p>
        <p><b>Model Type:</b> Logistic Regression</p>
        <p><b>Features Used:</b></p>
        <ol>
            <li>BMI - Body Mass Index</li>
            <li>Systolic BP - Blood Pressure (Upper)</li>
            <li>Diastolic BP - Blood Pressure (Lower)</li>
        </ol>
        <p><b>Use When:</b> Laboratory results NOT available (most common scenario)</p>
        <p><b>Note:</b> Provides preliminary screening. Lab tests recommended for moderate/high risk cases.</p>
        
        <hr>
        
        <h3>⚠️ Important Notes</h3>
        <ul>
            <li>This is a <b>screening tool</b>, not a diagnostic system</li>
            <li>Always follow clinical judgment and established protocols</li>
            <li>High-risk cases must be referred to qualified medical professionals</li>
            <li>System works completely offline</li>
            <li>Basic model provides preliminary assessment when lab values unavailable</li>
        </ul>
        
        <hr>
        
        <h3>📋 When to Use Which Model</h3>
        <table border="1" cellpadding="5">
        <tr>
            <th>Scenario</th>
            <th>Model</th>
            <th>Action</th>
        </tr>
        <tr>
            <td>Patient has recent lab results</td>
            <td>Full Model</td>
            <td>Check "Lab results available" ✓</td>
        </tr>
        <tr>
            <td>No lab tests done recently</td>
            <td>Basic Model</td>
            <td>Leave checkbox unchecked</td>
        </tr>
        <tr>
            <td>Basic model shows moderate/high risk</td>
            <td>-</td>
            <td>Recommend getting lab tests for full assessment</td>
        </tr>
        </table>
        
        <hr>
        
        <p><i>Developed as part of thesis research for improving maternal health outcomes 
        in rural communities.</i></p>
        
        <p><b>For support:</b> Municipal Health Office Bay, Laguna</p>
        """)
        
        layout.addWidget(about_text)
        tab.setLayout(layout)
        
        return tab
    
    def calculate_bmi(self):
        """Calculate and update BMI"""
        weight = self.weight_input.value()
        height = self.height_input.value() / 100  # Convert to meters
        
        if height > 0:
            bmi = weight / (height ** 2)
            self.bmi_label.setText(f"{bmi:.1f}")
            
            # Update status and color
            if bmi < 18.5:
                self.bmi_status.setText("⚠️ Underweight")
                self.bmi_label.setStyleSheet("color: orange;")
            elif 18.5 <= bmi < 25:
                self.bmi_status.setText("✅ Normal")
                self.bmi_label.setStyleSheet("color: green;")
            elif 25 <= bmi < 30:
                self.bmi_status.setText("⚠️ Overweight")
                self.bmi_label.setStyleSheet("color: orange;")
            else:
                self.bmi_status.setText("🚨 Obese")
                self.bmi_label.setStyleSheet("color: red;")
    
    def assess_risk(self):
        """Perform risk assessment using appropriate model"""
        try:
            # Get BMI
            weight = self.weight_input.value()
            height = self.height_input.value() / 100
            bmi = weight / (height ** 2)
            
            # Check if lab values are available
            lab_available = self.lab_available.isChecked()
            
            if lab_available:
                # USE FULL MODEL (Model A)
                input_data = pd.DataFrame({
                    'BMI': [bmi],
                    'SystolicBP': [self.systolic_input.value()],
                    'Blood Sugar Level': [self.blood_sugar_input.value()],
                    'Hemoglobin Level': [self.hemoglobin_input.value()],
                    'DiastolicBP': [self.diastolic_input.value()]
                })
                
                input_scaled = self.scaler_full.transform(input_data)
                prediction_num = self.model_full.predict(input_scaled)[0]
                prediction_proba = self.model_full.predict_proba(input_scaled)[0]
                
                model_used = "Full Model (5 features)"
                
            else:
                # USE BASIC MODEL (Model B)
                input_data = pd.DataFrame({
                    'BMI': [bmi],
                    'SystolicBP': [self.systolic_input.value()],
                    'DiastolicBP': [self.diastolic_input.value()]
                })
                
                input_scaled = self.scaler_basic.transform(input_data)
                prediction_num = self.model_basic.predict(input_scaled)[0]
                prediction_proba = self.model_basic.predict_proba(input_scaled)[0]
                
                model_used = "Basic Model (3 features)"
            
            # Get risk level
            risk_level = self.risk_labels[prediction_num]
            confidence = prediction_proba[prediction_num] * 100
            
            # Store for saving
            self.current_assessment = {
                'risk_level': risk_level,
                'confidence': confidence,
                'probabilities': prediction_proba,
                'input_data': input_data,
                'bmi': bmi,
                'model_used': model_used,
                'lab_available': lab_available
            }
            
            # Display results
            self.display_results(risk_level, confidence, prediction_proba, model_used, lab_available)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Assessment failed: {str(e)}")
    
    def display_results(self, risk_level, confidence, probabilities, model_used, lab_available):
        """Display assessment results"""
        # Show results group
        self.results_group.setVisible(True)
        
        # Set risk display
        risk_colors = {
            'Low': 'background-color: #d4edda; color: #155724; border: 3px solid #28a745;',
            'Moderate': 'background-color: #fff3cd; color: #856404; border: 3px solid #ffc107;',
            'High': 'background-color: #f8d7da; color: #721c24; border: 3px solid #dc3545;'
        }
        
        risk_icons = {
            'Low': '✅',
            'Moderate': '⚠️',
            'High': '🚨'
        }
        
        self.risk_display.setText(f"{risk_icons[risk_level]} {risk_level.upper()} RISK")
        self.risk_display.setStyleSheet(f"{risk_colors[risk_level]} border-radius: 10px; padding: 20px;")
        
        # Set confidence
        self.confidence_label.setText(f"Confidence: {confidence:.1f}%")
        
        # Set model used indicator
        if lab_available:
            self.model_used_label.setText(f"✓ {model_used} | Lab values: Included")
            self.model_used_label.setStyleSheet("color: #28a745;")
        else:
            self.model_used_label.setText(f"⚠️ {model_used} | Lab values: Not Available")
            self.model_used_label.setStyleSheet("color: #856404;")
        
        # Set recommendations
        recommendations = self.get_recommendations(risk_level, probabilities, lab_available)
        self.recommendations.setHtml(recommendations)
        
        # Scroll to results
        try:
            scroll_area = self.tabs.currentWidget().findChild(QScrollArea)
            if scroll_area:
                scroll_area.verticalScrollBar().setValue(
                    scroll_area.verticalScrollBar().maximum()
                )
        except:
            pass
    
    def get_recommendations(self, risk_level, probabilities, lab_available):
        """Get recommendations based on risk level"""
        low_prob = probabilities[0] * 100
        mod_prob = probabilities[1] * 100
        high_prob = probabilities[2] * 100
        
        # Add lab warning if basic model used
        lab_warning = ""
        if not lab_available and risk_level in ['Moderate', 'High']:
            lab_warning = """
            <div style='background-color: #fff3cd; padding: 10px; border-radius: 5px; margin: 10px 0; border-left: 5px solid #ffc107;'>
            <b>⚠️ Important:</b> This assessment used the <b>Basic Model</b> (3 features only) because 
            laboratory results were not available. For more accurate risk classification, blood tests 
            (hemoglobin and blood sugar) are <b>strongly recommended</b> for this patient.
            </div>
            """
        
        if risk_level == 'Low':
            return lab_warning + f"""
            <h3 style="color: #28a745;">✅ Low Risk - Routine Care</h3>
            <p><b>Probability Breakdown:</b></p>
            <ul>
                <li>Low Risk: {low_prob:.1f}%</li>
                <li>Moderate Risk: {mod_prob:.1f}%</li>
                <li>High Risk: {high_prob:.1f}%</li>
            </ul>
            <h4>📋 Recommended Actions:</h4>
            <ul>
                <li><b>Continue regular prenatal checkups</b> (monthly)</li>
                <li>Maintain healthy diet and moderate exercise</li>
                <li>Monitor for any changes in symptoms</li>
                <li>Return immediately if any warning signs appear</li>
                <li>Next checkup: Schedule in 4 weeks</li>
                {'<li><b>Consider getting lab tests</b> for complete assessment (if not yet done)</li>' if not lab_available else ''}
            </ul>
            <p><i>✓ Patient can be managed at barangay health center level.</i></p>
            """
        
        elif risk_level == 'Moderate':
            return lab_warning + f"""
            <h3 style="color: #856404;">⚠️ Moderate Risk - Enhanced Monitoring</h3>
            <p><b>Probability Breakdown:</b></p>
            <ul>
                <li>Low Risk: {low_prob:.1f}%</li>
                <li>Moderate Risk: {mod_prob:.1f}%</li>
                <li>High Risk: {high_prob:.1f}%</li>
            </ul>
            <h4>📋 Recommended Actions:</h4>
            <ul>
                <li><b>Refer to Rural Health Unit (RHU)</b> for evaluation</li>
                {'<li><b style="color: red;">PRIORITY: Get laboratory tests</b> (blood sugar & hemoglobin) before RHU visit</li>' if not lab_available else ''}
                <li>Increase prenatal visits (bi-weekly or as advised)</li>
                <li>Monitor blood pressure and blood sugar regularly</li>
                <li>Educate on warning signs to watch for</li>
                <li>May need additional tests or specialist consultation</li>
            </ul>
            <p><i>⚠️ Coordinate with RHU midwife or physician for management plan.</i></p>
            """
        
        else:  # High
            return lab_warning + f"""
            <h3 style="color: #721c24;">🚨 High Risk - URGENT REFERRAL NEEDED</h3>
            <p><b>Probability Breakdown:</b></p>
            <ul>
                <li>Low Risk: {low_prob:.1f}%</li>
                <li>Moderate Risk: {mod_prob:.1f}%</li>
                <li>High Risk: {high_prob:.1f}%</li>
            </ul>
            <h4>📋 Recommended Actions:</h4>
            <ul>
                <li><b style="color: red;">IMMEDIATE referral to hospital/OB-GYN</b></li>
                {'<li><b style="color: red;">URGENT: Arrange laboratory tests en route to hospital</b></li>' if not lab_available else ''}
                <li>Patient needs specialist care and close monitoring</li>
                <li>High-risk pregnancy requiring advanced interventions</li>
                <li>Weekly or more frequent prenatal visits required</li>
                <li>Prepare for potential complications</li>
            </ul>
            <p><b style="color: red;">⚠️ DO NOT DELAY: Refer to nearest hospital with OB-GYN services immediately.</b></p>
            """
    
    def save_assessment(self):
        """Save the current assessment"""
        try:
            # Prepare record
            record = {
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Patient_ID': self.patient_id.text() or 'N/A',
                'Age': self.age_input.value(),
                'BMI': self.current_assessment['bmi'],
                'SystolicBP': self.systolic_input.value(),
                'DiastolicBP': self.diastolic_input.value(),
                'Blood_Sugar': self.blood_sugar_input.value() if self.current_assessment['lab_available'] else 'N/A',
                'Hemoglobin': self.hemoglobin_input.value() if self.current_assessment['lab_available'] else 'N/A',
                'Risk_Level': self.current_assessment['risk_level'],
                'Confidence': f"{self.current_assessment['confidence']:.1f}%",
                'Model_Used': self.current_assessment['model_used'],
                'Lab_Available': 'Yes' if self.current_assessment['lab_available'] else 'No',
                'Health_Worker': self.health_worker.text() or 'N/A'
            }
            
            # Save to CSV
            history_file = 'assessment_history.csv'
            if os.path.exists(history_file):
                df = pd.read_csv(history_file)
                df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            else:
                df = pd.DataFrame([record])
            
            df.to_csv(history_file, index=False)
            
            # Refresh history table
            self.load_history()
            
            QMessageBox.information(self, "Success", "✅ Assessment saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def print_report(self):
        """Print assessment report"""
        try:
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            
            if dialog.exec_() == QPrintDialog.Accepted:
                self.recommendations.document().print_(printer)
                QMessageBox.information(self, "Success", "Report sent to printer!")
        except Exception as e:
            QMessageBox.warning(self, "Print Error", f"Could not print: {str(e)}")
    
    def new_assessment(self):
        """Start a new assessment"""
        # Clear all inputs
        self.patient_id.clear()
        self.health_worker.clear()
        self.age_input.setValue(25)
        self.weight_input.setValue(60.0)
        self.height_input.setValue(160.0)
        self.systolic_input.setValue(120)
        self.diastolic_input.setValue(80)
        self.blood_sugar_input.setValue(5.5)
        self.hemoglobin_input.setValue(12.0)
        
        # Reset lab checkbox
        self.lab_available.setChecked(False)
        
        # Hide results
        self.results_group.setVisible(False)
        
        # Scroll to top
        try:
            scroll_area = self.tabs.currentWidget().findChild(QScrollArea)
            if scroll_area:
                scroll_area.verticalScrollBar().setValue(0)
        except:
            pass
    
    def load_history(self):
        """Load assessment history into table"""
        try:
            if not os.path.exists('assessment_history.csv'):
                return
            
            df = pd.read_csv('assessment_history.csv')
            
            self.history_table.setRowCount(len(df))
            
            for idx, row in df.iterrows():
                self.history_table.setItem(idx, 0, QTableWidgetItem(row['Timestamp']))
                self.history_table.setItem(idx, 1, QTableWidgetItem(str(row['Patient_ID'])))
                self.history_table.setItem(idx, 2, QTableWidgetItem(str(row['Age'])))
                self.history_table.setItem(idx, 3, QTableWidgetItem(f"{row['BMI']:.1f}"))
                
                # Risk level with color
                risk_item = QTableWidgetItem(row['Risk_Level'])
                if row['Risk_Level'] == 'Low':
                    risk_item.setBackground(QColor(212, 237, 218))
                elif row['Risk_Level'] == 'Moderate':
                    risk_item.setBackground(QColor(255, 243, 205))
                else:
                    risk_item.setBackground(QColor(248, 215, 218))
                self.history_table.setItem(idx, 4, risk_item)
                
                self.history_table.setItem(idx, 5, QTableWidgetItem(row['Confidence']))
                
                # Model used
                model_item = QTableWidgetItem(row.get('Model_Used', 'Full Model'))
                self.history_table.setItem(idx, 6, model_item)
                
                self.history_table.setItem(idx, 7, QTableWidgetItem(row['Health_Worker']))
                
                # Lab available
                lab_item = QTableWidgetItem(row.get('Lab_Available', 'Unknown'))
                if row.get('Lab_Available') == 'Yes':
                    lab_item.setBackground(QColor(212, 237, 218))
                else:
                    lab_item.setBackground(QColor(255, 243, 205))
                self.history_table.setItem(idx, 8, lab_item)
                
                # Action
                self.history_table.setItem(idx, 9, QTableWidgetItem("✓ Saved"))
                
        except Exception as e:
            print(f"Error loading history: {e}")
    
    def export_history(self):
        """Export history to CSV"""
        try:
            if not os.path.exists('assessment_history.csv'):
                QMessageBox.warning(self, "No Data", "No assessment history to export.")
                return
            
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Export History",
                f"maternal_assessment_{datetime.now().strftime('%Y%m%d')}.csv",
                "CSV Files (*.csv)"
            )
            
            if filename:
                df = pd.read_csv('assessment_history.csv')
                df.to_csv(filename, index=False)
                QMessageBox.information(self, "Success", f"History exported to:\n{filename}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {e}")
    
    def apply_styles(self):
        """Apply custom styling to the application"""
        style = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #1f77b4;
            border-radius: 8px;
            margin-top: 10px;
            padding: 15px;
            background-color: white;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #1f77b4;
        }
        
        QPushButton {
            background-color: #1f77b4;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 12pt;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #155a8a;
        }
        
        QPushButton:pressed {
            background-color: #0d3a5c;
        }
        
        QLineEdit, QSpinBox, QDoubleSpinBox {
            padding: 8px;
            border: 2px solid #ccc;
            border-radius: 4px;
            font-size: 11pt;
        }
        
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
            border: 2px solid #1f77b4;
        }
        
        QCheckBox {
            font-size: 11pt;
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
        }
        
        QTabWidget::pane {
            border: 2px solid #1f77b4;
            border-radius: 5px;
            background-color: white;
        }
        
        QTabBar::tab {
            background-color: #e0e0e0;
            padding: 10px 20px;
            margin: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            font-size: 11pt;
            font-weight: bold;
        }
        
        QTabBar::tab:selected {
            background-color: #1f77b4;
            color: white;
        }
        
        QTableWidget {
            border: 1px solid #ccc;
            gridline-color: #e0e0e0;
            font-size: 10pt;
        }
        
        QTableWidget::item {
            padding: 5px;
        }
        
        QHeaderView::section {
            background-color: #1f77b4;
            color: white;
            padding: 8px;
            font-weight: bold;
            border: none;
        }
        
        QTextEdit {
            border: 2px solid #ccc;
            border-radius: 4px;
            padding: 10px;
            font-size: 11pt;
        }
        
        QScrollBar:vertical {
            background: #f0f0f0;
            width: 12px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background: #1f77b4;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #155a8a;
        }
        """
        
        self.setStyleSheet(style)
    
    def closeEvent(self, event):
        """Handle application close"""
        reply = QMessageBox.question(
            self,
            'Confirm Exit',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("Maternal Risk Assessment System")
    app.setOrganizationName("Municipal Health Office Bay, Laguna")
    
    # Create and show main window
    window = MaternalRiskApp()
    window.show()
    
    # Load existing history
    window.load_history()
    
    # Run application
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()