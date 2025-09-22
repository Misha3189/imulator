import os
import re
import sys

def expand_env_vars(line):
    def replace_var(match):
        var = match.group(1)
        return os.environ.get(var, match.group(0))
    return re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)', replace_var, line)

def parse_command(line):
    line = expand_env_vars(line.strip())
    if not line:
        return []
    # Простой сплит для базового парсинга (без кавычек)
    return line.split()

def main():
    while True:
        try:
            line = input("vfs> ").strip()
            cmd_parts = parse_command(line)
            if not cmd_parts:
                continue
            command = cmd_parts[0]
            args = cmd_parts[1:]
            if command == 'exit':
                sys.exit(0)
            elif command == 'ls':
                if args:
                    print(f"Stub: ls {' '.join(args)}")
                else:
                    print("Stub: ls")
            elif command == 'cd':
                if args:
                    print(f"Stub: cd {' '.join(args)}")
                else:
                    print("Error: cd requires a directory path")
            else:
                print(f"Error: unknown command '{command}'")
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == '__main__':
    main()