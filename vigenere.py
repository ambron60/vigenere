import sys
import matplotlib.pylab as plt
from statistics import mean


iocs = {}  # global index of coincidences dict (period, avg)
sequences = {}  # global storage of periods and corresponding sequences
deciphered = []  # global storage of min chi-sq values corresponding indices

english_letters_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 
                        'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15,
                        'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23,
                        'Y': 24, 'Z': 25}
english_letters_freq = {'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.127, 'F': 0.022,
                        'G': 0.020, 'H': 0.061, 'I': 0.070, 'J': 0.002, 'K': 0.008, 'L': 0.040,
                        'M': 0.024, 'N': 0.067, 'O': 0.075, 'P': 0.019, 'Q': 0.001, 'R': 0.060,
                        'S': 0.063, 'T': 0.091, 'U': 0.028, 'V': 0.010, 'W': 0.023, 'X': 0.001,
                        'Y': 0.020, 'Z': 0.001}
reversed_index = {v: k for k, v in english_letters_index.items()}  # reversed English letters index


def chi_squared(sequence):
    chis = []
    s = len(sequence)  # length of sequence
    letter_counts = count_frequency(sequence)
    for letter in letter_counts.keys():
        expected_value = s * english_letters_freq[letter]
        chis.append(((letter_counts[letter] - expected_value)**2) / expected_value)
    return round(sum(chis), 3)


def count_frequency(sequence):
    """Return a dictionary

    Keyword arguments:
    This function counts and sorts individual characters
    given a sequence or string of characters as input.
    """
    frequency_counts = {}
    for item in sequence:
        if (item in frequency_counts):
            frequency_counts[item] += 1
        else:
            frequency_counts[item] = 1
    return frequency_counts


def decipher_key(indices):
    key = []
    for index in indices:
        key.append(reversed_index[index])
    return key


def ic(sequence):
    denominator, numerator = 0.0, 0.0
    for val in count_frequency(sequence).values(): 
        i = val
        numerator += i * (i - 1)
        denominator += i
    if (denominator == 0.0):
        return 0.0
    else:
        return numerator / ( denominator * (denominator - 1))


def iocs_plot():
    # Print bar plot with avg iocs
    plt.bar(iocs.keys(), iocs.values(), color='gray')
    plt.xticks(range(1, 31))
    plt.xlabel('Period/Key Size')
    plt.ylabel('IoC Average')
    plt.title('Vigenere Cipher - Period (Key Size) Approximation')
    plt.show()


def period_finder(cipher):
    ics = []  # list of indices of coincidence to calculate averages
    period_sequences = []  # temporary storage list for every sequence under each key length
    for i in range(1, 31):  # periods (key size) must be between 1 and 30
        for j in range(i):
            ciphertext = cipher[j:]
            ics.append(ic(ciphertext[::i]))
            period_sequences.append(ciphertext[::i])
        iocs.update( {i : round(mean(ics), 13)} )  # append iocs avg to global ioc dict
        ics.clear()
        sequences[i] = [sequence for sequence in period_sequences]
        period_sequences.clear()
    return


def sequence_shifter(sequence):
    chi_stats = {}
    subsequence = []
    for i in range(26):
        chi_stats[i] = chi_squared(sequence)
        for letter in sequence:
            l_index = english_letters_index[letter]
            if l_index is 0:
                subsequence.append('Z')
            else:
                subsequence.append(reversed_index[l_index-1])
        sequence = ''.join(subsequence)
        subsequence.clear()
        if i == 25:
            min_chi = min(chi_stats.keys(), key=(lambda k: chi_stats[k]))
            deciphered.append(min_chi)
    return


def main():
    with open('ciphertext.txt') as ct:
        ciphertext = ct.read()
    print(f'\nciphertext is {len(ciphertext)} characters long -> {sys.getsizeof(ciphertext)} bytes\n' )
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))
    
    # Approximate the period length via IoC
    period_finder(ciphertext)
    iocs_plot()

    # Key estimation routine given the period (key) length from previous step
    key_size = int(input("Enter the desired period (key size): "))
    for sequence in sequences[key_size]:
        sequence_shifter(sequence)
    print(f'\nPossible KEY: {"".join(decipher_key(deciphered))}')  # print possible key


main()