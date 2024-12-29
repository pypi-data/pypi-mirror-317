import math
import re
from typing import Callable

from ..types import BoxSize


class Paper:
    """A piece of paper from the ISO-206 A series"""

    def __init__(self, spec: str):
        """Create a sheet of paper

        :param spec: The name of a paper size from the ISO-206 A series
        """
        if not re.match(r'^[aA]\d+$', spec):
            raise ValueError(f"'{spec}' is not a valid ISO 216 A-series paper size")
        self.spec = spec
        self.series = spec[0]
        self.size = int(spec[1:])

    def dimensions(self) -> BoxSize:
        """Get the width and height of the paper size being represented

        :returns: The width and height in
        """
        size = 0
        area = 1e6  # A0 area in square mm
        while size < self.size:
            area /= 2
            size += 1

        width = math.sqrt(area / math.sqrt(2))
        height = width * math.sqrt(2)

        rounder: Callable[[float], int] = round if size == 0 else math.floor  # type: ignore
        return rounder(width), rounder(height)
