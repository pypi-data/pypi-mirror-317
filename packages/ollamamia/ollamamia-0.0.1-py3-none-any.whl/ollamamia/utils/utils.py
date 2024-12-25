import sys
import readchar
import termcolor
import platform


def exiting_ollamamia():
    print("\nexiting ollamamia...")
    # need to stop


def input_with_placeholder(prefix=">>> ", placeholder="send your message "):
    try:
        # Try the interactive character-by-character input first
        print('\n\n' + prefix, end='', flush=True)

        input_text = []

        # Print the placeholder in gray
        print(termcolor.colored(placeholder, 'grey'), end='', flush=True)
        sys.stdout.write(f"\r{prefix}")
        sys.stdout.flush()

        while True:
            try:
                # Try to read a character
                char = readchar.readchar()
            except Exception:
                # Fallback to standard input if character reading fails
                return input()

            # Handle special keys
            if char in ['\r', '\n']:  # Enter key
                # If no input, keep placeholder
                if not input_text:
                    continue
                break

            elif char in ['\x7f', '\b']:  # Backspace
                if input_text:
                    input_text.pop()

            elif char == '\x03':  # Ctrl+C
                raise KeyboardInterrupt

            else:
                input_text.append(char)

            # Clear the line
            sys.stdout.write('\r>>> ' + ' ' * 80 + '\r>>> ')

            # If input exists, print the current input
            if input_text:
                sys.stdout.write(''.join(input_text))
            else:
                # If no input, show placeholder again
                sys.stdout.write(termcolor.colored(placeholder, 'grey'))

            sys.stdout.flush()

        print('\n')
        return ''.join(input_text)

    except Exception:
        # Complete fallback to standard input if anything goes wrong
        return input()