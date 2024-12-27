import io
from typing import TYPE_CHECKING

import click
import pyautogui
from pynput.keyboard import Key, KeyCode, Listener
from rich.console import Console

if TYPE_CHECKING:
    from click import Context, HelpFormatter

running = False


class RichGroup(click.Command):
    def format_help(self, ctx: "Context", formatter: "HelpFormatter") -> None:
        click.Group.format_help(self, ctx, formatter)

        sio = io.StringIO()
        console = Console(file=sio, force_terminal=True)
        console.print("[italic][green]Valid values for key:")
        console.print("[green]" + ", ".join(c.name for c in Key))
        formatter.write(sio.getvalue())


@click.command(cls=RichGroup)
@click.option("-D", "--delay", type=click.FLOAT, default=1.0, help="Delay in seconds.")
@click.option("-K", "--key", default="page_up", help="Toggle key")
@click.option("-B", "--button", default="left", help="Mouse button (left|right)")
def main(delay: float, key: str, button: str) -> None:
    toogle_key = getattr(Key, key, KeyCode.from_char(key))
    button = {
        "left": pyautogui.LEFT,
        "right": pyautogui.RIGHT,
    }.get(button)

    def on_press(key_pressed: KeyCode | Key) -> None:
        global running, pause  # noqa: PLW0603, PLW0602
        if key_pressed == toogle_key:
            running = not running
            print(f"key {key} status {running}")  # noqa: T201

    lis = Listener(on_press=on_press)
    lis.start()

    while True:
        if running:
            pyautogui.click(pyautogui.position(), button=button)
            pyautogui.PAUSE = delay
    lis.stop()
