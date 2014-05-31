import logging
import argparse

from caesarcipher import CaesarCipher
from caesarcipher import CaesarCipherError

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


def main():
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
