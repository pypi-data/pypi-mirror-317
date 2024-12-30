# pylint: disable=consider-using-f-string
"""Data model for an extracted Chapter."""

from dataclasses import dataclass, field


@dataclass(repr=False)
class Chapter:
    """A Chapter model class."""

    title: str = field(default="")
    content: str = field(default="")
    filename: str = field(default="")

    def __repr__(self):
        """For debugging output."""
        return "{}(filename='{}', title='{}', content='{}')".format(
            self.__class__.__name__,
            self.filename,
            self.title[:8],
            self.content[:5].strip(),
        )

    def __str__(self):
        """For string representation."""
        if self.title and self.content:
            return "{}\n\n{}".format(self.title, self.content)

        if self.title:
            return self.title

        if self.content:
            return self.content

        return ""
