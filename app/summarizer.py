# -*- coding: utf-8 -*-
from langdetect import detect
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

from string import punctuation
from itertools import groupby
from math import sqrt, log
from operator import itemgetter


class SentenceScorer:
    def __init__(self, text):
        self.raw_text = text
        self.language = self._language_code_dict[detect(text)]
        self._stopwords_set = stopwords.words(self.language)
        self._stemmer = SnowballStemmer(self.language)
        self.tokens = self._tokenize_clean_stem(text)
        self.n_tokens = len(self.tokens)
        self.sentences = sent_tokenize(text)
        self.n_sentences = len(self.sentences)

        self._tf = dict([(i, self._tf_repr(s))
                         for i, s in zip(range(self.n_sentences),
                                         self.sentences)])
        self._idf = \
            dict([(term, log(float(self.n_sentences)/self._term_occur(term)))
                  for term in set(self.tokens)])

        # Sentence position index with score
        self.sentence_centrality_scores = \
            dict([(i, self._sentence_centrality_score(s))
                  for i, s in zip(range(self.n_sentences),
                  self.sentences)])

    def sentence_centrality_score(self, sent):
        return self.sentence_centrality_scores[sent]

    def top_sentences(self, sent_count):
        top_sent_ind = \
            list(map(lambda ind_score: ind_score[0],
                     reversed(sorted(self.sentence_centrality_scores.items(),
                                     key=itemgetter(1)))))[:sent_count]
        return [self.sentences[ind] for ind in sorted(top_sent_ind)]

    # Mapping between ISO code, returned with langdetect
    # and language name in nltk.stopwords
    _language_code_dict = {
        "ru": "russian",
        "en": "english"
    }

    @staticmethod
    def _remove_punctuation(s):
        return "".join((char for char in s
                        if char not in punctuation + "«»—")).strip()

    def _remove_stopwords(self, words):
        return [word for word in words
                if words not in self._stopwords_set]

    def _tokenize_clean_stem(self, text):
        return list(filter(lambda s: len(s) > 0,
                           map(lambda s: self._stemmer.stem(s),
                               filter(lambda w: w not in self._stopwords_set,
                                      map(self._remove_punctuation,
                                          word_tokenize(text))))))

    def _tf_repr(self, sent):
        tokens = self._tokenize_clean_stem(sent)
        return dict([(token, len(list(group)))
                     for token, group in groupby(tokens)])

    def _term_occur(self, term):
        return len(list(filter(lambda tf: tf.get(term, 0) > 0,
                               self._tf.values())))

    def _tf_idf_norm(self, tf):
        return sqrt(sum([(tf[t] * self._idf[t]) ** 2 for t in tf.keys()]))

    def _tf_idf_cos_sim(self, s1, s2):
        tf_s1, tf_s2 = map(lambda s: self._tf[self.sentences.index(s)],
                           (s1, s2))
        common_tokens = set(tf_s1.keys()).intersection(tf_s2.keys())
        tf_idf_norm1, tf_idf_norm2 = map(self._tf_idf_norm, (tf_s1, tf_s2))
        return sum([tf_s1[t] * tf_s2[t] * (self._idf[t]) ** 2
                    for t in common_tokens]) / (tf_idf_norm1 * tf_idf_norm2)

    def _sentence_centrality_score(self, sent):
        return 1. / self.n_sentences * \
               sum([self._tf_idf_cos_sim(sent, other_sent)
                    for other_sent in self.sentences
                    if other_sent != sent])


def summarize_text(text, extract_sentence_fraction=0.25, upper_bound=4096):
    scorer = SentenceScorer(text)
    extract_sent_count = round(extract_sentence_fraction * scorer.n_sentences)
    extract_sentences = scorer.top_sentences(extract_sent_count)
    extract = " ".join(extract_sentences)

    while len(extract) > upper_bound:
        extract_sent_count -= 1
        extract_sentences = scorer.top_sentences(extract_sent_count)
        extract = " ".join(extract_sentences)
    return extract
