# Vigènere Cipher - A Primer
 The Vigènere cipher is the best-known example of a polyalphabetic substitution there is. The Vigenere Cipher initially seems very secure, however it can be broken fairly easily once the length of the keyword is known. If you know that the length of the keyword is n, you can break the ciphertext into n cosets and attack the cipher using frequency analysis if the ciphertext sample is long enough. This page will look at two methods to determine the length of the keyword, the Friedman and Kasiski tests \[LINK\](https://www.cs.uri.edu/cryptography/classicalvigenerecrypt.htm).
