# Manual Robot Arm – Pygame Demo

This repository currently contains a simple Pygame window that renders a red dot you can move with the arrow keys. Follow the steps below to set it up on a fresh machine.

## Prerequisites

- macOS, Linux, or Windows
- Python 3.9 or newer (verify with `python3 --version`)
- `pip` package manager (bundled with recent Python installs)

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/AppliedEngineeringClub/manual-robot-arm.git

# 2. Move into the cloned folder
cd manual-robot-arm

# 3. (Optional) create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate            # macOS/Linux
# .venv\Scripts\activate             # Windows PowerShell

# 4. Install dependencies
pip install pygame
```

## Run the demo

```bash
python3 pygame-window.py
# or, if executable:
./pygame-window.py
```

A 640×400 black window should appear. Use the arrow keys to move the red dot. Close the window or press `Ctrl+C` in the terminal to exit.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`**  
  Ensure step 4 succeeded. Re-run `pip install pygame` inside the same environment.

- **Permission denied when running `./pygame-window.py`**  
  Add execute permission: `chmod +x pygame-window.py`

- **Virtual environment not activating (macOS/Linux)**  
  Run `source .venv/bin/activate` from the project directory and confirm your shell prompt shows `(.venv)`.



  



