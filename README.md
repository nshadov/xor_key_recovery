# XOR key recovery

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
binary to contain phrase ```__gmon_start__```. We dont know key lenght, but
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

It's quite easy to understand on example but it's not a formal proof thoguh (or maybe because of it).

### Prepare template

First we need part of plaintext before being encrypted. Anything slightly longer than key lenght would be sufficient but to avoid false positives twice as long plaintext is prefered. We could in many cases guess it (like common phrases, strings etc.).

```
P[] = "This program cannot be run in DOS"
```

The other thing we will need is secret key length -- we could also guess it or iterate over possible lengths (n=3, n=4, n=5 ...).

```
k_len = 6
```

Now, if we xor symbols from plaintext that are keylenght apart, we receive:

```
T[1] = P[i] XOR P[i+k_len]
```

We build template that way of first part of the string XORed with another symbols one keylenght apart. It's easy as it sounds.

### Surprising XOR cipher characteristics

Because in cipertext symbols one keylenght apart are XORed with the same secret key symbol we get

```
C[i] = P[i] XOR Key[i]
C[i+k_len] = P[i+k_len] XOR Key[i]
```

If we XOR these two, we suprisingly (because of XOR characteristics) receive something independent from secret key used:

```
C[i] XOR C[i+k_len] = ( P[i] XOR Key[i] ) XOR ( P[i+k_len] XOR Key[i] ) =
                    = ( P[i] XOR P[i+k_len] ) XOR ( Key[i] XOR Key[i] ) =
                    = P[i] XOR P[i+k_len]
```

This is exactly the same, as our template and it's independent from secret key.

### Final blow

Now, when we do this for whole ciphertext (eg. encrypted file) we look for our template.
This way, we've found place in ciphertext where our encrypted string is and w know what it's plaintext version is.

From this place, it's trivial to extract secret key.

## Bugs & Credits

Please submit bugs/propositions via GitHub.

Author: nshadov
