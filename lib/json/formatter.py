import json
import sys
import re
from pathlib import Path

class JSONFormatter:
    """
    High-Performance JSON Formatter & Minifier:
    - Pretty prints with customizable indentation and key sorting
    - Ultra-dense token minification (stripping all unnecessary whitespace)
    - Terminal syntax highlighting without heavy external dependencies
    """

    @staticmethod
    def format(data, indent=2, sort_keys=False, minify=False):
        if isinstance(data, str):
            data = json.loads(data)

        if minify:
            return json.dumps(data, separators=(',', ':'), sort_keys=sort_keys, ensure_ascii=False)
        else:
            return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

    @staticmethod
    def colorize(json_str):
        """
        Applies lightweight ANSI syntax colorization to JSON string for terminal view.
        """
        KEY_COLOR = "\033[94m"     # Blue
        STR_COLOR = "\033[92m"     # Green
        NUM_COLOR = "\033[93m"     # Yellow
        BOOL_COLOR = "\033[95m"    # Magenta
        NULL_COLOR = "\033[90m"    # Gray
        RESET = "\033[0m"

        lines = json_str.split("\n")
        colored_lines = []
        for line in lines:
            colored = line
            colored = re.sub(r'("(\\"|[^"])*?")(\s*:)', f'{KEY_COLOR}\\1{RESET}\\3', colored)
            colored = re.sub(r'(:\s*)("(\\"|[^"])*?")', f'\\1{STR_COLOR}\\2{RESET}', colored)
            colored = re.sub(r'(:\s*)(-?\d+(\.\d+)?)', f'\\1{NUM_COLOR}\\2{RESET}', colored)
            colored = re.sub(r'(:\s*)(true|false)', f'\\1{BOOL_COLOR}\\2{RESET}', colored)
            colored = re.sub(r'(:\s*)(null)', f'\\1{NULL_COLOR}\\2{RESET}', colored)
            colored_lines.append(colored)

        return "\n".join(colored_lines)
