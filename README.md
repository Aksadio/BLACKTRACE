# BLACKTRACE // ZERO-DAY SIMULATION

BLACKTRACE is a cinematic, **100% harmless visual prank application** built in Python/Tkinter. It presents a fictional cyber-operations dashboard, animates locally generated simulation events, and ends with an explicit prank reveal.

## Safety

This application is simulation-only. It does not execute shell/PowerShell commands, inspect or modify files, read credentials, capture global keystrokes, access microphone/camera, contact external servers, scan networks/ports, modify system settings, create persistence, or collect/transmit personal information. Terminal input is handled only by predefined visual responses.

## Requirements

- Python 3.10+ recommended
- Tkinter (included with normal Windows Python installations)
- No third-party runtime packages
- No internet connection required

On Linux, if Tkinter is missing, install the OS package (for example `python3-tk` on Debian/Ubuntu).

## Run locally

```bash
python main.py
```

Run the checks:

```bash
python smoke_test.py
python tk_check.py
```

## Controls

- `Enter` — accelerate the next simulation event
- `Space` — pause/resume
- `M` — toggle local UI bell
- `F11` — fullscreen
- `Esc` — exit

The command box accepts harmless visual Easter eggs such as `sudo coffee`, `whoami`, and `hack nasa`.

## Windows EXE

Install PyInstaller on Windows:

```powershell
py -m pip install pyinstaller
pyinstaller --noconsole --onefile --name BLACKTRACE main.py
```

The executable will be created at `dist\\BLACKTRACE.exe`.

This repository also includes a GitHub Actions workflow at `.github/workflows/build-windows.yml`. From GitHub, run it manually with **Actions → Build Windows EXE → Run workflow**, or push a version tag such as `v1.0.0`. The workflow builds a Windows executable as an artifact.

## GitHub Pages

This is a **desktop Tkinter application**, not a browser application. GitHub Pages cannot run the Tkinter GUI. GitHub can host the source code and GitHub Actions can build the Windows `.exe`; users then run the executable on Windows.

## Project layout

```text
BLACKTRACE/
├── main.py
├── simulation/
│   ├── __init__.py
│   ├── engine.py
│   └── fake_data.py
├── .github/
│   └── workflows/
│       └── build-windows.yml
├── smoke_test.py
├── tk_check.py
├── requirements.txt
├── .gitignore
└── README.md
```
