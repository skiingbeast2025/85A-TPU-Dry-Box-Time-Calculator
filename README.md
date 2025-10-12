# 85A-TPU-Dry-Box-Time-Calculator

A simple desktop app that helps 3D printing enthusiasts calculate pre-print, during-print, and post-print drying times for 85A TPU filament.  
Features a modern dark/light GUI, quick calculations, and the app saves every run to a local `history.json` and shows a scrollable in-app history so you can review past print durations and previous recommended pre/during/post drying times.

![Screenshot](assets/screenshots/Dry_Box_Time_Calculator_V1.1.png)

- 🕐 Calculates drying times based on print duration  
- 🌡️ Uses a fixed drying temperature of **50°C**  
- 🕶️ Modern dark-theme interface  
- 💡 Includes helpful TPU drying recommendations  
- 💻 Works on Python (.py)
- ⚠️ Older versions used different drying heuristics and may produce inaccurate results. Please use the latest release for best results.

## 🚀 How to Use

1. **Launch the app**
   - Run `Dry_Box_Time_Calculator_V1.1.pyw or Dry_Box_Time_Calculator_V1.1.pyw` (Python version)
   - Run `Dry_Box_Time_Calculator_V1.1.exe` (executable version)

2. **Enter print duration**
   - Input your print’s estimated time (in hours or minutes)
   - Input when your last print was
   - Input how you stored your fillimant since last print

3. **View recommended drying times**
   - The app instantly calculates how long to dry your filament before, during, and after printing.

---

## 💻 Requirements

- Python 3.10+ (tested on Windows 11)
- tkinter (standard with Python on Windows/macOS; on some Linux distros install `python3-tk`)
- Optional: pyinstaller (if you want to build a single-file .exe)

If you don't have tkinter on Linux:
```bash
# Debian/Ubuntu

If you're on Debian/Ubuntu, make sure `tkinter` is installed:

```bash
sudo apt update
sudo apt install python3-tk
```
## 💾 Building From Source
If you’d like to modify or run the app yourself:
```
bash
git clone https://github.com/skiingbeast2025/85A-TPU-Dry-Box-Time-Calculator.git
cd 85A-TPU-Dry-Box-Time-Calculator
python tpu_dry_calculator.py
```
## 📦 Packaging (Windows / macOS / Linux)

You can run the app from source (Python) or build a single-file executable for distribution. Below are short, practical instructions and examples for each OS.

> **General tips**
> - Build on the **target OS** whenever possible (Windows builds on Windows, macOS builds on macOS). Cross-building is possible but more fragile.
> - Use a virtual environment for clean builds:
> ```bash
> python -m venv venv
> source venv/bin/activate   # macOS / Linux
> venv\Scripts\activate      # Windows
> pip install -r requirements.txt   # if you have one, otherwise `pip install pyinstaller`
> ```

---

### 🪟 Windows (PyInstaller — recommended)
1. Install PyInstaller:
```bash
pip install pyinstaller
```
Build a one-file .exe (no console window):
```
pyinstaller --onefile --noconsole --icon=3d-printer-icon.ico \
  --add-data "assets;assets" \
  tpu_dry_calculator.py
```
--noconsole prevents the console window from appearing.

--add-data "assets;assets" bundles the assets/ folder. (On Windows use ; as the separator.)

The generated file will be in dist/tpu_dry_calculator.exe.

Test the .exe by running it (double-click or from PowerShell).
history.json and setup.json will be created/updated next to the .exe when the program runs.

 macOS (py2app or PyInstaller on macOS)
Option A — py2app

Install:
```
pip install py2app
```
Minimal setup.py example:
```
# setup.py
from setuptools import setup

APP = ['tpu_dry_calculator.py']
OPTIONS = {'argv_emulation': True, 'iconfile': '3d-printer-icon.icns'}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```
Build:
```
python setup.py py2app
```
The .app bundle will be in dist/.

Option B — PyInstaller (works on mac when built there)
```
pyinstaller --onefile --windowed --icon=3d-printer-icon.icns \
  --add-data "assets:assets" \
  tpu_dry_calculator.py
```
On macOS/Linux the --add-data separator is :.

Note: For distributing on macOS you may need code signing and notarization for Gatekeeper.

🐧 Linux (PyInstaller / AppImage)
Install PyInstaller:
```
pip install pyinstaller
```
Build:
```
pyinstaller --onefile --windowed --icon=3d-printer-icon.png \
  --add-data "assets:assets" \
  tpu_dry_calculator.py
```
The --add-data separator on Linux/macOS is :.

The result will be dist/tpu_dry_calculator (make executable with chmod +x if needed).

Optional: create an AppImage (more advanced) if you need broad distribution across Linux distros.

🔗 Important ```--add-data notes```
Windows: ```--add-data "src;dest"```

macOS/Linux: ```--add-data "src:dest"```
Use the correct separator or PyInstaller won’t include the files.

🗂 Where runtime files go (history.json / setup.json)
When users run the packaged .exe / .app / binary, history.json and setup.json are created in the same folder as the executable (so they persist across runs). Mention this in your README so users know where to look for history or backups.

📤 Distribute via GitHub Releases
Build the executable on the target platform.

Go to Releases → Draft a new release in GitHub.

Attach the built .exe, .app, or Linux binary (or a .zip) to the release.

Publish the release so users can download without building.

⚠️ Troubleshooting & tips
If the GUI fails to start, verify tkinter is available on the runtime system. On Debian/Ubuntu:
```
sudo apt update
sudo apt install python3-tk
```
If assets (icons/screenshots) are missing in the packaged app, re-check the --add-data syntax and test the app from the dist/ folder.

For Windows GUI builds, you can also use a .pyw extension to avoid consoles for local runs; PyInstaller --noconsole is recommended for executables.

For macOS distribution outside the App Store, code sign and notarize the .app to avoid Gatekeeper issues.

Always build on the OS you intend to distribute to for best results.

## ⚡ Running the Pre-Built Executable
If you prefer the single-file .exe version (Windows):
1. Download the .exe from the latest release.
2. Double-click to run — no Python installation needed.

You can package it into an .exe with:

```bash
pyinstaller --onefile --noconsole Dry_Box_Time_Calculator_V1.1.pyw (or Dry_Box_Time_Calculator_V1.1.py)
```

---

## 🧠 TPU Notes

- Recommended drying temperature: **50°C**  
- Suggested initial drying time after opening a new spool: **6–7 hours**  
- Keep filament sealed in a dryer box or airtight bag with silica gel between prints.
- Recommended to only use 85A TPU while using dry times calculated by this app.

---

## 📝 License

This project is licensed under the **Apache License 2.0**.  
See the [LICENSE](LICENSE) file for details.
