import os
import shutil
import random
from copy import copy

from app.parser import extract_text
from app.summarizer import SentenceScorer


# Summary dir names
current_dir = os.getcwd()

reference_dir = os.path.join(current_dir, "reference")
system_dir = os.path.join(current_dir, "system")
# Clean up before previous test runs
for pyrouge_dir in [reference_dir, system_dir]:
    if os.path.exists(pyrouge_dir):
        shutil.rmtree(pyrouge_dir)
    os.mkdir(pyrouge_dir)


def prepare_test(test_name, url, extract_sentence_fraction=0.25):
    # Get text by url and construct scorer
    _, text = extract_text(url)
    scorer = SentenceScorer(text)

    # Number of sentences in summary
    n = round(extract_sentence_fraction * scorer.n_sentences)

    tldr_bot_summary = " ".join(scorer.top_sentences(n))
    with open(os.path.join(system_dir, test_name + "_tldr_bot.txt"), "w") as text_file:
        text_file.write(tldr_bot_summary)

    first_sentences_summary = " ".join(scorer.sentences[:n])
    with open(os.path.join(reference_dir, test_name + "_first_sentences.txt"), "w") as text_file:
        text_file.write(first_sentences_summary)

    sentences = copy(scorer.sentences)
    random.shuffle(sentences)
    random_sentences_summary = " ".join(sentences[:n])
    with open(os.path.join(reference_dir, test_name + "_random_sentences.txt"), "w") as text_file:
        text_file.write(random_sentences_summary)


test_url_1 = "https://russian.rt.com/world/news/389212-britanec-ostanovil-sluchaino-virus"
test_url_2 = "http://www.rbc.ru/economics/13/05/2017/5917025d9a79472dc90b64bc?from=main"
test_url_3 = "https://medium.com/chris-messina/amazon-echo-show-354b93b448b5"

prepare_test("test1", test_url_1)
prepare_test("test2", test_url_2)
prepare_test("test3", test_url_3)
