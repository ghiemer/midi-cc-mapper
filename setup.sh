#!/bin/bash
set -e

FORCE=0
if [ "$1" == "--force" ]; then
  FORCE=1
fi

echo "[INFO] Checking requirements..."

if ! command -v python3 >/dev/null 2>&1; then
  echo "[ERROR] python3 not found. Please install Python 3."
  exit 1
fi

if ! command -v pip3 >/dev/null 2>&1; then
  echo "[ERROR] pip3 not found. Please install pip for Python 3."
  exit 1
fi

echo "[INFO] Installing Python dependencies..."
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install --upgrade pyinstaller mido python-rtmidi

echo "[INFO] Building binary with PyInstaller..."

if [ $FORCE -eq 1 ]; then
  rm -rf build dist *.spec
fi

pyinstaller --onefile --name midi-cc-mapper \
  --hidden-import mido.backends.rtmidi \
  midi_cc_mapper.py

echo "[INFO] Installing binary to /usr/local/bin..."
sudo mv dist/midi-cc-mapper /usr/local/bin/midi-cc-mapper
sudo chown root:wheel /usr/local/bin/midi-cc-mapper
sudo chmod 755 /usr/local/bin/midi-cc-mapper

echo "[INFO] Creating default config in /usr/local/etc/midi-cc-mapper..."
sudo mkdir -p /usr/local/etc/midi-cc-mapper
if [ ! -f /usr/local/etc/midi-cc-mapper/config.json ]; then
  sudo tee /usr/local/etc/midi-cc-mapper/config.json >/dev/null <<'JSON'
{
  "input_port": "APC mini mk2 Control",
  "output_port": "IAC Driver Remap APC",
  "mappings": {
    "48": 80,
    "49": 81,
    "50": 82,
    "51": 83,
    "52": 84,
    "53": 85,
    "54": 86,
    "55": 87,
    "56": 88
  },
  "pass_through_other": true
}
JSON
  sudo chmod 644 /usr/local/etc/midi-cc-mapper/config.json
fi

echo "[INFO] Installation complete!"
echo "Run with: midi-cc-mapper /usr/local/etc/midi-cc-mapper/config.json"
