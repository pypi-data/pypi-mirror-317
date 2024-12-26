"""Module for the terminal-based graphics engine."""

import os


# Without this, the character escape sequences don't work on Windows.
os.system("")


class Display:
    """Base class for the display engine."""

    def __init__(self, num_columns, num_rows) -> None:
        self.cursor_pos = (0, 0)
        self.num_columns = num_columns
        self.num_rows = num_rows
        self._write = print
        top_row = f"┌{'─' * num_columns}┐\n"
        mid_row = f"│{' ' * num_columns}│\n"
        end_row = f"└{'─' * num_columns}┘"
        self._write(top_row + mid_row * num_rows + end_row, end="", flush=True)

    def write_string(self, text: str = "", pos: tuple[int, int] = None) -> None:
        """Writes the string to the console."""
        if pos is None:
            row, col = self.cursor_pos
        else:
            col, row = pos
        # To prevent overwriting text outside of the display window
        row = min(row, self.num_rows - 1)
        # Use the 'previous line' character as many times as it takes to get to the given line
        prev_line = "\033[F" * (self.num_rows - row)
        # Flush the line feed enough times for the whole output to be displayed
        next_line = "\n" * (self.num_rows - row - 1)

        # Use special Unicode characters for manipulating the terminal window
        self._write(f"{prev_line}\033[{col + 2}G{text}{next_line}")
        # This implementation does not care if the length of the text exceeds the number of columns
        col += len(text)
        self.cursor_pos = row, col

    def home(self) -> None:
        """Reset the cursor position to line 0, column 0."""
        self.cursor_pos = (0, 0)

    def clear(self) -> None:
        """Clears the display."""
        self.home()
        for row in range(self.num_rows):
            self.write_string(" " * self.num_columns, (0, row))
        self.home()

    def close(self, clear: bool = False) -> None:
        """Flushes the output stream."""
        if clear:
            self.clear()

        # Flush the line feed
        self._write()
