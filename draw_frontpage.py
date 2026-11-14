#!/usr/bin/env python3
"""Draw the news-image-01 v3 front page: 33 verified stories of Friday
13 November 2026, six continents, one broadsheet page, with a schematic
world-map strip and a by-the-numbers strip. Pure Pillow, DejaVu fonts."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 24                      # outer margin
CW = W - 2 * M              # 976 content width
PAPER = (247, 243, 234)
INK = (17, 17, 17)
GREY = (90, 90, 86)
RED = (163, 29, 29)
MAPFIELD = (223, 230, 234)
MAPLINE = (70, 90, 105)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SERIF_I = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

LEAD = ("Ukraine fires nearly 1,200 drones at Russia",
        "One of the war's biggest aerial attacks, as US-led talks widen to European security.")
TOP2 = [
    ("Microsoft 365 outage enters second day",
     "Outlook, Teams and Copilot down in 70+ countries; hospitals and courts disrupted."),
    ("FAA lifts nationwide ground stop",
     "US flights resume Friday evening after a communications failure halted departures for 4+ hours."),
]

# (continent, map count, grid stories)
SECTIONS = [
    ("NORTH AMERICA", 7, [
        ("Brooklyn collapse toll settles at eight",
         "Eight dead, including two children, after a Flatbush building fell into an excavation."),
        ("Trump tells Vance: focus on crime at home",
         "President directs vice-president away from Iran to 'corruption and crime' in US cities."),
        ("Van Hollen challenges Schumer for Senate leader",
         "Maryland senator to contest the post in a closed-ballot vote on 1 December."),
        ("US to seize $1.2bn from Binance hack",
         "Court approves seizure of crypto stolen in October hack blamed on North Korea."),
        ("Nvidia falls after chief Jensen Huang quits",
         "Shares slide as the chipmaker's CEO resigns amid scrutiny of his China links."),
        ("Bitcoin drops below $70,000",
         "The cryptocurrency falls to levels not seen since August."),
    ]),
    ("SOUTH AMERICA", 2, [
        ("Pope Leo meets abuse survivors in Peru",
         "Record crowds line Lima's streets on the pontiff's emotional return."),
        ("Puerto Rico's bomba heads to Australia",
         "El Laberinto del Coco to play WOMADelaide and WOMAD Aotearoa in March 2027."),
    ]),
    ("EUROPE", 8, [
        ("Europe to join Ukraine peace talks",
         "Dublin agrees a five-country team to represent Europe in negotiations."),
        ("Two killed as Russian drones hit Odesa",
         "Two women dead, seven hurt; Russia launched 117 drones overnight."),
        ("Pochettino confirmed as Man Utd head coach",
         "Former US boss to start on 18 November after release agreed."),
        ("UK welfare review targets under-25s",
         "Milburn plan would replace benefits with a youth allowance."),
        ("Moscow car bomb wounds ex-aide to Azarov",
         "Sergei Zavorotniy hurt in an explosion in the Chertanovo district."),
        ("EU warns of Russian traps as winter bites",
         "Kallas cautions as Ukraine faces power cuts in the cold."),
        ("US officer held in Britain over Russia spying",
         "Army officer at a NATO HQ arrested in an espionage inquiry."),
    ]),
    ("AFRICA", 5, [
        ("World Bank adds $500m for north Nigeria",
         "Extra financing for the ACReSAL land-restoration programme."),
        ("WHO: Nigeria carries 4.9% of global TB",
         "10.6m people developed TB in 2025; 1.13m died, a new report says."),
        ("Lagos readies three new Red Line trains",
         "24 coaches prepared for passenger service before the year's end."),
        ("Nigeria oil output slips to 1.51m a day",
         "October production down from 1.53m barrels a day in September."),
        ("Springboks stay unbeaten before France clash",
         "South Africa head into the Nations Championship's big weekend on top."),
    ]),
    ("ASIA", 7, [
        ("Taiwan details China's Pacific drills",
         "Taipei calls a large unannounced exercise intimidation."),
        ("Qatar and Turkey sign defence pact",
         "Mutual defence deal agreed in Istanbul."),
        ("Israeli strikes hit southern Lebanon",
         "Air strikes and shelling reported near Khiam and Kfar Tebnit."),
        ("Three killed by Israeli tank fire in Gaza",
         "A woman and a father and his 12-year-old son among the dead."),
        ("IAEA warns over Iran's Isfahan plant",
         "Inspectors barred from a plant declared in June 2025."),
        ("US downs two Iranian drones near Bahrain",
         "Iran claims a radar hit; four tankers struck in the Strait of Hormuz."),
        ("IEA sees Q4 oil surplus despite Gulf risk",
         "Supply forecast at 105m barrels a day, 1.7m above demand."),
    ]),
    ("OCEANIA", 3, [
        ("NZ suspends visa applications in outage",
         "Embassy email down and GP clinics hit as Microsoft fails."),
        ("Australia's hospitals and flights hit",
         "Prescriptions and flight papers delayed; students locked out of exams."),
        ("Rugby League final: Australia v New Zealand",
         "Brisbane hosts Sunday's decider; NZ's Ponga out with a broken arm."),
    ]),
]

MAP_ORDER = ["NORTH AMERICA", "SOUTH AMERICA", "EUROPE", "AFRICA", "ASIA", "OCEANIA"]
MAP_SHORT = {"NORTH AMERICA": "N. America", "SOUTH AMERICA": "S. America",
             "EUROPE": "Europe", "AFRICA": "Africa", "ASIA": "Asia", "OCEANIA": "Oceania"}
MAP_TINTS = [(178, 200, 214), (190, 208, 186), (205, 196, 172),
             (214, 190, 168), (196, 184, 205), (172, 205, 205)]


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines, each fitting width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_h(fnt):
    return fnt.getbbox("Ag")[3] - fnt.getbbox("Ag")[1]


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 18

    # ---- Masthead ----
    f_title = font(SERIF_B, 40)
    d.text((W // 2, y), "THE WORLD TODAY", font=f_title, fill=INK, anchor="ma")
    y += 52
    f_sub = font(SANS, 14)
    d.text((W // 2, y), "Friday 13 November 2026  \u2022  33 stories  \u2022  6 continents  \u2022  One page",
           font=f_sub, fill=INK, anchor="ma")
    y += 22
    d.line([(M, y), (W - M, y)], fill=INK, width=3)
    y += 8

    # ---- Lead story ----
    d.line([(M, y), (W - M, y)], fill=RED, width=3)
    y += 6
    f_lead = font(SERIF_B, 24)
    d.text((W // 2, y), LEAD[0], font=f_lead, fill=INK, anchor="ma")
    y += 33
    f_leadsum = font(SERIF, 14)
    d.text((W // 2, y), LEAD[1], font=f_leadsum, fill=INK, anchor="ma")
    y += 20
    d.line([(M, y), (W - M, y)], fill=INK, width=1)
    y += 8

    # ---- Second row: two half-width stories ----
    col_w = (CW - 16) // 2
    f_h2 = font(SERIF_B, 17)
    f_s2 = font(SERIF, 11)
    row_h = 0
    for i, (hl, sm) in enumerate(TOP2):
        x = M + i * (col_w + 16)
        hl_lines = wrap(d, hl, f_h2, col_w)
        sm_lines = wrap(d, sm, f_s2, col_w)
        yy = y
        for ln in hl_lines:
            d.text((x, yy), ln, font=f_h2, fill=INK)
            yy += 22
        yy += 2
        for ln in sm_lines:
            d.text((x, yy), ln, font=f_s2, fill=(40, 40, 40))
            yy += 15
        row_h = max(row_h, yy - y)
    y += row_h + 6
    d.line([(M, y), (W - M, y)], fill=INK, width=1)
    y += 7

    # ---- World map strip ----
    f_maplabel = font(SANS_B, 13)
    d.text((M, y), "WORLD AT A GLANCE \u2014 33 STORIES", font=f_maplabel, fill=INK)
    f_note = font(SERIF_I, 11)
    note = "(schematic map, not to scale)"
    d.text((W - M, y + 1), note, font=f_note, fill=GREY, anchor="ra")
    y += 18
    map_top = y
    map_h = 62
    d.rectangle([M, map_top, W - M, map_top + map_h], fill=MAPFIELD, outline=MAPLINE, width=1)
    slot_w = CW // 6
    counts = {name: c for name, c, _ in SECTIONS}
    for i, name in enumerate(MAP_ORDER):
        cx = M + slot_w * i + slot_w // 2
        tint = MAP_TINTS[i]
        # schematic continent blob: wide ellipse, varied by index
        bw = 118 if i not in (1, 5) else 96
        bh = 28
        by = map_top + 6
        d.ellipse([cx - bw // 2, by, cx + bw // 2, by + bh], fill=tint, outline=MAPLINE, width=1)
        f_cnt = font(SANS_B, 13)
        d.text((cx, by + 6), str(counts[name]), font=f_cnt, fill=INK, anchor="ma")
        f_mname = font(SANS_B, 11)
        d.text((cx, map_top + map_h - 18), MAP_SHORT[name], font=f_mname, fill=INK, anchor="ma")
    y = map_top + map_h + 4
    f_mapfoot = font(SANS, 10)
    d.text((W // 2, y), "Counts include the lead story (Europe) and the FAA story (North America); the Microsoft outage is global.",
           font=f_mapfoot, fill=GREY, anchor="ma")
    y += 14
    d.line([(M, y), (W - M, y)], fill=INK, width=1)
    y += 6

    # ---- By the numbers ----
    f_num = font(SANS_B, 14)
    d.text((W // 2, y), "BY THE NUMBERS:   1,200 drones  \u2022  70+ countries  \u2022  $1.2bn  \u2022  8 dead  \u2022  $70,000",
           font=f_num, fill=RED, anchor="ma")
    y += 20
    d.line([(M, y), (W - M, y)], fill=INK, width=1)
    y += 8

    # ---- Six continent sections, 2 columns x 3 rows ----
    grid_top = y
    grid_bottom = H - 30          # footer occupies the last ~30 px
    grid_h = grid_bottom - grid_top
    # Row heights proportional to the larger story count in the row.
    pairs = [(SECTIONS[0], SECTIONS[1]), (SECTIONS[2], SECTIONS[3]), (SECTIONS[4], SECTIONS[5])]
    row_max = [max(len(a[2]), len(b[2])) for a, b in pairs]   # [6, 7, 7]
    gap = 8
    avail = grid_h - gap * 2
    total = sum(row_max)
    row_hs = [avail * n // total for n in row_max]
    row_hs[-1] += avail - sum(row_hs)
    col_w = (CW - 16) // 2

    for r, ((na, ncount, nstories), (nb, nbcount, nbstories)) in enumerate(pairs):
        ry = grid_top + sum(row_hs[:r]) + gap * r
        rh = row_hs[r]
        for c, (name, mcount, stories) in enumerate([(na, ncount, nstories), (nb, nbcount, nbstories)]):
            x = M + c * (col_w + 16)
            # Header: name + listed count.
            f_sec = font(SANS_B, 12)
            d.text((x, ry), f"{name}  \u00b7  {len(stories)}", font=f_sec, fill=INK)
            d.line([(x, ry + 16), (x + col_w, ry + 16)], fill=INK, width=1)
            body_top = ry + 20
            body_h = rh - 20
            # Auto-shrink ladder until the stories fit the cell.
            for hpt, spt in [(12, 10), (11, 9), (10, 9), (10, 8), (9, 8)]:
                fh = font(SERIF_B, hpt)
                fs = font(SERIF, spt)
                lh, ls = hpt + 3, spt + 3
                need = sum(
                    len(wrap(d, hl, fh, col_w - 8)) * lh + len(wrap(d, sm, fs, col_w - 8)) * ls + 3
                    for hl, sm in stories) - 3
                if need <= body_h:
                    break
            yy = body_top
            for hl, sm in stories:
                for ln in wrap(d, hl, fh, col_w - 8):
                    d.text((x, yy), ln, font=fh, fill=INK)
                    yy += lh
                for ln in wrap(d, sm, fs, col_w - 8):
                    d.text((x, yy), ln, font=fs, fill=(40, 40, 40))
                    yy += ls
                yy += 3
            assert yy - 3 <= ry + rh, f"overflow in {name}: {yy} > {ry + rh}"
    y = grid_bottom + 4

    # ---- Footer ----
    d.line([(M, y), (W - M, y)], fill=INK, width=1)
    y += 5
    f_foot = font(SANS, 12)
    d.text((W // 2, y), "All events of Friday 13 November 2026  \u2022  Sources: AP, Reuters, BBC, IEA, IAEA, WHO",
           font=f_foot, fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    draw().save(out, "JPEG", quality=88)
    print("saved", out, os.path.getsize(out), "bytes")
