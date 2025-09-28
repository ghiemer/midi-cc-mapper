#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, json, time
os.environ.setdefault("MIDO_BACKEND", "mido.backends.rtmidi")

try:
    import mido
except Exception as e:
    print("Fehler: mido/python-rtmidi fehlt. Installiere mit:\n  pip install 'mido[ports-rtmidi]'\n", e)
    sys.exit(1)

DEFAULT_CFG = os.path.expanduser("~/midi-tools/config.json")
DEBUG = ("--debug" in sys.argv)

def pick_port(part: str, ports: list[str]) -> str:
    """Port finden, der 'part' enthält (case-insensitive)."""
    p = (part or "").lower()
    for n in ports:
        if p in n.lower():
            return n
    raise LookupError(f"Port nicht gefunden für '{part}'. Verfügbar: {ports}")

def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    mappings = {int(k): int(v) for k, v in cfg.get("mappings", {}).items()}
    return {
        "in_part": cfg.get("input_port", ""),
        "out_part": cfg.get("output_port", ""),
        "mappings": mappings,
        "pass_other": bool(cfg.get("pass_through_other", True)),
    }

def router(cfg_path: str):
    cfg = load_config(cfg_path)
    mappings = cfg["mappings"]
    pass_other = cfg["pass_other"]

    while True:
        try:
            in_name  = pick_port(cfg["in_part"],  mido.get_input_names())
            out_name = pick_port(cfg["out_part"], mido.get_output_names())
            print(f"[INFO] Öffne: {in_name}  →  {out_name}")

            # Event-driven: block until message arrives (no busy loop)
            with mido.open_input(in_name) as inp, mido.open_output(out_name) as outp:
                print("[INFO] Router läuft … [Strg+C beendet]")
                for msg in inp:
                    if msg.type == "control_change":
                        cc = msg.control
                        if cc in mappings:
                            new_cc = mappings[cc]
                            outp.send(msg.copy(control=new_cc))
                            if DEBUG: print(f"CC {cc:>3} → {new_cc:>3}  val={msg.value:>3}")
                            continue
                    if pass_other:
                        outp.send(msg)
                        if DEBUG: print(f"PASS {msg.type}: {msg.dict()}")

        except LookupError as e:
            print(f"[WARN] {e} | Neuer Versuch in 3s …"); _sleep_cancellable(3)
        except (OSError, IOError) as e:
            print(f"[ERROR] MIDI-Port verloren: {e} | Reconnect in 3s …"); _sleep_cancellable(3)
        except KeyboardInterrupt:
            print("\n[INFO] Beendet durch Benutzer."); break
        except Exception as e:
            print(f"[ERROR] Unerwartet: {e} | Reconnect in 3s …"); _sleep_cancellable(3)

def _sleep_cancellable(sec: float):
    end = time.time() + sec
    while time.time() < end:
        time.sleep(0.1)

def main():
    # optional config file as first argument
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cfg_path = os.path.expanduser(args[0]) if args else DEFAULT_CFG
    if not os.path.isfile(cfg_path):
        sys.exit(f"Config fehlt: {cfg_path}")
    router(cfg_path)

if __name__ == "__main__":
    main()