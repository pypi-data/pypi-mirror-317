from jupyter_server.auth import passwd


class ANSI:
    class codes:
        class octal:
            COLOURS = {
                # Text colours
                "PURPLE": "\033[35m",
                "BLUE": "\033[34m",
                "GREEN": "\033[32m",
                "RED": "\033[31m",
                "YELLOW": "\033[33m",
                "BLACK": "\033[30m",
                "CYAN": "\033[36m",
                "GREY": "\033[37m",
                "WHITE": "\033[38m",
                # Bright colours
                "BRIGHT-RED": "\u001b[91m",
                "BRIGHT-GREEN": "\u001b[92m",
                "BRIGHT-YELLOW": "\u001b[93m",
                "BRIGHT-BLUE": "\u001b[94m",
                "BRIGHT-PURPLE": "\u001b[95m",
                "BRIGHT-CYAN": "\u001b[96m",
                "BRIGHT-WHITE": "\u001b[97m",
                "BRIGHT-GREY": "\u001b[90m",
                # Background colours
                "RED-BACKGROUND": "\033[41m",
                "BLUE-BACKGROUND": "\033[44m",
                "GREEN-BACKGROUND": "\033[102m",
                "YELLOW-BACKGROUND": "\033[43m",
                "PURPLE-BACKGROUND": "\033[45m",
                "BLACK-BACKGROUND": "\033[40m",
                "PINK-BACKGROUND": "\033[45m",
                "CYAN-BACKGROUND": "\033[46m",
                "WHITE-BACKGROUND": "\033[8m",
                "GREY-BACKGROUND": "\033[47m",
                # Bright background colours
                "BRIGHT-RED-BACKGROUND": "\033[101m",
                "BRIGHT-GREEN-BACKGROUND": "\033[102m",
                "BRIGHT-YELLOW-BACKGROUND": "\033[103m",
                "BRIGHT-BLUE-BACKGROUND": "\033[104m",
                "BRIGHT-PURPLE-BACKGROUND": "\033[105m",
                "BRIGHT-GREY-BACKGROUND": "\033[100m",
                "BRIGHT-CYAN-BACKGROUND": "\033[106m",
                "BRIGHT-WHITE-BACKGROUND": "\033[107m",
            }
            FORMATS = {
                "BOLD": "\033[1m",
                "ITALIC": "\033[3m",
                "UNDERLINE": "\033[4m",
                "STRIKETHROUGH": "\033[9m",
                "BOXED": "\033[51m",
            }
        class rgb:
            pass
    class characters:
        CHARACTERS = [
        #     use a .csv file
        ]
for i in range(1000):
    print(f"\033[{i}m" + "test")
    print("\033[0m")
    i+=1
passwd()
print("\033[0m")
print(ANSI.codes.octal.FORMATS["DOUBLE-UNDERLINE"]+"help")