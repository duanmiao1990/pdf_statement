import PyPDF2
import re
import pandas as pd
import sidetable
import yaml

pd.options.mode.chained_assignment = None

with open('config.yaml', 'rb') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


def extract_text(file):
    """
    purpose: return pdf texts
    file (string): pdf file path
    """
    texts = ""
    with open(file, 'rb'):
        pdfReader = PyPDF2.PdfFileReader(file)
        count = pdfReader.numPages
        print('# of pages %s' % count)
        for i in range(count):
            pageObj = pdfReader.getPage(i)
            contents = pageObj.extractText()
            texts += contents
    # combine fragment texts into one long text string
    result = " ".join(texts.split())
    return result


def extract_transactions(texts, regex):
    """
    purpose: extract all transactions (all info between opening balance & close balance)
    texts (string): pdf texts
    regex (string): regex pattern
    """
    # find all matches
    matches = re.findall(regex, texts)

    # convert parse result into pandas df
    df = pd.DataFrame(matches, columns=['Date', 'Transaction', 'Amount'])

    # translate amount string into float
    df['Amount'] = df['Amount'].str.replace('$', '').str.replace(',', '')
    df['Amount'] = df['Amount'].astype(float)
    return df

