import os
from common_functions import *
from collections import defaultdict
from spacy.lang.en.stop_words import STOP_WORDS
stopWords = set(STOP_WORDS)

MIN_FREQ = 10 #frequency used to filter contexts and couples
def main():
    """
    Create couple, context between Matrix
    """
    processed_corpus_dir = r".\OutputDir" #the directory where compressed file of the processed corpus exist
    terms_file = r".\OutputDir\ExtractedTerms.txt" #the path for the extracted terms (NPs) file

    # Load the frequent terms file
    with open(terms_file) as f_in2:
        terms = set([line.strip() for line in f_in2])

    cooc_mat = defaultdict(lambda: defaultdict(int))

    corpus_files = sorted([processed_corpus_dir + '/' + file for file in os.listdir(processed_corpus_dir) if str(file).__contains__("processed")])

    for file_num, corpus_file in enumerate(corpus_files):

        print ('Processing corpus file %s (%d/%d)...' % (corpus_file, file_num + 1, len(corpus_files)))
        for sentence in get_sentences(corpus_file):
            update_window_based_cooc_matrix(cooc_mat, sentence, terms)

    # Filter contexts to decrease the sparsity of data
    frequent_contexts = filter_contexts(cooc_mat, MIN_FREQ)
    # Filter couples
    frequent_couples = filter_couples(cooc_mat, MIN_FREQ)
    # Save the files
    save_file_as_Matrix(cooc_mat, frequent_contexts, processed_corpus_dir, r"\coupleMatrix.csv", r"\MatrixCouples.txt", frequent_couples)
    save_file_as_Matrix2(cooc_mat, frequent_contexts, processed_corpus_dir, r"\coupleMatrix2.csv", frequent_couples)
    return

def update_window_based_cooc_matrix(cooc_mat, sentence, terms):
    """
    Updates the co-occurrence matrix with the current sentence
    :param cooc_mat: the co-occurrence matrix
    :param sentence: the current sentence
    :param terms: list of extracted terms in the process of terms extraction
    :return: the update co-occurrence matrix
    """

    # Remove all the non relevant words, keeping only Nouns, Adj, Pronouns, and Verbs
    strip_sentence = [(w_word, w_lemma, w_pos, w_index, w_parent, w_dep) for
                      (w_word, w_lemma, w_pos, w_index, w_parent, w_dep) in sentence
        if str(w_pos).__eq__('NOUN') or str(w_pos).__eq__('PROPN') or str(w_pos).__eq__('VERB') or str(w_pos).__eq__('ADJ')]

    sent = getSentence(strip_sentence)
    terms = list(terms)
    for i in range(0, len(terms)):
        t1= terms[i]
        if (" " + sent).__contains__(" " + t1 + " "):
            for j in range(0, len(terms)):
                if j == i:
                    continue
                t2 = terms[j]
                if (" " + sent).__contains__(" " + t2 + " "):
                    contexts = getContexts(sent, t1, t2)
                    couple = t1 + "\t" + t2
                    for context in contexts:
                        cooc_mat[couple][context] = cooc_mat[couple][context] + 1
    return cooc_mat

def getContexts(sent, t1, t2):
    """
        Returns list of contexts words between the two given terms in the given sentence
        :param sent: a sentence (space separated words)
        :param t1: the first term
        :param t2: the second term
        :return: list of context words between t1 and t2
    """
    #replace _ instead of space in multi-words terms (french navy --> french_navy) in the sentence.
    term1 = t1.strip().replace(" ", "_")
    sent = sent.replace(" " + t1 + " ", " " + term1 + " ")
    term2 = t2.strip().replace(" ", "_")
    sent = sent.replace(" " + t2 + " ", " " + term2 + " ")

    #split the sentence into list of words.
    swords = [st for st in sent.strip().split()]
    indexes1 = []
    indexes2 = []

    #get the indexes where t1 occurs in the sentence.
    while True:
        try:
            ind = swords.index(term1)
            indexes1.append(ind)
            swords[ind] = "_"
        except:
            break

    # get the indexes where t2 occurs in the sentence.
    while True:
        try:
            ind = swords.index(term2)
            indexes2.append(ind)
            swords[ind] = "_"
        except:
            break

    #get the context between the two terms if the t1 and t2 are seperated by at least 1 word and at most 5 words
    #1 and 5 can be changed based on your point of view
    context = []
    for index1 in indexes1:
        for index2 in indexes2:
            if abs(index2 - index1) > 1 and abs(index2 - index1) <= 5:
                    for i in range(min(index1,index2) + 1, max(index1,index2)):
                        context.append(swords[i])
    return context


if __name__ == '__main__':
    main()
