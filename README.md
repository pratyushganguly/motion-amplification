# Motion Amplifier

A modular, scalable Python library for motion amplification in video processing.

## Features
- Multi-scale, robust motion amplification using Eulerian video magnification
- GPU acceleration support (CUDA, OpenCL) with CPU fallback
- Chunked processing for memory efficiency with large videos
- Real-time progress tracking with parameter overlay on output videos
- Both CLI and GUI interfaces
- Cross-platform compatibility (Windows, macOS, Linux)

## Project Structure
```
motion_amplifier/
├── core/           # Core algorithms and processing logic
├── io_utils/       # Video and config I/O handling  
├── gui/            # PyQt5 GUI interface
├── metrics/        # Performance and resource monitoring
├── tests/          # Unit and regression tests
├── main.py         # CLI entry point
└── requirements.txt
```

## Quick Start

### Create Virtual env (optional but recommended)
```bash
python -m venv venv
```

### Installation
```bash
pip install -r requirements.txt
```

### CLI Usage
```bash
python main.py --in input_video.mp4 --low 0.5 --high 2.0 --alpha 15
```

### GUI Usage
```bash
python gui/app_gui.py
```

## Parameters
- `--low` / `--high`: Frequency band (Hz) to amplify
- `--alpha`: Amplification factor (higher = more motion)
- `--levels`: Pyramid levels (default: 4)
- `--order`: Filter order (default: 2)
- `--chunk_sec`: Chunk size in seconds (default: 2)
- `--color`: Color mode ["gray", "color", "auto"]
- `--backend`: Backend ["auto", "cpu", "cuda", "opencl"]
- `--out_fmt`: Output format ["avi", "mp4"]

## Output
- Automatically named with processing time: `input_96_sec.mp4`
- Parameter overlay on every frame for easy tuning
- Progress bar with elapsed time during processing

## Requirements
- Python 3.8+
- OpenCV
- NumPy
- SciPy
- PyQt5 (for GUI)

## Contributing
This project follows modular design principles for easy collaboration:
- Well-documented code with clear function purposes
- Separated concerns (I/O, processing, GUI, metrics)
- Unit tests for core functionality
- Cross-platform compatibility

Please see individual module docstrings for detailed API documentation.

## Performance Notes
- CPU-based processing is robust across all platforms
- GPU acceleration available on NVIDIA (CUDA) and AMD (OpenCL) systems
- Memory usage optimized through chunked processing
- Processing time scales with video resolution and frame rate

## License
Open source - contributions welcome!