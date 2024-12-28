import cmd
from ctl.terminal import cli  # 从另一个文件导入 cli


class SkyCtlCmd(cmd.Cmd):
    intro = "Welcome to SkyCtl CLI. Type 'help' or '?' for commands."
    prompt = "(skyctl) "

    def do_command(self, line):
        """Execute a CLI command."""
        try:
            cli.main(args=line.split())  # 调用 cli 的 main 方法
        except Exception as e:
            print(f"Error: {e}")

    def do_exit(self, line):
        """Exit the CLI."""
        print("Goodbye!")
        return True


if __name__ == '__main__':
    SkyCtlCmd().cmdloop()
