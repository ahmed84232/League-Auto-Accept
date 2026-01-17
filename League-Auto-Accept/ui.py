from datetime import datetime
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor

from worker import AutoAcceptWorker


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("League Auto-Accept")
        self.setMinimumSize(420, 650)
        self.resize(450, 700)
        
        self.worker = None
        self.matches_accepted = 0
        self._is_running = False
        
        self._setup_ui()
    
    def _setup_ui(self):

        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("🎮 League Auto-Accept")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Automatically accept matches for you")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)
        
        # Status Card
        self.status_card = self._create_status_card()
        layout.addWidget(self.status_card)
        
        # Activity Log
        self.log_card = self._create_log_card()
        layout.addWidget(self.log_card, 1)  # Stretch factor
        
        # Control Panel
        self.control_panel = self._create_control_panel()
        layout.addWidget(self.control_panel)
    
    def _create_status_card(self):

        card = QFrame()
        card.setObjectName("statusCard")
        
        layout = QVBoxLayout(card)
        layout.setSpacing(10)
        
        # Connection row
        conn_row = QHBoxLayout()
        
        self.conn_dot = QLabel("●")
        self.conn_dot.setObjectName("connectionDot")
        self.conn_dot.setStyleSheet("color: #ef4444;")
        conn_row.addWidget(self.conn_dot)
        
        self.conn_label = QLabel("Disconnected")
        self.conn_label.setObjectName("connectionLabel")
        conn_row.addWidget(self.conn_label)
        conn_row.addStretch()
        
        layout.addLayout(conn_row)
        
        # Divider
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #3d3d5c;")
        layout.addWidget(divider)
        
        # Phase section
        phase_label = QLabel("Current Phase")
        phase_label.setObjectName("phaseLabel")
        layout.addWidget(phase_label)
        
        self.phase_badge = QLabel("  Stopped  ")
        self.phase_badge.setObjectName("phaseBadge")
        self.phase_badge.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.phase_badge, alignment=Qt.AlignCenter)
        
        return card
    
    def _create_log_card(self):

        card = QFrame()
        card.setObjectName("logCard")
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Header row
        header_row = QHBoxLayout()
        
        header_label = QLabel("📋 Activity Log")
        header_label.setObjectName("logHeader")
        header_row.addWidget(header_label)
        
        header_row.addStretch()
        
        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("clearButton")
        clear_btn.clicked.connect(self._clear_log)
        header_row.addWidget(clear_btn)
        
        layout.addLayout(header_row)
        
        # Scroll area for log entries
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.log_container = QWidget()
        self.log_layout = QVBoxLayout(self.log_container)
        self.log_layout.setContentsMargins(5, 5, 5, 5)
        self.log_layout.setSpacing(3)
        self.log_layout.addStretch()
        
        scroll.setWidget(self.log_container)
        self.log_scroll = scroll
        
        layout.addWidget(scroll)
        
        return card
    
    def _create_control_panel(self):

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        self.toggle_btn = QPushButton("▶  START AUTO-ACCEPT")
        self.toggle_btn.setObjectName("startButton")
        self.toggle_btn.setMinimumHeight(55)
        self.toggle_btn.clicked.connect(self._toggle_service)
        layout.addWidget(self.toggle_btn)
        
        self.stats_label = QLabel("Matches Accepted: 0")
        self.stats_label.setObjectName("statsLabel")
        self.stats_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.stats_label)
        
        return panel
    
    def _add_log_entry(self, message: str, level: str = "info"):

        colors = {
            "info": "#60a5fa",
            "success": "#4ade80",
            "warning": "#fbbf24",
            "error": "#f87171"
        }
        icons = {
            "info": "●",
            "success": "✓",
            "warning": "⚠",
            "error": "✕"
        }
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = colors.get(level, "#60a5fa")
        icon = icons.get(level, "●")
        
        entry = QLabel(f'<span style="color:#666666">{timestamp}</span>  '
                      f'<span style="color:{color}">{icon}</span>  {message}')
        entry.setTextFormat(Qt.RichText)
        
        # Insert before the stretch
        self.log_layout.insertWidget(self.log_layout.count() - 1, entry)
        
        # Auto-scroll to bottom
        QTimer.singleShot(50, lambda: self.log_scroll.verticalScrollBar().setValue(
            self.log_scroll.verticalScrollBar().maximum()
        ))
    
    def _clear_log(self):

        while self.log_layout.count() > 1:
            item = self.log_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def _update_phase(self, phase: str):

        phase_colors = {
            "None": "#6b7280",
            "Lobby": "#3b82f6",
            "Matchmaking": "#f59e0b",
            "ReadyCheck": "#22c55e",
            "ChampSelect": "#8b5cf6",
            "InProgress": "#ef4444",
            "InGame": "#ef4444",
        }
        
        color = phase_colors.get(phase, "#3d3d5c")
        
        display = phase
        if phase == "Matchmaking":
            display = "🔍 Searching..."
        elif phase == "ReadyCheck":
            display = "⚡ Match Found!"
        elif phase == "ChampSelect":
            display = "🎮 Champion Select"
        elif phase in ("InProgress", "InGame"):
            display = "🎮 In Game"
        
        self.phase_badge.setText(f"  {display}  ")
        self.phase_badge.setStyleSheet(f"background-color: {color}; border-radius: 8px; padding: 10px 20px; font-size: 18px; font-weight: bold;")
    
    def _update_connected(self, connected: bool):

        if connected:
            self.conn_dot.setStyleSheet("color: #22c55e;")
            self.conn_label.setText("Connected to League Client")
        else:
            self.conn_dot.setStyleSheet("color: #ef4444;")
            self.conn_label.setText("Disconnected")
    
    def _on_match_accepted(self):

        self.matches_accepted += 1
        self.stats_label.setText(f"Matches Accepted: {self.matches_accepted}")
    
    def _toggle_service(self):

        if self._is_running:
            self._stop_service()
        else:
            self._start_service()
    
    def _start_service(self):

        self._is_running = True
        
        self.toggle_btn.setText("■  STOP AUTO-ACCEPT")
        self.toggle_btn.setObjectName("stopButton")
        self.toggle_btn.setStyle(self.toggle_btn.style())
        self.toggle_btn.setStyleSheet("background-color: #ef4444; color: white; border: none; border-radius: 12px; padding: 15px; font-size: 16px; font-weight: bold;")
        
        self._add_log_entry("Starting Auto-Accept...", "info")
        
        self.worker = AutoAcceptWorker()
        self.worker.log_signal.connect(self._add_log_entry)
        self.worker.phase_signal.connect(self._update_phase)
        self.worker.connected_signal.connect(self._update_connected)
        self.worker.match_accepted_signal.connect(self._on_match_accepted)
        self.worker.start()
    
    def _stop_service(self):

        self._is_running = False
        
        self.toggle_btn.setText("▶  START AUTO-ACCEPT")
        self.toggle_btn.setObjectName("startButton")
        self.toggle_btn.setStyleSheet("background-color: #22c55e; color: white; border: none; border-radius: 12px; padding: 15px; font-size: 16px; font-weight: bold;")
        
        if self.worker:
            self.worker.stop()
            self.worker.wait(2000)
            self.worker = None
        
        self._add_log_entry("Stopped Auto-Accept", "info")
        self._update_phase("Stopped")
        self._update_connected(False)
    
    def closeEvent(self, event):

        self._stop_service()
        event.accept()
