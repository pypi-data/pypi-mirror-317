import cmd
import sys

from ctl.constants import GENERAL_ERROR_CODE
from ctl.error import CLIError
from ctl.terminal import cli  # 从另一个文件导入 cli
import logging
import ctl.logging_config

logger = logging.getLogger(__name__)


class SkyCtlCmd(cmd.Cmd):
    intro = "Welcome to SkyCtl CLI. Type 'help' or '?' for commands."
    prompt = "(skyctl) "

    def do_command(self, line):
        """Execute a CLI command."""
        try:
            cli.main(args=line.split(), standalone_mode=False)
            logger.info("Command executed successfully.")
        except CLIError as e:
            e.show()
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            cli_error = CLIError(str(e), GENERAL_ERROR_CODE)
            cli_error.show()

    def do_exit(self, line):
        """Exit the CLI."""
        print("Goodbye!")
        return True


if __name__ == '__main__':
    try:
        logger.info("Starting SkyCtl CLI...")
        SkyCtlCmd().cmdloop()
    except CLIError as e:
        e.show()
    except Exception as e:
        logger.error(f"An unexpected error occurred11: {e}")
        cli_error = CLIError(str(e), GENERAL_ERROR_CODE)
        cli_error.show()
