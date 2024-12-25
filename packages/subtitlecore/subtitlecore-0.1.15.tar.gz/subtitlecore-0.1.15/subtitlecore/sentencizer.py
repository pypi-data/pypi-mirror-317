from importlib import import_module
from subtitlecore.constants import SPACY_PKG
import spacy
#from spacy.tokenizer import Tokenizer
#import re

class Sentencizer:
  """Sentenize a subtitle line object using spacy nlp

  Args:
    lang (srt): language of text
  """

  def __init__(self, lang):
    self._nlp = spacy.load(SPACY_PKG[lang])
  
  def mark(self, line):
    """Parse text into sentences
    
    Args:
      line (str): A piece of text 
    
    Returns:
      list: A list of sentences
    """
    sens = []
    doc = self._nlp(line, disable=["tagger", "ner", "lemmatizer","textcat"])
    for s in doc.sents:
      e = s.text
      sens.append(e)
    return sens

