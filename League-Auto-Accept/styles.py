STYLESHEET = """
QMainWindow {
    background-color: #0f0f1a;
}

QWidget {
    background-color: transparent;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QLabel {
    color: #e0e0e0;
}

#title {
    color: #f0c040;
    font-size: 24px;
    font-weight: bold;
}

#subtitle {
    color: #888888;
    font-size: 12px;
}

#statusCard {
    background-color: #1e1e2e;
    border: 1px solid #3d3d5c;
    border-radius: 15px;
    padding: 15px;
}

#connectionDot {
    font-size: 14px;
}

#connectionLabel {
    font-size: 14px;
    font-weight: bold;
}

#phaseLabel {
    color: #888888;
    font-size: 12px;
}

#phaseBadge {
    background-color: #3d3d5c;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 18px;
    font-weight: bold;
}

#startButton {
    background-color: #22c55e;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 15px;
    font-size: 16px;
    font-weight: bold;
}

#startButton:hover {
    background-color: #16a34a;
}

#stopButton {
    background-color: #ef4444;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 15px;
    font-size: 16px;
    font-weight: bold;
}

#stopButton:hover {
    background-color: #dc2626;
}

#logCard {
    background-color: #1e1e2e;
    border: 1px solid #3d3d5c;
    border-radius: 15px;
}

#logHeader {
    font-size: 14px;
    font-weight: bold;
    padding: 10px;
}

#clearButton {
    background-color: #3d3d5c;
    color: #e0e0e0;
    border: none;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 11px;
}

#clearButton:hover {
    background-color: #4d4d6c;
}

#statsLabel {
    color: #888888;
    font-size: 12px;
}

QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #1e1e2e;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #3d3d5c;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4d4d6c;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
