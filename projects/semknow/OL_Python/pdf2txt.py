from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from os.path import isfile, join
from os import listdir
from spacy.lang.en import English
nlp = English()
nlp.add_pipe(nlp.create_pipe('sentencizer'))

def main():
    """
    An algorithm that convert a list of pdf files into text files.
    DocsDir: a directory where pdf files exists
    DataDir: a directory where you want to save the results file
    """
    DocsDir= r".\pdf_docs"
    DataDir = r".\Corpus"
    alldocs = [f for f in listdir(DocsDir) if isfile(join(DocsDir, f)) and f.__contains__(".pdf")]
    for doc in alldocs:
        text = convert(join(DocsDir, doc))
        of = doc.replace(".pdf", ".txt")
        f1 = open(join(DataDir, of), 'w', errors='ignore')
        p = ""
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if line == "":
                continue
            if not line.endswith(".") and (len(line.split(" ")) >= 5 or len(p.split(" ")) >= 5) and len(lines[i+1].split(" ")) > 0:
                p += line.strip() + " "
                continue
            elif line.endswith("."):
                p += line
                if len(p.split(" ")) >= 5:
                    f1.write(preprocess(p) + "\n")
                p = ""
            else:
                if len(line.split(" ")) >= 5:
                    f1.write(preprocess(line) + "\n")
                p = ""

        f1.close()


def preprocess(file_str):
    doc = nlp(file_str)
    sents = [sent.string.strip() for sent in doc.sents]
    cleaned = list(map(lambda x: x.replace('-\n', '').replace('\n', ' ').replace(u'', 'fi'), sents))
    return '\n'.join(cleaned)

#converts pdf, returns its text content as a string
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return ' '.join(text.split())

if __name__ == '__main__':
    main()