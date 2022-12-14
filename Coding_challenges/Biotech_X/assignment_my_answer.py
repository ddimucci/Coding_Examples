"""
Coding exercise for COMPANY X
15 September 2022
dimuccidm@gmail.com

Notes on things to consider:

I wrote the code in PyCharm using python 3.9.13
For stop codons, since I don't know anything about the end user's goals I opted simply to print out to the console a message that a stop codon is encoded by one or more codons and display the list of the offending codons.
I wrote a 'parent_function' that invokes both functions an arbitraty number of times. Results are stored in a list that can optionally be saved to a txt file.
"""
# Import modules
from itertools import product, combinations
import itertools
import random
from collections import Counter


# Store provided dictionaries
translation_table = {'TTT': 'F', 'TCT': 'S', 'TAT': 'Y', 'TGT': 'C',
                     'TTC': 'F', 'TCC': 'S', 'TAC': 'Y', 'TGC': 'C',
                     'TTA': 'L', 'TCA': 'S', 'TAA': '*', 'TGA': '*',
                     'TTG': 'L', 'TCG': 'S', 'TAG': '*', 'TGG': 'W',
                     'CTT': 'L', 'CCT': 'P', 'CAT': 'H', 'CGT': 'R',
                     'CTC': 'L', 'CCC': 'P', 'CAC': 'H', 'CGC': 'R',
                     'CTA': 'L', 'CCA': 'P', 'CAA': 'Q', 'CGA': 'R',
                     'CTG': 'L', 'CCG': 'P', 'CAG': 'Q', 'CGG': 'R',
                     'ATT': 'I', 'ACT': 'T', 'AAT': 'N', 'AGT': 'S',
                     'ATC': 'I', 'ACC': 'T', 'AAC': 'N', 'AGC': 'S',
                     'ATA': 'I', 'ACA': 'T', 'AAA': 'K', 'AGA': 'R',
                     'ATG': 'M', 'ACG': 'T', 'AAG': 'K', 'AGG': 'R',
                     'GTT': 'V', 'GCT': 'A', 'GAT': 'D', 'GGT': 'G',
                     'GTC': 'V', 'GCC': 'A', 'GAC': 'D', 'GGC': 'G',
                     'GTA': 'V', 'GCA': 'A', 'GAA': 'E', 'GGA': 'G',
                     'GTG': 'V', 'GCG': 'A', 'GAG': 'E', 'GGG': 'G'
                     }

# nomenclature for degenerate codons
expanded_code = {'A': ['A'], 'C': ['C'], 'G': ['G'], 'T': ['T'],
                 'W': ['A', 'T'], 'S': ['C', 'G'], 'M': ['A', 'C'], 'K': ['G', 'T'], 'R': ['A', 'G'], 'Y': ['C', 'T'],
                 'B': ['C', 'G', 'T'], 'D': ['A', 'G', 'T'], 'H': ['A', 'C', 'T'], 'V': ['A', 'C', 'G'],
                 'N': ['A', 'C', 'G', 'T']
                 }

# helpful for validating input
valid_nucleotides = 'ACGTWSMKRYBDHVN'
valid_aa = 'GAVLIMFWPSTCYNQDEKRH*'

# Define functions, their order should tell a story

###
#
# Functions to check if the amino acid list is going to work in the workflow
#
###
def check_amino_acid_validity(aa_set):
    """
    Check that the object is a set
    Check if the items contained in a set are all valid amino acids
    :param set:
    :return:
    """
    valid_aa = 'GAVLIMFWPSTCYNQDEKRH*'
    if not isinstance(aa_set, set):
        print(type(aa_set))
        raise Exception('Argument must be an object of type: set')
    else:
        validity = [aa in valid_aa for aa in aa_set]
        return validity


def summarize_validity(validity_list, set):
    """
    Pass in validity list generated by check_amino_acid_validity and set of amino acids
    If any amino acids correspond to false let the user know
    Else tell them it looks ok
    :param validity_list:
    :param set:
    :return:
    """
    if False in validity_list:
        invalid_items = [item for status, item in zip(validity_list, set) if status == False]
        raise Exception(f'The following items are not valid amino acids. Check the case. {invalid_items}')

def validate_amino_acid_set(aa_set):
    """
    Takes in a set of amino acids, combined other functions to
    :param set:
    :return:
    """
    validity_list = check_amino_acid_validity(aa_set)
    summarize_validity(validity_list, aa_set)

###
#
# Define functions for precomputing amino acid to codon and codon to amino acid dictionaries
#
###

def identify_standard_codon_set(codon, expanded_code):
    """
    For a given codon, use the expanded_codon table to find out which regular dna codons it represents
    :param codon:
    :param expanded_code:
    :return:
    """
    if len(codon) == 3:
        nucleotide_sets = [expanded_code[nucleotide] for nucleotide in codon]
        codon_set = [(x, y, z) for x in nucleotide_sets[0] for y in nucleotide_sets[1] for z in nucleotide_sets[2]]
        return [('').join(codon) for codon in codon_set]


def identify_encoded_amino_acids_from_codon_set(codon_set, translation_table):
    """
    for a given set of codons use the translation table to make a list of which amino acids they encode
    :param codon:
    :param translation_table:
    :param expanded_code:
    :return:
    """
    amino_acids = [translation_table[codon] for codon in codon_set]
    return amino_acids


def convert_codon_to_amino_acid_set(codon, translation_table, expanded_code):
    """
    provided a codon, translation table and expanded code dictionaries
    returns a list of amino acids the codon represents
    :param codon:
    :param translation_table:
    :param expanded_code:
    :return:
    """
    codon_set = identify_standard_codon_set(codon, expanded_code)
    amino_acids = identify_encoded_amino_acids_from_codon_set(codon_set, translation_table)
    return amino_acids


def add_codon_to_amino_acid_dictionary(aa_to_codons_dict, codon, amino_acids):
    """
    For a given codon and it's corresponding amino acids, adds them to the amino acid to codon dictionary
    :param aa_to_codons:
    :param codon:
    :param amino_acids:
    :return:
    """
    for aa in amino_acids:
        aa_to_codons_dict[aa].append(codon)
    return aa_to_codons_dict

###
# Pre-compute a dictionary mapping all codons to the amino acids they code for
##
nucleotides = list(expanded_code.keys())
all_codons = [(x, y, z) for x in nucleotides for y in nucleotides for z in nucleotides]
codons_to_aa_dict = {}
for i in all_codons:
    codon = ('').join(i)
    amino_acids = convert_codon_to_amino_acid_set(codon, translation_table, expanded_code)
    codons_to_aa_dict[codon] = amino_acids

###
# Pre-compute a dictionary mapping amino acids to all codons that code for them
##
aa_list = [aa for aa in valid_aa]
aa_to_codons_dict = {}
for i in aa_list:
    aa_to_codons_dict[i] = []

for i in all_codons:
    codon = ('').join(i)
    amino_acids = convert_codon_to_amino_acid_set(codon, translation_table, expanded_code)
    aa_to_codons_dict = add_codon_to_amino_acid_dictionary(aa_to_codons_dict, codon, amino_acids)

###
#
# Functions to calculate codon efficiencies and consolidate best hits into a list
# Used by make get_codon_for_amino_acids()
#
###
def get_codon_set_for_amino_acid(aa, aa_to_codons_dict):
    """
    Look up which codons code for an amino acid
    :param aa:
    :param aa_to_codons_dict:
    :return:
    """
    return set(aa_to_codons_dict[aa])


def retrieve_codon_sets_for_amino_acid_set(aa_set, aa_to_codons_dict):
    """
    For a set of amino acids, return a list of which codons encode each amino acid
    :param aa_set:
    :param aa_to_codons_dict:
    :return:
    """
    return [get_codon_set_for_amino_acid(aa, aa_to_codons_dict) for aa in aa_set]


def intersect_codons_for_amino_acid_sets(codon_sets):
    """
    Given a list of sets of codons, find the codons that appear in every set.
    :param codon_sets:
    :return:
    """
    return set.intersection(*codon_sets)

def get_common_codons_set(aa_set, aa_to_codons_dict):
    """
    Provide an amino acid set and a dictionary mapping amino acids to codons
    returns a set of codons that all code for each aa in the set.
    :param aa_set:
    :param aa_to_codons_dict:
    :return:
    """
    codon_sets = retrieve_codon_sets_for_amino_acid_set(aa_set, aa_to_codons_dict)
    return intersect_codons_for_amino_acid_sets(codon_sets)

###
#
# Functions to calculate codon efficiencies and consolidate best hits into a list
#
###
def calculate_codon_efficiency(codon, aa_set, codons_to_aa_dict):
    """
    Confirm all the amino acids are coded for by the codon
    If not, raise an exception that efficiency can't be calculated
    Otherwise calculate efficiency
    Efficiency for a codon is defined as:
    (# encoded amino acids that are in the desired set) / (# encoded amino acids)
    :param codon:
    :param aa_set:
    :param codons_to_aa_dict:
    :return:
    """
    coded_aas = codons_to_aa_dict[codon]
    coded_set = set(coded_aas)
    if sum([a in coded_set for a in aa_set]) / len(aa_set) == 1:
        hits = [aa in aa_set for aa in coded_aas]
        efficiency = sum(hits) / len(coded_aas)
        return efficiency
    else:
        raise Exception(f"This codon {codon} does not encode for all desired amino acids")


def calculate_efficiencies_of_codon_set(common_set, aa_set, codons_to_aa_dict):
    """
    Given a set of codons common to each amino acid in a set
    Use codons_to_aa_dict to look up which amino acids each codon encodes
    This looked up value is used to calculate efficiency
    :param common_set:
    :param aa_set:
    :param codons_to_aa_dict:
    :return:
    """
    efficiency_dict = {}
    for codon in common_set:
        efficiency_dict[codon] = calculate_codon_efficiency(codon, aa_set, codons_to_aa_dict)
    return efficiency_dict

def find_highest_values_efficiency_dict(efficiency_dict):
    """
    Given a dictionary of
    :param efficiency_dict:
    :return:
    """
    highvalue = 0
    highset = []
    for key in efficiency_dict:
        score = efficiency_dict[key]
        if score > highvalue:
            highvalue = score
            highset = []
            highset.append(key)
        elif score == highvalue:
            highset.append(key)
    return set(highset), highvalue

def extract_most_efficient_codons(common_set, aa_set, codons_to_aa_dict):
    """
    Provided with a set of codons that code for each amino acid in the input set
    Calculate the efficiency of each codon
    returns a list of the most efficient codons
    :param common_set:
    :param aa_set:
    :param codons_to_aa_dict:
    :return:
    """
    efficiency_dict = calculate_efficiencies_of_codon_set(common_set, aa_set, codons_to_aa_dict)
    return find_highest_values_efficiency_dict(efficiency_dict)

def check_for_stop_codon(codon_set):
    """
    Look up each codon in a set
    If any of them produce stop codons print out an informative message to the screen to inform the user
    Intentionally doesn't make decisions for users about validity of the codon
    :param codon_set:
    :return:
    """
    stop_codons = [codon for codon in codon_set if '*' in codons_to_aa_dict[codon]]
    if stop_codons:
        print(f"The following codons can produce stop codons: {stop_codons}")

##
#
# FUNCTIONS TO AID IN TRUNCATING A LIST OF AMINO ACIDS TO A SET OF 100% EFFICIENT IF THEY EXIST
#
##

def create_truncated_amino_acid_lists(aa_set):
    """
    For a given amino acid set of length n this will create all subsets of length n-1
    :param amino_acids:
    :return:
    """
    truncated_list = []
    for i in range(len(aa_set)):
        temp = list(aa_set)
        temp.pop(i)
        truncated_list.append(temp)
    return truncated_list

def create_all_truncated_sets(aa_set):
    """
    For the set of amino acids just brute force generate all possible
    sub sets for it.
    :param aa_set:
    :return:
    """
    full_list = []
    for L in range(len(aa_set) + 1):
        for subset in itertools.combinations(aa_set, L):
            full_list.append(list(subset))
    return full_list

def calculate_efficiencies_for_list_of_aa_lists(aa_sets):
    """
    For a list of sets, return a list where each
    element is a list of amino acids, the most efficient codons for it, and the efficiency score
    :param aa_sets:
    :return:
    """
    return [[aa, get_codon_for_amino_acids(aa,silent=True,validate=False)] for aa in aa_sets]



# Fill out COMPANY X functions
def get_codon_for_amino_acids(amino_acids,silent=False,validate=True):
    """
    :param amino_acids: set
        the amino acids we want to code for, i.e. {'A','I','V'}
    :rtype: set, float
        returns two values the set of most efficient codons for the input set list, e.g. {'RYA', 'RYH', 'RYC', 'RYW', 'RYM', 'RYY', 'RYT'} and the achieved efficiency e.g. 0.75
    """
    if validate:
        validate_amino_acid_set(amino_acids)
    common_set = get_common_codons_set(amino_acids, aa_to_codons_dict)
    best_codons = extract_most_efficient_codons(common_set, amino_acids, codons_to_aa_dict)
    if not silent:
        check_for_stop_codon(best_codons[0])
    return best_codons

def truncate_list_of_amino_acids(aa_set):
    """
    Provided a set of amino acids, find the smallest set of sets (by number of sets) that can be encoded for with 100%
    efficiency
    :param aa_set:
    :return:
    """
    efficiency_results = calculate_efficiencies_for_list_of_aa_lists([aa_set])
    efficiency = efficiency_results[0][1][1]
    if efficiency == 1:
        return aa_set
    if efficiency < 1:
        # Create all sub sets to calcualte efficiency on
        sub_sets = create_all_truncated_sets(aa_set)
        sub_sets.pop(0)
        sub_sets.reverse()
        # Evaluate each sub-sets' efficiency
        sub_set_efficiencies = calculate_efficiencies_for_list_of_aa_lists(sub_sets)
        # List any sub-sets that are efficient (i.e. efficiency == 1)
        efficient_subs = [sub[0] for sub in sub_set_efficiencies if sub[1][1] == 1]
        if efficient_subs:
            # Sets are already sorted from longest to shortest, so greedily add sets until there are no more amino acids to account for
            settled_aas = []
            short_sub_list = []
            for sub in efficient_subs:
                useful = False
                for aa in sub:
                    if not aa in settled_aas:
                        settled_aas.append(aa)
                        useful = True
                if useful == True:
                    short_sub_list.append(sub)
                    useful = False
            return set(frozenset(s) for s in short_sub_list)


def parent_function(calls,save=False):
    """
    This function invokes get_codon_for_amino_acids and truncate_list_of_amino_acids
    with random amino acid sets.
    Can use it to check how robust the functions are.
    :return:
    """
    meta_results = []
    for i in range(calls):
        aa_num = random.randint(1,10)
        aa_set = random.sample(valid_aa,aa_num)
        print(f'Process amino acid set: {aa_set}')
        best_codon = get_codon_for_amino_acids(aa_set,validate=False)
        truncated = truncate_list_of_amino_acids(aa_set)
        print(best_codon)
        print(truncated)
        print('')
        Run_info = {"amino acid set":aa_set,"get_codon_for_amino_acids":best_codon,"truncate_list_of_amino_acids":truncated}
        meta_results.append(Run_info)
    if save:
            with open("myfile.txt", 'w') as f:
                for Run_info in meta_results:
                    f.write('\n')
                    for key, value in Run_info.items():
                        f.write('%s:%s\n' % (key, value))

# Run Tests if function invoked at command line
if __name__ == "__main__":
    # using sets instead of lists throughout the code since the order doesn't matter and all items should be unique
    assert get_codon_for_amino_acids({'A', 'I', 'V'}) == ({'RYA', 'RYH', 'RYC', 'RYW', 'RYM', 'RYY', 'RYT'}, 0.75)
    assert get_codon_for_amino_acids({'M', 'F'}) == ({'WTS', 'WTK', "WTB"}, 0.5)
    # "frozenset" here since this seems to be the only way to get a set of sets - see https://stackoverflow.com/questions/5931291/how-can-i-create-a-set-of-sets-in-python
    assert truncate_list_of_amino_acids({'A', 'V', 'I'}) == {frozenset({'V', 'A'}), frozenset({'V', 'I'})}
