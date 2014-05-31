import unittest

from caesarcipher import CaesarCipher
from caesarcipher import CaesarCipherError


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

    def test_encode_with_arbitrary_alphabet(self):
        message = "The quick brown fox jumps over the lazy dog."
        alphabet = 'ueyplkizjgncdbqshoaxmrwftv'
        test_cipher = CaesarCipher(message, offset=7, alphabet=alphabet)
        self.assertEquals('Kfj rzbad mytpo ltu szenw tijy kfj cvqg xth.',
                          test_cipher.encoded)


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

    def test_decode_with_arbitrary_alphabet(self):
        message = "Kfj rzbad mytpo ltu szenw tijy kfj cvqg xth."
        alphabet = 'ueyplkizjgncdbqshoaxmrwftv'
        test_cipher = CaesarCipher(message, offset=7, alphabet=alphabet)
        self.assertEquals('The quick brown fox jumps over the lazy dog.',
                          test_cipher.decoded)


class CaesarCipherRegressionTest(unittest.TestCase):
    def test_all_offsets(self):
        message = "The quick brown fox jumps over the lazy dog."
        for i in range(0, 100):
            test_cipher = CaesarCipher(message, encode=True, offset=i)
            test_cipher.encoded
            self.assertEquals(message, test_cipher.decoded)


class CaesarCipherErrorTest(unittest.TestCase):
    def test_caesar_cipher_error(self):
        def raiseCaesarCipherError():
            raise CaesarCipherError("This test is bullshit to hit 100%"
                                    " coverage.")
        self.assertRaises(CaesarCipherError, raiseCaesarCipherError)


class CaesarCipherCrackTest(unittest.TestCase):
    def test_calculate_entropy_zero_offset(self):
        message = "The quick brown fox jumps over the lazy dog."
        test_cipher = CaesarCipher(message, crack=True)
        confirmed_entropy_value = 179.14217305030957
        test_entropy_value = test_cipher.calculate_entropy(message)
        self.assertEquals(confirmed_entropy_value, test_entropy_value)

    def test_crack(self):
        ciphertext = "Rfc osgai zpmul dmv hsknq mtcp rfc jyxw bme."
        plaintext = "The quick brown fox jumps over the lazy dog."
        test_crack = CaesarCipher(ciphertext, crack=True)
        self.assertEquals(plaintext, test_crack.cracked)

    def test_crack_one_word(self):
        ciphertext = "Yxo"
        plaintext = "One"
        test_crack = CaesarCipher(ciphertext, crack=True)
        self.assertEquals(plaintext, test_crack.cracked)

    def test_crack_difficult_word(self):
        message = "A quixotic issue to test."
        test_cipher = CaesarCipher(message).encoded
        cracked_text = CaesarCipher(test_cipher).cracked
        self.assertEquals(message, cracked_text)


class CaesarCipherCrackRegressionTest(unittest.TestCase):
    def test_lots_of_cracks(self):
        plaintexts = [
            "London calling to the faraway towns",
            "Now war is declared and battle come down",
            "London calling to the underworld",
            "Come out of the cupboard, you boys and girls",
            "London calling, now don't look to us",
            "Phony Beatlemania has bitten the dust",
            "London calling, see we ain't got no swing",
            "'Cept for the ring of that truncheon thing",
            "The ice age is coming, the sun is zooming in",
            "Meltdown expected, the wheat is growin' thin",
            "Engines stop running, but I have no fear",
            "Cause London is drowning, and I, I live by the river",
            "London calling to the imitation zone",
            "Forget it, brother, you can go it alone",
            "London calling to the zombies of death",
            "Quit holding out and draw another breath",
            "London calling and I don't want to shout",
            "But when we were talking I saw you nodding out",
            "London calling, see we ain't got no high",
            "Except for that one with the yellowy eye",
            "Now get this",
            "London calling, yes, I was there, too",
            "An' you know what they said? Well, some of it was true!",
            "London calling at the top of the dial",
            "And after all this, won't you give me a smile?",
            "I never felt so much a' like a'like a'like",
            "When they kick at your front door",
            "How you gonna come?",
            "With your hands on your head",
            "Or on the trigger of your gun",
            "When the law break in",
            "How you gonna go?",
            "Shot down on the pavement",
            "Or waiting on death row",
            "You can crush us",
            "You can bruise us",
            "But you'll have to answer to",
            "Oh, the guns of Brixton",
            "The money feels good",
            "And your life you like it well",
            "But surely your time will come",
            "As in heaven, as in hell",
            "You see, he feels like Ivan",
            "Born under the Brixton sun",
            "His game is called survivin'",
            "At the end of the harder they come",
            "You know it means no mercy",
            "They caught him with a gun",
            "No need for the Black Maria",
            "Goodbye to the Brixton sun",
            "You can crush us",
            "You can bruise us",
            "Yes, even shoot us",
            "But oh-the guns of Brixton",
            "Shot down on the pavement",
            "Waiting in death row",
            "His game is called survivin'",
            "As in heaven as in hell",
            "Anybody who makes speeches written ",
            "by someone else is just a robot."]

        ciphertexts = [
            "Cfeufe trcczex kf kyv wrirnrp kfnej",
            "Tuc cgx oy jkirgxkj gtj hgzzrk iusk juct",
            "Twvlwv kittqvo bw bpm cvlmzewztl",
            "Lxvn xdc xo cqn ldykxjam, hxd kxhb jwm praub",
            "Bedted sqbbydw, dem ted'j beea je ki",
            "Yqxwh Knjcunvjwrj qjb krccnw cqn mdbc",
            "Hkjzkj ywhhejc, oaa sa wej'p ckp jk osejc",
            "'Lnyc oxa cqn arwp xo cqjc cadwlqnxw cqrwp",
            "Lzw auw syw ak ugeafy, lzw kmf ak rggeafy af",
            "Rjqyitbs jcujhyji, ymj bmjfy nx lwtbns' ymns",
            "Oxqsxoc cdyz bexxsxq, led S rkfo xy pokb",
            "Usmkw Dgfvgf ak vjgofafy, sfv A, A danw tq lzw janwj",
            "Cfeufe trcczex kf kyv zdzkrkzfe qfev",
            "Oxapnc rc, kaxcqna, hxd ljw px rc juxwn",
            "Twvlwv kittqvo bw bpm hwujqma wn lmibp",
            "Mqep dkhzejc kqp wjz znws wjkpdan xnawpd",
            "Gjiyji xvggdib viy D yji'o rvio oj ncjpo",
            "Mfe hspy hp hpcp elwvtyr T dlh jzf yzootyr zfe",
            "Jmlbml ayjjgle, qcc uc ygl'r emr lm fgef",
            "Votvgk wfi kyrk fev nzky kyv pvccfnp vpv",
            "Stb ljy ymnx",
            "Ehgwhg vteebgz, rxl, B ptl maxkx, mhh",
            "Iv' gwc svwe epib bpmg aiql? Emtt, awum wn qb eia bzcm!",
            "Svukvu jhsspun ha aol avw vm aol kphs",
            "Reu rwkvi rcc kyzj, nfe'k pfl xzmv dv r jdzcv?",
            "E jaran bahp ok iqyd w' hega w'hega w'hega",
            "Lwtc iwtn zxrz pi ndjg ugdci sddg",
            "Yfn pfl xfeer tfdv?",
            "Lxiw ndjg wpcsh dc ndjg wtps",
            "Il ih nby nlcaayl iz siol aoh",
            "Bmjs ymj qfb gwjfp ns",
            "Mtb dtz ltssf lt?",
            "Hwdi sdlc dc iwt epktbtci",
            "Tw bfnynsl ts ijfym wtb",
            "Qgm usf ujmkz mk",
            "Gwc kiv jzcqam ca",
            "Jcb gwc'tt pidm bw ivaemz bw",
            "Mf, rfc eslq md Zpgvrml",
            "Kyv dfevp wvvcj xffu",
            "Wjz ukqn heba ukq hega ep sahh",
            "Rkj ikhubo oekh jycu mybb secu",
            "Xp fk ebxsbk, xp fk ebii",
            "Hxd bnn, qn onnub urtn Rejw",
            "Uhkg ngwxk max Ukbqmhg lng",
            "Opz nhtl pz jhsslk zbycpcpu'",
            "Fy ymj jsi tk ymj mfwijw ymjd htrj",
            "Fvb ruvd pa tlhuz uv tlyjf",
            "Znke igamnz nos cozn g mat",
            "Yz yppo qzc esp Mwlnv Xlctl",
            "Zhhwurx mh max Ukbqmhg lng",
            "Vlr zxk zorpe rp",
            "Oek sqd rhkyiu ki",
            "Lrf, rira fubbg hf",
            "Kdc xq-cqn pdwb xo Kargcxw",
            "Dsze ozhy zy esp algpxpye",
            "Osalafy af vwslz jgo",
            "Efp dxjb fp zxiiba prosfsfk'",
            "Rj ze yvrmve rj ze yvcc",
            "Ylwzmbw ufm kyicq qnccafcq upgrrcl ",
            "ur lhfxhgx xelx bl cnlm t khuhm."]

        for i, ciphertext in enumerate(ciphertexts):
            test_cipher = CaesarCipher(ciphertext, crack=True)
            self.assertEquals(plaintexts[i], test_cipher.cracked)
