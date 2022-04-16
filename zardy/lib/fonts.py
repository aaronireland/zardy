from pyfiglet import Figlet, FontNotFound


def _render(text: str, font: str) -> str:
    '''
    Converts the string given into the specifed font

    Parameters
    ----------
    text : str
        A string to convert into ASCII font
    font : str
        A valid Figlet ASCII font name (e.x. 'slant')

    Returns
    -------
    The rendered text or a simulated tag showing the attempted invalid font:
        <font="imnotafont(invalid)">Example!!</font>
    '''
    try:
        f = Figlet(font=font)
    except FontNotFound:
        return f"<font=\"{font}(invalid)\">{text}</font>"

    return r"{}".format(f.renderText(text))


def doh(text: str) -> str:
    '''
            dddddddd
            d::::::d                hhhhhhh
            d::::::d                h:::::h
            d::::::d                h:::::h
            d:::::d                 h:::::h
    ddddddddd:::::d    ooooooooooo   h::::h hhhhh
  dd::::::::::::::d  oo:::::::::::oo h::::hh:::::hhh
 d::::::::::::::::d o:::::::::::::::oh::::::::::::::hh
d:::::::ddddd:::::d o:::::ooooo:::::oh:::::::hhh::::::h
d::::::d    d:::::d o::::o     o::::oh::::::h   h::::::h
d:::::d     d:::::d o::::o     o::::oh:::::h     h:::::h
d:::::d     d:::::d o::::o     o::::oh:::::h     h:::::h
d:::::d     d:::::d o::::o     o::::oh:::::h     h:::::h
d::::::ddddd::::::ddo:::::ooooo:::::oh:::::h     h:::::h
 d:::::::::::::::::do:::::::::::::::oh:::::h     h:::::h
  d:::::::::ddd::::d oo:::::::::::oo h:::::h     h:::::h
   ddddddddd   ddddd   ooooooooooo   hhhhhhh     hhhhhhh
    '''
    return _render(text,'doh')


def digital(text: str) -> str:
    '''
    +-+-+-+-+-+-+-+
    |d|i|g|i|t|a|l|
    +-+-+-+-+-+-+-+
    '''
    return _render(text, 'digital')


def doom(text: str) -> str:
    r'''
         _
        | |
      __| | ___   ___  _ __ ___
     / _` |/ _ \ / _ \| '_ ` _ \
    | (_| | (_) | (_) | | | | | |
     \__,_|\___/ \___/|_| |_| |_|
    '''
    return _render(text, 'doom')

def three_d(text: str) -> str:
    '''
      ****             **
     */// *           /**
    /    /*           /**
       ***  *****  ******
      /// */////  **///**
     *   /*      /**  /**
    / ****       //******
     ////         //////
    '''
    return _render(text, '3-d')
