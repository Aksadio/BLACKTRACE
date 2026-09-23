from __future__ import annotations

import random
import time
import tkinter as tk
from tkinter import ttk

from simulation.engine import Event, SimulationEngine, build_scenario
from simulation.fake_data import EASTER_EGGS, FAKE_COMMANDS, generated_key, metric, nodes, session_snapshot

BG = "#070a0f"
PANEL = "#0c1119"
PANEL_2 = "#101823"
GRID = "#182533"
CYAN = "#55d7ff"
BLUE = "#4f89ff"
WHITE = "#dcecff"
MUTED = "#71859a"
RED = "#ff5572"
GREEN = "#71e4b0"
FONT = ("Consolas", 10)


class BlacktraceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BLACKTRACE // ZERO-DAY SIMULATION")
        self.geometry("1440x900")
        self.minsize(1100, 720)
        self.configure(bg=BG)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.bind("<Escape>", lambda _e: self.destroy())
        self.bind("<Return>", lambda _e: self.engine.accelerate())
        self.bind("<space>", lambda _e: self.toggle_pause())
        self.bind("<KeyPress-m>", lambda _e: self.toggle_sound())
        self.bind("<F11>", lambda _e: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        self.sound_on = True
        self.paused = False
        self.phase = "CALM"
        self.snapshot = session_snapshot()
        self.engine = SimulationEngine(self._engine_emit)
        self._build_style()
        self._build_intro()

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Thin.Horizontal.TProgressbar", troughcolor=GRID, background=CYAN, bordercolor=GRID, lightcolor=CYAN, darkcolor=CYAN, thickness=5)

    def _build_intro(self):
        self.intro = tk.Frame(self, bg="#000000")
        self.intro.pack(fill="both", expand=True)
        self.intro_text = tk.Label(self.intro, text="", fg=WHITE, bg="#000000", font=("Consolas", 16), justify="left", anchor="w")
        self.intro_text.place(relx=.12, rely=.35, relwidth=.76, relheight=.3)
        self._intro_lines = []
        self.after(250, self._intro_step)

    def _intro_step(self):
        lines = ["BLACKTRACE", "ADVANCED CYBER OPERATIONS PLATFORM", "INITIALIZING...", "OPERATION: ZERO-DAY\nMODE: SIMULATION\nSECURITY LEVEL: OMEGA"]
        if len(self._intro_lines) < len(lines):
            self._intro_lines.append(lines[len(self._intro_lines)])
            self.intro_text.config(text="\n\n".join(self._intro_lines))
            self.after(850, self._intro_step)
        else:
            self.after(900, self._show_dashboard)

    def _show_dashboard(self):
        self.intro.destroy()
        self._build_dashboard()
        self.engine.load(build_scenario())
        self.engine.start()

    def _label(self, parent, text, size=9, color=MUTED, bold=False):
        return tk.Label(parent, text=text, bg=parent.cget("bg"), fg=color, font=("Consolas", size, "bold" if bold else "normal"), anchor="w")

    def _panel(self, parent, title, row, col, rowspan=1, colspan=1):
        frame = tk.Frame(parent, bg=PANEL, highlightbackground=GRID, highlightthickness=1)
        frame.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan, sticky="nsew", padx=6, pady=6)
        head = tk.Frame(frame, bg=PANEL_2, height=30)
        head.pack(fill="x")
        tk.Label(head, text=f"  {title}", bg=PANEL_2, fg=CYAN, font=("Consolas", 9, "bold"), anchor="w").pack(fill="both", expand=True)
        return frame

    def _build_dashboard(self):
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=12, pady=10)
        top = tk.Frame(root, bg=BG)
        top.pack(fill="x", pady=(0, 8))
        tk.Label(top, text="BLACKTRACE", bg=BG, fg=WHITE, font=("Consolas", 19, "bold")).pack(side="left")
        tk.Label(top, text="  //  ADVANCED CYBER OPERATIONS PLATFORM", bg=BG, fg=MUTED, font=("Consolas", 9)).pack(side="left", pady=7)
        self.phase_label = tk.Label(top, text="●  CALM / SIMULATION", bg=BG, fg=GREEN, font=("Consolas", 9, "bold"))
        self.phase_label.pack(side="right", padx=12)
        self.sound_btn = tk.Button(top, text="SOUND: ON", command=self.toggle_sound, bg=PANEL, fg=CYAN, activebackground=GRID, activeforeground=WHITE, relief="flat", font=FONT, padx=10)
        self.sound_btn.pack(side="right")

        grid = tk.Frame(root, bg=BG)
        grid.pack(fill="both", expand=True)
        grid.columnconfigure(1, weight=1); grid.rowconfigure(0, weight=1); grid.rowconfigure(1, weight=1)
        left = self._panel(grid, "OPERATION STATUS", 0, 0, rowspan=2)
        left.configure(width=220); left.grid_propagate(False)
        self._status_block(left, "OPERATION", "ZERO-DAY")
        self._status_block(left, "STATUS", "ACTIVE [SIMULATION]", GREEN)
        self._status_block(left, "THREAT LEVEL", "ELEVATED", "#f8c56b")
        self._status_block(left, "SESSION", self.snapshot["session"], CYAN)
        self._status_block(left, "ENCRYPTION", "AES-256 [SIMULATED]", BLUE)
        tk.Label(left, text="\nFICTIONAL TELEMETRY\nNO HOST ACCESS\nNO NETWORK ACTIVITY", bg=PANEL, fg=MUTED, font=("Consolas", 8), justify="left", anchor="w").pack(side="bottom", fill="x", padx=14, pady=18)

        terminal = self._panel(grid, "LIVE OPERATION STREAM  /  VIRTUAL ENVIRONMENT", 0, 1)
        terminal.rowconfigure(1, weight=1); terminal.columnconfigure(0, weight=1)
        self.terminal = tk.Text(terminal, bg="#080d13", fg=WHITE, insertbackground=CYAN, relief="flat", font=("Consolas", 10), padx=14, pady=12, wrap="word")
        self.terminal.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        self.terminal.tag_configure("muted", foreground=MUTED); self.terminal.tag_configure("cyan", foreground=CYAN); self.terminal.tag_configure("red", foreground=RED); self.terminal.tag_configure("green", foreground=GREEN)
        self.cmd_var = tk.StringVar()
        entry = tk.Entry(terminal, textvariable=self.cmd_var, bg="#0a1119", fg=CYAN, insertbackground=CYAN, relief="flat", font=FONT)
        entry.grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 8)); entry.bind("<Return>", self._typed_command)
        self._terminal_cursor()

        right = self._panel(grid, "SYSTEM INTELLIGENCE", 0, 2)
        right.configure(width=260); right.grid_propagate(False)
        self._metric = {}
        for name, value in [("CPU LOAD", "42%"), ("MEMORY", "61%"), ("NETWORK", "SECURE"), ("FIREWALL", "ACTIVE"), ("ENCRYPTION", "ENABLED"), ("THREAT EVENTS", "03"), ("TRACE STATUS", "UNDETECTED")]:
            row = tk.Frame(right, bg=PANEL); row.pack(fill="x", padx=14, pady=6)
            tk.Label(row, text=name, bg=PANEL, fg=MUTED, font=("Consolas", 8), anchor="w").pack(side="left")
            lab = tk.Label(row, text=value, bg=PANEL, fg=WHITE if name != "TRACE STATUS" else GREEN, font=("Consolas", 9, "bold"), anchor="e"); lab.pack(side="right"); self._metric[name] = lab
        nexus = self._panel(grid, "NEXUS AI  /  COGNITIVE ENGINE", 1, 2)
        for text, value in [("Pattern recognition", "82%"), ("Threat correlation", "91%"), ("Route prediction", "64%"), ("Decision confidence", "99%")]:
            tk.Label(nexus, text=text, bg=PANEL, fg=MUTED, font=("Consolas", 8), anchor="w").pack(fill="x", padx=14, pady=(9, 0))
            ttk.Progressbar(nexus, style="Thin.Horizontal.TProgressbar", value=int(value[:-1]), maximum=100).pack(fill="x", padx=14, pady=(3, 0))
        self.nexus_text = tk.Label(nexus, text="\n[NEXUS]\nAwaiting simulated telemetry...", bg=PANEL, fg=CYAN, font=("Consolas", 9), justify="left", anchor="nw")
        self.nexus_text.pack(fill="both", expand=True, padx=14, pady=12)

        bottom = tk.Frame(root, bg=BG); bottom.pack(fill="x", pady=(7, 0))
        self.map_canvas = tk.Canvas(bottom, height=160, bg=PANEL, highlightbackground=GRID, highlightthickness=1); self.map_canvas.pack(side="left", fill="both", expand=True, padx=(0, 6))
        self._draw_map()
        controls = tk.Frame(bottom, bg=PANEL, width=190, highlightbackground=GRID, highlightthickness=1); controls.pack(side="right", fill="y"); controls.pack_propagate(False)
        tk.Label(controls, text="OPERATION TIMELINE", bg=PANEL, fg=CYAN, font=("Consolas", 9, "bold")).pack(anchor="w", padx=12, pady=10)
        self.progress = ttk.Progressbar(controls, style="Thin.Horizontal.TProgressbar", maximum=100, value=0); self.progress.pack(fill="x", padx=12)
        self.progress_label = tk.Label(controls, text="SEQUENCE  00%", bg=PANEL, fg=MUTED, font=("Consolas", 8)); self.progress_label.pack(anchor="w", padx=12, pady=5)
        self.pause_btn = tk.Button(controls, text="PAUSE", command=self.toggle_pause, bg=PANEL_2, fg=WHITE, relief="flat", font=FONT); self.pause_btn.pack(fill="x", padx=12, pady=(8, 4))
        tk.Button(controls, text="EXIT SIMULATION", command=self.destroy, bg="#17121b", fg=RED, relief="flat", font=("Consolas", 9, "bold")).pack(fill="x", padx=12, pady=4)
        self._animate_map()

    def _status_block(self, parent, name, value, color=WHITE):
        box = tk.Frame(parent, bg=PANEL); box.pack(fill="x", padx=14, pady=(16, 0))
        tk.Label(box, text=name, bg=PANEL, fg=MUTED, font=("Consolas", 8), anchor="w").pack(fill="x")
        tk.Label(box, text=value, bg=PANEL, fg=color, font=("Consolas", 10, "bold"), anchor="w", wraplength=185).pack(fill="x", pady=(3, 0))

    def _draw_map(self):
        self.map_nodes = nodes()
        self.map_canvas.create_text(14, 14, text="SIMULATED NETWORK MAP  /  ROUTE ANALYSIS", fill=CYAN, font=("Consolas", 9, "bold"), anchor="w")
        for i in range(len(self.map_nodes) - 1):
            _, x1, y1 = self.map_nodes[i]; _, x2, y2 = self.map_nodes[i + 1]
            self.map_canvas.create_line(x1 + 26, y1 + 45, x2 + 26, y2 + 45, fill=GRID, width=1, tags="link")
        for name, x, y in self.map_nodes:
            self.map_canvas.create_oval(x + 20, y + 39, x + 32, y + 51, fill="#152f45", outline=CYAN, tags="node")
            self.map_canvas.create_text(x + 40, y + 45, text=name, fill=MUTED, font=("Consolas", 8), anchor="w")

    def _animate_map(self):
        if not self.winfo_exists(): return
        for item in self.map_canvas.find_withtag("node"):
            self.map_canvas.itemconfigure(item, outline=random.choice([CYAN, BLUE, WHITE, GRID]))
        self.after(700, self._animate_map)

    def _terminal_cursor(self):
        if hasattr(self, "terminal") and self.terminal.winfo_exists():
            self.terminal.tag_delete("cursor"); self.terminal.insert("end", "▌\n", "cursor"); self.terminal.tag_configure("cursor", foreground=CYAN); self.terminal.after(600, self._terminal_cursor)

    def _engine_emit(self, kind, payload):
        if kind == "schedule":
            delay, event = payload
            self.after(delay, lambda e=event: self._handle_event(e))

    def _handle_event(self, event: Event):
        if not hasattr(self, "terminal") or not self.winfo_exists(): return
        if event.kind == "intro": return
        if event.kind == "phase": self._set_phase("CURIOUS"); self._log("Virtual dashboard online.", "cyan")
        elif event.kind == "log": self._log(f"[{time.strftime('%H:%M:%S')}] {event.payload}", "red" if "[!]" in str(event.payload) else "muted")
        elif event.kind == "nexus": self.nexus_text.config(text=f"\n[NEXUS]\n{event.payload}")
        elif event.kind == "status": self._metric["TRACE STATUS"].config(text=event.payload, fg=RED if event.payload == "DETECTED" else "#f8c56b"); self._set_phase("TENSION")
        elif event.kind == "countermeasure": self.progress["value"] = event.payload; self.progress_label.config(text=f"SEQUENCE  {event.payload:02d}%"); self._set_phase("PANIC" if event.payload >= 83 else "TENSION"); self._log(f"[!] COUNTERMEASURE PROTOCOL  {event.payload}%", "red")
        elif event.kind == "trace": self._trace_reveal()
        elif event.kind == "failure": self._log("\nSYSTEM FAILURE", "red"); self._set_phase("SILENCE")
        elif event.kind == "reveal": self._final_reveal()
        elif event.kind == "second_reveal": self._second_reveal()
        self.engine.on_event_complete()

    def _log(self, text, tag="muted"):
        self.terminal.insert("end", text + "\n", tag); self.terminal.see("end")
        if self.sound_on and ("[!]" in text or "SYSTEM" in text): self.bell()

    def _trace_reveal(self):
        self._metric["TRACE STATUS"].config(text="DETECTED", fg=RED)
        self._log("\n!!! WARNING !!!\nEXTERNAL TRACE DETECTED\nSOURCE: UNKNOWN\nTRACE DISTANCE: 0.7 KM\nRESPONSE: IMMEDIATE", "red")
        self.nexus_text.config(text="\n[NEXUS AI]\nWait...\n\nThis doesn't look right.")
        self._set_phase("PANIC")

    def _final_reveal(self):
        self._set_phase("PRANK REVEAL")
        win = tk.Toplevel(self); win.attributes("-fullscreen", True); win.configure(bg="#050509"); win.bind("<Escape>", lambda _e: win.destroy())
        msg = tk.Label(win, text="╔══════════════════════════════════╗\n║                                  ║\n║          YOU GOT PRANKED         ║\n║                                  ║\n║      BLACKTRACE WAS FAKE.        ║\n║                                  ║\n╚══════════════════════════════════╝\n\nNO FILES WERE ACCESSED\nNO PASSWORDS WERE COLLECTED\nNO NETWORK WAS SCANNED\nNO SYSTEM SETTINGS WERE CHANGED\nNO HACKING OCCURRED\n\nIT WAS ALL A SIMULATION.", bg="#050509", fg=CYAN, font=("Consolas", 19, "bold"), justify="center")
        msg.pack(expand=True)
        self.reveal_win = win
        self.after(2600, lambda: win.destroy() if win.winfo_exists() else None)

    def _second_reveal(self):
        if hasattr(self, "reveal_win") and self.reveal_win.winfo_exists(): self.reveal_win.destroy()
        self._log("\nWAIT...\n\nNEXUS AI HAS ONE MORE MESSAGE.\n\n[NEXUS]\nHonestly...\nI think you were the easiest target today. 😂\n\nOPERATION STATUS: PRANK SUCCESSFUL", "cyan")
        self.nexus_text.config(text="\n[NEXUS]\nHonestly...\nI think you were the easiest target today. 😂\n\nPRANK SUCCESSFUL", fg=GREEN)

    def _set_phase(self, phase):
        self.phase = phase; self.phase_label.config(text=f"●  {phase} / SIMULATION", fg=RED if phase in ("PANIC", "TENSION") else (GREEN if phase == "CALM" else CYAN))

    def toggle_pause(self):
        self.paused = self.engine.toggle_pause(); self.pause_btn.config(text="RESUME" if self.paused else "PAUSE")

    def toggle_sound(self):
        self.sound_on = not self.sound_on; self.sound_btn.config(text=f"SOUND: {'ON' if self.sound_on else 'OFF'}")

    def _typed_command(self, _event=None):
        command = self.cmd_var.get().strip().lower(); self.cmd_var.set("")
        self._log(f"> {command}", "cyan")
        if command in EASTER_EGGS:
            self.nexus_text.config(text="\n[NEXUS]\n" + "\n".join(EASTER_EGGS[command]), fg=GREEN)
        elif command:
            self._log("Visual command acknowledged. No operating-system command was executed.", "muted")


if __name__ == "__main__":
    app = BlacktraceApp()
    app.mainloop()
