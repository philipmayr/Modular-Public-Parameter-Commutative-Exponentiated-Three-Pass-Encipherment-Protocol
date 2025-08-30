# Shamir's Three-Pass Protocol

import random, secrets

def list_small_primes(upper_bound):
    pass


def test_primality(prime_candidate):
    if prime_candidate & 1 != 1: return False
    '''
    
    TODO:
    
    1. divide prime candidate by first few hundred primes:
       return false if any prime divides prime candidate evenly
       
    2. test prime candidate for perfect exponentiality:
       return false if prime candidate is a perfect power
       
    '''
    
    # small_primes = list_small_primes(1000)
    
    # for prime in small_primes:
    #     if prime * prime > prime_candidate: break
    #     if prime_candidate % prime == 0: return False
    
    # n - 1 = 2ᵏ ⋅ m
    # n: prime candidate
    # k: index
    # m: quotient
    
    index = 1
    
    while True:
        if prime_candidate - 1 % exponentiate(2, index) == 0:
            index += 1
        else:
            index -= 1
            break
            
    quotient = (prime_candidate - 1) // exponentiate(2, index)
    
    # 1 < a < n - 1
    # a: witness
    
    witness = random.randint(2, prime_candidate - 2)
    
    # b₀ = aᵐ mod n
    # b = residue
    
    residue = exponentiate_modularly(witness, quotient, prime_candidate)
    
    if residue == 1 or residue == -1 or residue == (residue - prime_candidate):
        return True
    else:
        residue = exponentiate_modularly(residue, 2, prime_candidate)
        if residue == 1:
            return False
        elif residue == -1 or (residue - prime_candidate == -1):
            return True
            
    return False


def exponentiate(base, index):
    if index == 0: return 1
    if base == 0: return 0
    if index == 1: return base
    
    power = 1
    
    while index > 0:
        if index & 1: power *= base
        
        index >>= 1
        base *= base
        
    return power


def exponentiate_modularly(base, index, modulus):
    if modulus == 1: return 0
    if index == 0: return 1
    if base == 0: return 0
    
    base %= modulus
    
    residue = 1
    
    while index > 0:
        if index & 1:
            residue = (residue * base) % modulus
            
        base = (base * base) % modulus
        index >>= 1
        
    return residue


def find_greatest_common_divisor(a, b):
    return find_greatest_common_divisor(b, a % b) if b else a


def test_coprimality(a, b):
    return find_greatest_common_divisor(a, b) == 1


def draw_random_number(bit_length):
    random_bits = secrets.randbits(bit_length)
    
    return random_bits


def draw_random_prime_number(bit_length):
    while True:
        random_bits = secrets.randbits(bit_length)
        
        # turn on leading and trailing bits of mask to make sure prime candidate is both significantly large and odd
        bit_mask = (1 << (bit_length - 1)) | 1
        random_bits |= bit_mask
        
        if test_primality(random_bits): return random_bits
        
        
def find_modular_multiplicative_inverse(multiplicand, modulus):
    if find_greatest_common_divisor(multiplicand, modulus) != 1:
        raise ValueError("Multiplicand and modulus are not coprime; there is no modular multiplicative inverse.")
        
    foregoing_coefficient, coefficient = 0, 1
    foregoing_remainder, remainder = modulus, multiplicand
    
    while remainder:
        quotient, upcoming_remainder = foregoing_remainder // remainder, foregoing_remainder % remainder
        
        foregoing_coefficient, coefficient = (coefficient, (foregoing_coefficient - quotient * coefficient) % modulus)
        foregoing_remainder, remainder = remainder, upcoming_remainder
        
    return foregoing_coefficient


def make_key_pair(bit_length, lower_exclusive_bound, phi):
    while True:
        encryption_key = secrets.randbits(bit_length)
        
        if encryption_key > lower_exclusive_bound and find_greatest_common_divisor(encryption_key, phi) == 1:
            decryption_key = find_modular_multiplicative_inverse(encryption_key, phi)
            
            key_pair = encryption_key, decryption_key
            
            return key_pair


def main():
    public_prime_number_bit_length = 512
    
    print("Public prime number modulus bit length: " + str(public_prime_number_bit_length), end='\n\n')
    
    public_prime_number = draw_random_prime_number(public_prime_number_bit_length)
    public_prime_number_less_one = public_prime_number - 1
    
    sender_key_pair = make_key_pair(public_prime_number_bit_length, lower_exclusive_bound=2, phi=public_prime_number_less_one)
    
    sender_encryption_key, sender_decryption_key = sender_key_pair
    
    receiver_key_pair = make_key_pair(public_prime_number_bit_length, lower_exclusive_bound=2, phi=public_prime_number_less_one)
    
    receiver_encryption_key, receiver_decryption_key = receiver_key_pair
    
    while True:
        message = input("➣ Enter integer message: ")
        
        try:
            message = int(message)
            break
        except ValueError:
            print("Message must be an integer (whole number).", end="\n\n")
    
    print()
    
    if message > public_prime_number_less_one:
        raise ValueError("Message must be smaller than pubic prime number.")
        
    sender_encrypted_cipher_text = exponentiate_modularly(message, sender_encryption_key, public_prime_number)
    print("Sender encrypts message with his private encryption key and sends it to receiver: \n" + str(sender_encrypted_cipher_text), end="\n\n")
    
    receiver_encrypted_sender_encrypted_cipher_text = exponentiate_modularly(sender_encrypted_cipher_text, receiver_encryption_key, public_prime_number)
    print("Receiver encrypts sender encrypted message with his private encryption key and sends it back to sender: \n" + str(receiver_encrypted_sender_encrypted_cipher_text), end="\n\n")
    
    sender_decrypted_receiver_encrypted_cipher_text = exponentiate_modularly(receiver_encrypted_sender_encrypted_cipher_text, sender_decryption_key, public_prime_number)
    print("Sender decrypts receiver and sender encrypted message with his private decryption key and sends it to receiver: \n" + str(sender_decrypted_receiver_encrypted_cipher_text), end="\n\n")
    
    receiver_decrypted_sender_decrypted_cipher_text = exponentiate_modularly(sender_decrypted_receiver_encrypted_cipher_text, receiver_decryption_key, public_prime_number)
    print("Receiver decrypts sender decrypted sender and receiver encrypted message with his private decryption key: \n" + str(receiver_decrypted_sender_decrypted_cipher_text), end="\n\n")
    
    clear_text = receiver_decrypted_sender_decrypted_cipher_text
    
    print('✿' * len(str(public_prime_number_bit_length)))
    
main()
