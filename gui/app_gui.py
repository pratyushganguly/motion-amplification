"""
Enhanced GUI for motion amplifier with all parameters and compression control.
Includes comprehensive parameter controls, file selection, and error handling.
"""
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox, QMessageBox, 
    QSpinBox, QDoubleSpinBox, QGroupBox, QTextEdit, QProgressBar,
    QCheckBox, QSlider, QFrame, QTabWidget
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from argparse import Namespace
import os
import time

class ProcessingThread(QThread):
    """Separate thread for video processing to keep GUI responsive."""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)  # For status updates

    def __init__(self, args):
        super().__init__()
        self.args = args

    def run(self):
        try:
            from core.amplify import run_amplifier
            self.progress.emit("Starting motion amplification...")
            
            start_time = time.perf_counter()
            temp_out = run_amplifier(self.args)
            total_time_sec = int(round(time.perf_counter() - start_time))
            
            self.progress.emit("Processing completed, finalizing output...")
            
            # Build output filename based on input and seconds
            input_name, ext = os.path.splitext(os.path.basename(self.args.infile))
            final_out = f"{input_name}_{total_time_sec}_sec{ext}"
            
            if os.path.exists(temp_out):
                os.replace(temp_out, final_out)
                file_size = os.path.getsize(final_out) / (1024 * 1024)  # MB
                self.finished.emit(
                    f"✅ Processing completed successfully!\n\n"
                    f"📁 Output: {final_out}\n"
                    f"⏱️ Processing time: {total_time_sec} seconds\n"
                    f"💾 File size: {file_size:.1f} MB"
                )
            else:
                self.error.emit("❌ Temporary output file not found!")
        except Exception as e:
            self.error.emit(f"❌ Processing error:\n{str(e)}")

class ParameterGroup(QGroupBox):
    """Custom group box for organizing parameters."""
    def __init__(self, title):
        super().__init__(title)
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)

class AmplifierGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.processing_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Motion Amplifier - Advanced Controls")
        self.setFixedSize(900, 800)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Create tab widget for better organization
        tab_widget = QTabWidget()
        
        # Basic parameters tab
        basic_tab = self.create_basic_tab()
        tab_widget.addTab(basic_tab, "Basic Settings")
        
        # Advanced parameters tab
        advanced_tab = self.create_advanced_tab()
        tab_widget.addTab(advanced_tab, "Advanced Settings")
        
        # Output settings tab
        output_tab = self.create_output_tab()
        tab_widget.addTab(output_tab, "Output Settings")
        
        main_layout.addWidget(tab_widget)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🚀 Start Processing")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.start_btn.clicked.connect(self.start_processing)
        
        self.reset_btn = QPushButton("🔄 Reset to Defaults")
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.start_btn)
        
        main_layout.addLayout(button_layout)
        
        # Status area
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        self.status_text.setText("Ready to process video...")
        
        main_layout.addWidget(QLabel("Status:"))
        main_layout.addWidget(self.status_text)
        
        self.setLayout(main_layout)

    def create_basic_tab(self):
        """Create the basic settings tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # File selection group
        file_group = ParameterGroup("File Selection")
        file_layout = QGridLayout()
        
        # Input file
        file_layout.addWidget(QLabel("Input Video:"), 0, 0)
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Select input video file...")
        file_layout.addWidget(self.input_path, 0, 1)
        
        self.input_btn = QPushButton("📁 Browse")
        self.input_btn.clicked.connect(self.select_input_file)
        file_layout.addWidget(self.input_btn, 0, 2)
        
        # Output directory
        file_layout.addWidget(QLabel("Output Directory:"), 1, 0)
        self.output_dir = QLineEdit()
        self.output_dir.setPlaceholderText("Optional: choose output directory...")
        file_layout.addWidget(self.output_dir, 1, 1)
        
        self.output_btn = QPushButton("📁 Browse")
        self.output_btn.clicked.connect(self.select_output_dir)
        file_layout.addWidget(self.output_btn, 1, 2)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Core parameters group
        core_group = ParameterGroup("Core Motion Amplification Parameters")
        core_layout = QGridLayout()
        
        # Alpha (amplification factor)
        core_layout.addWidget(QLabel("Amplification Factor (α):"), 0, 0)
        self.alpha_box = QDoubleSpinBox()
        self.alpha_box.setRange(1.0, 100.0)
        self.alpha_box.setValue(15.0)
        self.alpha_box.setSingleStep(1.0)
        self.alpha_box.setToolTip("Higher values = more motion amplification")
        core_layout.addWidget(self.alpha_box, 0, 1)
        
        # Frequency band
        core_layout.addWidget(QLabel("Low Frequency (Hz):"), 1, 0)
        self.low_box = QDoubleSpinBox()
        self.low_box.setRange(0.1, 50.0)
        self.low_box.setValue(0.5)
        self.low_box.setSingleStep(0.1)
        self.low_box.setDecimals(2)
        self.low_box.setToolTip("Lower bound of frequency band to amplify")
        core_layout.addWidget(self.low_box, 1, 1)
        
        core_layout.addWidget(QLabel("High Frequency (Hz):"), 1, 2)
        self.high_box = QDoubleSpinBox()
        self.high_box.setRange(0.2, 100.0)
        self.high_box.setValue(2.0)
        self.high_box.setSingleStep(0.1)
        self.high_box.setDecimals(2)
        self.high_box.setToolTip("Upper bound of frequency band to amplify")
        core_layout.addWidget(self.high_box, 1, 3)
        
        core_group.setLayout(core_layout)
        layout.addWidget(core_group)
        
        # Processing parameters group
        proc_group = ParameterGroup("Processing Parameters")
        proc_layout = QGridLayout()
        
        # Pyramid levels
        proc_layout.addWidget(QLabel("Pyramid Levels:"), 0, 0)
        self.levels_box = QSpinBox()
        self.levels_box.setRange(1, 10)
        self.levels_box.setValue(4)
        self.levels_box.setToolTip("Number of spatial pyramid levels")
        proc_layout.addWidget(self.levels_box, 0, 1)
        
        # Filter order
        proc_layout.addWidget(QLabel("Filter Order:"), 0, 2)
        self.order_box = QSpinBox()
        self.order_box.setRange(1, 5)
        self.order_box.setValue(2)
        self.order_box.setToolTip("Temporal filter order (higher = sharper)")
        proc_layout.addWidget(self.order_box, 0, 3)
        
        # Chunk size
        proc_layout.addWidget(QLabel("Chunk Size (seconds):"), 1, 0)
        self.chunk_box = QDoubleSpinBox()
        self.chunk_box.setRange(0.5, 10.0)
        self.chunk_box.setValue(2.0)
        self.chunk_box.setSingleStep(0.5)
        self.chunk_box.setToolTip("Memory management: smaller = less RAM usage")
        proc_layout.addWidget(self.chunk_box, 1, 1)
        
        proc_group.setLayout(proc_layout)
        layout.addWidget(proc_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def create_advanced_tab(self):
        """Create the advanced settings tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Processing options group
        proc_group = ParameterGroup("Processing Options")
        proc_layout = QGridLayout()
        
        # Color mode
        proc_layout.addWidget(QLabel("Color Mode:"), 0, 0)
        self.color_combo = QComboBox()
        self.color_combo.addItems(["gray", "color", "auto"])
        self.color_combo.setToolTip("Color processing mode")
        proc_layout.addWidget(self.color_combo, 0, 1)
        
        # Backend
        proc_layout.addWidget(QLabel("Processing Backend:"), 0, 2)
        self.backend_combo = QComboBox()
        self.backend_combo.addItems(["auto", "cpu", "cuda", "opencl"])
        self.backend_combo.setToolTip("Computation backend (GPU if available)")
        proc_layout.addWidget(self.backend_combo, 0, 3)
        
        # Custom FPS settings
        proc_layout.addWidget(QLabel("Input FPS Override:"), 1, 0)
        self.fps_box = QDoubleSpinBox()
        self.fps_box.setRange(1.0, 480.0)
        self.fps_box.setValue(30.0)
        self.fps_box.setSpecialValueText("Auto-detect")
        self.fps_box.setMinimum(0)  # 0 means auto-detect
        self.fps_box.setToolTip("Override input video FPS (0 = auto-detect)")
        proc_layout.addWidget(self.fps_box, 1, 1)
        
        proc_layout.addWidget(QLabel("Output FPS:"), 1, 2)
        self.out_fps_box = QDoubleSpinBox()
        self.out_fps_box.setRange(1.0, 480.0)
        self.out_fps_box.setValue(30.0)
        self.out_fps_box.setSpecialValueText("Same as input")
        self.out_fps_box.setMinimum(0)  # 0 means same as input
        self.out_fps_box.setToolTip("Output video FPS (0 = same as input)")
        proc_layout.addWidget(self.out_fps_box, 1, 3)
        
        proc_group.setLayout(proc_layout)
        layout.addWidget(proc_group)
        
        # Text overlay group
        overlay_group = ParameterGroup("Text Overlay Settings")
        overlay_layout = QGridLayout()
        
        self.overlay_enabled = QCheckBox("Enable parameter overlay on output video")
        self.overlay_enabled.setChecked(True)
        self.overlay_enabled.setToolTip("Show processing parameters on each frame")
        overlay_layout.addWidget(self.overlay_enabled, 0, 0, 1, 4)
        
        overlay_layout.addWidget(QLabel("Text Size:"), 1, 0)
        self.text_size_slider = QSlider(Qt.Horizontal)
        self.text_size_slider.setRange(3, 15)  # 0.3 to 1.5 scale
        self.text_size_slider.setValue(5)  # 0.5 scale
        self.text_size_slider.setToolTip("Overlay text size")
        overlay_layout.addWidget(self.text_size_slider, 1, 1)
        
        self.text_size_label = QLabel("0.5")
        self.text_size_slider.valueChanged.connect(
            lambda v: self.text_size_label.setText(f"{v/10:.1f}")
        )
        overlay_layout.addWidget(self.text_size_label, 1, 2)
        
        overlay_layout.addWidget(QLabel("Position:"), 1, 3)
        self.text_position_combo = QComboBox()
        self.text_position_combo.addItems(["bottom", "top", "center"])
        overlay_layout.addWidget(self.text_position_combo, 1, 4)
        
        overlay_group.setLayout(overlay_layout)
        layout.addWidget(overlay_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def create_output_tab(self):
        """Create the output settings tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Output format group
        format_group = ParameterGroup("Output Format")
        format_layout = QGridLayout()
        
        format_layout.addWidget(QLabel("Video Format:"), 0, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp4", "avi"])
        self.format_combo.setToolTip("Output video container format")
        format_layout.addWidget(self.format_combo, 0, 1)
        
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        # Compression group
        compression_group = ParameterGroup("Video Compression")
        compression_layout = QGridLayout()
        
        self.compression_enabled = QCheckBox("Enable video compression")
        self.compression_enabled.setChecked(True)
        self.compression_enabled.setToolTip("Compress output to reduce file size")
        compression_layout.addWidget(self.compression_enabled, 0, 0, 1, 4)
        
        compression_layout.addWidget(QLabel("Compression Level:"), 1, 0)
        self.compression_combo = QComboBox()
        self.compression_combo.addItems(["light", "medium", "heavy", "maximum"])
        self.compression_combo.setCurrentText("medium")
        self.compression_combo.setToolTip("Compression vs quality trade-off")
        compression_layout.addWidget(self.compression_combo, 1, 1)
        
        # Compression quality slider
        compression_layout.addWidget(QLabel("Quality:"), 1, 2)
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(25, 95)
        self.quality_slider.setValue(75)
        self.quality_slider.setToolTip("Compression quality (higher = better quality, larger file)")
        compression_layout.addWidget(self.quality_slider, 1, 3)
        
        self.quality_label = QLabel("75")
        self.quality_slider.valueChanged.connect(
            lambda v: self.quality_label.setText(str(v))
        )
        compression_layout.addWidget(self.quality_label, 1, 4)
        
        compression_group.setLayout(compression_layout)
        layout.addWidget(compression_group)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def select_input_file(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, "Select Input Video", "", 
            "Video Files (*.mp4 *.avi *.mov *.mkv *.wmv *.flv);;All Files (*)"
        )
        if fname:
            self.input_path.setText(fname)

    def select_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_dir.setText(directory)

    def reset_to_defaults(self):
        """Reset all parameters to default values."""
        self.alpha_box.setValue(15.0)
        self.low_box.setValue(0.5)
        self.high_box.setValue(2.0)
        self.levels_box.setValue(4)
        self.order_box.setValue(2)
        self.chunk_box.setValue(2.0)
        self.color_combo.setCurrentText("gray")
        self.backend_combo.setCurrentText("auto")
        self.fps_box.setValue(0)  # Auto-detect
        self.out_fps_box.setValue(0)  # Same as input
        self.format_combo.setCurrentText("mp4")
        self.compression_enabled.setChecked(True)
        self.compression_combo.setCurrentText("medium")
        self.quality_slider.setValue(75)
        self.overlay_enabled.setChecked(True)
        self.text_size_slider.setValue(5)
        self.text_position_combo.setCurrentText("bottom")
        
        self.status_text.setText("Parameters reset to defaults.")

    def validate_parameters(self):
        """Validate all input parameters."""
        if not self.input_path.text().strip():
            return False, "Please select an input video file."
            
        if not os.path.exists(self.input_path.text()):
            return False, "Input video file does not exist."
            
        if self.low_box.value() >= self.high_box.value():
            return False, "Low frequency must be less than high frequency."
            
        if self.alpha_box.value() <= 0:
            return False, "Amplification factor must be positive."
            
        return True, "Parameters are valid."

    def start_processing(self):
        # Validate parameters
        valid, message = self.validate_parameters()
        if not valid:
            QMessageBox.warning(self, "Parameter Error", message)
            return
        
        # Disable start button and enable cancel
        self.start_btn.setEnabled(False)
        self.start_btn.setText("🔄 Processing...")
        
        # Clear status
        self.status_text.clear()
        self.status_text.append("🚀 Starting motion amplification processing...")
        
        # Gather parameters
        args = Namespace(
            infile=self.input_path.text().strip(),
            low=self.low_box.value(),
            high=self.high_box.value(),
            alpha=self.alpha_box.value(),
            levels=self.levels_box.value(),
            order=self.order_box.value(),
            chunk_sec=self.chunk_box.value(),
            color=self.color_combo.currentText(),
            backend=self.backend_combo.currentText(),
            out_fmt=self.format_combo.currentText(),
            fps=self.fps_box.value() if self.fps_box.value() > 0 else None,
            out_fps=self.out_fps_box.value() if self.out_fps_box.value() > 0 else None,
            outfile=None,
            # Additional parameters for enhanced features
            compression_enabled=self.compression_enabled.isChecked(),
            compression_level=self.compression_combo.currentText(),
            compression_quality=self.quality_slider.value(),
            overlay_enabled=self.overlay_enabled.isChecked(),
            text_size=self.text_size_slider.value() / 10.0,
            text_position=self.text_position_combo.currentText()
        )
        
        # Start processing in separate thread
        self.processing_thread = ProcessingThread(args)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.error.connect(self.on_processing_error)
        self.processing_thread.progress.connect(self.on_processing_progress)
        self.processing_thread.start()

    def on_processing_progress(self, message):
        """Handle progress updates from processing thread."""
        self.status_text.append(message)
        self.status_text.ensureCursorVisible()

    def on_processing_finished(self, message):
        """Handle successful completion."""
        self.start_btn.setEnabled(True)
        self.start_btn.setText("🚀 Start Processing")
        self.status_text.append("\n" + message)
        QMessageBox.information(self, "Success", message)

    def on_processing_error(self, error_msg):
        """Handle processing errors."""
        self.start_btn.setEnabled(True)
        self.start_btn.setText("🚀 Start Processing")
        self.status_text.append(f"\n❌ Error: {error_msg}")
        QMessageBox.critical(self, "Processing Error", error_msg)

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set color palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    app.setPalette(palette)
    
    ex = AmplifierGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()