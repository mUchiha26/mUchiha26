#!/usr/bin/env python3
"""Generates every SVG used by README.md.

Edit the PALETTE / CONTENT blocks, run `python build_assets.py`, commit assets/.
Why a script: one palette, one place. Changing the accent color is a 1-line edit
instead of hand-editing 12 SVGs.
"""
import textwrap
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).parent / "assets"
(ROOT / "projects").mkdir(parents=True, exist_ok=True)

# ---------- PALETTE (match these to your terminal theme) ----------
BG, SURFACE, LINE = "#0b1020", "#111a2e", "#1e2d4a"
TEXT, MUTED = "#d6e2ff", "#7d8fb3"
ACCENT, GLOW = "#3b82f6", "#5aa9ff"
FONT = "JetBrains Mono, Fira Code, SF Mono, Menlo, Consolas, monospace"

# ---------- CONTENT ----------
NAME = "Yasseene"
TAGLINE = "Security-first computer engineering student"
SUBLINE = "Offensive and defensive tooling, with AI where it earns its place."

TERMINAL = [
    ("cmd", "whoami"),
    ("out", "yasseene: computer engineering student, TEK-UP, Tunisia"),
    ("cmd", "cat focus.txt"),
    ("out", "offensive security, defensive security, AI engineering"),
    ("cmd", "ls projects/"),
    ("out", "sharingan/  helix/  splunksploit2/  loopvolta/"),
    ("cmd", "cat now.txt"),
    ("out", "building toward a summer 2027 cybersecurity internship"),
]

SECTIONS = {"about": "About", "projects": "Projects", "stack": "Stack",
            "certs": "Certifications", "activity": "Activity", "contact": "Contact"}

# slug, name, description, stack, status  (verify the statuses are true today)
PROJECTS = [
    ("sharingan", "Sharingan",
     "AI-assisted red team CLI. Maps recon output to MITRE ATT&CK using local LLMs.",
     "Python, local LLMs, MITRE ATT&CK", "in progress"),
    ("helix", "HELIX",
     "Blue team counterpart to Sharingan: detection, automation and dashboards for defenders.",
     "Python, anomaly detection, dashboards", "paused"),
    ("splunksploit2", "SplunkSploit2",
     "Isolated lab: Kali attacks Metasploitable 2 while Splunk monitors every step.",
     "Splunk, Kali, Metasploitable 2, VMware", "in progress"),
    ("loopvolta", "LoopVolta",
     "AI-powered autonomous robot that classifies waste and converts it into energy.",
     "Robotics, AI, green energy", "in progress"),
]

# ---------- helpers ----------
def write(path, w, h, body, css="", label=""):
    (ROOT / path).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">\n'
        f'<style>text{{font-family:{FONT}}}{css}'
        f'@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>\n'
        f'{body}\n</svg>\n', encoding="utf-8")

def header():
    css = ("@keyframes scan{from{transform:translateY(-40px)}to{transform:translateY(280px)}}"
           "@keyframes blink{50%{opacity:0}}"
           ".scan{animation:scan 7s linear infinite}.cur{animation:blink 1.1s steps(1) infinite}")
    body = f'''<defs>
<pattern id="g" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{LINE}" opacity=".5"/></pattern>
<linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/><stop offset="1" stop-color="{ACCENT}" stop-opacity=".22"/></linearGradient>
<clipPath id="c"><rect width="1000" height="240" rx="16"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="1000" height="240" fill="{BG}"/><rect width="1000" height="240" fill="url(#g)"/>
<rect class="scan" width="1000" height="40" fill="url(#s)"/></g>
<rect x=".5" y=".5" width="999" height="239" rx="16" fill="none" stroke="{LINE}"/>
<text x="56" y="112" font-size="56" font-weight="700" fill="{TEXT}">{esc(NAME)}<tspan class="cur" fill="{ACCENT}">_</tspan></text>
<text x="58" y="156" font-size="18" fill="{GLOW}">{esc(TAGLINE)}</text>
<text x="58" y="186" font-size="14" fill="{MUTED}">{esc(SUBLINE)}</text>'''
    write("header.svg", 1000, 240, body, css, f"{NAME}: {TAGLINE}")

def terminal():
    w, n = 860, len(TERMINAL)
    h = 64 + (n + 1) * 26 + 16
    css = ("@keyframes reveal{from{opacity:0}}@keyframes blink{50%{opacity:0}}"
           ".r{animation:reveal .35s ease both}.cur{animation:blink 1.1s steps(1) infinite}")
    rows = []
    for i, (kind, text) in enumerate(TERMINAL):
        y, d = 84 + i * 26, f'style="animation-delay:{i*0.55:.2f}s"'
        if kind == "cmd":
            rows.append(f'<text class="r" {d} x="28" y="{y}" font-size="15"><tspan fill="{ACCENT}">❯</tspan><tspan fill="{TEXT}" dx="10">{esc(text)}</tspan></text>')
        else:
            rows.append(f'<text class="r" {d} x="48" y="{y}" font-size="15" fill="{MUTED}">{esc(text)}</text>')
    y = 84 + n * 26
    d = f'style="animation-delay:{n*0.55:.2f}s"'
    rows.append(f'<text class="r" {d} x="28" y="{y}" font-size="15" fill="{ACCENT}">❯</text>')
    rows.append(f'<rect class="cur" x="48" y="{y-14}" width="9" height="18" fill="{GLOW}"/>')
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="{BG}" stroke="{LINE}"/>'
            f'<path d="M.5 40H{w-.5}" stroke="{LINE}"/>'
            + "".join(f'<circle cx="{24+i*20}" cy="20" r="5" fill="{LINE}"/>' for i in range(3))
            + f'<text x="{w/2}" y="25" text-anchor="middle" font-size="13" fill="{MUTED}">~/profile</text>'
            + "".join(rows))
    write("terminal.svg", w, h, body, css, "Animated terminal: whoami, focus, projects, current goal")

def divider():
    css = "@keyframes run{from{transform:translateX(120px)}to{transform:translateX(880px)}}.p{animation:run 6s ease-in-out infinite alternate}"
    body = (f'<defs><linearGradient id="d"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient></defs>'
            f'<rect y="5" width="1000" height="2" fill="url(#d)"/><circle class="p" cx="0" cy="6" r="3" fill="{GLOW}"/>')
    write("divider.svg", 1000, 12, body, css, "")

def title(slug, text):
    w = int(56 + len(text) * 12.6)
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="43" rx="10" fill="{SURFACE}" stroke="{LINE}"/>'
            f'<rect x="14" y="12" width="4" height="20" rx="2" fill="{ACCENT}"/>'
            f'<text x="32" y="29" font-size="20" font-weight="700" fill="{TEXT}">{esc(text)}</text>')
    write(f"title-{slug}.svg", w, 44, body, "", text)

def card(slug, name, desc, stack, status):
    w, h = 490, 150
    live = status != "paused"
    pw = len(status) * 8 + 24
    lines = textwrap.wrap(desc, 50)[:2]
    desc_svg = "".join(f'<text x="28" y="{74+i*20}" font-size="13" fill="{TEXT}">{esc(l)}</text>' for l, i in zip(lines, range(2)))
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="{SURFACE}" stroke="{LINE}"/>'
            f'<rect x="0" y="22" width="4" height="30" rx="2" fill="{ACCENT if live else MUTED}"/>'
            f'<text x="28" y="44" font-size="20" font-weight="700" fill="{TEXT}">{esc(name)}</text>'
            f'<rect x="{w-24-pw}" y="26" width="{pw}" height="22" rx="11" fill="none" stroke="{GLOW if live else MUTED}"/>'
            f'<text x="{w-24-pw/2}" y="41" text-anchor="middle" font-size="11" fill="{GLOW if live else MUTED}">{esc(status)}</text>'
            f'{desc_svg}<text x="28" y="{h-22}" font-size="12" fill="{MUTED}">{esc(stack)}</text>')
    write(f"projects/{slug}.svg", w, h, body, "", f"{name}: {desc}")

if __name__ == "__main__":
    header(); terminal(); divider()
    for s, t in SECTIONS.items():
        title(s, t)
    for p in PROJECTS:
        card(*p)
    print("assets/ rebuilt")
