"""
Module:        Pylematch
Description:   A module for matching file system paths against patterns.
Author:        Andrii Burkatskyi aka andr11b
Year:          2024
Version:       0.0.1.241223
License:       MIT License
Email:         4ndr116@gmail.com, andr11b@ukr.net
Link:          https://github.com/codyverse/pylematch
"""

import os
import re
import random
import string
from collections import defaultdict


class Pylematch:
    """
    A class for managing file match patterns using custom `.pylematch` protocol files.

    This class scans directories starting from a root path, reads `.pylematch` files to load match rules, and
    determines whether files or directories should be matched based on those rules.

    Attributes:
        _root (str): The root directory where the scanning starts.
        _protocol (str): The filename of the protocol file to be processed (default: `.pylematch`).
        _rules (dict): A dictionary mapping directories to their associated rules.
        _matched (dict): A dictionary of file paths and whether they are matched.
    """

    class PylematchRule:
        """
        Represents a single rule in the match protocol.

        Attributes:
            pattern (str): The raw pattern string from the match file.
            context (str): The directory context for the rule.
            regex (str): The compiled regular expression representing the rule.
            is_negation (bool): Whether the rule negates matching files.
            is_strictly_dir (bool): Whether the rule applies only to directories.
        """

        def __init__(self, pattern, context='', parent=None):
            if parent is None or not isinstance(parent, Pylematch):
                raise Exception("Cannot instantiate PylematchRule directly.")

            self._rule = self._compose(pattern, context)

        def __str__(self):
            return self._rule

        def __repr__(self):
            return f'PylematchRule({self._rule})'

        def _compose(self, pattern, context):
            placeholder_map = {}

            def _hidescape(match):
                placeholder = self._random()
                placeholder_map[placeholder] = match.group(0)

                return placeholder

            context = '' if context in {'.', '/'} else re.escape(context.rstrip('/')) + r'/'

            pattern = pattern.strip()

            repattern = re.sub(r'\\(.)', _hidescape, pattern)

            # Ignore empty lines and comments
            if repattern.strip() == '' or repattern[0] == '#':
                repattern = ''

            # Handle negation patterns (start with '!')
            if repattern.startswith('!'):
                is_negation = True
                repattern = repattern[1:]
            else:
                is_negation = False

            # Normalize slashes, e.g., `//` -> `/`, and remove leading slashes.
            repattern = (re.sub(r'/+', '/', repattern)).lstrip('/')
            #  Normalize asterisks, i.e., `***` -> `**`.
            repattern = re.sub(r'\*{3,}', '**', repattern)

            # Trailing slash (/) means this is explicitly a directory pattern
            is_strictly_dir = repattern.endswith('/')
            repattern = repattern.rstrip('/')

            if not is_strictly_dir and repattern == '**':
                repattern = r'.+$'
            elif not is_strictly_dir and repattern == '*':
                repattern = r'[^/]+/?$'
            else:

                def _rebrackets(match):
                    content = match.group(0)

                    if content.startswith('[!'): content = content.replace('[!', '[^')

                    placeholder = self._random()
                    placeholder_map[placeholder] = content

                    return f"{placeholder}"

                repattern = re.sub(r'\[.*?\]', _rebrackets, repattern)

                is_ending = False

                if not is_strictly_dir:
                    instance = r'/\*\*$'  # a trailing `/**`
                    if re.search(instance, repattern):
                        is_ending = True

                        placeholder = self._random()
                        placeholder_map[placeholder] = r'/(.+)$'
                        repattern = re.sub(instance, placeholder, repattern)

                    instance = r'\*\*$'  # a trailing `**`
                    if re.search(instance, repattern):
                        is_ending = True

                        placeholder = self._random()
                        placeholder_map[placeholder] = r'.*'
                        repattern = re.sub(instance, placeholder, repattern)

                    instance = r'/\*$'  # a trailing `/*`
                    if re.search(instance, repattern):
                        is_ending = True

                        placeholder = self._random()
                        placeholder_map[placeholder] = r'/[^/]+/?$'
                        repattern = re.sub(instance, placeholder, repattern)

                instance = r'\*\*'  # all instances of the `**`
                if re.search(instance, repattern):
                    placeholder = self._random()
                    placeholder_map[placeholder] = r'(.*)?'
                    repattern = re.sub(instance, placeholder, repattern)

                instance = r'\*'  # all instances of the `*`
                if re.search(instance, repattern):
                    placeholder = self._random()
                    placeholder_map[placeholder] = r'[^/]*'
                    repattern = re.sub(instance, placeholder, repattern)

                instance = r'\?'  # all instances of the the `?`
                if re.search(instance, repattern):
                    placeholder = self._random()
                    placeholder_map[placeholder] = r'[^/]{1}'
                    repattern = re.sub(instance, placeholder, repattern)

                repattern = re.escape(repattern)

                for placeholder, value in placeholder_map.items():
                    repattern = re.sub(re.escape(placeholder), value, repattern)

                if not is_ending:
                    if is_strictly_dir:
                        repattern += r'\/$'  # matches directory paths that explicitly end with a slash (/)
                    else:
                        repattern += r'(/?$)'  # matches paths that may or may not end with a slash (/)
            repattern = '^' + context + repattern

            return {
                'pattern': pattern,
                'context': context,
                'regex': repattern,
                'is_negation': is_negation,
                'is_strictly_dir': is_strictly_dir,
            }

        def _random(self, k=8):
            return f"_{''.join(random.choices(string.ascii_letters + string.digits, k=k))}_"

        def match(self, relpath):
            return bool(re.compile(self.regex).match(relpath))

        @property
        def rule(self):
            return self._rule

        @property
        def pattern(self):
            return self._rule['pattern']

        @property
        def regex(self):
            return self._rule['regex']

        @property
        def context(self):
            return self._rule['context']

        @property
        def is_strictly_dir(self):
            return self._rule['is_strictly_dir']

        @property
        def is_negation(self):
            return self._rule['is_negation']

    def __init__(self, root, protocol='.pylematch'):
        """
        Initialize the Pylematch instance.


        This method initializes the Pylematch class by setting the root directory from where the scanning starts and
        specifying the match protocol file.

        Args:
            root (str): The root directory where the scanning should begin.
                        This should be an absolute or relative path, and it must point to a valid directory.
                        If the path is relative, it will be resolved relative to the current working directory.
            protocol (str): The name of the protocol file to use for pattern matching.
                            Default is `.pylematch`. The file must be readable, and should contain valid match patterns.

        Raises:
            ValueError: If the root directory does not exist or is not a directory.
            OSError: If there are any issues accessing the protocol file.

        Example:
            # Create an instance of Pylematch with the current directory as the root
            pylematch = Pylematch(root='.', protocol='.ignorem')
        """
        self._root = os.path.normpath(os.path.abspath(root))
        if not os.path.isdir(self._root):
            raise ValueError(f"The root directory '{self._root}' is invalid or does not exist.")

        self._protocol = protocol
        self._rules = defaultdict(list)
        self._matched = {}
        self._load_rules()
        self._load_paths()

    def _load_rules(self):
        """
        Collect all relative paths and check them against the accumulated rules.

        Traverses directories from the root to the deepest level to gather
        match rules from protocol files.
        """
        for dirpath, _, filenames in sorted(os.walk(self._root), key=lambda x: x[0]):
            ancestor = dirpath if dirpath == self._root else os.path.dirname(dirpath)
            self._rules[dirpath].extend(self._rules[ancestor])

            # Process local rules if the protocol file exists
            if self._protocol in filenames:
                try:
                    self._parse_file(dirpath, os.path.join(dirpath, self._protocol))
                except Exception as e:
                    print(f"Error processing protocol file in directory '{dirpath}': {e}")

    def _parse_file(self, directory, filepath):
        """
        Load rules from the file and store them in rules.

        Args:
            directory (str): The directory containing the protocol file.
            filepath (str): The full path to the protocol file.
        """
        context = os.path.relpath(directory, self._root)

        try:
            with open(filepath, 'r') as file:
                for line in file:
                    pattern = line.strip()

                    if pattern and not pattern.startswith('#'):
                        rule = self.PylematchRule(pattern, parent=self, context=context)
                        self._rules[directory].append(rule)
        except FileNotFoundError:
            print(f"File not found: The protocol file '{filepath}' does not exist.")
        except PermissionError:
            print(f"Error: Permission denied to read '{filepath}'.")
        except Exception as e:
            print(f"Error: An unexpected error occurred while reading '{filepath}': {e}")

    def _load_paths(self):
        """
        Collect all relative paths and check them against the accumulated rules.

        This method traverses the file tree and applies the rules to each file
        and directory to determine if they should be matched.
        """
        relpaths = []

        for dirpath, dirnames, filenames in sorted(os.walk(self._root), key=lambda x: x[0]):
            for dirname in dirnames:
                relpaths.append(os.path.relpath(os.path.join(dirpath, dirname), self._root) + os.sep)

            for filename in filenames:
                relpaths.append(os.path.relpath(os.path.join(dirpath, filename), self._root))

        for relpath in relpaths:
            abspath = os.path.join(self._root, relpath)
            is_matched = False

            # Check rules for the directory containing the file/directory
            directory = os.path.dirname(abspath) if abspath != self._root else self._root

            for rule in self._rules[directory]:
                if rule.match(relpath):
                    is_matched = not rule.is_negation

            # Store the path status in the dictionary
            self._matched[relpath] = is_matched

    def is_matched(self, path):
        """
        Public method for checking if a path is matched.

        Args:
            path (str): The absolute or relative path to check.

        Returns:
            bool: True if the path is matched, False otherwise.
        """
        path = os.path.normpath(os.path.abspath(path))
        path = os.path.relpath(path, self._root) + (os.sep if os.path.isdir(path) else '')

        is_matched = self._matched.get(path, None)

        return is_matched

    def matched(self):
        """
        Public method to retrieve matching results for files and directories.

        This method returns a list of tuples, where each tuple contains a relative path and a boolean value indicating
        whether the file or directory is matched based on the specified rules.

        Returns:
            dict: A dictionary where keys are relative paths, and values are booleans indicating whether each
                  path is matched (True) or ignored (False).
        """
        return self._matched.items()

    def get_all_rules(self):
        """
        Public method to retrieve all declared rules.

        This method returns a list of all rules defined for each directory.

        Returns:
            dict: A dictionary where the keys are directory paths and the values are lists of 
                  `PylematchRule` objects associated with those directories.
        """
        return self._rules.items()

    def get_rules(self, directory):
        """
        Public method to retrieve rules for a specific directory.

        Args:
            directory (str): The directory to fetch rules for.

        Returns:
            list: A list of `PylematchRule` objects associated with the specified directory.
        """
        return self._rules.get(directory, [])

    def add_rule(self, directory, pattern):
        """
        Optionally, add a new rule to a specific directory.

        This method adds a new match rule for the specified directory.

        Args:
            directory (str): The directory to add the rule to.
            pattern (str): The match pattern to add.
        """
        pattern = pattern.strip()
        if pattern and not pattern.startswith('#'):
            rule = self.PylematchRule(pattern, parent=self)
            self._rules[directory].append(rule)


if __name__ == '__main__':
    pylematch = Pylematch(root='.', protocol='.pylematch')
    # Retrieve a list of matched and unmatched files and directories and print their status
    for path, is_matched in pylematch.matched:
        status = "Matched" if is_matched else "Ignored"
        print(f"{path}: {status}")
