"""Highlighting utilities for the tutorial."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum, auto
from re import Pattern
from typing import NamedTuple

from rich.style import Style


class FocusType(Enum):
    """Types of focus patterns."""

    LITERAL = auto()
    REGEX = auto()
    LINE = auto()
    RANGE = auto()
    STARTSWITH = auto()
    BETWEEN = auto()


@dataclass
class Focus:
    """A pattern to focus on with its style."""

    pattern: str | Pattern | tuple[int, int] | int | tuple[str, bool] | _BetweenTuple
    style: Style = Style(color="yellow", bold=True)  # noqa: RUF009
    type: FocusType = FocusType.LITERAL

    @classmethod
    def literal(
        cls,
        text: str,
        style: Style = Style(color="yellow", bold=True),  # noqa: B008
        *,
        word_boundary: bool = False,
    ) -> Focus:
        """Create a focus for a literal string.

        Parameters
        ----------
        text
            The text to match
        style
            The style to apply to the matched text
        word_boundary
            If True, only match the text when it appears as a word

        """
        if word_boundary:
            pattern = re.compile(rf"\b{re.escape(text)}\b")
            return cls(pattern, style, FocusType.REGEX)
        return cls(text, style, FocusType.LITERAL)

    @classmethod
    def regex(
        cls,
        pattern: str | Pattern,
        style: Style = Style(color="green", bold=True),  # noqa: B008
    ) -> Focus:
        """Create a focus for a regular expression."""
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        return cls(pattern, style, FocusType.REGEX)

    @classmethod
    def line(
        cls,
        line_number: int,
        style: Style = Style(color="cyan", bold=True),  # noqa: B008
    ) -> Focus:
        """Create a focus for a line number."""
        return cls(line_number, style, FocusType.LINE)

    @classmethod
    def range(
        cls,
        start: int,
        end: int,
        style: Style = Style(color="magenta", bold=True),  # noqa: B008
    ) -> Focus:
        """Create a focus for a range of characters."""
        return cls(_RangeTuple(start, end), style, FocusType.RANGE)

    @classmethod
    def startswith(
        cls,
        text: str,
        style: Style = Style(color="blue", bold=True),  # noqa: B008
        *,
        from_start_of_line: bool = False,
    ) -> Focus:
        """Create a focus for text that starts with the given pattern.

        Parameters
        ----------
        text
            The text to match at the start
        style
            The style to apply to the matched text
        from_start_of_line
            If True, only match at the start of lines, if False match anywhere

        """
        return cls(_StartsWithTuple(text, from_start_of_line), style, FocusType.STARTSWITH)

    @classmethod
    def between(
        cls,
        start_pattern: str,
        end_pattern: str,
        style: Style = Style(color="blue", bold=True),  # noqa: B008
        *,
        inclusive: bool = True,
        multiline: bool = True,
        match_index: int | None = None,  # Add this parameter
        greedy: bool = False,  # Add this parameter
    ) -> Focus:
        """Create a focus for text between two patterns.

        Parameters
        ----------
        start_pattern
            The pattern marking the start of the region
        end_pattern
            The pattern marking the end of the region
        style
            The style to apply to the matched text
        inclusive
            If True, include the start and end patterns in the highlighting
        multiline
            If True, match across multiple lines
        match_index
            If provided, only highlight the nth match (0-based).
            If None, highlight all matches.
        greedy
            If True, use greedy matching (matches longest possible string).
            If False, use non-greedy matching (matches shortest possible string).

        """
        return cls(
            _BetweenTuple(start_pattern, end_pattern, inclusive, multiline, match_index, greedy),
            style,
            FocusType.BETWEEN,
        )


class _BetweenTuple(NamedTuple):
    start_pattern: str
    end_pattern: str
    inclusive: bool
    multiline: bool
    match_index: int | None
    greedy: bool


class _StartsWithTuple(NamedTuple):
    text: str
    from_start_of_line: bool


class _RangeTuple(NamedTuple):
    start: int
    end: int
