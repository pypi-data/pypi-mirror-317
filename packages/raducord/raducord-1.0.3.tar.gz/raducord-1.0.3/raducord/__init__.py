# https://github.com/H4cK3dR4Du/
# https://discord.gg/raducord/
# Made By H4cK3dR4Du
# @ 29/05/2024

import os, re, sys, time, random, string, ctypes, subprocess, requests, datetime
import pyautogui, colorsys, shutil, numpy as np, base64, json

from fake_useragent import UserAgent
from tls_client import Session
from pyfiglet import Figlet

# <-- Raducord Library --> #

class Global:
    creator = "H4cK3dR4Du"
    windows = os.name == "nt"

class Console:
    def init():
        os.system('')

    def clear():
        return os.system("cls")
    
    def size(x: int, y: int):
        if Global.windows: return os.system('mode %s, %s' % (x, y))

    def execute_command(command: str):
        return os.system(command)
    
    def title(title: str):
        return ctypes.windll.kernel32.SetConsoleTitleW(title)
    
    def close():
        sys.exit()

    def full_screen():
        pyautogui.hotkey('win', 'up')

class ColorUtils:
    def hex_color(hex_color):
        return f"\033[38;2;{int(hex_color[1:3], 16)};{int(hex_color[3:5], 16)};{int(hex_color[5:], 16)}m"

    def rgb_color(r: int, g: int, b: int):
        return f"\033[38;2;{r};{g};{b}m"

    def hsl_color(h: int, s: int, l: int):
        r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return f"\033[38;2;{r};{g};{b}m"
    
    def ansi_color(color: str, text: str):
        return f"\033[38;2;{color}m{text}\033[38;2;255;255;255m"

class BannerUtils:
    def box_1(text: str):
        return "╔═" + "═" * len(text) + "═╗\n" + f"║ {text} ║\n" + "╚═" + "═" * len(text) + "═╝\n"
    
    def box_2(text: str):
        return "╭─" + "─" * len(text) + "─╮\n" + f"│ {text} │\n" + "╰─" + "─" * len(text) + "─╯\n"
    
    def box_3(text: str):
        return "╭•" + "•" * len(text) + "•╮\n" + f"• {text} •\n" + "╰•" + "•" * len(text) + "•╯\n"

    def box_4(text: str):
        return "╭" + "─" * (len(text) + 2) + "╮\n" + f"│ {text} │\n" + "╰" + "─" * (len(text) + 2) + "╯\n"

    def box_5(text: str):
        return "┏" + "━" * (len(text) + 2) + "┓\n" + f"┃ {text} ┃\n" + "┗" + "━" * (len(text) + 2) + "┛\n"

    def box_6(text: str):
        return "╭━" + "━" * len(text) + "━╮\n" + f"┃ {text} ┃\n" + "╰━" + "━" * len(text) + "━╯\n"

    def box_7(text: str):
        return "╭─" + "─" * len(text) + "─╮\n" + f"| {text} |\n" + "╰─" + "─" * len(text) + "─╯\n"

    def box_8(text: str):
        return "┌" + "─" * (len(text) + 2) + "┐\n" + f"│ {text} │\n" + "└" + "─" * (len(text) + 2) + "┘\n"
    
    def box_9(text: str):
        return "•" + "•" * (len(text) + 2) + "•\n" + f"• {text} •\n" + "•" + "•" * (len(text) + 2) + "•\n"
    
    def lines_1(text: str):
        return f"{'─' * (len(text) + 14)}\n{' ' * ((len(text) + 12 - len(text)) // 2)}{text}\n{'─' * (len(text) + 14)}\n"

    def lines_2(text: str):
        return f"{'=' * (len(text) + 14)}\n{' ' * ((len(text) + 12 - len(text)) // 2)}{text}\n{'=' * (len(text) + 14)}\n"

    def lines_3(text: str):
        return f"{'*' * (len(text) + 14)}\n{' ' * ((len(text) + 12 - len(text)) // 2)}{text}\n{'*' * (len(text) + 14)}\n"
    
    def lines_4(text: str):
        return f"─═{''.join('═' if i % 2 == 0 else '' for i in range(len(text)))}ቐቐ{''.join('═' if i % 2 == 0 else '' for i in range(len(text)))}═─\n{' '*4}{' '*((len(''.join('═' if i % 2 == 0 else '' for i in range(len(text)))) - (len(text) + 4)) // 2)}{text}{' '*((len(''.join('═' if i % 2 == 0 else '' for i in range(len(text)))) - (len(text) + 4)) // 2)}\n─═{''.join('═' if i % 2 == 0 else '' for i in range(len(text)))}ቐቐ{''.join('═' if i % 2 == 0 else '' for i in range(len(text)))}═─"

    def lines_5(text: str):
        return f"❤{'━' * (len(text) + 8 + (len(text) // 2 + 2) * 2)}❤\n{' ' * 4}{' ' * (((len(text) + 8 + (len(text) // 2 + 2) * 2) - (len(text) + 4)) // 2)}{text}{' ' * (((len(text) + 8 + (len(text) // 2 + 2) * 2) - (len(text) + 4)) // 2)}\n❤{'━' * (len(text) + 8 + (len(text) // 2 + 2) * 2)}❤"
    
    def lines_6(text: str):
        return f"{'╱╲' * (len(text) // 2 + 2)}╱╲╱╲\n{' ' * 4}{text}\n{'╱╲' * (len(text) // 2 + 2)}╱╲╱╲"
    
    def center_text(text: str):
        return text.center(120)

class TextUtils:
    def fancy_text(text: str):
        convert = {
            "abcdefghijklmnopqrstuvwxyz": "𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ": "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"
        }
        for normal, fancy in convert.items():
            for c_normal, c_fancy in zip(normal, fancy):
                text = text.replace(c_normal, c_fancy)
        return text
    
    def fraktur_text(text: str):
        convert = {
            "abcdefghijklmnopqrstuvwxyz": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ": "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
        }
        for normal, fancy in convert.items():
            for c_normal, c_fancy in zip(normal, fancy):
                text = text.replace(c_normal, c_fancy)
        return text
    
    def cursive_text(text: str):
        convert = {
            "abcdefghijklmnopqrstuvwxyz": "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ": "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"
        }
        for normal, fancy in convert.items():
            for c_normal, c_fancy in zip(normal, fancy):
                text = text.replace(c_normal, c_fancy)
        return text
    
    def syllabic_text(text: str):
        for normal, fancy in zip("abcdefghijklmnopqrstuvwxyz", "ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ"):
            text = text.replace(normal, fancy)
        for normal, fancy in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ"):
            text = text.replace(normal, fancy)

        return text
    
    def strikethrough_text(text: str):
        return ''.join(c + '\u0337' for c in text)
    
    def double_struck_text(text: str):
        convert = {
            "abcdefghijklmnopqrstuvwxyz": "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ": "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"
        }
        for normal, fancy in convert.items():
            for c_normal, c_fancy in zip(normal, fancy):
                text = text.replace(c_normal, c_fancy)
        return text
    
    def make_ascii(text: str, font: str):
        return Figlet(font=font).renderText(text)

class GradientColors:
    red_to_blue = "255, 0, 0/0, 0, 255"
    red_to_yellow = "255, 0, 0/255, 255, 0"
    red_to_green = "255, 0, 0/0, 255, 0"
    red_to_orange = "255, 0, 0/255, 165, 0"
    red_to_brown = "255, 0, 0/139, 69, 19"
    red_to_purple = "255, 0, 0/128, 0, 128"
    red_to_white = "255, 0, 0/255, 255, 255"
    red_to_black = "255, 0, 0/0, 0, 0"
    red_to_pink = "255, 0, 0/255, 192, 203"
    red_to_silver = "255, 0, 0/192, 192, 192"
    red_to_cyan = "255, 0, 0/0, 255, 255"
    red_to_gray = "255, 0, 0/128, 128, 128"
    red_to_gold = "255, 0, 0/255, 215, 0"

    yellow_to_blue = "255, 255, 0/0, 0, 255"
    yellow_to_red = "255, 255, 0/255, 0, 0"
    yellow_to_green = "255, 255, 0/0, 255, 0"
    yellow_to_orange = "255, 255, 0/255, 165, 0"
    yellow_to_brown = "255, 255, 0/139, 69, 19"
    yellow_to_purple = "255, 255, 0/128, 0, 128"
    yellow_to_white = "255, 255, 0/255, 255, 255"
    yellow_to_black = "255, 255, 0/0, 0, 0"
    yellow_to_pink = "255, 255, 0/255, 192, 203"
    yellow_to_silver = "255, 255, 0/192, 192, 192"
    yellow_to_cyan = "255, 255, 0/0, 255, 255"
    yellow_to_gray = "255, 255, 0/128, 128, 128"
    yellow_to_gold = "255, 255, 0/255, 215, 0"

    green_to_blue = "0, 255, 0/0, 0, 255"
    green_to_red = "0, 255, 0/255, 0, 0"
    green_to_yellow = "0, 255, 0/255, 255, 0"
    green_to_orange = "0, 255, 0/255, 165, 0"
    green_to_brown = "0, 255, 0/139, 69, 19"
    green_to_purple = "0, 255, 0/128, 0, 128"
    green_to_white = "0, 255, 0/255, 255, 255"
    green_to_black = "0, 255, 0/0, 0, 0"
    green_to_pink = "0, 255, 0/255, 192, 203"
    green_to_silver = "0, 255, 0/192, 192, 192"
    green_to_cyan = "0, 255, 0/0, 255, 255"
    green_to_gray = "0, 255, 0/128, 128, 128"
    green_to_gold = "0, 255, 0/255, 215, 0"

    blue_to_green = "0, 0, 255/0, 255, 0"
    blue_to_red = "0, 0, 255/255, 0, 0"
    blue_to_yellow = "0, 0, 255/255, 255, 0"
    blue_to_orange = "0, 0, 255/255, 165, 0"
    blue_to_brown = "0, 0, 255/139, 69, 19"
    blue_to_purple = "0, 0, 255/128, 0, 128"
    blue_to_white = "0, 0, 255/255, 255, 255"
    blue_to_black = "0, 0, 255/0, 0, 0"
    blue_to_pink = "0, 0, 255/255, 192, 203"
    blue_to_silver = "0, 0, 255/192, 192, 192"
    blue_to_cyan = "0, 0, 255/0, 255, 255"
    blue_to_gray = "0, 0, 255/128, 128, 128"
    blue_to_gold = "0, 0, 255/255, 215, 0"

    orange_to_green = "255, 165, 0/0, 255, 0"
    orange_to_red = "255, 165, 0/255, 0, 0"
    orange_to_yellow = "255, 165, 0/255, 255, 0"
    orange_to_blue = "255, 165, 0/0, 0, 255"
    orange_to_brown = "255, 165, 0/139, 69, 19"
    orange_to_purple = "255, 165, 0/128, 0, 128"
    orange_to_white = "255, 165, 0/255, 255, 255"
    orange_to_black = "255, 165, 0/0, 0, 0"
    orange_to_pink = "255, 165, 0/255, 192, 203"
    orange_to_silver = "255, 165, 0/192, 192, 192"
    orange_to_cyan = "255, 165, 0/0, 255, 255"
    orange_to_gray = "255, 165, 0/128, 128, 128"
    orange_to_gold = "255, 165, 0/255, 215, 0"

    purple_to_green = "128, 0, 128/0, 255, 0"
    purple_to_red = "128, 0, 128/255, 0, 0"
    purple_to_yellow = "128, 0, 128/255, 255, 0"
    purple_to_blue = "128, 0, 128/0, 0, 255"
    purple_to_orange = "128, 0, 128/255, 165, 0"
    purple_to_brown = "128, 0, 128/139, 69, 19"
    purple_to_white = "128, 0, 128/255, 255, 255"
    purple_to_black = "128, 0, 128/0, 0, 0"
    purple_to_pink = "128, 0, 128/255, 192, 203"
    purple_to_silver = "128, 0, 128/192, 192, 192"
    purple_to_cyan = "128, 0, 128/0, 255, 255"
    purple_to_gray = "128, 0, 128/128, 128, 128"
    purple_to_gold = "128, 0, 128/255, 215, 0"

    brown_to_green = "139, 69, 19/0, 255, 0"
    brown_to_red = "139, 69, 19/255, 0, 0"
    brown_to_yellow = "139, 69, 19/255, 255, 0"
    brown_to_blue = "139, 69, 19/0, 0, 255"
    brown_to_orange = "139, 69, 19/255, 165, 0"
    brown_to_purple = "139, 69, 19/128, 0, 128"
    brown_to_white = "139, 69, 19/255, 255, 255"
    brown_to_black = "139, 69, 19/0, 0, 0"
    brown_to_pink = "139, 69, 19/255, 192, 203"
    brown_to_silver = "139, 69, 19/192, 192, 192"
    brown_to_cyan = "139, 69, 19/0, 255, 255"
    brown_to_gray = "139, 69, 19/128, 128, 128"
    brown_to_gold = "139, 69, 19/255, 215, 0"

    white_to_green = "255, 255, 255/0, 255, 0"
    white_to_red = "255, 255, 255/255, 0, 0"
    white_to_yellow = "255, 255, 255/255, 255, 0"
    white_to_blue = "255, 255, 255/0, 0, 255"
    white_to_orange = "255, 255, 255/255, 165, 0"
    white_to_purple = "255, 255, 255/128, 0, 128"
    white_to_brown = "255, 255, 255/139, 69, 19"
    white_to_black = "255, 255, 255/0, 0, 0"
    white_to_pink = "255, 255, 255/255, 192, 203"
    white_to_silver = "255, 255, 255/192, 192, 192"
    white_to_cyan = "255, 255, 255/0, 255, 255"
    white_to_gray = "255, 255, 255/128, 128, 128"
    white_to_gold = "255, 255, 255/255, 215, 0"

    gold_to_green = "255, 215, 0/0, 255, 0"
    gold_to_red = "255, 215, 0/255, 0, 0"
    gold_to_yellow = "255, 215, 0/255, 255, 0"
    gold_to_blue = "255, 215, 0/0, 0, 255"
    gold_to_orange = "255, 215, 0/255, 165, 0"
    gold_to_purple = "255, 215, 0/128, 0, 128"
    gold_to_brown = "255, 215, 0/139, 69, 19"
    gold_to_white = "255, 215, 0/255, 255, 255"
    gold_to_black = "255, 215, 0/0, 0, 0"
    gold_to_pink = "255, 215, 0/255, 192, 203"
    gold_to_silver = "255, 215, 0/192, 192, 192"
    gold_to_cyan = "255, 215, 0/0, 255, 255"
    gold_to_gray = "255, 215, 0/128, 128, 128"

    cyan_to_green = "0, 255, 255/0, 255, 0"
    cyan_to_red = "0, 255, 255/255, 0, 0"
    cyan_to_yellow = "0, 255, 255/255, 255, 0"
    cyan_to_blue = "0, 255, 255/0, 0, 255"
    cyan_to_orange = "0, 255, 255/255, 165, 0"
    cyan_to_purple = "0, 255, 255/128, 0, 128"
    cyan_to_brown = "0, 255, 255/139, 69, 19"
    cyan_to_white = "0, 255, 255/255, 255, 255"
    cyan_to_black = "0, 255, 255/0, 0, 0"
    cyan_to_pink = "0, 255, 255/255, 192, 203"
    cyan_to_silver = "0, 255, 255/192, 192, 192"
    cyan_to_gold = "0, 255, 255/255, 215, 0"
    cyan_to_gray = "0, 255, 255/128, 128, 128"

    gray_to_green = "128, 128, 128/0, 255, 0"
    gray_to_red = "128, 128, 128/255, 0, 0"
    gray_to_yellow = "128, 128, 128/255, 255, 0"
    gray_to_blue = "128, 128, 128/0, 0, 255"
    gray_to_orange = "128, 128, 128/255, 165, 0"
    gray_to_purple = "128, 128, 128/128, 0, 128"
    gray_to_brown = "128, 128, 128/139, 69, 19"
    gray_to_white = "128, 128, 128/255, 255, 255"
    gray_to_black = "128, 128, 128/0, 0, 0"
    gray_to_pink = "128, 128, 128/255, 192, 203"
    gray_to_silver = "128, 128, 128/192, 192, 192"
    gray_to_gold = "128, 128, 128/255, 215, 0"
    gray_to_cyan = "128, 128, 128/0, 255, 255"

    pink_to_green = "255, 192, 203/0, 255, 0"
    pink_to_red = "255, 192, 203/255, 0, 0"
    pink_to_yellow = "255, 192, 203/255, 255, 0"
    pink_to_blue = "255, 192, 203/0, 0, 255"
    pink_to_orange = "255, 192, 203/255, 165, 0"
    pink_to_purple = "255, 192, 203/128, 0, 128"
    pink_to_brown = "255, 192, 203/139, 69, 19"
    pink_to_white = "255, 192, 203/255, 255, 255"
    pink_to_black = "255, 192, 203/0, 0, 0"
    pink_to_silver = "255, 192, 203/192, 192, 192"
    pink_to_gold = "255, 192, 203/255, 215, 0"
    pink_to_cyan = "255, 192, 203/0, 255, 255"
    pink_to_gray = "255, 192, 203/128, 128, 128"

    silver_to_green = "192, 192, 192/0, 255, 0"
    silver_to_red = "192, 192, 192/255, 0, 0"
    silver_to_yellow = "192, 192, 192/255, 255, 0"
    silver_to_blue = "192, 192, 192/0, 0, 255"
    silver_to_orange = "192, 192, 192/255, 165, 0"
    silver_to_purple = "192, 192, 192/128, 0, 128"
    silver_to_brown = "192, 192, 192/139, 69, 19"
    silver_to_white = "192, 192, 192/255, 255, 255"
    silver_to_pink = "192, 192, 192/255, 192, 203"
    silver_to_gold = "192, 192, 192/255, 215, 0"
    silver_to_cyan = "192, 192, 192/0, 255, 255"
    silver_to_gray = "192, 192, 192/128, 128, 128"

    black_to_green = "0, 0, 0/0, 255, 0"
    black_to_red = "0, 0, 0/255, 0, 0"
    black_to_yellow = "0, 0, 0/255, 255, 0"
    black_to_blue = "0, 0, 0/0, 0, 255"
    black_to_orange = "0, 0, 0/255, 165, 0"
    black_to_purple = "0, 0, 0/128, 0, 128"
    black_to_brown = "0, 0, 0/139, 69, 19"
    black_to_white = "0, 0, 0/255, 255, 255"
    black_to_pink = "0, 0, 0/255, 192, 203"
    black_to_silver = "0, 0, 0/192, 192, 192"
    black_to_gold = "0, 0, 0/255, 215, 0"
    black_to_cyan = "0, 0, 0/0, 255, 255"
    black_to_gray = "0, 0, 0/128, 128, 128"

class Gradient:
    def gradient_text_custom(text: str, rgb, rgb2, direction: str = "random"):
        gradient_step = 1 / (len(text) - 1)
        directions = {
            'vertical': [(1, 0), (0, 1)],
            'horizontal': [(0, 1), (1, 0)],
            'diagonal': [(1, 1), (-1, 1)],
            'antidiagonal': [(1, -1), (-1, -1)],
            'random': random.choice([[(1, 0), (0, 1)], [(0, 1), (1, 0)], [(1, 1), (-1, 1)], [(1, -1), (-1, -1)]])
        }

        direction_vectors = directions[direction]
        rgb_text = ""

        for i, char in enumerate(text):
            vector = direction_vectors[i % len(direction_vectors)]
            position = i * gradient_step
        
            r = int((1 - position) * rgb[0] + position * rgb2[0])
            g = int((1 - position) * rgb[1] + position * rgb2[1])
            b = int((1 - position) * rgb[2] + position * rgb2[2])

            rgb_text += f"\033[38;2;{r};{g};{b}m{char}"

        rgb_text += "\033[0m"
        return rgb_text
    
    def gradient_text(text: str, color: list):
        colors = color.split('/')
        start_color = tuple(map(int, colors[0].split(', ')))
        end_color = tuple(map(int, colors[1].split(', ')))
        return Gradient.gradient_text_custom(text, start_color, end_color)

class Discord:
    def get_native_build():
        return requests.get(
            "https://updates.discord.com/distributions/app/manifests/latest",
            params={
                "install_id":'0',
                "channel":"stable",
                "platform":"win",
                "arch":"x86"
            },
            headers={
                "user-agent": "Discord-Updater/1",
                "accept-encoding": "gzip"
        }).json()["metadata_version"]
    
    def get_main_version():
        r = requests.get(
            "https://discord.com/api/downloads/distributions/app/installers/latest",
            params={
                "channel":"stable",
                "platform":"win",
                "arch":"x86"
            },
            allow_redirects=False
        ).text

        return re.search(r'x86/(.*?)/', r).group(1)
    
    def get_build_number():
        page = requests.get("https://discord.com/app").text.split("app-mount")[1]
        assets = re.findall(r'src="/assets/([^"]+)"', page)[::-1]

        for asset in assets:
            js=requests.get(f"https://discord.com/assets/{asset}").text
            
            if "buildNumber:" in js:
                return int(js.split('buildNumber:"')[1].split('"')[0])
            
    def get_xsuper_properties(build, version, buildnumb):
        return base64.b64encode(json.dumps({
            "os": "Windows",
            "browser": "Discord Client",
            "release_channel": "stable",
            "client_version": version,
            "os_version": "10.0.19045",
            "os_arch": "x64",
            "app_arch": "ia32",
            "system_locale": "en",
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9038 Chrome/120.0.6099.291 Electron/28.2.7 Safari/537.36",
            "browser_version": "22.3.26",
            "client_build_number": buildnumb,
            "native_build_number": build,
            "client_event_source": None,
            "design_id": 0
        }).encode()).decode()
    
    def get_cookies(proxy: str):
        session = requests.Session()
        session.proxies=f"http://{proxy}"

        return session.get("https://discord.com").cookies
    
    def generate_birthdate():
        return f"{str(random.randint(1970,2000))}-{str(random.randint(1,12)).zfill(2)}-{str(random.randint(1,23)).zfill(2)}"

    def check_token(token):
        return requests.get("https://discord.com/api/v9/users/@me/settings", headers={
            "Authorization": token
        }).status_code == 200
    
    def get_fingerprint(proxy: str):
        session = requests.Session()
        session.proxies=f"http://{proxy}"

        return session.get("https://discord.com/api/v9/experiments?with_guild_experiments=true").json()['fingerprint']

class Utils:
    def get_full_name():
        full_names = ['Amber, Illich', 'Cole, Barrows', 'Scott, Lee', 'Paul, Lapp', 'Amy, Johnson', 'Jackie, Naill', 'Tamara, Wiggins', 'Brett, Fullerton', 'David, Crisci', 'Lavona, Caldwell', 'Kristine, Merryman', 'Courtney, Pearce', 'Carla, Murray', 'Ronald, Oldham', 'Scott, Ulrich', 'Caprice, Brenner', 'William, Jacobsen', 'Micheal, Cunningham', 'Julie, Cashion', 'Earnest, Maddox', 'Tawana, Luckhardt', 'Kathleen, Ellingham', 'Robert, Chavez', 'Anthony, Kleis', 'Lisa, Moreta', 'Yvette, Mann', 'Tisha, Martinez', 'Joseph, Fitzpatrick', 'Holly, Oneal', 'Dewey, Jasso', 'James, Bulter', 'James, Bekis', 'Henry, Tomlin', 'Alexander, Martin', 'Ronnie, Pirtle', 'William, Kearney', 'Martha, Hickman', 'Robert, Brayton', 'Cecilia, Doolittle', 'James, Morales', 'Sam, Reed', 'Suzanne, Breaud', 'Susan, Higgins', 'Jerry, Hofheimer', 'Jessica, Baker', 'Jose, Wesley', 'Arturo, Foesch', 'Warren, Seller', 'Stacy, Swank', 'Laverne, Faustini', 'Wendy, Slaughter', 'James, Reynalds', 'Luis, Hannah', 'Gayle, Mcneill', 'Elizabeth, Thorne', 'David, Kochevar', 'Deborah, Dubois', 'Emily, Dean', 'Herbert, Brightwell', 'Joe, Mazur', 'Trudy, Amos', 'Virginia, Hollingsworth', 'John, Skeesick', 'Maria, Haley', 'Linda, Grochmal', 'Eric, Stapleton', 'Josephine, Littich', 'Jill, Neeley', 'Christina, Roberts', 'Gretchen, Boyd', 'Stephanie, Scala', 'Aaron, Wolery', 'Lorraine, Bonnell', 'Luis, Mayfield', 'Charles, Riehl', 'Oscar, Woodward', 'Larry, Maio', 'Benjamin, Leyva', 'Theodore, Shockey', 'William, Terrano', 'Karen, Romero', 'Joel, Reynolds', 'Jamie, Smith', 'Erin, Samson', 'Lela, Matson', 'Lois, Bird', 'Karen, Walker', 'Evelyn, Campbell', 'Donald, Allen', 'Morgan, Stamey', 'Julie, Geer', 'Nelly, Berry', 'Tom, Hall', 'Opal, Griess', 'William, Garner', 'William, Wallace', 'Elsie, Kenely', 'James, Bolden', 'Troy, Chamberlin', 'Hien, Hebert', 'Kenneth, Pena', 'Mary, Mitchell', 'Virginia, Armenta', 'Catherine, Tremblay', 'Maureen, Thorson', 'Van, Wilkowitz', 'William, Kampa', 'Christopher, Bell', 'Linda, Lawson', 'Michael, Mccalpane', 'Bradley, Sherman', 'Dominic, Sage', 'Eva, Mattson', 'Kathryn, Jones', 'Alice, Shafer', 'Marcel, Coachman', 'Amy, Seville', 'Ralph, Recalde', 'Imelda, Maldonado', 'Larry, Smith', 'Donna, Henderson', 'Douglas, Meyers', 'Ashley, Saffell', 'Patricia, Calico', 'Richard, Kirk', 'Philip, Mcdonald', 'Grace, Rodgers', 'Doris, Allen', 'Larry, Arnold', 'Olive, Valle', 'Marilyn, Campuzano', 'Dorothy, Malcolm', 'Paul, Tienda', 'Shelia, Hanson', 'James, Richardson', 'Frederick, Ivory', 'Dana, Stolte', 'Kenneth, Mclean', 'Johnie, Holyfield', 'Ana, Fields', 'Arthur, Jackson', 'Victoria, Matthews', 'Claudia, Lemos', 'Regina, Kost', 'Janie, Sippel', 'Patricia, Barthel', 'Melissa, Hartzell', 'Harold, Perkins', 'Nancy, Duke', 'Joan, Malone', 'James, Demeo', 'Tamika, Albert', 'Patricia, Schulze', 'Jeffrey, Holt', 'Donald, Sanez', 'Clay, Price', 'John, Williams', 'Matthew, Jones', 'Fernando, Hutchison', 'Joshua, Morris', 'Freda, Flander', 'Jordan, Martinez', 'Dorothy, Mazza', 'Michael, Cameron', 'Chris, Lacy', 'Ronald, Wise', 'Terry, Jefferson', 'Rose, Murray', 'Kathleen, Barr', 'Neva, Jervey', 'Diane, Hudson', 'Petronila, Garmon', 'Christopher, Bryant', 'Patricia, Stevens', 'Carmen, Couch', 'Bradley, Gonzales', 'Lissette, Lenis', 'Cathey, Montey', 'William, Flores', 'Melissa, Coggin', 'Nicholas, Williams', 'Carolyn, Noriega', 'Wes, Angelini', 'James, Kobayashi', 'Thomas, Parks', 'Mark, Day', 'Gay, Gleason', 'Bettye, Byrd', 'Michael, Mackie', 'Joseph, Walston', 'Stella, Rivera', 'Sharon, Hudek', 'John, Riley', 'Alvin, Krell', 'Jonathan, Mercado', 'Martha, Endo', 'Ciara, Delacruz', 'Earl, Atwell', 'Glenn, Overmyer', 'Steven, Toher', 'Amanda, Doleman', 'Charles, Weaver', 'Clifford, Marchetti', 'Edythe, Cassell', 'Kathleen, Stewart', 'Joseph, Adorno', 'Nydia, Kercheval', 'Cynthia, Noel', 'Amanda, Miller', 'Susan, Gordon', 'Michelle, Bogle', 'Michael, Higa', 'Mary, Smolder', 'Archie, Mooney', 'Jennifer, Carter', 'Juan, Evans', 'David, Heard', 'Mildred, Templeton', 'Faye, Jordan', 'Laura, Moskal', 'Josiah, Vaughan', 'Nolan, Burges', 'Jennifer, Low', 'Joseph, Young', 'David, White', 'Thomas, Harmon', 'Melba, Cox', 'Earl, Cruz', 'Micheal, Burton', 'Otis, Dean', 'Gertrude, Brown', 'Jessica, Campbell', 'Gary, Clark', 'Kenneth, Gamble', 'Sidney, Bove', 'Michael, Hoffman', 'Jessica, Lindsey', 'Carla, Scott', 'Danny, Obannon', 'Erma, Gavitt', 'Sasha, Bernal', 'Charles, Ates', 'Daniel, Vondielingen', 'Robert, Black', 'Edward, Fort', 'Steven, Ellis', 'Anthony, Howard', 'Eli, Moses', 'Charles, Landfair', 'John, Miranda', 'Karen, Tuggle', 'Raymond, Lerch', 'Devon, Asbury', 'Darnell, Cook', 'Courtney, Vazquez', 'Leah, Tatum', 'Judith, Rumble', 'Russell, Stanford', 'Donald, Walker', 'Carol, Longfellow', 'Anthony, Thompson', 'Carol, Greer', 'Blanche, Guinn', 'Melissa, Loper', 'Marvin, Riveria', 'Barbara, Russell', 'Raymundo, Howard', 'Eileen, Ashford', 'Jettie, Garber', 'Annmarie, Navejas', 'Gail, Galloway', 'Norma, Gazzo', 'Joseph, Richardson', 'Mary, Walters', 'James, Rhoades', 'Brenda, Pope', 'Nancy, Roekle', 'Peter, Holmes', 'Sherri, Johnson', 'Donald, Geer', 'Warren, Adams', 'Anja, Bartell', 'Emily, Mccoy', 'Ricky, Clark', 'Mary, Austin', 'Wallace, Cacy', 'Mohammed, Lietzke', 'Emma, Jaggers', 'Shirley, Leggett', 'Lea, Cox', 'Shawn, Mackey', 'Norma, Spoor', 'Allen, Wolfe', 'Richard, Loaiza', 'Renee, Kershaw', 'Georgia, Austin', 'William, Hinckley', 'Ronald, Pisano', 'Angela, Howard', 'James, Shelby', 'Tonya, Hunt', 'David, Ward', 'John, Gates', 'Michel, Campos', 'Carrie, Neumann', 'Ismael, Canclini', 'Misty, Odum', 'Tiffany, King', 'Kenneth, Blake', 'Frances, Johnson', 'Francisco, Odermott', 'Wanda, Bagshaw', 'Michael, Reynolds', 'Angel, Woodard', 'Helen, Aronson', 'Hugo, Ruiz', 'Don, Weeks', 'Cindy, Otero', 'Kimberly, Smith', 'Gary, Harpster', 'David, Johnson', 'Gloria, Tipps', 'Mariah, Meyer', 'Ann, Morales', 'Barry, Aman', 'Brendan, Gruber', 'Paul, Epperson', 'Leonard, Diss', 'Raymond, Morgan', 'Kathleen, Cason', 'Kelsey, Triche', 'Nora, Studivant', 'David, Moore', 'Gwendolyn, Goldblatt', 'Margie, Frank', 'Ann, Schimmel', 'Jordan, Higgins', 'Billie, Husar', 'Robert, Rodenberger', 'Joseph, Adams', 'Angela, Villalobas', 'Enrique, Debernardi', 'Georgia, Green', 'William, Camacho', 'Charlie, Spaulding', 'Cynthia, Robinson', 'Jennifer, Arnold', 'Effie, Fagan', 'Christopher, Holloway', 'Patricia, Tiemann', 'Candelaria, Summerlin', 'Amber, Wiseman', 'Robert, Hunsucker', 'Louis, Matthias', 'Terry, Johnson', 'Elsie, Sokolowich', 'Brandon, Pichardo', 'Hilary, Luneau', 'Clara, Martin', 'Kimberly, Powell', 'Chris, Nagy', 'Kara, Condie', 'John, Meunier', 'Lois, Eld', 'Tammy, Welch', 'Eric, Bagwell', 'Michael, Strand', 'Charlie, Saurel', 'Frederick, Ichikawa', 'Victor, Ware', 'John, Howard', 'Edmund, Williams', 'Herbert, Ray', 'Betty, Knipper', 'Christine, Johnson', 'Sandra, Garcia', 'Jason, Nicewander', 'Kevin, Heath', 'Steven, Saunders', 'Christopher, Jones', 'Juanita, Grimes', 'Virginia, Jozwiak', 'Wallace, Stanley', 'Melvin, Kendall', 'Rona, Salgado', 'Tera, Brooks', 'Jack, Mesa', 'Donna, Maya', 'Katharine, Dahlstrom', 'Eloise, Hooper', 'Heidi, Branch', 'Raul, Howard', 'Virginia, Poe', 'Donald, Whisler', 'Evelyn, Cunningham', 'Mary, Miller', 'Michael, Boe', 'John, Duncan', 'Rachel, Brown', 'Carolyn, Logan', 'Francis, Morano', 'Freda, Mcelwaine', 'Paige, Steele', 'David, Mcgee', 'Justin, Preece', 'Teresa, Robledo', 'Wilbert, Cuffie', 'Danny, Mullen', 'Lynette, Levy', 'Margaret, Whittaker', 'William, Carroll', 'Rochelle, Sardin', 'John, Turner', 'Loretta, Frierson', 'Melissa, Boesiger', 'Barbra, Bevan', 'Deanna, Diaz', 'Willie, Morales', 'Charles, Royster', 'Alan, Wuest', 'Samuel, Gorman', 'Irving, Stephenson', 'Tina, Pittman', 'Charles, Torkelson', 'Rodney, Green', 'Yukiko, Dennis', 'Joseph, Menn', 'Keith, Johnson', 'Matthew, Sirois', 'Pauline, Culler', 'Julia, Vines', 'Jason, Kammerer', 'George, Lewis', 'Margo, Wood', 'Heidi, Barnard', 'Brenda, Bosworth', 'Daisy, Bryant', 'Harold, Ha', 'Hector, Lara', 'Cheryl, Holmes', 'Mike, Cowles', 'Maynard, Lawson', 'Audrey, Jackson', 'Shelby, Hester', 'Sara, Martino', 'Dennis, Beeler', 'Jerry, Diaz', 'David, Ellis', 'Laurie, Vaughn', 'Kristan, Dahnke', 'Mark, Pollard', 'Mary, Jones', 'Emma, Stover', 'Ricky, Solomon', 'Chad, Williams', 'Rodney, Quintanilla', 'Angela, Norton', 'Valerie, Lenk', 'Marcia, Bodie', 'Andre, Clay', 'Stephen, Ness', 'Virginia, Singleton', 'David, Gobel', 'Amy, Washington', 'Chad, Gluck', 'Heidi, Welke', 'Joseph, Bergman', 'Kristen, Brennan', 'Timothy, Fulton', 'Kyle, Leblanc', 'Elizabeth, Germy', 'Dale, Payne', 'Christina, Jewett', 'Katherine, Allison', 'Lillian, Shelby', 'Donald, Kelley', 'Justin, Banks', 'William, Oneil', 'Teri, Law', 'James, Harris', 'Scott, Schwandt', 'Dorothy, Dyess', 'David, Godwin', 'Penny, Rowlett', 'Christopher, Roberts', 'David, Mcclain', 'Veronica, Lamke', 'Nancy, Robinson', 'Arnold, Bradway', 'Glenda, Perkins', 'Bonnie, Specht', 'Kelvin, Ramey', 'Minnie, Cunningham', 'Tamara, Garcia', 'Lucia, Howard', 'Aaron, Lundgren', 'Soraya, Rogers', 'Patricia, Estimable', 'Henrietta, Tyler', 'Claudia, Grimm', 'Jorge, Menda', 'Sonia, Esteban']
        return random.choice(full_names)
    
    def generate_uuid():
        return '-'.join(''.join(random.choice('abcdef0123456789') for _ in range(x)) for x in [8, 4, 4, 4, 12])
    
    def generate_user_agent():
        ua = UserAgent()
        return ua.random
    
    def get_timestamp():
        return int(time.time() * 1000)
    
    def log_time():
        return "{:%H:%M:%S}".format(datetime.datetime.now())

class Logger:
    def success(text: str) -> None:
        print(f' [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}- {ColorUtils.hex_color("#FFFFFF")}[ {ColorUtils.hex_color("#00FF00")}+{ColorUtils.hex_color("#FFFFFF")} ] {ColorUtils.hex_color("#00FF00")}{text.split(",")[0]}: {ColorUtils.hex_color("#00ccff")}{text.split(",")[1]} {ColorUtils.hex_color("#FFFFFF")}({ColorUtils.hex_color("#00ccff")}{text.split(",")[2]}{ColorUtils.hex_color("#FFFFFF")})')

    def failed(text: str) -> None:
        print(f' [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}- {ColorUtils.hex_color("#FFFFFF")}[ {ColorUtils.hex_color("#FF0000")}-{ColorUtils.hex_color("#FFFFFF")} ] {ColorUtils.hex_color("#FF0000")}{text.split(",")[0]}: {ColorUtils.hex_color("#00ccff")}{text.split(",")[1]} {ColorUtils.hex_color("#FFFFFF")}({ColorUtils.hex_color("#00ccff")}{text.split(",")[2]}{ColorUtils.hex_color("#FFFFFF")})')

    def captcha(text: str) -> None:
        print(f' [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}- {ColorUtils.hex_color("#FFFFFF")}[ {ColorUtils.hex_color("#fcf300")}${ColorUtils.hex_color("#FFFFFF")} ] {ColorUtils.hex_color("#fcf300")}{text.split(",")[0]}: {ColorUtils.hex_color("#00ccff")}{text.split(",")[1]} {ColorUtils.hex_color("#FFFFFF")}({ColorUtils.hex_color("#00ccff")}{text.split(",")[2]}{ColorUtils.hex_color("#FFFFFF")})')

    def info(text: str) -> None:
        print(f' [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}- {ColorUtils.hex_color("#FFFFFF")}[ {ColorUtils.hex_color("#f77f00")}*{ColorUtils.hex_color("#FFFFFF")} ] {ColorUtils.hex_color("#f77f00")}{text.split(",")[0]}: {ColorUtils.hex_color("#00ccff")}{text.split(",")[1]} {ColorUtils.hex_color("#FFFFFF")}({ColorUtils.hex_color("#00ccff")}{text.split(",")[2]}{ColorUtils.hex_color("#FFFFFF")})')

    def warning(text: str) -> None:
        print(f' [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}- {ColorUtils.hex_color("#FFFFFF")}[ {ColorUtils.hex_color("#ffd60a")}!{ColorUtils.hex_color("#FFFFFF")} ] {ColorUtils.hex_color("#ffd60a")}{text.split(",")[0]}: {ColorUtils.hex_color("#00ccff")}{text.split(",")[1]} {ColorUtils.hex_color("#FFFFFF")}({ColorUtils.hex_color("#00ccff")}{text.split(",")[2]}{ColorUtils.hex_color("#FFFFFF")})')

    def pretty(text: str) -> None:
        print(f' [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}- {ColorUtils.hex_color("#FFFFFF")}[ {ColorUtils.hex_color("#5e548e")}^{ColorUtils.hex_color("#FFFFFF")} ] {ColorUtils.hex_color("#5e548e")}{text.split(",")[0]}: {ColorUtils.hex_color("#00ccff")}{text.split(",")[1]} {ColorUtils.hex_color("#FFFFFF")}({ColorUtils.hex_color("#00ccff")}{text.split(",")[2]}{ColorUtils.hex_color("#FFFFFF")})')

    def custom(color: str, symbol: str, text: str) -> None:
        print(f' [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}- {ColorUtils.hex_color("#FFFFFF")}[ {ColorUtils.hex_color(f"#{color}")}{symbol}{ColorUtils.hex_color("#FFFFFF")} ] {ColorUtils.hex_color(f"#{color}")}{text.split(",")[0]}: {ColorUtils.hex_color("#00ccff")}{text.split(",")[1]} {ColorUtils.hex_color("#FFFFFF")}({ColorUtils.hex_color("#00ccff")}{text.split(",")[2]}{ColorUtils.hex_color("#FFFFFF")})')

class RaduLogger:
    def success(text: str) -> None:
        print(f'{ColorUtils.hex_color("#FFFFFF")} [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}| {ColorUtils.hex_color("#29bf12")}SUC {ColorUtils.hex_color("#6c757d")}| {text}')

    def failed(text: str) -> None:
        print(f'{ColorUtils.hex_color("#FFFFFF")} [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}| {ColorUtils.hex_color("#d00000")}ERR {ColorUtils.hex_color("#6c757d")}| {text}')

    def info(text: str) -> None:
        print(f'{ColorUtils.hex_color("#FFFFFF")} [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}| {ColorUtils.hex_color("#2a9d8f")}INF {ColorUtils.hex_color("#6c757d")}| {text}')
    
    def warning(text: str) -> None:
        print(f'{ColorUtils.hex_color("#FFFFFF")} [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}| {ColorUtils.hex_color("#ffea00")}WAR {ColorUtils.hex_color("#6c757d")}| {text}')

    def debuginfo(text: str) -> None:
        print(f'{ColorUtils.hex_color("#FFFFFF")} [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}| {ColorUtils.hex_color("#ff7b00")}DBG {ColorUtils.hex_color("#6c757d")}| {text}')
