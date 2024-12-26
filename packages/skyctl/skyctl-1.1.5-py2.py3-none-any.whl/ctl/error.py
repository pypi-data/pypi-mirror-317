import sys

import click


class CLIError(click.ClickException):
    def __init__(self, message, code, resolution=None):
        super().__init__(message)
        self.code = code
        self.resolution = resolution

    def show(self, file=None):
        if file is None:
            file = sys.stderr
        click.secho(f"Error [{self.code}]: {self.message}", fg="red", file=file)
        if self.resolution:
            click.secho(f"Suggested resolution: {self.resolution}", fg="yellow", file=file)

