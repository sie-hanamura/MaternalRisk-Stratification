"""
MATERNAL RISK ASSESSMENT SYSTEM - Desktop Application
PyQt5 Version - MODERN UI DESIGN
Municipal Health Office Bay, Laguna
"""

import sys
import os
import pickle
import json
import pandas as pd
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import numpy as np

# Design System Colors
COLORS = {
    'primary_dark': '#1e3a4c', 'primary': '#4FC3C9', 'primary_light': '#b8e6e9',
    'primary_subtle': '#e8f4f8', 'success': '#48BB78', 'success_bg': '#C6F6D5',
    'success_text': '#22543D', 'warning': '#F6AD55', 'warning_bg': '#FEF3C7',
    'warning_text': '#92400E', 'danger': '#FC8181', 'danger_bg': '#FED7D7',
    'danger_text': '#742A2A', 'info': '#60A5FA', 'info_bg': '#DBEAFE',
    'info_text': '#1E3A8A', 'gray_900': '#0f172a', 'gray_600': '#475569',
    'gray_400': '#94a3b8', 'gray_200': '#e2e8f0', 'gray_50': '#f8fafc',
    'white': '#ffffff'
}

class ModernCard(QFrame):
    def __init__(self, title=None, parent=None):
        super().__init__(parent)
        self.setObjectName("modernCard")
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        if title:
            title_label = QLabel(title)
            title_label.setObjectName("cardTitle")
            layout.addWidget(title_label)
        self.content_layout = layout
        self.setLayout(layout)

class RiskIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.risk_level = "Low"
        self.confidence = 46.3
        self.setMinimumSize(200, 200)
    
    def set_risk(self, level, confidence):
        self.risk_level = level
        self.confidence = confidence
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.risk_level == "Low":
            color = QColor(COLORS['success'])
        elif self.risk_level == "Moderate":
            color = QColor(COLORS['warning'])
        else:
            color = QColor(COLORS['danger'])
        
        rect = self.rect().adjusted(10, 10, -10, -10)
        painter.setPen(Qt.NoPen)
        painter.setBrush(color.lighter(150))
        painter.drawEllipse(rect)
        
        inner_rect = rect.adjusted(15, 15, -15, -15)
        painter.setBrush(color)
        painter.drawEllipse(inner_rect)
        
        painter.setPen(QColor(COLORS['white']))
        font = QFont("Inter", 24, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f"{self.confidence:.1f}%")

class MaternalRiskApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maternal Risk Assessment System - Bay, Laguna")
        self.setGeometry(100, 50, 1400, 900)
        self.load_models()
        self.init_ui()
        self.apply_modern_styles()
    
    def load_models(self):
        try:
            with open('model_BEST_for_deployment.pkl', 'rb') as f:
                self.model_full = pickle.load(f)
            with open('scaler.pkl', 'rb') as f:
                self.scaler_full = pickle.load(f)
            with open('model_config.json', 'r') as f:
                self.config_full = json.load(f)
            with open('model_BASIC_for_deployment.pkl', 'rb') as f:
                self.model_basic = pickle.load(f)
            with open('scaler_BASIC.pkl', 'rb') as f:
                self.scaler_basic = pickle.load(f)
            with open('model_config_BASIC.json', 'r') as f:
                self.config_basic = json.load(f)
            self.risk_labels = {0: 'Low', 1: 'Moderate', 2: 'High'}
            print("✓ Models loaded successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load models: {e}")
            sys.exit(1)
    
    def init_ui(self):
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        header = self.create_modern_header()
        main_layout.addWidget(header)
        
        self.tabs = QTabWidget()
        self.tabs.setObjectName("modernTabs")
        self.assessment_tab = self.create_modern_assessment_tab()
        self.history_tab = self.create_history_tab()
        self.about_tab = self.create_about_tab()
        self.tabs.addTab(self.assessment_tab, "New Assessment")
        self.tabs.addTab(self.history_tab, "History")
        self.tabs.addTab(self.about_tab, "About")
        
        main_layout.addWidget(self.tabs)
        self.statusBar().showMessage("Ready | Dual Model: Full (90.6%) | Basic (85.2%)")
    
    def create_modern_header(self):
        header = QFrame()
        header.setObjectName("modernHeader")
        header.setFixedHeight(100)
        layout = QHBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        
        # Logo and title container
        left_layout = QHBoxLayout()
        left_layout.setSpacing(16)
        
        # Logo
        logo_label = QLabel()
        try:
            # Try multiple possible paths
            possible_paths = [
                "assets/heart.png",
                "./assets/heart.png",
                "heart.png",
                os.path.join(os.path.dirname(__file__), "assets", "heart.png")
            ]
            
            pixmap = None
            for path in possible_paths:
                if os.path.exists(path):
                    pixmap = QPixmap(path)
                    if not pixmap.isNull():
                        print(f"Logo loaded from: {path}")
                        break
            
            if pixmap and not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
            else:
                print("Logo not found, using fallback")
                logo_label.setText("♥")
                logo_label.setStyleSheet("font-size: 48px; color: #4FC3C9;")
        except Exception as e:
            print(f"Error loading logo: {e}")
            logo_label.setText("♥")
            logo_label.setStyleSheet("font-size: 48px; color: #4FC3C9;")
        
        logo_label.setFixedSize(60, 60)
        logo_label.setAlignment(Qt.AlignCenter)
        
        # Title and subtitle
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        title = QLabel("MATERNAL RISK ASSESSMENT SYSTEM")
        title.setObjectName("headerTitle")
        subtitle = QLabel("Municipal Health Office Bay, Laguna | AI-Assisted Screening Tool")
        subtitle.setObjectName("headerSubtitle")
        
        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)
        
        left_layout.addWidget(logo_label)
        left_layout.addLayout(text_layout)
        
        layout.addLayout(left_layout)
        layout.addStretch()
        header.setLayout(layout)
        return header
    
    def create_modern_assessment_tab(self):
        tab = QWidget()
        tab.setObjectName("assessmentTab")
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)
        
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setObjectName("modernScroll")
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(24)
        
        patient_card = self.create_patient_info_card()
        left_layout.addWidget(patient_card)
        clinical_card = self.create_clinical_measurements_card()
        left_layout.addWidget(clinical_card)
        
        self.assess_btn = QPushButton("Calculate Risk Assessment")
        self.assess_btn.setObjectName("primaryButton")
        self.assess_btn.setMinimumHeight(56)
        self.assess_btn.setCursor(Qt.PointingHandCursor)
        self.assess_btn.clicked.connect(self.assess_risk)
        left_layout.addWidget(self.assess_btn)
        left_layout.addStretch()
        left_widget.setLayout(left_layout)
        left_scroll.setWidget(left_widget)
        
        self.right_panel = self.create_results_panel()
        main_layout.addWidget(left_scroll, 60)
        main_layout.addWidget(self.right_panel, 40)
        tab.setLayout(main_layout)
        return tab
    
    def create_patient_info_card(self):
        card = ModernCard("Patient Information")
        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(16)
        form_layout.setHorizontalSpacing(16)
        
        patient_id_label = QLabel("Patient ID")
        patient_id_label.setObjectName("formLabel")
        self.patient_id = QLineEdit()
        self.patient_id.setObjectName("modernInput")
        self.patient_id.setPlaceholderText("e.g., P-2024-001")
        
        worker_label = QLabel("Health Worker")
        worker_label.setObjectName("formLabel")
        self.health_worker = QLineEdit()
        self.health_worker.setObjectName("modernInput")
        self.health_worker.setPlaceholderText("Your name")
        
        date_label = QLabel("Date")
        date_label.setObjectName("formLabel")
        date_value = QLabel(datetime.now().strftime("%Y-%m-%d"))
        date_value.setObjectName("formValue")
        
        form_layout.addWidget(patient_id_label, 0, 0)
        form_layout.addWidget(self.patient_id, 1, 0)
        form_layout.addWidget(worker_label, 0, 1)
        form_layout.addWidget(self.health_worker, 1, 1)
        form_layout.addWidget(date_label, 2, 0)
        form_layout.addWidget(date_value, 3, 0, 1, 2)
        card.content_layout.addLayout(form_layout)
        return card
    
    def create_clinical_measurements_card(self):
        card = ModernCard("Clinical Measurements")
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)
        
        age_layout = self.create_input_row("Age (years)", "Normal: 18-35")
        self.age_input = QSpinBox()
        self.age_input.setObjectName("modernSpinBox")
        self.age_input.setRange(15, 49)
        self.age_input.setValue(25)
        age_layout.insertWidget(1, self.age_input)
        form_layout.addLayout(age_layout)
        
        wh_layout = QHBoxLayout()
        wh_layout.setSpacing(16)
        weight_layout = self.create_input_row("Weight (kg)", "")
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setObjectName("modernSpinBox")
        self.weight_input.setRange(30.0, 150.0)
        self.weight_input.setValue(60.0)
        self.weight_input.valueChanged.connect(self.calculate_bmi)
        weight_layout.insertWidget(1, self.weight_input)
        
        height_layout = self.create_input_row("Height (cm)", "")
        self.height_input = QDoubleSpinBox()
        self.height_input.setObjectName("modernSpinBox")
        self.height_input.setRange(130.0, 200.0)
        self.height_input.setValue(160.0)
        self.height_input.valueChanged.connect(self.calculate_bmi)
        height_layout.insertWidget(1, self.height_input)
        wh_layout.addLayout(weight_layout)
        wh_layout.addLayout(height_layout)
        form_layout.addLayout(wh_layout)
        
        bmi_container = QHBoxLayout()
        bmi_label_text = QLabel("BMI:")
        bmi_label_text.setObjectName("formLabel")
        self.bmi_label = QLabel("23.4")
        self.bmi_label.setObjectName("bmiBadge")
        self.bmi_status = QLabel("Normal")
        self.bmi_status.setObjectName("bmiStatus")
        bmi_container.addWidget(bmi_label_text)
        bmi_container.addWidget(self.bmi_label)
        bmi_container.addWidget(self.bmi_status)
        bmi_container.addStretch()
        form_layout.addLayout(bmi_container)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setObjectName("divider")
        form_layout.addWidget(divider)
        
        bp_layout = QHBoxLayout()
        bp_layout.setSpacing(16)
        systolic_layout = self.create_input_row("Systolic BP", "Normal: 90-120")
        self.systolic_input = QSpinBox()
        self.systolic_input.setObjectName("modernSpinBox")
        self.systolic_input.setRange(90, 180)
        self.systolic_input.setValue(120)
        systolic_layout.insertWidget(1, self.systolic_input)
        
        diastolic_layout = self.create_input_row("Diastolic BP", "Normal: 60-80")
        self.diastolic_input = QSpinBox()
        self.diastolic_input.setObjectName("modernSpinBox")
        self.diastolic_input.setRange(60, 120)
        self.diastolic_input.setValue(80)
        diastolic_layout.insertWidget(1, self.diastolic_input)
        bp_layout.addLayout(systolic_layout)
        bp_layout.addLayout(diastolic_layout)
        form_layout.addLayout(bp_layout)
        
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.HLine)
        divider2.setObjectName("divider")
        form_layout.addWidget(divider2)
        
        lab_title = QLabel("Laboratory Test Results")
        lab_title.setObjectName("sectionTitle")
        form_layout.addWidget(lab_title)
        
        self.lab_available = QCheckBox("Laboratory results available")
        self.lab_available.setObjectName("modernCheckbox")
        self.lab_available.setChecked(False)
        self.lab_available.stateChanged.connect(self.toggle_lab_fields)
        form_layout.addWidget(self.lab_available)
        
        lab_values_layout = QHBoxLayout()
        lab_values_layout.setSpacing(16)
        bs_layout = self.create_input_row("Blood Sugar (mmol/L)", "Normal: 4.0-7.0")
        self.blood_sugar_input = QDoubleSpinBox()
        self.blood_sugar_input.setObjectName("modernSpinBox")
        self.blood_sugar_input.setRange(4.0, 18.0)
        self.blood_sugar_input.setValue(5.5)
        self.blood_sugar_input.setSingleStep(0.1)
        self.blood_sugar_input.setEnabled(False)
        bs_layout.insertWidget(1, self.blood_sugar_input)
        
        hb_layout = self.create_input_row("Hemoglobin (g/dL)", "Normal: 11-14")
        self.hemoglobin_input = QDoubleSpinBox()
        self.hemoglobin_input.setObjectName("modernSpinBox")
        self.hemoglobin_input.setRange(9.5, 14.0)
        self.hemoglobin_input.setValue(12.0)
        self.hemoglobin_input.setSingleStep(0.1)
        self.hemoglobin_input.setEnabled(False)
        hb_layout.insertWidget(1, self.hemoglobin_input)
        lab_values_layout.addLayout(bs_layout)
        lab_values_layout.addLayout(hb_layout)
        form_layout.addLayout(lab_values_layout)
        
        self.model_indicator = QLabel()
        self.model_indicator.setObjectName("modelIndicator")
        self.model_indicator.setWordWrap(True)
        self.update_model_indicator()
        form_layout.addWidget(self.model_indicator)
        card.content_layout.addLayout(form_layout)
        return card
    
    def create_input_row(self, label, hint):
        layout = QVBoxLayout()
        layout.setSpacing(4)
        label_widget = QLabel(label)
        label_widget.setObjectName("formLabel")
        layout.addWidget(label_widget)
        if hint:
            hint_widget = QLabel(hint)
            hint_widget.setObjectName("formHint")
            layout.addWidget(hint_widget)
        return layout
    
    def create_results_panel(self):
        panel = QWidget()
        panel.setObjectName("resultsPanel")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        self.results_card = ModernCard("Assessment Results")
        self.results_card.setVisible(False)
        results_layout = QVBoxLayout()
        results_layout.setSpacing(24)
        
        risk_container = QWidget()
        risk_container.setObjectName("riskContainer")
        risk_layout = QVBoxLayout()
        risk_layout.setAlignment(Qt.AlignCenter)
        
        self.risk_text = QLabel("LOW RISK")
        self.risk_text.setObjectName("riskText")
        self.risk_text.setAlignment(Qt.AlignCenter)
        self.risk_indicator = RiskIndicator()
        confidence_label = QLabel("Confidence Level")
        confidence_label.setObjectName("confidenceLabel")
        confidence_label.setAlignment(Qt.AlignCenter)
        
        risk_layout.addWidget(self.risk_text)
        risk_layout.addWidget(self.risk_indicator)
        risk_layout.addWidget(confidence_label)
        risk_container.setLayout(risk_layout)
        results_layout.addWidget(risk_container)
        
        self.model_used_label = QLabel()
        self.model_used_label.setObjectName("modelUsedLabel")
        self.model_used_label.setWordWrap(True)
        self.model_used_label.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(self.model_used_label)
        
        rec_title = QLabel("Recommended Actions")
        rec_title.setObjectName("sectionTitle")
        results_layout.addWidget(rec_title)
        
        self.recommendations = QTextEdit()
        self.recommendations.setObjectName("recommendationsText")
        self.recommendations.setReadOnly(True)
        results_layout.addWidget(self.recommendations)
        
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(12)
        self.save_btn = QPushButton("Save Assessment")
        self.save_btn.setObjectName("successButton")
        self.save_btn.setMinimumHeight(44)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_assessment)
        
        self.print_btn = QPushButton("Print Report")
        self.print_btn.setObjectName("secondaryButton")
        self.print_btn.setMinimumHeight(44)
        self.print_btn.setCursor(Qt.PointingHandCursor)
        self.print_btn.clicked.connect(self.print_report)
        
        self.new_btn = QPushButton("New Assessment")
        self.new_btn.setObjectName("outlineButton")
        self.new_btn.setMinimumHeight(44)
        self.new_btn.setCursor(Qt.PointingHandCursor)
        self.new_btn.clicked.connect(self.new_assessment)
        
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.print_btn)
        btn_layout.addWidget(self.new_btn)
        results_layout.addLayout(btn_layout)
        self.results_card.content_layout.addLayout(results_layout)
        layout.addWidget(self.results_card)
        layout.addStretch()
        panel.setLayout(layout)
        return panel
    
    def toggle_lab_fields(self):
        is_available = self.lab_available.isChecked()
        self.blood_sugar_input.setEnabled(is_available)
        self.hemoglobin_input.setEnabled(is_available)
        self.update_model_indicator()
    
    def update_model_indicator(self):
        if self.lab_available.isChecked():
            self.model_indicator.setText("Using: Full Model (5 features) - 90.6% accuracy")
            self.model_indicator.setProperty("indicatorType", "full")
        else:
            self.model_indicator.setText("Using: Basic Model (3 features) - 85.2% accuracy")
            self.model_indicator.setProperty("indicatorType", "basic")
        self.model_indicator.style().unpolish(self.model_indicator)
        self.model_indicator.style().polish(self.model_indicator)
    
    def calculate_bmi(self):
        weight = self.weight_input.value()
        height = self.height_input.value() / 100
        if height > 0:
            bmi = weight / (height ** 2)
            self.bmi_label.setText(f"{bmi:.1f}")
            if bmi < 18.5:
                self.bmi_status.setText("Underweight")
                bmi_type = "warning"
            elif 18.5 <= bmi < 25:
                self.bmi_status.setText("Normal")
                bmi_type = "success"
            elif 25 <= bmi < 30:
                self.bmi_status.setText("Overweight")
                bmi_type = "warning"
            else:
                self.bmi_status.setText("Obese")
                bmi_type = "danger"
            self.bmi_label.setProperty("bmiType", bmi_type)
            self.bmi_status.setProperty("bmiType", bmi_type)
            self.bmi_label.style().unpolish(self.bmi_label)
            self.bmi_label.style().polish(self.bmi_label)
            self.bmi_status.style().unpolish(self.bmi_status)
            self.bmi_status.style().polish(self.bmi_status)
    
    def assess_risk(self):
        try:
            weight = self.weight_input.value()
            height = self.height_input.value() / 100
            bmi = weight / (height ** 2)
            lab_available = self.lab_available.isChecked()
            
            if lab_available:
                input_data = pd.DataFrame({
                    'BMI': [bmi], 'SystolicBP': [self.systolic_input.value()],
                    'Blood Sugar Level': [self.blood_sugar_input.value()],
                    'Hemoglobin Level': [self.hemoglobin_input.value()],
                    'DiastolicBP': [self.diastolic_input.value()]
                })
                input_scaled = self.scaler_full.transform(input_data)
                prediction_num = self.model_full.predict(input_scaled)[0]
                prediction_proba = self.model_full.predict_proba(input_scaled)[0]
                model_used = "Full Model (5 features)"
            else:
                input_data = pd.DataFrame({
                    'BMI': [bmi], 'SystolicBP': [self.systolic_input.value()],
                    'DiastolicBP': [self.diastolic_input.value()]
                })
                input_scaled = self.scaler_basic.transform(input_data)
                prediction_num = self.model_basic.predict(input_scaled)[0]
                prediction_proba = self.model_basic.predict_proba(input_scaled)[0]
                model_used = "Basic Model (3 features)"
            
            risk_level = self.risk_labels[prediction_num]
            confidence = prediction_proba[prediction_num] * 100
            self.current_assessment = {
                'risk_level': risk_level, 'confidence': confidence,
                'probabilities': prediction_proba, 'input_data': input_data,
                'bmi': bmi, 'model_used': model_used, 'lab_available': lab_available
            }
            self.display_results(risk_level, confidence, prediction_proba, model_used, lab_available)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Assessment failed: {str(e)}")
    
    def display_results(self, risk_level, confidence, probabilities, model_used, lab_available):
        self.results_card.setVisible(True)
        risk_icons = {'Low': '[LOW]', 'Moderate': '[MODERATE]', 'High': '[HIGH]'}
        self.risk_text.setText(f"{risk_icons[risk_level]} {risk_level.upper()} RISK")
        self.risk_text.setProperty("riskType", risk_level.lower())
        self.risk_text.style().unpolish(self.risk_text)
        self.risk_text.style().polish(self.risk_text)
        self.risk_indicator.set_risk(risk_level, confidence)
        
        if lab_available:
            self.model_used_label.setText(f"[FULL] {model_used} | Lab: Included")
            self.model_used_label.setProperty("modelType", "full")
        else:
            self.model_used_label.setText(f"[BASIC] {model_used} | Lab: Not Available")
            self.model_used_label.setProperty("modelType", "basic")
        self.model_used_label.style().unpolish(self.model_used_label)
        self.model_used_label.style().polish(self.model_used_label)
        
        recommendations = self.get_recommendations(risk_level, probabilities, lab_available)
        self.recommendations.setHtml(recommendations)
    
    def get_recommendations(self, risk_level, probabilities, lab_available):
        low, mod, high = probabilities[0]*100, probabilities[1]*100, probabilities[2]*100
        lab_warn = ""
        if not lab_available and risk_level in ['Moderate', 'High']:
            lab_warn = "<div style='background:#FEF3C7;padding:12px;border-radius:8px;margin:12px 0;border-left:4px solid #F6AD55'><b style='color:#92400E'>Important:</b> Basic Model used. Lab tests <b>strongly recommended</b>.</div>"
        
        style = "font-family:Inter,sans-serif;font-size:13px;line-height:1.6;color:#475569;"
        
        if risk_level == 'Low':
            lab_note = "<li><b>Get lab tests</b> for complete assessment</li>" if not lab_available else ""
            return (
                f"<div style='{style}'>{lab_warn}"
                f"<h3 style='color:#48BB78'>Low Risk - Routine Care</h3>"
                f"<div style='background:#f8fafc;padding:12px;border-radius:8px;margin:12px 0'>"
                f"<b>Probability:</b> Low:{low:.1f}% | Mod:{mod:.1f}% | High:{high:.1f}%</div>"
                f"<b>Actions:</b><ul>"
                f"<li>Regular prenatal checkups (monthly)</li>"
                f"<li>Healthy diet and exercise</li>"
                f"<li>Monitor symptoms</li>"
                f"<li>Return if warning signs</li>"
                f"<li>Next: 4 weeks</li>"
                f"{lab_note}"
                f"</ul>"
                f"<p style='font-style:italic;color:#48BB78'>Patient can be managed at barangay health center level</p>"
                f"</div>"
            )
        elif risk_level == 'Moderate':
            lab_priority = "<li style='color:#FC8181'><b>PRIORITY: Get lab tests</b> before RHU visit</li>" if not lab_available else ""
            return (
                f"<div style='{style}'>{lab_warn}"
                f"<h3 style='color:#F6AD55'>Moderate Risk - Enhanced Monitoring</h3>"
                f"<div style='background:#f8fafc;padding:12px;border-radius:8px;margin:12px 0'>"
                f"<b>Probability:</b> Low:{low:.1f}% | Mod:{mod:.1f}% | High:{high:.1f}%</div>"
                f"<b>Actions:</b><ul>"
                f"<li><b>Refer to RHU</b> for evaluation</li>"
                f"{lab_priority}"
                f"<li>Bi-weekly prenatal visits</li>"
                f"<li>Monitor BP and blood sugar</li>"
                f"<li>Watch for warning signs</li>"
                f"</ul>"
                f"<p style='font-style:italic;color:#F6AD55'>Coordinate with RHU midwife/physician</p>"
                f"</div>"
            )
        else:
            lab_urgent = "<li style='color:#FC8181'><b>URGENT: Lab tests en route</b></li>" if not lab_available else ""
            return (
                f"<div style='{style}'>{lab_warn}"
                f"<h3 style='color:#FC8181'>High Risk - URGENT REFERRAL</h3>"
                f"<div style='background:#f8fafc;padding:12px;border-radius:8px;margin:12px 0'>"
                f"<b>Probability:</b> Low:{low:.1f}% | Mod:{mod:.1f}% | High:{high:.1f}%</div>"
                f"<b style='color:#742A2A'>Actions:</b><ul>"
                f"<li style='color:#FC8181'><b>IMMEDIATE hospital/OB-GYN referral</b></li>"
                f"{lab_urgent}"
                f"<li>Specialist care required</li>"
                f"<li>Weekly+ visits needed</li>"
                f"<li>Prepare for complications</li>"
                f"</ul>"
                f"<p style='font-weight:bold;color:#FC8181'>DO NOT DELAY: Hospital referral immediately</p>"
                f"</div>"
            )
    
    def save_assessment(self):
        try:
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
            history_file = 'assessment_history.csv'
            if os.path.exists(history_file):
                df = pd.read_csv(history_file)
                df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            else:
                df = pd.DataFrame([record])
            df.to_csv(history_file, index=False)
            self.load_history()
            QMessageBox.information(self, "Success", "Assessment saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    def print_report(self):
        try:
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                self.recommendations.document().print_(printer)
                QMessageBox.information(self, "Success", "Report sent to printer!")
        except Exception as e:
            QMessageBox.warning(self, "Print Error", f"Could not print: {str(e)}")
    
    def new_assessment(self):
        self.patient_id.clear()
        self.health_worker.clear()
        self.age_input.setValue(25)
        self.weight_input.setValue(60.0)
        self.height_input.setValue(160.0)
        self.systolic_input.setValue(120)
        self.diastolic_input.setValue(80)
        self.blood_sugar_input.setValue(5.5)
        self.hemoglobin_input.setValue(12.0)
        self.lab_available.setChecked(False)
        self.results_card.setVisible(False)
    
    def create_history_tab(self):
        tab = QWidget()
        tab.setObjectName("historyTab")
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        header_layout = QHBoxLayout()
        title = QLabel("Assessment History")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
        export_btn = QPushButton("Export to CSV")
        export_btn.setObjectName("secondaryButton")
        export_btn.setMinimumHeight(40)
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.clicked.connect(self.export_history)
        header_layout.addWidget(export_btn)
        layout.addLayout(header_layout)
        
        self.history_table = QTableWidget()
        self.history_table.setObjectName("modernTable")
        self.history_table.setColumnCount(10)
        self.history_table.setHorizontalHeaderLabels([
            "Date/Time", "Patient ID", "Age", "BMI", "Risk Level",
            "Confidence", "Model Used", "Health Worker", "Lab Available", "Action"
        ])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.history_table)
        tab.setLayout(layout)
        return tab
    
    def load_history(self):
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
                risk_item = QTableWidgetItem(row['Risk_Level'])
                if row['Risk_Level'] == 'Low':
                    risk_item.setBackground(QColor(COLORS['success_bg']))
                elif row['Risk_Level'] == 'Moderate':
                    risk_item.setBackground(QColor(COLORS['warning_bg']))
                else:
                    risk_item.setBackground(QColor(COLORS['danger_bg']))
                self.history_table.setItem(idx, 4, risk_item)
                self.history_table.setItem(idx, 5, QTableWidgetItem(row['Confidence']))
                self.history_table.setItem(idx, 6, QTableWidgetItem(row.get('Model_Used', 'Full Model')))
                self.history_table.setItem(idx, 7, QTableWidgetItem(row['Health_Worker']))
                lab_item = QTableWidgetItem(row.get('Lab_Available', 'Unknown'))
                if row.get('Lab_Available') == 'Yes':
                    lab_item.setBackground(QColor(COLORS['success_bg']))
                else:
                    lab_item.setBackground(QColor(COLORS['warning_bg']))
                self.history_table.setItem(idx, 8, lab_item)
                self.history_table.setItem(idx, 9, QTableWidgetItem("Saved"))
        except Exception as e:
            print(f"Error loading history: {e}")
    
    def export_history(self):
        try:
            if not os.path.exists('assessment_history.csv'):
                QMessageBox.warning(self, "No Data", "No assessment history to export.")
                return
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export History",
                f"maternal_assessment_{datetime.now().strftime('%Y%m%d')}.csv",
                "CSV Files (*.csv)"
            )
            if filename:
                df = pd.read_csv('assessment_history.csv')
                df.to_csv(filename, index=False)
                QMessageBox.information(self, "Success", "History exported successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {e}")
    
    def create_about_tab(self):
        tab = QWidget()
        tab.setObjectName("aboutTab")
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        about_text = QTextEdit()
        about_text.setObjectName("aboutText")
        about_text.setReadOnly(True)
        about_text.setHtml("""
        <div style='font-family:Inter,sans-serif;font-size:14px;line-height:1.6;color:#475569'>
        <h2 style='color:#1e3a4c;font-size:28px'>Maternal Risk Assessment System</h2>
        <h3 style='color:#4FC3C9;font-size:18px'>Municipal Health Office Bay, Laguna</h3>
        <p><b>Version:</b> 2.0 (Dual Model System)</p>
        <p><b>Training Data:</b> 986 maternal health records (2019-2025)</p>
        <hr style='border:none;border-top:2px solid #e2e8f0;margin:24px 0'>
        <h3 style='color:#1e3a4c;font-size:20px'>Dual Model System</h3>
        <div style='background:#C6F6D5;padding:16px;border-radius:12px;margin:16px 0;border-left:4px solid #48BB78'>
        <h4 style='color:#22543D;margin-bottom:8px'>Model A - Full Model (5 Features)</h4>
        <p><b>Accuracy:</b> 90.6% (Balanced: 90.58%)</p>
        <p><b>Type:</b> Logistic Regression</p>
        <p><b>Features:</b> BMI, Systolic BP, Blood Sugar, Hemoglobin, Diastolic BP</p>
        <p><b>Use When:</b> Lab test results available</p>
        </div>
        <div style='background:#FEF3C7;padding:16px;border-radius:12px;margin:16px 0;border-left:4px solid #F6AD55'>
        <h4 style='color:#92400E;margin-bottom:8px'>Model B - Basic Model (3 Features)</h4>
        <p><b>Accuracy:</b> ~85%</p>
        <p><b>Type:</b> Logistic Regression</p>
        <p><b>Features:</b> BMI, Systolic BP, Diastolic BP</p>
        <p><b>Use When:</b> Lab results NOT available</p>
        <p><b>Note:</b> Preliminary screening. Lab tests recommended for moderate/high risk.</p>
        </div>
        <hr style='border:none;border-top:2px solid #e2e8f0;margin:24px 0'>
        <h3 style='color:#1e3a4c;font-size:20px'>⚠️ Important Notes</h3>
        <ul style='padding-left:20px'>
        <li>This is a <b>screening tool</b>, not a diagnostic system</li>
        <li>Always follow clinical judgment and protocols</li>
        <li>High-risk cases must be referred to medical professionals</li>
        <li>System works completely offline</li>
        <li>Basic model provides preliminary assessment when lab values unavailable</li>
        </ul>
        <hr style='border:none;border-top:2px solid #e2e8f0;margin:24px 0'>
        <p style='font-style:italic;color:#94a3b8'>Developed for improving maternal health outcomes in rural communities.</p>
        <p><b>For support:</b> Municipal Health Office Bay, Laguna</p>
        </div>
        """)
        layout.addWidget(about_text)
        tab.setLayout(layout)
        return tab
    
    def apply_modern_styles(self):
        self.setStyleSheet(f"""
        QMainWindow {{background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 {COLORS['primary_subtle']},stop:1 {COLORS['white']})}}
        #centralWidget {{background:transparent}}
        #modernHeader {{background:{COLORS['white']};border-bottom:2px solid {COLORS['gray_200']}}}
        #headerTitle {{color:{COLORS['primary']};font-size:24px;font-weight:bold}}
        #headerSubtitle {{color:{COLORS['gray_600']};font-size:12px}}
        QTabWidget#modernTabs::pane {{border:none;background:transparent}}
        QTabWidget#modernTabs QTabBar::tab {{background:{COLORS['gray_200']};color:{COLORS['gray_600']};padding:12px 24px;margin-right:4px;border-top-left-radius:8px;border-top-right-radius:8px;font-size:14px;font-weight:600}}
        QTabWidget#modernTabs QTabBar::tab:selected {{background:{COLORS['white']};color:{COLORS['primary']}}}
        QTabWidget#modernTabs QTabBar::tab:hover {{background:{COLORS['gray_50']}}}
        #modernCard {{background:{COLORS['white']};border:2px solid {COLORS['gray_200']};border-radius:16px}}
        #cardTitle {{color:{COLORS['gray_900']};font-size:18px;font-weight:bold}}
        #formLabel {{color:{COLORS['gray_900']};font-size:13px;font-weight:600}}
        #formHint {{color:{COLORS['gray_400']};font-size:11px;font-style:italic}}
        #formValue {{color:{COLORS['gray_900']};font-size:14px;font-weight:600}}
        #modernInput {{padding:12px 16px;border:2px solid {COLORS['gray_200']};border-radius:10px;font-size:14px;background:{COLORS['white']};color:{COLORS['gray_900']}}}
        #modernInput:focus {{border:2px solid {COLORS['primary']}}}
        #modernSpinBox {{padding:12px 16px;border:2px solid {COLORS['gray_200']};border-radius:10px;font-size:14px;background:{COLORS['white']};color:{COLORS['gray_900']}}}
        #modernSpinBox:focus {{border:2px solid {COLORS['primary']}}}
        #modernSpinBox:disabled {{background:{COLORS['gray_50']};color:{COLORS['gray_400']}}}
        #bmiBadge {{font-size:20px;font-weight:bold;padding:8px 16px;border-radius:8px}}
        #bmiBadge[bmiType="success"] {{background:{COLORS['success_bg']};color:{COLORS['success_text']}}}
        #bmiBadge[bmiType="warning"] {{background:{COLORS['warning_bg']};color:{COLORS['warning_text']}}}
        #bmiBadge[bmiType="danger"] {{background:{COLORS['danger_bg']};color:{COLORS['danger_text']}}}
        #bmiStatus {{font-size:14px;font-weight:600;padding:8px 12px;border-radius:6px}}
        #bmiStatus[bmiType="success"] {{color:{COLORS['success']}}}
        #bmiStatus[bmiType="warning"] {{color:{COLORS['warning']}}}
        #bmiStatus[bmiType="danger"] {{color:{COLORS['danger']}}}
        #modernCheckbox {{font-size:14px;font-weight:500;color:{COLORS['gray_900']}}}
        #modernCheckbox::indicator {{width:20px;height:20px;border:2px solid {COLORS['gray_200']};border-radius:4px}}
        #modernCheckbox::indicator:checked {{background:{COLORS['primary']};border:2px solid {COLORS['primary']}}}
        #divider {{border:none;border-top:2px solid {COLORS['gray_200']}}}
        #sectionTitle {{color:{COLORS['primary_dark']};font-size:16px;font-weight:bold}}
        #modelIndicator {{padding:12px;border-radius:8px;font-size:12px;font-weight:500}}
        #modelIndicator[indicatorType="full"] {{background:{COLORS['success_bg']};color:{COLORS['success_text']}}}
        #modelIndicator[indicatorType="basic"] {{background:{COLORS['warning_bg']};color:{COLORS['warning_text']}}}
        #primaryButton {{background:{COLORS['primary']};color:{COLORS['white']};border:none;border-radius:10px;padding:16px;font-size:14px;font-weight:600}}
        #primaryButton:hover {{background:#3db3b9}}
        #primaryButton:pressed {{background:#2da3a9}}
        #secondaryButton {{background:{COLORS['primary_dark']};color:{COLORS['white']};border:none;border-radius:10px;padding:12px 24px;font-size:14px;font-weight:600}}
        #secondaryButton:hover {{background:#152b3b}}
        #successButton {{background:{COLORS['success']};color:{COLORS['white']};border:none;border-radius:10px;padding:12px 24px;font-size:14px;font-weight:600}}
        #successButton:hover {{background:#38a169}}
        #outlineButton {{background:{COLORS['white']};color:{COLORS['primary']};border:2px solid {COLORS['primary']};border-radius:10px;padding:12px 24px;font-size:14px;font-weight:600}}
        #outlineButton:hover {{background:{COLORS['primary']};color:{COLORS['white']}}}
        #resultsPanel {{background:transparent}}
        #riskContainer {{background:{COLORS['gray_50']};border-radius:16px;padding:24px}}
        #riskText {{font-size:24px;font-weight:bold;padding:12px;border-radius:12px;margin-bottom:16px}}
        #riskText[riskType="low"] {{color:{COLORS['success']};background:{COLORS['success_bg']}}}
        #riskText[riskType="moderate"] {{color:{COLORS['warning']};background:{COLORS['warning_bg']}}}
        #riskText[riskType="high"] {{color:{COLORS['danger']};background:{COLORS['danger_bg']}}}
        #confidenceLabel {{font-size:14px;color:{COLORS['gray_600']};font-weight:600}}
        #modelUsedLabel {{font-size:12px;font-style:italic;padding:8px;border-radius:6px}}
        #modelUsedLabel[modelType="full"] {{color:{COLORS['success_text']};background:{COLORS['success_bg']}}}
        #modelUsedLabel[modelType="basic"] {{color:{COLORS['warning_text']};background:{COLORS['warning_bg']}}}
        #recommendationsText {{border:2px solid {COLORS['gray_200']};border-radius:12px;padding:16px;background:{COLORS['white']}}}
        #modernScroll {{border:none;background:transparent}}
        QScrollBar:vertical {{background:{COLORS['gray_50']};width:12px;border-radius:6px}}
        QScrollBar::handle:vertical {{background:{COLORS['primary']};border-radius:6px;min-height:20px}}
        QScrollBar::handle:vertical:hover {{background:#3db3b9}}
        #modernTable {{border:2px solid {COLORS['gray_200']};border-radius:12px;gridline-color:{COLORS['gray_200']};font-size:13px;background:{COLORS['white']}}}
        #modernTable::item {{padding:8px}}
        #modernTable QHeaderView::section {{background:{COLORS['primary_dark']};color:{COLORS['white']};padding:12px;font-weight:bold;border:none}}
        #pageTitle {{color:{COLORS['primary_dark']};font-size:24px;font-weight:bold}}
        #aboutTab,#historyTab,#assessmentTab {{background:transparent}}
        #aboutText {{border:2px solid {COLORS['gray_200']};border-radius:12px;background:{COLORS['white']};padding:24px}}
        QStatusBar {{background:{COLORS['primary_dark']};color:{COLORS['white']};font-size:12px}}
        QMessageBox {{background:{COLORS['white']}}}
        QMessageBox QLabel {{color:{COLORS['gray_900']};font-size:14px}}
        QMessageBox QPushButton {{background:{COLORS['primary']};color:{COLORS['white']};border:none;border-radius:8px;padding:10px 20px;font-size:13px;font-weight:600;min-width:80px}}
        QMessageBox QPushButton:hover {{background:#3db3b9}}
        """)
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Maternal Risk Assessment System")
    app.setOrganizationName("Municipal Health Office Bay, Laguna")
    font = QFont("Inter", 10)
    if font.family() != "Inter":
        font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MaternalRiskApp()
    window.show()
    window.load_history()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()