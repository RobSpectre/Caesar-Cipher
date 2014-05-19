import unittest

from caesarcipher import CaesarCipher
from caesarcipher import CaesarCipherError


class CaesarCipherTest(unittest.TestCase):
    def test_encode_with_known_offset(self):
        message = "Twilio"
        test_cipher = CaesarCipher(message, encode=True, offset=1)
        self.assertEquals(test_cipher.encoded, "UXJMJP")

    def test_encode_long_phrase_with_known_offset(self):
        message = "The quick brown fox jumps over the lazy dog."
        test_cipher = CaesarCipher(message, encode=True, offset=7)
        self.assertEquals(test_cipher.encoded,
                          "AOL XBPJR IYVDU MVE QBTWZ VCLY AOL SHGF KVN.")

    def test_encode_with_mirror_offset(self):
        message = "The quick brown fox jumps over the lazy dog."
        test_cipher = CaesarCipher(message, encode=True, offset=26)
        self.assertEquals(test_cipher.encoded,
                          "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.")

    def test_encode_with_offset_greater_than_alphabet_length(self):
        message = "The quick brown fox jumps over the lazy dog."
        test_cipher = CaesarCipher(message, encode=True, offset=28)
        self.assertEquals(test_cipher.encoded,
                          "VJG SWKEM DTQYP HQZ LWORU QXGT VJG NCBA FQI.")

    def test_encode_with_very_large_offset(self):
        message = "The quick brown fox jumps over the lazy dog."
        test_cipher = CaesarCipher(message, encode=True, offset=10008)
        self.assertEquals(test_cipher.encoded,
                          "RFC OSGAI ZPMUL DMV HSKNQ MTCP RFC JYXW BME.")

    def test_encode_decode_consistent(self):
        message = "The quick brown fox jumps over the lazy dog."
        setup_cipher = CaesarCipher(message, encode=True, offset=14)
        encoded_message = setup_cipher.encoded
        test_cipher = CaesarCipher(encoded_message, decode=True, offset=14)
        self.assertEquals(message.upper(), test_cipher.decoded)

    def test_decode_with_known_offset(self):
        message = "UXJMJP"
        test_cipher = CaesarCipher(message, encode=True, offset=1)
        self.assertEquals(test_cipher.decoded, "TWILIO")

    def test_decode_long_phrase_with_known_offset(self):
        message = "AOL XBPJR IYVDU MVE QBTWZ VCLY AOL SHGF KVN."
        test_cipher = CaesarCipher(message, decode=True, offset=7)
        self.assertEquals(test_cipher.decoded,
                          "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.")

    def test_decode_with_offset_greater_than_alphabet_length(self):
        message = "VJG SWKEM DTQYP HQZ LWORU QXGT VJG NCBA FQI."
        test_cipher = CaesarCipher(message, decode=True, offset=28)
        self.assertEquals(test_cipher.decoded,
                          "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.")

    def test_decode_with_very_large_offset(self):
        message = "RFC OSGAI ZPMUL DMV HSKNQ MTCP RFC JYXW BME."
        test_cipher = CaesarCipher(message, decode=True, offset=10008)
        self.assertEquals(test_cipher.decoded,
                          "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG.")

    def test_encode_decode_persistence(self):
        message = "The quick brown fox jumps over the lazy dog."
        test_cipher = CaesarCipher(message, encode=True, offset=14)
        test_cipher.encoded
        self.assertEquals(message.upper(), test_cipher.decoded)
