#!/usr/bin/env python3
"""
Nexus - Advanced ASCII Art Generator
Usage: python3 nexus.py "Your Text" [options]
"""
import sys
import argparse
import random
import math
from typing import List, Tuple, Optional

# ============================================
# ARGUMENT PARSER
# ============================================
parser = argparse.ArgumentParser(
    description='Nexus - Advanced ASCII Art Generator',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog='''
╔══════════════════════════════════════════════════════════════╗
║  NEXUS - ASCII Art Generator                               ║
║  Usage: python3 nexus.py "Your Text" [options]             ║
╚══════════════════════════════════════════════════════════════╝

EXAMPLES:
  python3 nexus.py "Hello World" --rainbow
  python3 nexus.py "NEXUS" --font comet --rainbow
  python3 nexus.py "RECON" --font recon --gradient 00FF00 00AAFF
  python3 nexus.py "Text" --blend FF0000 0000FF --shadow
  python3 nexus.py "Matrix" --matrix --font big
  python3 nexus.py "Random" --random-color --width 80

FONTS:
  standard, big, block, bubble, digital, mini, script, shadow, slant, small,
  recon, comet, alligator, doom, epic, fender, ivrit, lean, mnemonic, morse,
  o8, puffy, rectangles, sblood, smshadow, smsmemory, smsoft, starwars, thin,
  upside, wow

EFFECTS:
  --rainbow      Rainbow colors
  --blend HEX1 HEX2  Blend between two colors
  --gradient HEX1 HEX2  Smooth gradient
  --matrix       Matrix green (falling code effect)
  --outline HEX  Add outline in color
  --shadow       Add drop shadow
  --random-color Random colors per character
  --center       Center the output
  --width WIDTH  Max line width (default: terminal width)
  --font FONT    Font to use (default: standard)
  --list-fonts   List all available fonts
  --no-color     Disable colors (plain output)
'''
)

parser.add_argument('text', type=str, nargs='?', default='', help='Text to convert to ASCII art')
parser.add_argument('--rainbow', action='store_true', help='Rainbow colors')
parser.add_argument('--blend', nargs=2, metavar=('HEX1', 'HEX2'), help='Blend two colors (hex: FF0000)')
parser.add_argument('--gradient', nargs=2, metavar=('HEX1', 'HEX2'), help='Smooth gradient between two colors')
parser.add_argument('--matrix', action='store_true', help='Matrix green style')
parser.add_argument('--outline', metavar='HEX', help='Add outline in color (hex)')
parser.add_argument('--shadow', action='store_true', help='Add drop shadow')
parser.add_argument('--random-color', action='store_true', help='Random colors per character')
parser.add_argument('--center', action='store_true', help='Center the output')
parser.add_argument('--width', type=int, default=None, help='Max line width (default: terminal width)')
parser.add_argument('--font', type=str, default='standard', help='Font to use (see --list-fonts)')
parser.add_argument('--list-fonts', action='store_true', help='List all available fonts')
parser.add_argument('--no-color', action='store_true', help='Disable colors (plain output)')
parser.add_argument('--version', action='version', version='Nexus v2.0')

args = parser.parse_args()

# ============================================
# COLOR UTILITIES
# ============================================
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_ansi(r: int, g: int, b: int) -> str:
    """Convert RGB to ANSI 256 color code"""
    return f'\033[38;2;{r};{g};{b}m'

def hex_to_ansi(hex_color: str) -> str:
    """Convert hex to ANSI color code"""
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_ansi(r, g, b)

def blend_colors(hex1: str, hex2: str, ratio: float) -> str:
    """Blend two hex colors by ratio (0.0 to 1.0)"""
    r1, g1, b1 = hex_to_rgb(hex1)
    r2, g2, b2 = hex_to_rgb(hex2)
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    return rgb_to_ansi(r, g, b)

def rainbow_color(index: int, total: int) -> str:
    """Generate rainbow color for position"""
    if total <= 0:
        return ''
    hue = (index / total) * 360
    r = int(128 + 127 * math.sin(math.radians(hue)))
    g = int(128 + 127 * math.sin(math.radians(hue + 120)))
    b = int(128 + 127 * math.sin(math.radians(hue + 240)))
    return rgb_to_ansi(r, g, b)

def matrix_color() -> str:
    """Matrix green with slight variation"""
    shades = ['\033[32m', '\033[92m', '\033[38;2;0;255;0m']
    return random.choice(shades)

# ============================================
# ASCII FONTS
# ============================================
ASCII_FONTS = {
    # Standard fonts
    'standard': [
        "  #  ",
        " ##  ",
        "# #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "#####"
    ],
    'big': [
        " ##### ",
        "#     #",
        "#     #",
        "#     #",
        "#     #",
        "#     #",
        " ##### "
    ],
    'block': [
        "███████",
        "█     █",
        "█     █",
        "█     █",
        "█     █",
        "█     █",
        "███████"
    ],
    'bubble': [
        " ╭───╮ ",
        " │   │ ",
        " │   │ ",
        " │   │ ",
        " │   │ ",
        " ╰───╯ ",
        "       "
    ],
    'digital': [
        " ═══ ",
        " ║ ║ ",
        " ═══ ",
        " ║ ║ ",
        " ═══ ",
        "     ",
        "     "
    ],
    'mini': [
        " # ",
        "## ",
        "# #",
        " # ",
        " # ",
        " # ",
        "###"
    ],
    'script': [
        "  _   ",
        " (_)  ",
        "  _   ",
        " (_)  ",
        "  _   ",
        " (_)  ",
        "     "
    ],
    'shadow': [
        "███████",
        "█     █",
        "█     █",
        "█     █",
        "█     █",
        "█     █",
        "███████"
    ],
    'slant': [
        "     #",
        "    ##",
        "   ###",
        "  ####",
        " #####",
        "######",
        "######"
    ],
    'small': [
        " # ",
        "## ",
        "# #",
        " # ",
        " # ",
        " # ",
        "###"
    ],
    
    # ============================================
    # RECON-NG STYLE FONT
    # ============================================
    'recon': [
        " ███████ ",
        " ███████ ",
        " ██   ██ ",
        " ███████ ",
        " ███████ ",
        " ██   ██ ",
        " ██   ██ "
    ],
    
    # ============================================
    # COMET FONT (from screenshot)
    # ============================================
    'comet': [
        "   ▄████████  ▄█   ▄█          ▄████████ ",
        "  ███    ███ ███  ███         ███    ███ ",
        "  ███    █▀  ███▌ ███         ███    ███ ",
        "  ███        ███▌ ███        ▄███▄▄▄▄██▀ ",
        "▀███████████ ███▌ ███       ▀▀███▀▀▀▀▀   ",
        "         ███ ███  ███         ███    ███ ",
        "   ▄█    ███ ███  ███▌    ▄   ███    ███ ",
        " ▄████████▀  █▀   █████▄▄██   ██████████ ",
        "                ▀                        "
    ],
    
    # Additional fonts
    'alligator': [
        "  ___  ",
        " / _ \\ ",
        "| | | |",
        "| |_| |",
        " \\___/ ",
        "       ",
        "       "
    ],
    'doom': [
        " ███████ ",
        " ███████ ",
        " ██   ██ ",
        " ███████ ",
        " ███████ ",
        " ██   ██ ",
        " ██   ██ "
    ],
    'epic': [
        " █████████ ",
        " ██     ██ ",
        " ██     ██ ",
        " ██     ██ ",
        " ██     ██ ",
        " ██     ██ ",
        " █████████ "
    ],
    'starwars': [
        "  ██████  ",
        " ██    ██ ",
        " ██    ██ ",
        " ██    ██ ",
        " ██    ██ ",
        " ██    ██ ",
        "  ██████  "
    ],
    'thin': [
        " ─── ",
        " ─── ",
        " ─── ",
        " ─── ",
        " ─── ",
        " ─── ",
        " ─── "
    ],
    'wow': [
        "  ██████  ",
        " ██    ██ ",
        " ██    ██ ",
        " ██    ██ ",
        " ██    ██ ",
        " ██    ██ ",
        "  ██████  "
    ],
    'puffy': [
        "  ╭──╮  ",
        " ╭╯  ╰╮ ",
        " │    │ ",
        " │    │ ",
        " │    │ ",
        " ╰╮  ╭╯ ",
        "  ╰──╯  "
    ],
    'lean': [
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  "
    ],
    'ivrit': [
        "  _  ",
        " (_) ",
        "  _  ",
        " (_) ",
        "  _  ",
        " (_) ",
        "     "
    ],
    'rectangles': [
        " ███ ",
        " ██  ",
        " █   ",
        "     ",
        "     ",
        "     ",
        "     "
    ],
    'sblood': [
        "███████",
        "█     █",
        "█     █",
        "█     █",
        "█     █",
        "█     █",
        "███████"
    ],
    'smshadow': [
        "████████",
        "█      █",
        "█      █",
        "█      █",
        "█      █",
        "█      █",
        "████████"
    ],
    'smsmemory': [
        " █████ ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        " █████ "
    ],
    'smsoft': [
        "  ███  ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        "  ███  "
    ],
    'upside': [
        "#####",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        " ##  ",
        "#    "
    ],
    'morse': [
        ".---",
        "---.",
        "---.",
        "---.",
        "---.",
        "---.",
        ".---"
    ],
    'fender': [
        " █████ ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        " █████ "
    ],
    'mnemonic': [
        " ███ ",
        " █ █ ",
        " █ █ ",
        " █ █ ",
        " █ █ ",
        " █ █ ",
        " ███ "
    ],
    'o8': [
        " ███ ",
        " █ █ ",
        " █ █ ",
        " █ █ ",
        " █ █ ",
        " █ █ ",
        " ███ "
    ]
}

# ============================================
# GENERATE ASCII ART
# ============================================
def get_character_block(char: str, font: str = 'standard') -> List[str]:
    """Get ASCII block for a character using the specified font"""
    if font not in ASCII_FONTS:
        font = 'standard'
    
    base = ASCII_FONTS[font]
    
    # For COMET and RECON fonts, return the entire font block
    if font in ['comet', 'recon']:
        return base
    
    # For other fonts, map character to block
    if char.isalpha():
        return [line.replace('#', char.upper()) for line in base]
    elif char.isdigit():
        return [line.replace('#', str(char)) for line in base]
    else:
        return [' ' * len(base[0]) for _ in range(len(base))]

def generate_ascii_art(text: str, font: str = 'standard') -> List[str]:
    """Generate ASCII art from text using specified font"""
    if not text:
        return []
    
    # Special handling for COMET and RECON fonts
    if font in ['comet', 'recon']:
        return ASCII_FONTS[font]
    
    # For character-based fonts
    lines = ['' for _ in range(7)]
    for char in text:
        block = get_character_block(char, font)
        for i in range(7):
            if i < len(block):
                lines[i] += block[i] + ' '
            else:
                lines[i] += ' ' * (len(block[0]) + 1) if block else '  '
    return lines

# ============================================
# COLOR APPLICATION
# ============================================
def apply_colors(lines: List[str]) -> List[str]:
    """Apply color effects to ASCII art"""
    if args.no_color:
        return lines
    
    colored_lines = []
    effect_type = None
    
    if args.rainbow:
        effect_type = 'rainbow'
    elif args.blend:
        effect_type = 'blend'
    elif args.gradient:
        effect_type = 'gradient'
    elif args.matrix:
        effect_type = 'matrix'
    elif args.random_color:
        effect_type = 'random'
    elif args.outline:
        effect_type = 'outline'
    
    total_chars = sum(len(line) for line in lines) if lines else 1
    
    for line_idx, line in enumerate(lines):
        colored_line = ''
        char_pos = 0
        
        for char in line:
            color = ''
            
            if effect_type == 'rainbow':
                color = rainbow_color(char_pos, total_chars)
            elif effect_type == 'blend':
                ratio = char_pos / max(total_chars, 1)
                color = blend_colors(args.blend[0], args.blend[1], ratio)
            elif effect_type == 'gradient':
                ratio = char_pos / max(total_chars, 1)
                color = blend_colors(args.gradient[0], args.gradient[1], ratio)
            elif effect_type == 'matrix':
                color = matrix_color()
            elif effect_type == 'random':
                color = rgb_to_ansi(random.randint(0,255), random.randint(0,255), random.randint(0,255))
            elif effect_type == 'outline':
                if char != ' ':
                    color = hex_to_ansi(args.outline)
            
            # Shadow effect
            if args.shadow and char != ' ':
                shadow_color = '\033[90m'
                colored_line += f'{shadow_color}{char}'
                if color:
                    colored_line += color + char + '\033[0m'
                else:
                    colored_line += char
                char_pos += 1
            else:
                if color:
                    colored_line += color + char + '\033[0m'
                else:
                    colored_line += char
            
            if char != ' ':
                char_pos += 1
        
        colored_lines.append(colored_line)
    
    return colored_lines

# ============================================
# NEXUS BANNER
# ============================================
def show_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║  ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗              ║
║  ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝              ║
║  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗              ║
║  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║              ║
║  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║              ║
║  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝              ║
║                                                              ║
║  NEXUS - ASCII Art Generator v2.0                           ║
║  Usage: python3 nexus.py "Your Text" [options]             ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

# ============================================
# MAIN
# ============================================
def main():
    # Show banner if no args
    if len(sys.argv) == 1:
        show_banner()
        print("\nUse --help for more information.")
        return
    
    # List fonts
    if args.list_fonts:
        print("\n╔══════════════════════════════════════════╗")
        print("║  NEXUS - Available Fonts               ║")
        print("╚══════════════════════════════════════════╝")
        fonts = sorted(ASCII_FONTS.keys())
        for i, font in enumerate(fonts):
            print(f"  {font:>15}", end='  ')
            if (i + 1) % 4 == 0:
                print()
        print("\n")
        return
    
    # No text provided
    if not args.text:
        print("Error: Please provide text to convert.")
        print("Usage: python3 nexus.py \"Your Text\" [options]")
        print("Use --help for more information.")
        return
    
    # Generate ASCII art
    lines = generate_ascii_art(args.text, args.font)
    
    # Apply colors
    colored_lines = apply_colors(lines)
    
    # Center output
    if args.center and colored_lines:
        term_width = args.width or 80
        max_len = max(len(line) for line in colored_lines) if colored_lines else 0
        for i, line in enumerate(colored_lines):
            padding = (term_width - max_len) // 2
            colored_lines[i] = ' ' * padding + line
    
    # Print result
    print('\n'.join(colored_lines))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Nexus interrupted.")
        sys.exit(0)
