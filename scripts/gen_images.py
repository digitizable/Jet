"""Generate Jet theme marketing assets for images/."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images"
OUT.mkdir(exist_ok=True)

# Palette from README / theme
PALETTE = {
    "bg": (12, 12, 12),  # editor #0C0C0C
    "chrome": (10, 10, 10),  # #0A0A0A
    "panel": (14, 14, 16),
    "border": (36, 36, 40),
    "gutter": (70, 70, 74),
    "text": (212, 212, 212),
    "keyword": (94, 184, 245),  # #5EB8F5
    "func": (240, 224, 112),  # #F0E070
    "field": (240, 212, 128),  # #F0D480
    "pp": (165, 180, 252),  # #A5B4FC
    "macro": (240, 163, 255),  # #F0A3FF
    "comment": (111, 212, 90),  # #6FD45A
    "string": (240, 180, 138),  # #F0B48A
    "type": (78, 201, 176),
    "num": (181, 206, 168),
    "white": (240, 240, 240),
    "tab_active": (20, 20, 22),
    "tab_idle": (14, 14, 16),
    "line_hi": (22, 24, 28),
}


def load_font(size: int, mono: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if mono:
        candidates = [
            r"C:\Windows\Fonts\consola.ttf",
            r"C:\Windows\Fonts\CascadiaMono.ttf",
            r"C:\Windows\Fonts\CascadiaCode.ttf",
            r"C:\Windows\Fonts\lucon.ttf",
        ]
    else:
        candidates = [
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_icon() -> Path:
    size = 128
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)

    bg = (10, 10, 10, 255)
    border = (32, 32, 36, 255)
    accent = (94, 184, 245, 255)
    accent2 = (240, 224, 112, 255)
    violet = (165, 180, 252, 255)

    pad = 4
    draw.rounded_rectangle(
        [pad, pad, size - pad - 1, size - pad - 1],
        radius=28,
        fill=bg,
        outline=border,
        width=2,
    )

    cx, cy = size // 2, size // 2

    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=(94, 184, 245, 40))
    icon = Image.alpha_composite(icon, glow)
    draw = ImageDraw.Draw(icon)

    def chevron(ox: float, oy: float, scale: float, color: tuple[int, ...], width: int) -> None:
        pts = [
            (ox - 22 * scale, oy + 18 * scale),
            (ox + 10 * scale, oy - 4 * scale),
            (ox - 22 * scale, oy - 26 * scale),
        ]
        draw.line(pts, fill=color, width=width, joint="curve")

    chevron(cx - 8, cy + 6, 1.0, (94, 184, 245, 90), 5)
    chevron(cx + 2, cy + 2, 1.05, accent, 7)
    draw.ellipse([cx + 14, cy - 18, cx + 26, cy - 6], fill=accent2)
    draw.ellipse([cx - 28, cy + 18, cx - 18, cy + 28], fill=violet)

    path = OUT / "icon.png"
    icon.save(path, "PNG", optimize=True)
    return path


def make_preview() -> Path:
    w, h = 1280, 720
    c = PALETTE
    preview = Image.new("RGB", (w, h), c["chrome"])
    d = ImageDraw.Draw(preview)

    font_ui = load_font(13)
    font_ui_sm = load_font(12)
    font_title = load_font(14)
    font_code = load_font(15, mono=True)
    font_code_sm = load_font(13, mono=True)

    # Title bar + menu
    d.rectangle([0, 0, w, 36], fill=c["chrome"])
    d.rectangle([0, 36, w, 72], fill=c["chrome"])
    d.line([(0, 72), (w, 72)], fill=c["border"], width=1)
    d.text((14, 10), "Jet — Visual Studio 2022", font=font_title, fill=c["white"])
    for i, col in enumerate([(232, 17, 35), (255, 185, 0), (40, 40, 44)]):
        x = w - 18 - i * 22
        d.ellipse([x - 6, 12, x + 6, 24], fill=col)

    menus = [
        "File",
        "Edit",
        "View",
        "Project",
        "Build",
        "Debug",
        "Tools",
        "Extensions",
        "Window",
        "Help",
    ]
    x = 16
    for m in menus:
        d.text((x, 48), m, font=font_ui_sm, fill=(180, 180, 184))
        x += 72

    # Activity bar
    ab_w = 48
    d.rectangle([0, 72, ab_w, h - 28], fill=(8, 8, 8))
    for i, y in enumerate([100, 150, 200, 250, 300]):
        col = c["keyword"] if i == 1 else (90, 90, 96)
        d.rounded_rectangle([12, y, 36, y + 24], radius=4, outline=col, width=2)

    # Solution Explorer
    sp_x0, sp_x1 = ab_w, ab_w + 260
    d.rectangle([sp_x0, 72, sp_x1, h - 28], fill=c["panel"])
    d.line([(sp_x1, 72), (sp_x1, h - 28)], fill=c["border"], width=1)
    d.text((sp_x0 + 12, 84), "SOLUTION EXPLORER", font=font_ui_sm, fill=(140, 140, 148))
    tree = [
        (0, "Solution 'JetDemo'", c["white"]),
        (1, "JetDemo", c["text"]),
        (2, "src", (180, 180, 184)),
        (3, "main.cpp", c["keyword"]),
        (3, "pe32.hpp", c["text"]),
        (2, "include", (180, 180, 184)),
        (3, "jet_utils.h", c["text"]),
        (1, "README.md", c["text"]),
    ]
    ty = 118
    for indent, name, col in tree:
        d.text((sp_x0 + 16 + indent * 14, ty), name, font=font_ui_sm, fill=col)
        ty += 22

    # Editor chrome
    ed_x0 = sp_x1 + 1
    ed_y0 = 72
    d.rectangle([ed_x0, ed_y0, w, ed_y0 + 32], fill=c["tab_idle"])
    d.rectangle([ed_x0, ed_y0, ed_x0 + 140, ed_y0 + 32], fill=c["tab_active"])
    d.text((ed_x0 + 16, ed_y0 + 8), "main.cpp", font=font_ui, fill=c["white"])
    d.text((ed_x0 + 150, ed_y0 + 8), "pe32.hpp", font=font_ui, fill=(120, 120, 128))
    d.line([(ed_x0, ed_y0 + 32), (w, ed_y0 + 32)], fill=c["border"], width=1)
    d.rectangle([ed_x0, ed_y0 + 33, w, h - 28], fill=c["bg"])

    # Code showcasing Jet syntax roles
    code: list[list[tuple[str, tuple[int, int, int]]]] = [
        [("#include ", c["pp"]), ("<windows.h>", c["string"])],
        [("#include ", c["pp"]), ('"pe32.hpp"', c["string"])],
        [("", c["text"])],
        [("#define ", c["pp"]), ("JET_VERSION ", c["macro"]), ("0x0105", c["num"])],
        [("", c["text"])],
        [("// Near-black surfaces, distinct syntax hues", c["comment"])],
        [("namespace ", c["keyword"]), ("jet", c["type"]), (" {", c["text"])],
        [("", c["text"])],
        [
            ("bool ", c["keyword"]),
            ("open_pe", c["func"]),
            ("(const ", c["keyword"]),
            ("wchar_t", c["type"]),
            ("* path) {", c["text"]),
        ],
        [
            ("    ", c["text"]),
            ("HANDLE ", c["type"]),
            ("h = ", c["text"]),
            ("CreateFileW", c["func"]),
            ("(path, ", c["text"]),
        ],
        [
            ("        ", c["text"]),
            ("GENERIC_READ", c["macro"]),
            (", ", c["text"]),
            ("FILE_SHARE_READ", c["macro"]),
            (", ", c["text"]),
        ],
        [
            ("        nullptr, ", c["keyword"]),
            ("OPEN_EXISTING", c["macro"]),
            (", 0, nullptr);", c["text"]),
        ],
        [
            ("    if ", c["keyword"]),
            ("(h == ", c["text"]),
            ("INVALID_HANDLE_VALUE", c["macro"]),
            (") {", c["text"]),
        ],
        [
            ("        ", c["text"]),
            ("return ", c["keyword"]),
            ("false", c["keyword"]),
            (";", c["text"]),
        ],
        [("    }", c["text"])],
        [("", c["text"])],
        [
            ("    ", c["text"]),
            ("IMAGE_DOS_HEADER ", c["type"]),
            ("dos{};", c["text"]),
        ],
        [
            ("    dos.", c["text"]),
            ("e_magic", c["field"]),
            (" = ", c["text"]),
            ("IMAGE_DOS_SIGNATURE", c["macro"]),
            (";", c["text"]),
        ],
        [
            ("    ", c["text"]),
            ("printf", c["func"]),
            ("(", c["text"]),
            (r'"opened %ls\n"', c["string"]),
            (", path);", c["text"]),
        ],
        [
            ("    ", c["text"]),
            ("CloseHandle", c["func"]),
            ("(h);", c["text"]),
        ],
        [
            ("    ", c["text"]),
            ("return ", c["keyword"]),
            ("true", c["keyword"]),
            (";", c["text"]),
        ],
        [("}", c["text"])],
        [("", c["text"])],
        [("} ", c["text"]), ("// namespace jet", c["comment"])],
    ]

    gutter_w = 52
    code_x = ed_x0 + gutter_w + 12
    code_y0 = ed_y0 + 48
    line_h = 22
    active = 9

    d.rectangle(
        [ed_x0, code_y0 + active * line_h - 2, w, code_y0 + (active + 1) * line_h - 2],
        fill=c["line_hi"],
    )

    # White VsVim-style block caret
    caret_x = code_x + 280
    caret_y = code_y0 + active * line_h
    d.rectangle([caret_x, caret_y, caret_x + 9, caret_y + 16], fill=(255, 255, 255))

    for i, segs in enumerate(code):
        y = code_y0 + i * line_h
        d.text((ed_x0 + 14, y), f"{i + 1:>3}", font=font_code_sm, fill=c["gutter"])
        x = code_x
        for text, col in segs:
            d.text((x, y), text, font=font_code, fill=col)
            bbox = d.textbbox((0, 0), text, font=font_code)
            x += bbox[2] - bbox[0]

    # Minimap
    d.rectangle([w - 48, ed_y0 + 33, w, h - 28], fill=(14, 14, 16))
    mini_colors = [
        c["pp"],
        c["comment"],
        c["keyword"],
        c["func"],
        c["macro"],
        c["string"],
        c["field"],
        c["type"],
        c["num"],
    ]
    for i in range(18):
        col = mini_colors[i % len(mini_colors)]
        d.rectangle(
            [w - 40, ed_y0 + 50 + i * 14, w - 12, ed_y0 + 56 + i * 14],
            fill=col,
        )

    # Status bar
    d.rectangle([0, h - 28, w, h], fill=(0, 100, 180))
    d.text(
        (12, h - 22),
        "Jet  |  Ln 10, Col 28  |  C++  |  UTF-8  |  CRLF",
        font=font_ui_sm,
        fill=c["white"],
    )
    d.text((w - 220, h - 22), "Tools > Theme > Jet", font=font_ui_sm, fill=c["white"])

    # Theme chip
    d.rounded_rectangle(
        [w - 200, 84, w - 60, 108],
        radius=6,
        fill=(20, 28, 40),
        outline=c["keyword"],
        width=1,
    )
    d.text((w - 188, 88), "theme: Jet", font=font_ui_sm, fill=c["keyword"])

    path = OUT / "preview.png"
    preview.save(path, "PNG", optimize=True)
    return path


def main() -> None:
    icon = make_icon()
    preview = make_preview()
    print(f"icon    {icon}  {icon.stat().st_size} bytes")
    print(f"preview {preview}  {preview.stat().st_size} bytes")


if __name__ == "__main__":
    main()
