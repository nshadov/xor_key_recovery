# CryptoLib

## Description

Short script able to recover repeating XOR key from ciphertext, based on
plaintext fragment expected to be found in decrypted file.

## Install

```
git clone --recursive https://github.com/nshadov/xor_key_recovery.git
```

## Example Usage

First, we create example XOR encrypted '/bin/ls' file:

```
$ ./xor_encrypt_file.py -f /bin/ls -o encrypted.file -k "secret"
```

Now to recover secret key "secret", we use second script. We expect ELF
binary to contain phrase "__gmon_start__". We dont know key lenght, but
after few tries with consecutive ```n=1```, ```n=2```, ```n=3``` ... we finally try ```n=6```:

```
$ ./xor_key_recovery.py -f encrypted.file -o decrypted.file -p "__gmon_start__" -n 6

[+] Fragment '__gmon_start__' expected to be found in plaintext
[+] Reading encrypted file from: 'encrypted.file'
[+] Found plaintext at position: 3909
[+] Key found: RollingKey(['0x73', '0x65', '0x63', '0x72', '0x65', '0x74'])
[+] Saving decrypted file to: 'decrypted.file'
```

Encryption key, when found is presented in hex format and decrypted file is saved.

## How it works



## Bugs & Credits

Please submit bugs/propositions via GitHub.

Author: nshadov