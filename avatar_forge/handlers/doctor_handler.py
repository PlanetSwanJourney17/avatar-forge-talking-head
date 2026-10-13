"""Doctor handler: report runtime + adapter + weight status."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rich.console import Console
    from avatar_forge.bootstrap.container import Container


class DoctorHandler:
    def __init__(self, container: "Container") -> None:
        self._c = container

    def handle(self, *, console: "Console") -> None:
        console.print(f"python      : {self._c.settings.python_version}")
        console.print(f"cuda        : {self._c.cuda.describe()}")
        console.print(f"ffmpeg      : {self._c.ffmpeg.describe()}")
        console.print(f"weights     : {self._c.models.describe()}")
        missing = self._c.models.missing_weights()
        if missing:
            console.print(f"[yellow]missing weights:[/yellow] {', '.join(missing)}")
        else:
            console.print("[green]all weights present[/green]")