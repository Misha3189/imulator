import os
import re
import sys
import argparse
import shlex  # Для лучшего парсинга аргументов

def expand_env_vars(line):
    def replace_var(match):
        var = match.group(1)
        return os.environ.get(var, match.group(0))
    return re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)', replace_var, line)

def parse_command(line):
    line = expand_env_vars(line.strip())
    if not line:
        return []
    return shlex.split(line)  # Поддержка пробелов в аргументах

def process_command(cmd_parts, is_interactive=True):
    if not cmd_parts:
        return
    command = cmd_parts[0]
    args = cmd_parts[1:]
    output = []
    if command == 'exit':
        sys.exit(0)
    elif command == 'ls':
        if args:
            output.append(f"Stub: ls {' '.join(args)}")
        else:
            output.append("Stub: ls")
    elif command == 'cd':
        if args:
            output.append(f"Stub: cd {' '.join(args)}")
        else:
            output.append("Error: cd requires a directory path")
    else:
        output.append(f"Error: unknown command '{command}'")
    for out in output:
        print(out)
    return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description="VFS Emulator")
    parser.add_argument('--vfs-path', default='.', help="Path to VFS ZIP")
    parser.add_argument('--script', default=None, help="Path to startup script")
    args = parser.parse_args()
    print(f"Debug params: vfs_path={args.vfs_path}, script={args.script}")

    if args.script:
        try:
            with open(args.script, 'r') as f:
                for raw_line in f:
                    line = raw_line.rstrip()
                    if line.startswith('#') or not line:
                        continue
                    print(f"$ {line}")
                    cmd_parts = parse_command(line)
                    process_command(cmd_parts, is_interactive=False)
        except FileNotFoundError:
            print(f"Error: Script file '{args.script}' not found")
        except Exception as e:
            print(f"Error during script execution: {e}")
    else:
        # Interactive REPL
        while True:
            try:
                line = input("vfs> ").strip()
                cmd_parts = parse_command(line)
                process_command(cmd_parts)
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\nExiting...")
                break

if __name__ == '__main__':
    main()