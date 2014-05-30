import argparse
import logging
from random import randrange
import string
import math


class CaesarCipher(object):
    def __init__(self, message=None, encode=False, decode=False, offset=False,
                 crack=None, verbose=None, alphabet=None):
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
            cracked: A boolean indicating to desire to crack the string, used
                as command line script flag.
            verbose: A boolean indicating the desire to turn on debug output,
                use as command line script flag.
            offset: Integer by which you want to shift the value of a letter.
            alphabet: A tuple containing the ASCII alphabet in uppercase.
        """
        self.message = message
        self.encode = encode
        self.decode = decode
        self.offset = offset
        self.verbose = verbose
        self.crack = crack
        self.alphabet = alphabet

        # Frequency of letters used in English, taken from Wikipedia.
        # http://en.wikipedia.org/wiki/Letter_frequency
        self.frequency = {
            'a': 0.08167,
            'b': 0.01492,
            'c': 0.02782,
            'd': 0.04253,
            'e': 0.130001,
            'f': 0.02228,
            'g': 0.02015,
            'h': 0.06094,
            'i': 0.06966,
            'j': 0.00153,
            'k': 0.00772,
            'l': 0.04025,
            'm': 0.02406,
            'n': 0.06749,
            'o': 0.07507,
            'p': 0.01929,
            'q': 0.00095,
            'r': 0.05987,
            's': 0.06327,
            't': 0.09056,
            'u': 0.02758,
            'v': 0.00978,
            'w': 0.02360,
            'x': 0.00150,
            'y': 0.01974,
            'z': 0.00074}

        # Get ASCII alphabet if one is not provided by the user.
        if alphabet is None:
            self.alphabet = {}
            self.alphabet['lower'] = tuple(string.ascii_lowercase)
            self.alphabet['upper'] = tuple(string.ascii_uppercase)

    def cipher(self):
        """Applies the Caesar shift cipher.

        Based on the attributes of the object, applies the Caesar shift cipher
        to the message attribute.

        Required attributes:
            message

        Returns:
            String with cipher applied.
        """
        # If no offset is selected, pick random one with sufficient distance
        # from original.
        if self.offset is False:
            self.offset = randrange(5, 25)
            logging.info("Random offset selected: {0}".format(self.offset))
        logging.debug("Offset set: {0}".format(self.offset))

        # Cipher
        ciphered_message_list = list(self.message)
        for i, letter in enumerate(ciphered_message_list):
            if letter.isalpha():
                if letter.isupper():
                    alphabet = self.alphabet.get('upper', None)
                else:
                    alphabet = self.alphabet.get('lower', None)
                if alphabet is None:
                    alphabet = self.alphabet

                logging.debug("Letter: {0}".format(letter))
                value = alphabet.index(letter)
                cipher_value = value + self.offset
                if cipher_value > 25 or cipher_value < 0:
                    cipher_value = cipher_value % 26
                logging.debug("Cipher value: {0}".format(cipher_value))
                ciphered_message_list[i] = alphabet[cipher_value]
                logging.debug("Ciphered letter: {0}".format(letter))
        self.message = ''.join(ciphered_message_list)
        return self.message

    def calculate_entropy(self, entropy_string):
        """Calculates the entropy of a string based on known frequency of
        English letters.

        Args:
            entropy_string: A str representing the string to calculate.

        Returns:
            A negative float with the total entropy of the string (higher
            is better).
        """
        total = 0
        ignored_chars = []
        for char in entropy_string:
            if char.isalpha():
                total += math.log(self.frequency[char.lower()])
            else:
                ignored_chars.append(char)
        logging.debug("Total sum of freq logging. of letters: {0}".format(
                      total))
        logging.debug("Total ignored characters: {0}".format(ignored_chars))
        return total / math.log(2) / len(ignored_chars)

    @property
    def cracked(self):
        """Attempts to crack ciphertext using frequency of letters in English.

        Returns:
            String of most likely message.
        """
        logging.info("Cracking message: {0}".format(self.message))
        entropy_values = {}
        message = self.message
        for i in range(25):
            self.message = message
            self.offset = i * -1
            logging.debug("Attempting crack with offset: "
                          "{0}".format(self.offset))
            test_cipher = self.cipher()
            logging.debug("Attempting plaintext: {0}".format(test_cipher))
            entropy_values[i] = self.calculate_entropy(test_cipher)

        sorted_by_entropy = sorted(entropy_values, key=entropy_values.get,
                                   reverse=True)
        self.offset = sorted_by_entropy[0] * -1
        self.message = message
        cracked_text = self.cipher()

        logging.debug("Most likely offset: {0}".format(self.offset))

        return cracked_text

    @property
    def encoded(self):
        """Encodes message using Caesar shift cipher

        Returns:
            String encoded with cipher.
        """
        logging.info("Encoding message: {0}".format(self.message))
        return self.cipher()

    @property
    def decoded(self):
        """Decodes message using Caesar shift cipher

        Inverse operation of encoding, applies negative offset to Caesar shift
        cipher.

        Returns:
            String decoded with cipher.
        """
        logging.info("Decoding message: {0}".format(self.message))
        self.offset = self.offset * -1
        return self.cipher()


class CaesarCipherError(Exception):
    def __init__(self, message):
        logging.error("ERROR: {0}".format(message))
        logging.error("Try running with --help for more information.")


# Parser configuration
parser = argparse.ArgumentParser(description="Caesar Cipher - encode, decode "
                                             "or crack messages with an "
                                             "English alphabet offset.",
                                 epilog="Written by Rob Spectre for Hacker "
                                 "Olympics London.\n"
                                 "http://www.brooklynhacker.com")
parser.add_argument('message',
                    help="Message to be encoded, decoded or cracked.")
parser.add_argument('-e', '--encode', action="store_true",
                    help="Encode this message.")
parser.add_argument('-d', '--decode', action="store_true",
                    help="Decode this message.")
parser.add_argument('-c', '--crack', action="store_true",
                    help="Crack this ciphertext to find most likely message.")
parser.add_argument('-v', '--verbose', action="store_true",
                    help="Turn on verbose output.")
parser.add_argument('-o', '--offset',
                    help="Integer offset to encode/decode message against.")
parser.add_argument('-a', '--alphabet',
                    help="String of alphabet you want to use to apply the "
                         "cipher against.")

if __name__ == "__main__":
    caesar_cipher = CaesarCipher()
    parser.parse_args(namespace=caesar_cipher)

    # Logging configuration
    if caesar_cipher.verbose is True:
        log_level = logging.DEBUG
        log_format = "%(asctime)s - %(levelname)s: %(message)s"
    else:
        log_level = logging.INFO
        log_format = "%(message)s"

    logging.basicConfig(level=log_level, format=log_format)

    # Non-required arguments and error conditions.
    if caesar_cipher.offset:
        caesar_cipher.offset = int(caesar_cipher.offset)
    if caesar_cipher.offset is False and caesar_cipher.decode is True:
        raise CaesarCipherError("Message cannot be decoded without "
                                "selecting an offset.  Please try "
                                "again with -o switch.")
    if caesar_cipher.encode is True and caesar_cipher.decode is True:
        raise CaesarCipherError("Please select to encode or encode a message, "
                                "not both.")

    # Required arguments.
    if caesar_cipher.decode is True:
        logging.info("Decoded message: {0}".format(caesar_cipher.decoded))
    elif caesar_cipher.crack is True:
        logging.info("Cracked message: {0}".format(caesar_cipher.cracked))
    elif caesar_cipher.encode is True:
        logging.info("Encoded message: {0}".format(caesar_cipher.encoded))
    else:
        logging.error("Please select a message to encode, decode or "
                      "crack.  For more information, use --help.")
