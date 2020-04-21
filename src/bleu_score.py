#!/usr/bin/env python3
from sys import argv, exit
import math
import re
import string


def read_file(filepath):
    """Reads a file line by line
    Arguments: filepath -> String
    Return: List of Strings
    """
    with open(filepath, "r") as file:
        return list(map(lambda s: s.strip(), file.readlines()))


def tokenize(s):
    """Tokenize a string
    Arguments: s -> String
    Return: A list of words
    """
    _splited = s.split()
    regex = re.compile(f"[{re.escape(string.punctuation)}]")
    return list(map(lambda str: regex.sub("", str), _splited))


def n_grama(sentence, n):
    """Returns a words n_gram from a sentence
    Arguments: 
        sentence -> String
        n -> int
    """
    t = tokenize(sentence)
    n_grams = zip(*[t[i:] for i in range(n)])
    return list(map(lambda n_gram: ' '.join(n_gram), n_grams))


def calculate_bp_penality(candidate, reference):
    """ Calculates the Brevity Penalty for 2 sentences
    Arguments:
        candidate -> String
        reference -> String
    """
    c, r = len(tokenize(candidate)), len(tokenize(reference))
    return 1 if c > r else math.exp(1-(r/c))


def calculate_p(candidate, reference):
    """Calculates the relation between two n_grams
    Arguments:
        candidate -> List of tuples (n-grams)
        reference -> List of tuples (n-grams)
    """
    matches = 0
    for grama in candidate:
        if grama in reference:
            matches += 1
    return matches/len(candidate)


def calculate_bleu(candidate, reference):
    """Calculates the bleu score for 2 sentences
    Arguments:
        candidate -> String
        reference -> String
    """
    pn_sum = 0
    for n in range(1, 4):
        cand_grama, ref_grama = n_grama(candidate, n), n_grama(reference, n)
        p = calculate_p(cand_grama, ref_grama)
        if p != 0:
            # If there are no matches between n_grams,
            # don't add nothing
            pn_sum += (0.33 * math.log(p))
    bp = calculate_bp_penality(candidate, reference)
    return bp * math.exp(pn_sum)


def bleu_score(output, reference):
    """Calculates and prints each bleu score for each sentence on the texts
    Arguments: 
        output -> List of Strings (List of sentences)
        reference -> List of Strings (List of sentences)        
    """
    num_sentences = min(len(output), len(reference))
    for i in range(num_sentences):
        if i == 5:
            print("Do you want to calculate all sentences? (y/n)")
            answer = input()
            if answer.lower() == 'n':
                break
        out_sentence, ref_sentence = output[i], reference[i]
        bleu_score = calculate_bleu(out_sentence, ref_sentence)
        print(
            f"Sentence {i + 1}, Score: {bleu_score}")


if __name__ == "__main__":
    if len(argv) != 3:
        print("bleu_score.py <output file> <reference file>")
        exit()
    out_path, ref_path = argv[1], argv[2]
    output, reference = read_file(out_path), read_file(ref_path)
    bleu_score(output, reference)
