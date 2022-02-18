import spacy
from os import listdir
from os.path import isfile, join
nlp = spacy.load('en_core_web_sm')
from spacy.lang.en.stop_words import STOP_WORDS
stopWords = set(STOP_WORDS)

def main():
    """
    document terms extraction
    """
    #inputs
    corpus_dir = r".\Corpus" #directory for corpus documents
    output_dir = r".\OutputDir" #result files output directory
    output_file = output_dir + r"\ExtractedTerms.txt" #the path to save the extracted terms
    minFreq = 5 #minimum frequency threshold

    terms_file = open(output_file, "w", errors='ignore')
    #compute tf for each term in the corpus
    tf= computerTf(corpus_dir)
    #if tf of the term is greater than minimum freq save it to the output file
    for term, score in tf.items():
        if score >= minFreq:
            terms_file.write(str(term) + "\n")

def removeArticles(text):
    #remove stop words from the begining of a NP
    words = text.split()
    if words[0] in stopWords:
        return text.replace(words[0]+ " ", "")
    return text

def computerTf(dir):
    alldocs = [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]
    AllTerms = dict()
    for doc in alldocs:
        docText = open(doc, "r", errors='ignore').read()
        docParsing = nlp(docText)
        for chunk in docParsing.noun_chunks:
            np = removeArticles(chunk.text.lower())
            if np in stopWords:
                continue
            if np in AllTerms.keys():
                AllTerms[np] += 1
            else:
                AllTerms[np] = 1

    return AllTerms

if __name__ == '__main__':
    main()
