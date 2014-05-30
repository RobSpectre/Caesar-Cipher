import unittest

from caesarcipher import CaesarCipher


class CaesarCipherEncodeTest(unittest.TestCase):
    def test_encode_with_known_offset(self):
        message = "Twilio"
        test_cipher = CaesarCipher(message, encode=True, offset=1)
        self.assertEquals(test_cipher.encoded, "Uxjmjp")

    def test_encode_long_phrase_with_known_offset(self):
        message = "The quick brown fox jumps over the lazy dog."
        test_cipher = CaesarCipher(message, encode=True, offset=7)
        self.assertEquals(test_cipher.encoded,
                          "Aol xbpjr iyvdu mve qbtwz vcly aol shgf kvn.")

    def test_encode_with_mirror_offset(self):
        message = "The quick brown fox jumps over the lazy dog."
        test_cipher = CaesarCipher(message, encode=True, offset=26)
        self.assertEquals(test_cipher.encoded,
                          "The quick brown fox jumps over the lazy dog.")

    def test_encode_with_offset_greater_than_alphabet_length(self):
        message = "The quick brown fox jumps over the lazy dog."
        test_cipher = CaesarCipher(message, encode=True, offset=28)
        self.assertEquals(test_cipher.encoded,
                          "Vjg swkem dtqyp hqz lworu qxgt vjg ncba fqi.")

    def test_encode_with_very_large_offset(self):
        message = "The quick brown fox jumps over the lazy dog."
        test_cipher = CaesarCipher(message, encode=True, offset=10008)
        self.assertEquals(test_cipher.encoded,
                          "Rfc osgai zpmul dmv hsknq mtcp rfc jyxw bme.")

    def test_encode_decode_consistent(self):
        message = "The quick brown fox jumps over the lazy dog."
        setup_cipher = CaesarCipher(message, encode=True, offset=14)
        encoded_message = setup_cipher.encoded
        test_cipher = CaesarCipher(encoded_message, decode=True, offset=14)
        self.assertEquals(message, test_cipher.decoded)


class CaesarCipherDecodeTest(unittest.TestCase):
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
        self.assertEquals(message, test_cipher.decoded)


class CaesarCipherRegressionTest(unittest.TestCase):
    def test_all_offsets(self):
        message = "The quick brown fox jumps over the lazy dog."
        for i in range(0, 100):
            test_cipher = CaesarCipher(message, encode=True, offset=i)
            test_cipher.encoded
            self.assertEquals(message, test_cipher.decoded)
