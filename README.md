# Resistor Recognition System

A computer vision application that recognizes resistor color bands and calculates resistance values using real-time camera feed.

## Features

- Real-time camera feed for resistor detection
- Automatic image preprocessing (rotation, cropping, white balancing)
- Color band detection for all standard resistor colors
- Resistance calculation with tolerance values
- User-friendly GUI interface

## Requirements

- Python 3.7+
- OpenCV
- Tkinter
- PIL (Pillow)
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resistor-recognition.git
cd resistor-recognition
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python gui.py
```

## Usage

1. Launch the application
2. Click "Start" to open camera feed
3. Position resistor in camera view
4. Click "Capture Image" to analyze
5. View calculated resistance value

## Project Structure

```
resistor-recognition/
├── gui.py              # Main application entry point
├── FrontEnd.py         # GUI implementation
├── Preprocessing.py    # Image preprocessing classes
├── Bands.py           # Color band detection classes
├── Analysis.py        # Band sorting and analysis
├── assets/            # Image assets
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License