import cmd

from ctl.constants import GENERAL_ERROR_CODE
from ctl.error import CLIError
from ctl.terminal import cli  # 从另一个文件导入 cli


class SkyCtlCmd(cmd.Cmd):
    intro = "Welcome to SkyCtl CLI. Type 'help' or '?' for commands."
    prompt = "(skyctl) "

    def do_command(self, line):
        """Execute a CLI command."""
        try:
            cli.main(args=line.split())  # 调用 cli 的 main 方法
        except CLIError as e:
            e.show()
        except Exception as e:
            cli_error = CLIError(str(e), GENERAL_ERROR_CODE)
            cli_error.show()

    def do_exit(self, line):
        """Exit the CLI."""
        print("Goodbye!")
        return True


if __name__ == '__main__':
    SkyCtlCmd().cmdloop()
