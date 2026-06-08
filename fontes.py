import pyfiglet


for font in pyfiglet.FigletFont.getFonts():
    print(font)
    print(pyfiglet.figlet_format(font, font=font))