class PolishUtfToAscii:
    @staticmethod
    def translate(text):
        table = {
            ord(u'ó'): u'o',
            ord(u'ę'): u'e',
            ord(u'ą'): u'a',
            ord(u'ś'): u's',
            ord(u'ł'): u'l',
            ord(u'ż'): u'z',
            ord(u'ź'): u'z',
            ord(u'ć'): u'c',
            ord(u'ń'): u'n',
            ord(u'ń'): u'n',
            0x2013: u'-',
            0xbd: u'1/2',
        }
        return text.translate(table)
