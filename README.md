# 🎛️ MIDI CC Router for macOS  

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python)](https://www.python.org/) [![Built with Nuitka](https://img.shields.io/badge/Built%20with-Nuitka-003545)](https://nuitka.net/) [![Platform: macOS](https://img.shields.io/badge/Platform-macOS-lightgrey?logo=apple)](https://www.apple.com/macos/) [![Ableton Live](https://img.shields.io/badge/Tested%20with-Ableton%20Live-orange?logo=abletonlive)](https://www.ableton.com/)  

☕ If this project helps you, consider supporting me:  
👉 [**Buy Me a Coffee**](https://buymeacoffee.com/ghiemer)  

---

## 👋 Personal Note  

Hi there!  

I built this tool because I was struggling with a really annoying issue in **Ableton Live**:  
When using both my **AKAI APC mini mk2** and **AKAI MIDI Mix**, the faders and knobs were sending **overlapping CC numbers**.  

This meant I couldn’t map them independently — Live saw them as the same control.  
After a lot of trial and error (and some frustration 😅), I worked with **ChatGPT** to create a small but powerful solution: a **MIDI CC Router**.  

It’s lightweight, runs only when I need it, and makes my workflow smooth again.  
I’m sharing it here so others don’t have to go through the same headache.  

---

## 🎶 Problem  

- APC mini mk2 sends faders on CC **48–56**  
- MIDI Mix also uses overlapping CCs (e.g. faders and knobs)  
- Ableton Live **does not differentiate devices by CC number** → conflicts happen  

---

## ✅ Solution  

The **MIDI CC Router**:  

1. Reads CC messages from the APC mini mk2  
2. Remaps them to a new, unused CC range (e.g. 80–88)  
3. Forwards them into a **virtual MIDI port** created by macOS **IAC Driver**  
4. Ableton Live only listens to the remapped port  

Result: **No more CC collisions** 🎉  

---

## 🚀 Installation  

### 1. Install the binary  

```bash
python3 -m pip install --upgrade nuitka "mido[ports-rtmidi]" python-rtmidi
cd midi-tools
python3 -m nuitka --onefile   --include-module=mido.backends.rtmidi   --include-module=rtmidi   midi_cc_router.py
sudo mv ~/midi-tools/midi_cc_router.bin /usr/local/bin/midi-cc-router
sudo chown root:wheel /usr/local/bin/midi-cc-router
sudo chmod 755 /usr/local/bin/midi-cc-router
```

### 2. Configuration  

Create:  

```bash
sudo mkdir -p /usr/local/etc/midi-cc-router
sudo nano /usr/local/etc/midi-cc-router/config.json
```

Example:  

```json
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
```

---

## 🎹 macOS Setup  

### Enable IAC Driver  

1. Open **Audio MIDI Setup** → **Show MIDI Studio**(In menu Window)  
2. Double-click **IAC Driver**  
3. Enable *Device is online*  
4. Add a port: **Remap APC**  

### Ableton Live  

- Preferences → **Link/Tempo/MIDI**  
- Enable **Track Input** for **IAC Driver (Remap APC)**  
- Use this virtual port for mapping instead of the raw APC mini mk2  

---

## ⚡ Usage  

```bash
midi-cc-router /usr/local/etc/midi-cc-router/config.json
```

Debug mode:  

```bash
midi-cc-router /usr/local/etc/midi-cc-router/config.json --debug
```

Stop: `CTRL+C`  

---

## 🛠️ Roadmap  

- Support multiple configs / profiles  
- Hot reload configuration  
- Optional GUI for mapping  

---

## 🙌 Credits  

This project was **built together with ChatGPT**.  
AI helped me:  
- Debug conflicting configs  
- Design the router in Python  
- Optimize performance  
- Compile to a macOS binary with Nuitka  

It’s proof that **human–AI collaboration** can solve niche but painful problems in music production. 😉
