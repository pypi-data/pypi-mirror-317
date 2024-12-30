import cmd
import sys

from ctl.constants import GENERAL_ERROR_CODE
from ctl.error import CLIError
from ctl.terminal import cli  # 从另一个文件导入 cli


class SkyCtlCmd(cmd.Cmd):
    intro = "Welcome to SkyCtl CLI. Type 'help' or '?' for commands."
    prompt = "(skyctl) "

    def do_command(self, line):
        """Execute a CLI command."""
        try:
            cli.main(args=line.split(),standalone_mode=False)  # 调用 cli 的 main 方法
        except CLIError as ex:
            ex.show()
        except Exception as ex:
            err = CLIError(str(ex), GENERAL_ERROR_CODE)
            err.show()

    def do_exit(self, line):
        """Exit the CLI."""
        print("Goodbye!")
        return True


if __name__ == '__main__':
    try:
        SkyCtlCmd().cmdloop()
    except CLIError as e:
        e.show()
    except Exception as e:
        cli_error = CLIError(str(e), GENERAL_ERROR_CODE)
        cli_error.show()
