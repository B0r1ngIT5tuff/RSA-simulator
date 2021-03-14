from random import randint
from math import gcd, sqrt, factorial
from sympy.ntheory import isprime

def pub_keygen():
    ''' 
        This function generates the public key, it is composed of two parts: 'n' and 'e'.

        p and q are two large prime numbers, randomly generated that are needed to compute n.

        Parameters: None.

        pub_keygen() -> (int: e, int: n, int: phi_n)
    '''

    # I verify if 'p' and 'q' are prime numbers with the isprime() function, if they're not they will be re-generated randomly.
    loop = True
    while loop == True:
        p = randint(1,1000000000)
        q = randint(1,1000000000)

        if isprime(p) == True and isprime(q) == True:
            loop = False

    n = p*q                     # Compute n
    phi_n = (p - 1) *(q - 1)    # Compute phi(n)


    # Generates 'e' which must be coprime to phi(n) and 1 < e < phi(n).
    e = 0
    while e < phi_n:
        if gcd(e, phi_n) == 1:
            break
        else:
            e = e + 1

    return e, n, phi_n


def priv_keygen(e, phi_n):
    ''' 
        This function generates the private key: 'd'.

        Parameters:
        - e, is a public exponent, coprime to phi(n). It's the second part of the public key.
        - phi_n, is the totien function of Euler and tells us how many numbers < 'n' are prime numbers and are coprime to 'n'.

        priv_keygen(e, phi_n) -> (int: d)
    '''

    # k is a random number, needed to compute d.
    k_loop = True
    
    while k_loop == True:
        k = randint(1,20)
        if isprime(k) == True:
            k_loop = False

    d = ((k*phi_n)+1) // e

    return d 

def encrypt_m(m, e, n):
    '''
        This function encrypts every letter of the message with: m**e % n = c.

        Parameters:
            - m, is a characters list of all the message characters.
            - e, is a public exponent, coprime to phi(n). It's the second part of the public key. 
            - n, is a very big prime number. It's the first part of the public key.

        encrypt_m(m, e, n) -> (list: c)
    '''

    mex_int = []
    c = []

    for i in range(len(m)):
        mex_int.append(ord(m[i]))

    # Every number in mex_int will be added in the list: 'c' which contains the crypted characters of the message.
    for i in range(len(mex_int)):
        c.append(pow(mex_int[i],e,n))

    return c

def decrypt_m(c, d, n):
    '''
        This function decrypts the crypted message.

        Parameters:
        - c, is a list that contains all the crypted characters of the message.
        - d, is the private key.
        - n, is a very big prime number. It's the first part of the public key.


        decrypt_m(c, d, n) -> (list: m)
    '''

    mex = []
    m = []
    print("I'm decrypting the message, this might take some time.\n")
    for i in c: 
        mex.append(pow(i,d,n))

    for j in mex:
        m.append(chr(j))

    return m