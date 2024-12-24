from pylematch.pylematch import Pylematch
import os


# ANSI escape codes for colors
class Colors:
    BOLD = "\033[1m"
    RESET = "\033[0m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"


def run(test_path, test_cases, test_name):
    # Initialize the Pylematch object
    pylematch = Pylematch(root=test_path)

    print(f"\n{Colors.CYAN}Scan dir: {test_path}{Colors.RESET}")

    for path, is_matched in pylematch.matched():
        status = f"{Colors.BOLD}Matched{Colors.RESET}" if is_matched else "Ignored"
        print(f"{path}: {status}")

    for path, rules in pylematch.get_all_rules():
        print(f"{Colors.YELLOW}{os.path.relpath(path, test_path)}{Colors.RESET}")
        for rule in rules:
            _r = ', '.join(f"'{key}': '{Colors.CYAN}{value}{Colors.RESET}'" for key, value in rule.rule.items())
            print(f"    {_r}")

    for input, expected in test_cases.items():
        output = pylematch.is_matched(test_path / input)
        assert output == expected, f"{Colors.RED}Test {test_name} failed for '{input}': Expected '{expected}', got '{output}'{Colors.RESET}"
