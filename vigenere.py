import sys
import matplotlib.pylab as plt
from statistics import mean


iocs = {}  # global index of coincidences dict (period, avg)
sequences = {}  # global storage of periods and corresponding sequences
english_letters_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 
                        'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15,
                        'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23,
                        'Y': 24, 'Z': 25}
english_letters_freq = {'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.127, 'F': 0.022,
                        'G': 0.020, 'H': 0.061, 'I': 0.070, 'J': 0.002, 'K': 0.008, 'L': 0.040,
                        'M': 0.024, 'N': 0.067, 'O': 0.075, 'P': 0.019, 'Q': 0.001, 'R': 0.060,
                        'S': 0.063, 'T': 0.091, 'U': 0.028, 'V': 0.010, 'W': 0.023, 'X': 0.001,
                        'Y': 0.020, 'Z': 0.001}


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


def period_finder(original):
    ics = []  # list of indices of coincidence to calculate averages
    period_sequences = []  # temporary storage list for every sequence under each key length
    for i in range(2, 16):  # periods less than 2 and greater than 15 are not allowed
        for j in range(i):
            cyphertext = original[j:]
            ics.append(ic(cyphertext[::i]))
            period_sequences.append(cyphertext[::i])
        iocs.update( {i : round(mean(ics), 13)} )  # append iocs avg to global ioc dict
        ics.clear()
        sequences[i] = [sequence for sequence in period_sequences]
        period_sequences.clear()
    return

def iocs_table():
    print("\n{:<8} {:<15}".format('Period','AVG IoC'))
    print("{:<8} {:<15}".format('--------','---------------'))
    for k, v in iocs.items():
        period, avg = k, v
        print("{:<8} {:<15}".format(period, avg))


def iocs_chart():
    # Print bar plot with avg iocs
    plt.bar(iocs.keys(), iocs.values(), color='gray')
    plt.xticks(range(2, 16))
    plt.xlabel('Period/Key Size')
    plt.ylabel('IOC Average')
    plt.title('Vigenere Cipher - Period (Key Size) Approximation')
    plt.show()


def main():
    with open('cyphertext.txt') as ct:
        cyphertext = ct.read()

    print(f'\nCyphertext is {len(cyphertext)} characters long -> {sys.getsizeof(cyphertext)} bytes\n' )
    cyphertext = ''.join(filter(str.isalpha, cyphertext.upper()))
    period_finder(cyphertext)
    iocs_chart()

    # Select and print a period (key length) number
    key_size = int(input("Enter the desired period (key size): "))
    print()
    for sequence in sequences[key_size]:
        print(sequence, chi_squared(sequence))  # print all sequences shifted by key size or period number
        #print(count_frequency(sequence))  # print letter frequencies
        
        # Find letter with highest frequency in current sequence
        #highest_freq_letter = max(count_frequency(sequence), key=count_frequency(sequence).get)
        #print(highest_freq_letter)


main()