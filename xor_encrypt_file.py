#!/usr/bin/env python

import sys
from cryptolib import RollingKey, cryptolib as cl
from itertools import izip
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="input_filename", default="samples/binary_elf", help="Input file filename")
parser.add_option("-o", "--output", dest="output_filename", default="samples/binary_elf_encrypted", help="Output file filename")
parser.add_option("-k", "--key", dest="key", default="\x55\x1a\x07\x3d", help="Encryption key")
(options, args) = parser.parse_args()


rk = RollingKey(cl.str2int(options.key))
plaintext = open(options.input_filename, "rb").read()
ciphertext = list()

for c,k in izip(plaintext,rk):
    ciphertext.append(chr(ord(c)^k))

out = open(options.output_filename, "wb")
out.write("".join(ciphertext))
out.close()
