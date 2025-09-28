# 🎛️ MIDI CC Mapper for macOS  

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python)](https://www.python.org/) [![Built with PyInstaller](https://img.shields.io/badge/Built%20with-PyInstaller-FFDD00)](https://pyinstaller.org/) [![Platform: macOS](https://img.shields.io/badge/Platform-macOS-lightgrey?logo=apple)](https://www.apple.com/macos/) [![Ableton Live](https://img.shields.io/badge/Tested%20with-Ableton%20Live-orange?logo=abletonlive)](https://www.ableton.com/)  

☕ If this project helps you, consider supporting me:  
👉 [**Buy Me a Coffee**](https://buymeacoffee.com/ghiemer)  

---

## 👋 Personal Note  

Hi there!  

I built this tool because I was struggling with a really annoying issue in **Ableton Live**:  
When using both my **AKAI APC mini mk2** and **AKAI MIDI Mix**, the faders and knobs were sending **overlapping CC numbers**.  

This meant I couldn’t map them independently — Live saw them as the same control.  
After a lot of trial and error (and some frustration 😅), I worked with **ChatGPT** to create a small but powerful solution: a **MIDI CC Mapper**.  

It’s lightweight, runs only when I need it, and makes my workflow smooth again.  
I’m sharing it here so others don’t have to go through the same headache.  

---

## 🎶 Problem  

- APC mini mk2 sends faders on CC **48–56**  
- MIDI Mix also uses overlapping CCs (e.g. faders and knobs)  
- Ableton Live **does not differentiate devices by CC number** → conflicts happen  

---

## ✅ Solution  

The **MIDI CC Mapper**:  

1. Reads CC messages from the APC mini mk2  
2. Remaps them to a new, unused CC range (e.g. 80–88)  
3. Forwards them into a **virtual MIDI port** created by macOS **IAC Driver**  
4. Ableton Live only listens to the remapped port  

Result: **No more CC collisions** 🎉  

---

## 🚀 Installation  

### 1. Clone the repo  

```bash
git clone https://github.com/ghiemer/midi-cc-mapper.git
cd midi-cc-mapper
```

### 2. Run setup script  

```bash
chmod +x setup.sh
./setup.sh
```

Use `./setup.sh --force` if you want to rebuild everything from scratch.  

---

## 🎹 macOS Setup  

### Enable IAC Driver  

1. Open **Audio MIDI Setup** → **Show MIDI Studio** (in menu *Window*)  
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
midi-cc-mapper /usr/local/etc/midi-cc-mapper/config.json
```

Debug mode:  

```bash
midi-cc-mapper /usr/local/etc/midi-cc-mapper/config.json --debug
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
- Compile to a macOS binary with PyInstaller  

It’s proof that **human–AI collaboration** can solve niche but painful problems in music production. 😉
