import sys
import matplotlib.pylab as plt
from statistics import mean


iocs = {}  # global index of coincidences dict (period, avg)


def build_trigrams(cyphertext):
    trigrams = list(ngrams(cyphertext, 3))
    grouped_trigrams = []
    for trigram in trigrams:
        grouped_trigrams.append(''.join(trigram))
    return grouped_trigrams


def count_frequency(sequence):
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
    for i in range(2, 16):  # periods less than 2 and greater than 15 are not allowed
        print(f'\nperiod {i}')
        for j in range(i):
            cyphertext = original[j:]
            ics.append(ic(cyphertext[::i]))
            print(cyphertext[::i])
        iocs.update( {i : round(mean(ics), 13)} )  # append iocs avg to global ioc dict
        ics.clear()


def print_iocs():
    print("\n{:<8} {:<15}".format('Period','AVG IoC'))
    print("{:<8} {:<15}".format('--------','---------------'))
    for k, v in iocs.items():
        period, avg = k, v
        print("{:<8} {:<15}".format(period, avg))


def main():
    with open('cyphertext.txt') as ct:
        cyphertext = ct.read()

    print(f'\nCyphertext {cyphertext} is {len(cyphertext)} characters long - {sys.getsizeof(cyphertext)} bytes.' )
    cyphertext = ''.join(filter(str.isalpha, cyphertext.upper()))
    char_count = len(cyphertext)
    period_finder(cyphertext)
    print_iocs()

    # Print bar plot with avg iocs
    plt.bar(iocs.keys(), iocs.values(), color='gray')
    plt.xticks(range(2, 16))
    plt.xlabel('Period/Key Size')
    plt.ylabel('IOC Average')
    plt.title('Vigenere Cipher - Period (Key Size) Approximation')
    plt.show()

    
main()