## Caesar Cipher

Command line script for encoding and decoding messages with the [Caesar Shift
Cipher](http://en.wikipedia.org/wiki/Caesar_cipher).

[![Build
Status](https://travis-ci.org/RobSpectre/Caesar-Cipher.svg)](https://travis-ci.org/RobSpectre/Caesar-Cipher)

### Usage

#### Encoding messages

`python caesarcipher.py --encode "This is a message I want to encode."`


Output:

```Random offset selected: 7
Encoding message: This is a message I want to encode.
Encoded message: AOPZ PZ H TLZZHNL P DHUA AV LUJVKL.```

#### Decoding messages

`python caesarcipher.py --encode "QEFP FP X JBPPXDB F TXKQ QL ABZLAB."`


Output:

```Encoding message: QEFP FP X JBPPXDB F TXKQ QL ABZLAB.
Decoded message: THIS IS A MESSAGE I WANT TO DECODE.```


#### Running Tests

Test suite on the cipher function and encode/decode properties is available
using [Nose](https://nose.readthedocs.org/en/latest/).

`nosetests -v test_caesarciphre.py`


### Meta

* Written by [Rob Spectre](http://www.brooklynhacker.com).
* Used for Hacker Olympics London 2014.
* Released under [MIT License](http://opensource.org/licenses/MIT)
* Software is as is - no warranty expressed or implied.
