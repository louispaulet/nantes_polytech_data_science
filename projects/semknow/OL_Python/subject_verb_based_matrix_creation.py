import os
from common_functions import *
from collections import defaultdict


MIN_FREQ = 5 #frequency used to filter contexts


def main():
    """
    Create window-based co-occurence file
    """
    processed_corpus_dir = r".\OutputDir"
    freq_file = r".\OutputDir\freqTerms.txt"
    terms_file = r".\OutputDir\ExtractedTerms.txt"
    window_size = 5

    # Load the frequent words file
    with open(freq_file) as f_in:
        freq_words = set([line.strip() for line in f_in])
    with open(terms_file) as f_in2:
        terms = set([line.strip() for line in f_in2])

    cooc_mat = defaultdict(lambda: defaultdict(int))

    corpus_files = sorted([processed_corpus_dir + '/' + file for file in os.listdir(processed_corpus_dir) if str(file).__contains__("processed")])

    for file_num, corpus_file in enumerate(corpus_files):

        print('Processing corpus file %s (%d/%d)...' % (corpus_file, file_num + 1, len(corpus_files)))
        for sentence in get_sentences(corpus_file):
            update_window_based_cooc_matrix(cooc_mat, freq_words, sentence, window_size, terms)

    # Filter contexts to decrease sparsity
    frequent_contexts = filter_contexts(cooc_mat, 1)
    # Save the files
    save_file_as_Matrix1(cooc_mat, frequent_contexts, processed_corpus_dir, r"\sub_verb_matrix.csv", r"\sub_verb_matrix_terms.txt")
    save_file_as_Matrix12(cooc_mat, frequent_contexts, processed_corpus_dir, r"\sub_verb_matrix2.csv", r"\sub_verb_matrix_terms.txt")


def update_window_based_cooc_matrix(cooc_mat, freq_words, sentence, window_size, terms):
    """
    Updates the co-occurrence matrix with the current sentence
    :param cooc_mat: the co-occurrence matrix
    :param freq_words: the list of frequent words
    :param sentence: the current sentence
    :param window_size: the number of words on each side of the target
    :param directional: whether to distinguish between contexts before and after the target
    :return: the update co-occurrence matrix
    """

    # Remove all the non relevant words, keeping only NN, JJ and VB
    strip_sentence = [(w_word, w_lemma, w_pos, w_index, w_parent, w_dep) for
                      (w_word, w_lemma, w_pos, w_index, w_parent, w_dep) in sentence
            if str(w_pos).__eq__('NOUN') or str(w_pos).__eq__('PROPN') or str(w_pos).__eq__('VERB') or str(w_pos).__eq__('ADJ')]

    sent = getSentence(strip_sentence)
    for term in terms:
        Indexes = getIndexes(sent, term)
        if len(Indexes) > 0:
            term_words = term.split()
            for w in strip_sentence:
                word, _, _, _, parent, dep_rel = w
                if word in term_words and str(dep_rel) == "nsubj":
                    # if parent in freq_words:
                    print(parent)
                    context = parent
                    cooc_mat[term][context] = cooc_mat[term][context] + 1

    return cooc_mat

def getIndexes(sent, term):
    """
        Returns all indexes where a term occurs in a sentence
        :param sent: a sentence (space separated words)
        :param term: the term
        :return: list of indexes where the term occurs in the sentence
    """
    indexes = []
    if (" " + sent).__contains__( " " + term + " "):
        term2 = term.replace(" ", "_")
        sent = sent.replace(" " + term + " ", " " + term2 + " ")
        twords = [t for t in term2.strip().split()]
        swords = [st for st in sent.strip().split()]
        ln = len(term.strip().split()) - 1
        word = twords[0]
        while True:
            try:
                ind = swords.index(word)
                indlen = len(indexes)
                indexes.append(ind + (indlen * ln))
                swords[ind] = "_"
            except:
                break
    return indexes


if __name__ == '__main__':
    main()
