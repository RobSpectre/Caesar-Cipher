import argparse
import logging
from random import randrange
import string


class CaesarCipher(object):
    def __init__(self, message=None, encode=False, decode=False, offset=False):
        """
        A class that encodes and decodes strings using the Caesar shift cipher.
        
        Accepts messages in a string and encodes or decodes by shifting the
        value of the letter by an arbitrary integer and transforming to
        uppercase.

        http://en.wikipedia.org/wiki/Caesar_cipher

        Do not ever use this for real communication, but definitely use it for
        fun events like the Hacker Olympics.

        Attributes:
            message: The string you wish to encode.
            encode: A boolean indicating desire to encode the string, used as
                command line script flag.
            decoded: A boolean indicating desire to decode the string, used as
                command line script flag.
            offset: Integer by which you want to shift the value of a letter.
            alphabet: A tuple containing the ASCII alphabet in uppercase.
        """
        self.message = message
        self.encode = encode
        self.decode = decode
        self.offset = offset

        # Get ASCII alphabet in uppercase tuple.
        self.alphabet = tuple(string.ascii_uppercase)

    def cipher(self):
        """Applies the Caesar shift cipher.
        
        Based on the attributes of the object, applies the Caesar shift cipher
        to the message attribute.

        Required attributes:
            message
            offset

        Returns:
            String with cipher applied.
        """
        if self.offset is False:
            self.offset = randrange(5, 25)
            logging.info("Random offset selected: %i" % self.offset)

        logging.info("Encoding message: %s" % self.message)
        encoded_message_list = list(self.message.upper())
        for i, letter in enumerate(encoded_message_list):
            if letter.isupper():
                logging.debug("Encoding letter: %s" % letter)
                value = self.alphabet.index(letter)
                cipher_value = value + self.offset
                if cipher_value > 25 or cipher_value < 0:
                    cipher_value = cipher_value % 26
                logging.debug("Cipher value: %s" % cipher_value)
                encoded_message_list[i] = self.alphabet[cipher_value]
                logging.debug("Encoded letter: %s" % letter)
        self.message = ''.join(encoded_message_list)
        return self.message 

    @property
    def encoded(self):
        """Encodes message using Caesar shift cipher
        
        Returns:
            String encoded with cipher.
        """
        return self.cipher()

    @property
    def decoded(self):
        """Decodes message using Caesar shift cipher
        
        Inverse operation of encoding, applies negative offset to Caesar shift
        cipher.

        Returns:
            String decoded with cipher.
        """
        self.offset = self.offset * -1
        return self.cipher()


class CaesarCipherError(Exception):
    def __init__(self, message):
        logging.error(message)

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Parser configuration
parser = argparse.ArgumentParser(description="Caesar Cipher - encode and "
                                             "decode messages with an English"
                                             "alphabet offset.",
                                 epilog="Written by Rob Spectre for Hacker "
                                        "Olympics London.")
parser.add_argument('message',
                    help="Message to be encoded or decoded.")
parser.add_argument('-e', '--encode', action="store_true",
                    help="Encode this message.")
parser.add_argument('-d', '--decode', action="store_true",
                    help="Decode this message.")
parser.add_argument('-o', '--offset',
                    help="Integer offset to encode/decode message against.")

if __name__ == "__main__":
    caesar_cipher = CaesarCipher()
    parser.parse_args(namespace=caesar_cipher)
    if caesar_cipher.offset:
        caesar_cipher.offset = int(caesar_cipher.offset)
    if caesar_cipher.offset is False and caesar_cipher.decode is True:
        raise CaesarCipherError("Message cannot be decoded without "
                                    "selecting an offset.  Please try "
                                    "again with -o switch.")
    if caesar_cipher.encode is True and caesar_cipher.decode is True:
        raise CaesarCipherError("Please select to encode *or* decode message, "
                                "not both.")
    if caesar_cipher.encode is True:
        print "Encoded message: %s" % caesar_cipher.encoded
    if caesar_cipher.decode is True:
        print "Decoded message: %s" % caesar_cipher.decoded
