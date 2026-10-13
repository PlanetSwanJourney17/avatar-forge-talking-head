"""Typer CLI entry point for avatar-forge-talking-head."""

from __future__ import annotations

import logging
from pathlib import Path

import typer
from rich.console import Console

from avatar_forge.bootstrap.container import build_container
from avatar_forge.handlers.render_handler import RenderHandler
from avatar_forge.handlers.rig_handler import RigHandler
from avatar_forge.handlers.doctor_handler import DoctorHandler

app = typer.Typer(help="AI avatar / talking-head generator", no_args_is_help=True)
console = Console()
log = logging.getLogger("avatar_forge.cli")


def _configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


@app.command()
def render(
    face: Path = typer.Option(..., "--face", exists=True, dir_okay=False, help="Input face image"),
    audio: Path = typer.Option(..., "--audio", exists=True, dir_okay=False, help="Input audio"),
    out: Path = typer.Option(Path("output/avatar.mp4"), "--out", help="Output video path"),
    rig: str = typer.Option("default", "--rig", help="Rig profile name"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Generate a talking-head video from a face image and an audio track."""
    _configure_logging(verbose)
    container = build_container()
    handler = RenderHandler(container)
    result = handler.handle(face=face, audio=audio, out=out, rig_name=rig)
    console.print(f"[green]rendered[/green] {result.frames} frames -> {result.output_path}")


@app.command()
def rig(
    face: Path = typer.Option(..., "--face", exists=True, dir_okay=False),
    out: Path = typer.Option(Path("output/rig.json"), "--out"),
) -> None:
    """Extract a face rig (landmarks + blendshape basis) from an image."""
    _configure_logging(False)
    handler = RigHandler(build_container())
    profile = handler.handle(face=face, out=out)
    console.print(f"[cyan]rig[/cyan] {profile.landmark_count} landmarks -> {out}")


@app.command()
def doctor() -> None:
    """Check runtime, adapters, and model weights."""
    _configure_logging(False)
    DoctorHandler(build_container()).handle(console=console)


def main() -> None:
    app()


if __name__ == "__main__":
    main()