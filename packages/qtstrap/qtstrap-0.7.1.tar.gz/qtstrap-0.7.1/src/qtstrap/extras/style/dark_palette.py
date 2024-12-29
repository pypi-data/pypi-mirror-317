from qtstrap import *


darkPalette = QStyleFactory.create('fusion').standardPalette()


light = QColor('#525252')
mid = QColor('#414141')
dark = QColor('#313131')
accent = QColor('#ca3e47')


# base
darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
darkPalette.setColor(QPalette.WindowText, QColor(180, 180, 180))
darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
darkPalette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
darkPalette.setColor(QPalette.ToolTipText, QColor(180, 180, 180))
# darkPalette.setColor(QPalette.PlaceholderText, QColor(180, 180, 180))
darkPalette.setColor(QPalette.Text, QColor(180, 180, 180))

darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
darkPalette.setColor(QPalette.ButtonText, QColor(180, 180, 180))
darkPalette.setColor(QPalette.BrightText, QColor(180, 180, 180))

darkPalette.setColor(QPalette.Light, QColor(180, 180, 180))
darkPalette.setColor(QPalette.Midlight, QColor(90, 90, 90))
darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
# darkPalette.setColor(QPalette.Mid, QColor(35, 35, 35))
darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))

darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
darkPalette.setColor(QPalette.HighlightedText, QColor(180, 180, 180))

darkPalette.setColor(QPalette.Link, QColor(56, 252, 196))
# darkPalette.setColor(QPalette.LinkVisited, QColor(56, 252, 196))

# disabled
darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))


def install_dark_palette(app):
    app.setStyle('Fusion')
    app.setPalette(darkPalette)
    OPTIONS.theme = 'dark'
