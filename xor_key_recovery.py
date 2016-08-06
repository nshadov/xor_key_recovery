#!/usr/bin/env python

import sys
from cryptolib import RollingKey, cryptolib as cl
from itertools import izip
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="input_filename", default="samples/binary_elf_encrypted", help="Input encrtypted file filename")
parser.add_option("-o", "--output", dest="output_filename", default="output", help="Output file filename")
parser.add_option("-p", "--plaintext", dest="plaintext_fragment", default="__libc_start_main", help="Fragment of plaintext that should be present somewhere in decrypted binary")
parser.add_option("-n", "--keylength", dest="keylength", default="4", help="Key length (in bytes) to check")
(options, args) = parser.parse_args()


plaintext = options.plaintext_fragment
keylength = int(options.keylength)
if keylength < 1:
    print "[!] Key lenght must be larger than one."
    sys.exit(-1);
if len(plaintext) < 2*keylength:
    print "[!] Plaintext must be at least 2 times longer than expected keylength"
    sys.exit(-1);

print "[+] Reading encrypted file from: '%s'" % options.input_filename
ciphertext = open(options.input_filename, "rb").read()


plaintext_template  = "".join([ chr(ord(plaintext[i])^ord(plaintext[i+keylength])) for i in range(0, len(plaintext)-keylength)])
ciphertext_template = "".join([ chr(ord(ciphertext[i])^ord(ciphertext[i+keylength])) for i in range(0, len(ciphertext)-keylength)])
index = ciphertext_template.index(plaintext_template)

if index < 0:
    print "[i] Plaintext not found in ciphertext with provided keylength"
    sys.exit(0)

print "[+] Found plaintext at position: %d" % index

key = RollingKey([ hex(ord(ciphertext[index+i])^ord(plaintext[i])) for i in range(0, keylength) ])
key = RollingKey([key[k] for k in range(-index,-index+keylength)])
print "[+] Key found: %s" % key

print "[+] Saving decrypted file to: '%s'" % options.output_filename
out = open(options.output_filename, "wb")
out.write("".join([ chr(ord(c)^int(k,16)) for c,k in izip(ciphertext,key) ]))
out.close()
