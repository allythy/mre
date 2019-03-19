from abc import ABC
from typing import Union


class Regex(ABC):
    """Base class."""
    # Metacharacter
    ANY = "."
    DOT = "\."
    DIGIT = "\d"
    WHITESPACE = "\s"
    WORD_CHARS = "\w"  # Equivalent [A-Za-z0-9_]
    SLASH = "\/"

    # Metacharacter (Negate)
    NOT_DIGIT = "\D"
    NOT_WHITESPACE = "\S"
    NOT_WORD_CHARS = "\W"

    # Quantifiers
    ZERO_OR_ONE = "?"
    ZERO_OR_MULTIPLE = "*"
    ONE_OR_MULTIPLE = "+"

    # Set
    HYPHEN = "\-"

    def __init__(self, *regexs: Union[str, 'Regex', int]):
        self.rgx = ""

        for regex in regexs:
            if isinstance(regex, int):
                self.rgx = self.back_references(regex).get()
            elif isinstance(regex, str):
                self.rgx += regex
            else:
                self.rgx += regex.get()

    def __str__(self):
        """Magic method to print."""
        return self.rgx

    def __eq__(self, other: Union[str, 'Regex']):
        """Operator = ."""
        return (self.rgx == other.rgx) if isinstance(other, Regex) else (self.rgx == other)

    def __iadd__(self, other: Union[str, 'Regex']):
        """Operator += ."""
        self.rgx += other.rgx if isinstance(other, Regex) else str(other)
        return self

    def __add__(self, regex: Union[str, 'Regex']):
        """Operator + ."""
        rgx = Regex()
        if isinstance(regex, Regex):
            rgx._set_regex(self.get() + regex.get())
        else:
            rgx._set_regex(self.rgx + regex)

        return rgx

    def get(self):
        """Return regex."""
        return self.rgx

    def quantifier(self, n: int = 0, m: int = 0, without_maximum: bool = False):
        """Quantify the regex."""
        rgx = self.rgx
        if n == 0 and m == 1:
            rgx += self.ZERO_OR_ONE
        elif n == 0 and without_maximum:
            rgx += self.ZERO_OR_MULTIPLE
        elif n == 1 and without_maximum:
            rgx += self.ONE_OR_MULTIPLE
        else:
            regex = str(n)
            if without_maximum:
                regex += ','
            elif not m <= n:
                regex += "," + str(m)
            rgx += "{" + regex + "}"

        return Regex(rgx)

    def back_references(self, group_n: int = 1):
        """Back reference to a group."""
        return Regex(self.rgx, "\{}".format(group_n))

    def _set_regex(self, regex: Union[str, 'Regex']):
        """Set regex value."""
        if isinstance(regex, Regex):
            self.rgx = regex.rgx
        else:
            self.rgx = str(regex)
