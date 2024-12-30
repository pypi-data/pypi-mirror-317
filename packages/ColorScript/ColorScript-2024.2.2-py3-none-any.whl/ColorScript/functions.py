"""





This is the function section of the ColorScript module.








"""



from time import sleep


class text:
    """
    This is the main class for text.\n
    text(self) prints with predetermined formatting.
    """
    def __init__(self, message):
        self.message = message
        print(self.message)

    def reset() -> None:
        """
        This function is used to reset the text formatting.\n
        This is in octal function
        :return:
        """
        print('\033[0;0m')

    def plain(self):
        """
        This function prints plain text. \n
        This is an octal function

        :return:
        """
        print('\033[0;0m' + str(self))

    def red(self):
        """
        This function prints red text.
        This is an octal function
        :return:
        """
        print('\033[31m' + str(self))

    def green(self):
        """
        This function prints green text.
        :return:
        """
        print('\033[32m' + str(self))

    def yellow(self):
        """
        This function prints yellow text.
        :return:
        """

        print('\033[33m' + str(self))

    def blue(self):
        """
        This function prints blue text.
        :return:
        """
        print('\033[34m' + str(self))

    def purple(self):
        """
        This function prints purple text.
        :return:
        """
        print('\033[35m' + str(self))

    def cyan(self):
        """
        This function prints cyan text.
        :return:
        """
        print('\033[36m' + str(self))

    def white(self):
        """
        This function prints white text.
        :return:
        """
        print('\033[38m' + str(self))

    def black(self):
        """
        This function prints black text.
        :return:
        """
        print('\033[30m' + str(self))

    def custom_octal(self, code):
        """
        This function allows you to print a custom octal escape code."""
        print(f"\033[{code}m" + str(self))

    def bold(self):
        """
        This function prints bold text.
        :return:
        """
        print('\033[1m' + str(self))

    def underline(self):
        """
        This function prints underlined text.
        :return:
        """
        print('\033[4m' + str(self))

    def italic(self):
        """
        This function prints italic text.
        :return:
        """
        print('\033[3m' + str(self))

    def strikethrough(self):
        """
        This function prints strikethrough text.
        :return:
        """
        print('\033[9m' + str(self))

    def orange(self: str):
        """
        This function prints orange text.
        :return:
        """
        print('\033[38;5;202m' + str(self))

    # Functions for each HTML color (RGB)
    def AliceBlue(self: str):
        """
        This function prints the rgb color of AliceBlue.
        :return:"""
        print('\033[38;5;153m' + str(self))

    def AntiqueWhite(self: str):
        """
        This function prints the rgb color of AntiqueWhite.
        :return:
        """
        print('\033[38;5;127m' + str(self))

    def Aqua(self: str):
        """
        This function prints the rgb color of Aqua.
        :return:
        """
        print('\033[38;5;51m' + str(self))

    def Aquamarine(self: str):
        """
        This function prints the rgb color of Aquamarine.
        :return:
        """
        print('\033[38;5;79m' + str(self))

    def Azure(self: str):
        """
        This function prints the rgb color of Azure.
        :return:
        """
        print('\033[38;5;159m' + str(self))

    def Beige(self: str):
        """
        This function prints the rgb color of Beige.
        :return:
        """
        print('\033[38;5;230m' + str(self))

    def Bisque(self: str):
        print('\033[38;5;223m' + str(self))

    def Black(self: str):
        print('\033[38;5;0m' + str(self))

    def BlanchedAlmond(self: str):
        print('\033[38;5;214m' + str(self))

    def Blue(self: str):
        print('\033[38;5;32m' + str(self))

    def BlueViolet(self: str):
        print('\033[38;5;57m' + str(self))

    def Brown(self: str):
        print('\033[38;5;94m' + str(self))

    def BurlyWood(self: str):
        print('\033[38;5;127m' + str(self))

    def CadetBlue(self: str):
        print('\033[38;5;61m' + str(self))

    def Chartreuse(self: str):
        print('\033[38;5;118m' + str(self))

    def Chocolate(self: str):
        print('\033[38;5;94m' + str(self))

    def Coral(self: str):
        print('\033[38;5;214m' + str(self))

    def CornflowerBlue(self: str):
        print('\033[38;5;32m' + str(self))

    def Cornsilk(self: str):
        print('\033[38;5;229m' + str(self))

    def Crimson(self: str):
        print('\033[38;5;196m' + str(self))

    def Cyan(self: str):
        print('\033[38;5;51m' + str(self))

    def DarkBlue(self: str):
        print('\033[38;5;19m' + str(self))

    def DarkCyan(self: str):
        print('\033[38;5;36m' + str(self))

    def DarkGoldenrod(self: str):
        print('\033[38;5;136m' + str(self))

    def DarkGray(self: str):
        print('\033[38;5;239m' + str(self))

    def DarkGreen(self: str):
        print('\033[38;5;22m' + str(self))

    def DarkKhaki(self: str):
        print('\033[38;5;143m' + str(self))

    def DarkMagenta(self: str):
        print('\033[38;5;91m' + str(self))

    def DarkOliveGreen(self: str):
        print('\033[38;5;100m' + str(self))

    def DarkOrange(self: str):
        print('\033[38;5;202m' + str(self))

    def DarkOrchid(self: str):
        print('\033[38;5;92m' + str(self))

    def DarkRed(self: str):
        print('\033[38;5;88m' + str(self))

    def DarkSalmon(self: str):
        print('\033[38;5;217m' + str(self))

    def DarkSeaGreen(self: str):
        print('\033[38;5;143m' + str(self))

    def DarkSlateBlue(self: str):
        print('\033[38;5;61m' + str(self))

    def DarkSlateGray(self: str):
        print('\033[38;5;23m' + str(self))

    def DarkTurquoise(self: str):
        print('\033[38;5;44m' + str(self))

    def DarkViolet(self: str):
        print('\033[38;5;90m' + str(self))

    def DeepPink(self: str):
        print('\033[38;5;198m' + str(self))

    def DeepSkyBlue(self: str):
        print('\033[38;5;63m' + str(self))

    def DimGray(self: str):
        print('\033[38;5;239m' + str(self))

    def DodgerBlue(self: str):
        print('\033[38;5;33m' + str(self))

    def Firebrick(self: str):
        print('\033[38;5;88m' + str(self))

    def FloralWhite(self: str):
        print('\033[38;5;255m' + str(self))

    def ForestGreen(self: str):
        print('\033[38;5;34m' + str(self))

    def Fuchsia(self: str):
        print('\033[38;5;13m' + str(self))

    def Gainsboro(self: str):
        print('\033[38;5;253m' + str(self))

    def GhostWhite(self: str):
        print('\033[38;5;15m' + str(self))

    def Gold(self: str):
        print('\033[38;5;220m' + str(self))

    def Goldenrod(self: str):
        print('\033[38;5;136m' + str(self))

    def Gray(self: str):
        print('\033[38;5;243m' + str(self))

    def Green(self: str):
        print('\033[38;5;28m' + str(self))

    def GreenYellow(self: str):
        print('\033[38;5;118m' + str(self))

    def Honeydew(self: str):
        print('\033[38;5;157m' + str(self))

    def HotPink(self: str):
        print('\033[38;5;198m' + str(self))

    def IndianRed(self: str):
        print('\033[38;5;167m' + str(self))

    def Indigo(self: str):
        print('\033[38;5;54m' + str(self))

    def Ivory(self: str):
        print('\033[38;5;255m' + str(self))

    def Khaki(self: str):
        print('\033[38;5;180m' + str(self))

    def Lavender(self: str):
        print('\033[38;5;159m' + str(self))

    def LavenderBlush(self: str):
        print('\033[38;5;219m' + str(self))

    def LawnGreen(self: str):
        print('\033[38;5;118m' + str(self))

    def LemonChiffon(self: str):
        print('\033[38;5;227m' + str(self))

    def LightBlue(self: str):
        print('\033[38;5;153m' + str(self))

    def LightCoral(self: str):
        print('\033[38;5;217m' + str(self))

    def LightCyan(self: str):
        print('\033[38;5;159m' + str(self))

    def LightGoldenrodYellow(self: str):
        print('\033[38;5;227m' + str(self))

    def LightGray(self: str):
        print('\033[38;5;250m' + str(self))

    def LightGreen(self: str):
        print('\033[38;5;120m' + str(self))

    def LightPink(self: str):
        print('\033[38;5;218m' + str(self))

    def LightSalmon(self: str):
        print('\033[38;5;214m' + str(self))

    def LightSeaGreen(self: str):
        print('\033[38;5;42m' + str(self))

    def LightSkyBlue(self: str):
        print('\033[38;5;117m' + str(self))

    def LightSlateGray(self: str):
        print('\033[38;5;145m' + str(self))

    def LightSteelBlue(self: str):
        print('\033[38;5;145m' + str(self))

    def LightYellow(self: str):
        print('\033[38;5;228m' + str(self))

    def Lime(self: str):
        print('\033[38;5;10m' + str(self))

    def LimeGreen(self: str):
        print('\033[38;5;48m' + str(self))

    def Linen(self: str):
        print('\033[38;5;230m' + str(self))

    def Magenta(self: str):
        print('\033[38;5;13m' + str(self))

    def Maroon(self: str):
        print('\033[38;5;88m' + str(self))

    def MediumAquaMarine(self: str):
        print('\033[38;5;79m' + str(self))

    def CustomRGB(red: int, green: int, blue: int, string: str):
        print(f'\033[{red};{green};{blue}m' + string)


class pause:
    def __init__(self, duration: float | None = None):
        self.duration = duration
        sleep(self.duration / 1000)  # Pause for the given milliseconds

    def secs(seconds: float | None = None):
        sleep(seconds)  # Pause for the given seconds

    def mins(minutes: float | None = None):
        sleep(minutes * 60)  # Pause for the given minutes