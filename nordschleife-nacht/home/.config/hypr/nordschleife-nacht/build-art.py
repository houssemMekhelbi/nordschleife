#!/usr/bin/env python3
"""Generate the Nordschleife nacht art: everything that is an image rather than CSS.

  ~/.config/hypr/nordschleife-nacht/wallpaper.svg, wallpaper.png   1920x1080: the circuit's outline as a survey
        drawing (a thin line with kilometre ticks, sector marks, one corner called out in
        orange, an elevation strip) on a perforated dial, by night. The left of the picture
        is kept empty for windows. No car, no badge.
  ~/.config/hypr/nordschleife-nacht/lock-scale.png    the lock's lap scale without needle and sector fill (what
        the lock shows until ~/.local/bin/nordschleife-lock-scale has rendered the current minute)
  ~/.config/hypr/nordschleife-nacht/lock-field.png    440x50 the password plate with crop marks
  ~/.config/waybar/nordschleife-nacht/ws-<slot>-<state>.png   40x38 numerals 1-10 in five states, standing on
        the plate's tick scale; focused, active and urgent carry a needle
  ~/.config/waybar/nordschleife-nacht/ws.css          the rules that pick them (imported by style.css)
  ~/.config/waybar/nordschleife-nacht/scale.png       40x7 tile of the tick scale (major tick every 40px, minor every 8px)
  ~/.config/waybar/nordschleife-nacht/frame.png       15x15 9-slice frame: hairline edges with a crop mark on every corner
  ~/.config/gtk-3.0/nordschleife-nacht/crumb-tick.png Thunar path separator; scale.png is copied there too
  ~/.config/swaync/nordschleife-nacht/frame.png       the same frame for notification cards

Deterministic; edit and re-run (needs rsvg-convert and the theme's fonts):  python3 build-art.py
"""

import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

CONF = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
HYPR = CONF / "hypr/nordschleife-nacht"
BAR = CONF / "waybar/nordschleife-nacht"
GTK = CONF / "gtk-3.0/nordschleife-nacht"
NOTI = CONF / "swaync/nordschleife-nacht"

GROUND, PANEL, LINE, DIM, MUTED_C, ALU_C, TEXT = "#0A0A0B", "#16181B", "#2E3238", "#6B717A", "#8A9099", "#C9CDD2", "#F4F5F6"
ORANGE_C, ORANGE_T, RED_T, TICK_MAJOR, TICK_MINOR = "#FF6A1A", "#FF6A1A", "#F5555B", "#C9CDD2", "#8A9099"

# wallpaper colours per variant
WALL = dict(
    nacht=dict(alu="#C9CDD2", white="#F4F5F6", muted="#8A9099", hair="#2E3238", g=("#121417", "#16181B", "#0D0E10"),
               lift=("#23262B", "#1A1C20", "#0A0A0B"), vig="#0A0A0B", vig_op=0.75, hole="#08090A", rim="#454B53", hide=0.5,
               shadow="#000", shadow_op=0.55, bed="#1F2226"),
    tag=dict(alu="#2B2F35", white="#0F1113", muted="#555B64", hair="#B9BEC6", g=("#ECEEF1", "#E4E7EB", "#D9DDE2"),
             lift=("#F7F8F9", "#EEF0F2", "#E9EBEE"), vig="#9AA1AB", vig_op=0.45, hole="#BFC5CD", rim="#FFFFFF", hide=0.10,
             shadow="#5A606A", shadow_op=0.30, bed="#F5F6F7"),
)
K = WALL["nacht"]


def render(svg, out, keep=False):
    out.parent.mkdir(parents=True, exist_ok=True)
    src = out.with_suffix(".svg")
    src.write_text(svg)
    subprocess.run(["rsvg-convert", "-o", str(out), str(src)], check=True)
    if not keep:
        src.unlink()


# ---- wallpaper -------------------------------------------------------------------
def wallpaper():
    W, H = 1920, 1080
    ALU, WHITE, ORANGE, MUTED, HAIR = K["alu"], K["white"], "#FF6A1A", K["muted"], K["hair"]
    FONT = "Barlow Semi Condensed, DejaVu Sans Condensed, sans-serif"

    # control points, clockwise from the start line (south-west), y down. Names are only comments.
    P = [
        (1004, 800), (978, 790), (958, 770),                         # start, link
        (950, 748), (932, 738), (928, 716), (908, 706), (902, 684),  # Hatzenbach esses
        (884, 660), (880, 632), (862, 604),                          # Hocheichen, Quiddelbacher Hoehe
        (858, 566), (842, 528), (846, 490), (830, 452),              # Flugplatz, Schwedenkreuz
        (822, 418), (836, 392), (866, 388),                          # Aremberg
        (902, 398), (940, 380), (972, 352),                          # Fuchsroehre
        (990, 326), (1014, 330), (1026, 308), (1052, 300),           # Adenauer Forst
        (1086, 304), (1112, 282), (1104, 256), (1128, 238),          # Metzgesfeld, Kallenhard
        (1162, 246), (1182, 222), (1170, 198), (1196, 184),          # Wehrseifen
        (1236, 196), (1268, 182), (1302, 196), (1330, 178),          # Breidscheid, Ex-Muehle, Lauda-Links
        (1366, 166), (1390, 180), (1392, 210),                       # Bergwerk
        (1416, 246), (1452, 270), (1480, 304), (1520, 322),          # Kesselchen
        (1548, 350), (1570, 342), (1592, 366),                       # Klostertal
        (1597, 400), (1621, 418), (1645, 402), (1646, 374), (1668, 360),   # Karussell (index 47..51)
        (1700, 372), (1738, 398), (1776, 410), (1800, 440),          # Hohe Acht
        (1794, 476), (1812, 504), (1790, 530), (1796, 560),          # Wippermann, Eschbach
        (1764, 584), (1752, 616), (1716, 632), (1700, 664),          # Bruennchen, Eiskurve
        (1664, 682), (1640, 716), (1652, 744), (1622, 768),          # Pflanzgarten
        (1586, 776), (1570, 806), (1536, 812), (1524, 842),          # Schwalbenschwanz
        (1496, 858), (1488, 884), (1456, 892),                       # kleines Karussell, Galgenkopf
        (1400, 884), (1300, 868), (1200, 850), (1120, 836),          # Doettinger Hoehe
        (1082, 832), (1058, 816), (1036, 818),                       # Tiergarten, Hohenrain
    ]
    KAR = (46, 49)   # control-point span drawn in orange

    # the GP loop: a second, fainter line hanging from the start straight (open path, joins the main loop at both ends)
    GP = [(1036, 818), (1004, 800), (960, 806), (900, 822), (866, 834), (850, 856), (868, 874), (896, 866), (914, 884), (896, 906), (906, 930),
          (940, 938), (990, 930), (1030, 944), (1062, 966), (1086, 956), (1080, 928), (1052, 906), (1060, 880), (1088, 866), (1096, 844),
          (1082, 832)]

    def catmull(pts, closed=True, n=16):
        out, idx = [], []
        m = len(pts)
        rng = range(m) if closed else range(m - 1)
        for i in rng:
            if closed:
                p0, p1, p2, p3 = pts[(i - 1) % m], pts[i], pts[(i + 1) % m], pts[(i + 2) % m]
            else:
                p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, m - 1)]
            for k in range(n):
                t = k / n
                t2, t3 = t * t, t * t * t
                x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
                y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
                out.append((x, y)); idx.append(i)
        if not closed:
            out.append(pts[-1]); idx.append(m - 1)
        return out, idx

    def d_of(pts, close=False):
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if close else "")

    def build(scale=1.0, ox=0, oy=0):
        tr = lambda pts: [(ox + x * scale, oy + y * scale) for x, y in pts]
        main, idx = catmull(tr(P))
        gp, _ = catmull(tr(GP), closed=False)
        return main, idx, gp

    SQ = lambda pts: [(1320 + (x - 1320) * 1.05, 585 + (y - 585) * 0.80) for x, y in pts]
    P, GP = SQ(P), SQ(GP)
    main, idx, gp = build(1.0, 0, 0)
    n = len(main)
    seg = [math.dist(main[i], main[(i + 1) % n]) for i in range(n)]
    total = sum(seg)
    KM = 20.832

    def at(dist):
        dist %= total
        acc = 0
        for i in range(n):
            if acc + seg[i] >= dist:
                t = (dist - acc) / seg[i]
                a, b = main[i], main[(i + 1) % n]
                x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
                L = math.dist(a, b)
                tx, ty = (b[0] - a[0]) / L, (b[1] - a[1]) / L
                return x, y, -ty, tx      # point and left normal (outside for a clockwise loop with y down is the left side)
            acc += seg[i]

    ticks, labels = "", ""
    for half in range(0, int(KM * 2) + 1):
        km = half / 2
        x, y, nx, ny = at(total * km / KM)
        major = half % 10 == 0
        whole = half % 2 == 0
        ln = 16 if major else (9 if whole else 5)
        col = ALU if major else MUTED
        op = 0.95 if major else (0.75 if whole else 0.5)
        ticks += f'<line x1="{x + nx * 4:.1f}" y1="{y + ny * 4:.1f}" x2="{x + nx * (4 + ln):.1f}" y2="{y + ny * (4 + ln):.1f}" stroke="{col}" stroke-opacity="{op}" stroke-width="{1.4 if major else 1}"/>'
        if major and km > 0:
            lx, ly = x + nx * 34, y + ny * 34 + 5
            labels += f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-family="{FONT}" font-size="15" letter-spacing="1" fill="{WHITE}" fill-opacity="0.9">{int(km)}</text>'
    # sector marks on the inside: three sectors
    for k, name in enumerate(("S1", "S2", "S3")):
        x, y, nx, ny = at(total * (k / 3))
        ticks += f'<line x1="{x - nx * 4:.1f}" y1="{y - ny * 4:.1f}" x2="{x - nx * 22:.1f}" y2="{y - ny * 22:.1f}" stroke="{WHITE}" stroke-width="1.4"/>'
        labels += f'<text x="{x - nx * 38:.1f}" y="{y - ny * 38 + 4:.1f}" text-anchor="middle" font-family="{FONT}" font-size="11" letter-spacing="2" fill="{MUTED}">{name}</text>'
    # start line: a short double bar across the track
    x, y, nx, ny = at(0)
    start = "".join(f'<line x1="{x + dx - nx * 7:.1f}" y1="{y - ny * 7:.1f}" x2="{x + dx + nx * 7:.1f}" y2="{y + ny * 7:.1f}" stroke="{WHITE}" stroke-width="1.6"/>' for dx in (-2.5, 2.5))

    kar = [p for p, i in zip(main, idx) if KAR[0] <= i <= KAR[1]]
    kx, ky = kar[len(kar) // 2]
    callout = (f'<path d="M{kx:.0f},{ky + 12:.0f} V{ky + 58:.0f} H{kx - 150:.0f} M{kx - 4:.0f},{ky + 12:.0f} H{kx + 4:.0f}" fill="none" stroke="{MUTED}" stroke-opacity="0.7" stroke-width="1"/>'
               f'<text x="{kx - 150:.0f}" y="{ky + 51:.0f}" font-family="{FONT}" font-size="11" letter-spacing="2.5" fill="{ORANGE}">KARUSSELL</text>'
               f'<text x="{kx - 150:.0f}" y="{ky + 74:.0f}" font-family="{FONT}" font-size="10" letter-spacing="2" fill="{MUTED}">STEILKURVE · 210°</text>')

    # elevation strip, bottom right: a hairline profile over a tick scale (invented but plausible: down to Breidscheid, up to Hohe Acht)
    ex0, ex1, ey = 1180, 1840, 1012
    prof = []
    for k in range(0, 201):
        t = k / 200
        if t < 0.47:
            e = 0.60 - 0.52 * math.sin(math.pi / 2 * t / 0.47) ** 1.2 + 0.03 * math.sin(t * 60)
        elif t < 0.66:
            e = 0.08 + 0.92 * math.sin(math.pi / 2 * (t - 0.47) / 0.19) ** 1.1 + 0.02 * math.sin(t * 70)
        else:
            u = (t - 0.66) / 0.34
            e = 1.0 - 0.52 * math.sin(math.pi / 2 * min(u / 0.62, 1)) + 0.22 * max(0, (u - 0.62) / 0.38) ** 1.2 + 0.03 * math.sin(t * 55)
        prof.append((ex0 + (ex1 - ex0) * t, ey - 6 - e * 44))
    scale = "".join(f'<line x1="{ex0 + (ex1 - ex0) * k / KM:.1f}" y1="{ey}" x2="{ex0 + (ex1 - ex0) * k / KM:.1f}" y2="{ey + (9 if k % 5 == 0 else 5)}" stroke="{ALU if k % 5 == 0 else MUTED}" stroke-opacity="{0.9 if k % 5 == 0 else 0.55}" stroke-width="1"/>' for k in range(0, 21))
    scale += "".join(f'<text x="{ex0 + (ex1 - ex0) * k / KM:.1f}" y="{ey + 24}" text-anchor="middle" font-family="{FONT}" font-size="10" letter-spacing="1" fill="{MUTED}">{k}</text>' for k in (0, 5, 10, 15, 20))
    kx13 = ex0 + (ex1 - ex0) * 13 / KM
    elevation = (f'<line x1="{ex0}" y1="{ey}" x2="{ex1}" y2="{ey}" stroke="{HAIR}" stroke-width="1"/>{scale}'
                 f'<path d="{d_of(prof)}" fill="none" stroke="{ALU}" stroke-opacity="0.8" stroke-width="1.2"/>'
                 f'<line x1="{kx13:.1f}" y1="{ey - 56}" x2="{kx13:.1f}" y2="{ey}" stroke="{ORANGE}" stroke-width="1.2"/>'
                 f'<text x="{ex0}" y="{ey - 58}" font-family="{FONT}" font-size="10" letter-spacing="2.5" fill="{MUTED}">HÖHENPROFIL · 320–617 M</text>'
                 f'<text x="{ex1}" y="{ey - 58}" text-anchor="end" font-family="{FONT}" font-size="10" letter-spacing="2.5" fill="{MUTED}">20,832 KM · 73 KURVEN</text>')

    # registration crosses on a 120 px grid, fading out to the left
    dial = ""
    for gx in range(120, W, 120):
        for gy in range(120, H, 120):
            op = max(0.0, min(1.0, (gx - 480) / 700)) * 0.34
            if op <= 0.02:
                continue
            dial += f'<path d="M{gx - 5},{gy} H{gx + 5} M{gx},{gy - 5} V{gy + 5}" stroke="{ALU}" stroke-opacity="{op:.2f}" stroke-width="1"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
    <defs>
    <linearGradient id="ground" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{K["g"][0]}"/><stop offset="0.55" stop-color="{K["g"][1]}"/><stop offset="1" stop-color="{K["g"][2]}"/></linearGradient>
    <radialGradient id="lift" gradientUnits="userSpaceOnUse" cx="1330" cy="540" r="900"><stop offset="0" stop-color="{K["lift"][0]}" stop-opacity="0.85"/><stop offset="0.6" stop-color="{K["lift"][1]}" stop-opacity="0.35"/><stop offset="1" stop-color="{K["lift"][2]}" stop-opacity="0"/></radialGradient>
    <radialGradient id="vig" gradientUnits="userSpaceOnUse" cx="1100" cy="540" r="1250"><stop offset="0.55" stop-color="{K["vig"]}" stop-opacity="0"/><stop offset="1" stop-color="{K["vig"]}" stop-opacity="{K["vig_op"]}"/></radialGradient>
    <pattern id="perf" width="12" height="12" patternUnits="userSpaceOnUse">
    <circle cx="3" cy="3" r="1.5" fill="{K["hole"]}" fill-opacity="0.85"/><circle cx="9" cy="9" r="1.5" fill="{K["hole"]}" fill-opacity="0.85"/>
    <path d="M1.6,3.6 A1.6,1.6 0 0 0 4.4,3.6" fill="none" stroke="{K["rim"]}" stroke-opacity="0.7" stroke-width="0.6"/><path d="M7.6,9.6 A1.6,1.6 0 0 0 10.4,9.6" fill="none" stroke="{K["rim"]}" stroke-opacity="0.7" stroke-width="0.6"/>
    </pattern>
    <linearGradient id="perfmask-g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0.55"/><stop offset="0.45" stop-color="#fff" stop-opacity="0.9"/><stop offset="1" stop-color="#fff" stop-opacity="0.7"/></linearGradient>
    <mask id="perfmask"><rect width="{W}" height="{H}" fill="url(#perfmask-g)"/></mask>
    <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 0.9  0 0 0 0 0.92  0 0 0 0 0.95  0 0 0 0.07 0"/></filter>
    <filter id="hide" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.02" numOctaves="3" seed="21"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.55 -0.2"/></filter>
    <filter id="soft" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="5"/></filter>
    </defs>
    <rect width="{W}" height="{H}" fill="url(#ground)"/>
    <rect width="{W}" height="{H}" fill="url(#lift)"/>
    <rect width="{W}" height="{H}" fill="url(#perf)" mask="url(#perfmask)"/>
    <rect width="{W}" height="{H}" filter="url(#hide)" opacity="{K["hide"]}"/>
    {dial}
    <path d="{d_of(main, True)}" fill="none" stroke="{K["shadow"]}" stroke-opacity="{K["shadow_op"]}" stroke-width="14" stroke-linejoin="round" filter="url(#soft)"/>
    <path d="{d_of(main, True)}" fill="none" stroke="{K["bed"]}" stroke-width="9" stroke-linejoin="round"/>
    <path d="{d_of(gp)}" fill="none" stroke="{K["bed"]}" stroke-width="7" stroke-linejoin="round"/>
    <path d="{d_of(gp)}" fill="none" stroke="{MUTED}" stroke-opacity="0.75" stroke-width="1.2" stroke-linejoin="round" stroke-dasharray="1 0"/>
    <path d="{d_of(main, True)}" fill="none" stroke="{ALU}" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="{d_of(kar)}" fill="none" stroke="{ORANGE}" stroke-width="3.4" stroke-linecap="butt" stroke-linejoin="round"/>
    {ticks}{start}{labels}{callout}
    {elevation}
    <rect width="{W}" height="{H}" fill="url(#vig)"/>
    <rect width="{W}" height="{H}" filter="url(#grain)"/>
    </svg>'''
    render(svg, HYPR / "wallpaper.png", keep=True)


# ---- bar: numerals on the scale, the scale tile, crop marks -----------------------
def workspaces():
    """40x38 per slot and state: the numeral in Overpass Mono, and a 2px needle rising from
    the bottom edge for focused (orange, 11px), active elsewhere (aluminium, 11px) and urgent (red, 9px)."""
    states = {"empty": (DIM, 400, None, 0), "occupied": (ALU_C, 400, None, 0), "active": (TEXT, 400, ALU_C, 11),
              "focused": (ORANGE_T, 700, ORANGE_C, 11), "urgent": (RED_T, 700, RED_T, 9)}
    css = ["/* Generated by ~/.config/hypr/nordschleife-nacht/build-art.py: the numeral image for every slot and state. */"]
    for n in range(1, 11):
        for state, (fg, weight, needle, nh) in states.items():
            mark = f'<rect x="19" y="{38 - nh}" width="2" height="{nh}" fill="{needle}"/>' if needle else ""
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="40" height="38" viewBox="0 0 40 38">'
                   f'<text x="20" y="20.5" text-anchor="middle" font-family="Overpass Mono" font-weight="{weight}" font-size="13" fill="{fg}">{n}</text>{mark}</svg>')
            render(svg, BAR / f"ws-{n}-{state}.png")
            sel = f"#custom-ws-{n}" if state == "occupied" else f"#custom-ws-{n}.{state}"
            css.append(f'{sel} {{ background-image: url("ws-{n}-{state}.png"); }}')
    (BAR / "ws.css").write_text("\n".join(css) + "\n")


def furniture():
    ticks = f'<rect x="0" y="0" width="1" height="7" fill="{TICK_MAJOR}" fill-opacity="0.85"/>' + "".join(
        f'<rect x="{x}" y="3" width="1" height="4" fill="{TICK_MINOR}" fill-opacity="0.45"/>' for x in (8, 16, 24, 32))
    render(f'<svg xmlns="http://www.w3.org/2000/svg" width="40" height="7" viewBox="0 0 40 7">{ticks}</svg>', BAR / "scale.png")
    # 9-slice frame, 15x15 with 7px slices: a hairline on the outermost pixel of every edge, and on
    # each corner a 7px crop mark over it. GTK paints a CSS border over the background, so marks that
    # sit on the border line have to come from a border-image.
    hair = f'<rect x="0.5" y="0.5" width="14" height="14" fill="none" stroke="{LINE}"/>'
    marks = "".join(f'<path d="{d}" fill="none" stroke="{ALU_C}"/>' for d in ("M0.5 7 V0.5 H7", "M8 0.5 H14.5 V7", "M0.5 8 V14.5 H7", "M8 14.5 H14.5 V8"))
    render(f'<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 15 15">{hair}{marks}</svg>', BAR / "frame.png")
    for dest in (GTK, NOTI):
        dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BAR / "scale.png", GTK / "scale.png")
    shutil.copy2(BAR / "frame.png", NOTI / "frame.png")
    render(f'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="18" viewBox="0 0 10 18"><rect x="4.5" y="5" width="1" height="8" fill="{MUTED_C}"/></svg>',
           GTK / "crumb-tick.png")


# ---- lock ------------------------------------------------------------------------
def lock():
    helper = Path.home() / ".local/bin/nordschleife-lock-scale"
    subprocess.run([sys.executable, str(helper), "--static", str(HYPR / "lock-scale.png")], check=True)
    w, h = 440, 50
    crop = "".join(f'<path d="{d}" fill="none" stroke="{ALU_C}"/>' for d in (
        "M0.5 8 V0.5 H8", f"M{w - 8} 0.5 H{w - 0.5} V8", f"M0.5 {h - 8} V{h - 0.5} H8", f"M{w - 8} {h - 0.5} H{w - 0.5} V{h - 8}"))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" fill="{PANEL}" fill-opacity="0.92" stroke="{LINE}"/>{crop}'
           f'<rect x="17" y="17" width="3" height="16" fill="{ORANGE_C}"/></svg>')
    render(svg, HYPR / "lock-field.png")


if __name__ == "__main__":
    wallpaper()
    workspaces()
    furniture()
    lock()
    print("art written under", CONF)
