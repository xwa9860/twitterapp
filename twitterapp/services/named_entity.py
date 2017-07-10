import nltk
from nltk.tokenize import word_tokenize
from nltk.tree import Tree
from twitterapp.models.model import Tweet


# NLTK POS and NER taggers
def nltk_tagger(token_text):
        tagged_words = nltk.pos_tag(token_text)
        ne_tagged = nltk.ne_chunk(tagged_words)
        return(ne_tagged)


def process_text():
    raw_text = Tweet.query.all()[:20]
    token_text = []
    for t in raw_text:
        token_text.extend(word_tokenize(t.tweet))
    return token_text


# Tag tokens with standard NLP BIO tags
def bio_tagger(ne_tagged):
    bio_tagged = []
    prev_tag = "O"
    for token, tag in ne_tagged:
        if tag == "O":
            bio_tagged.append((token, tag))
            prev_tag = tag
            continue
        if tag != "O" and prev_tag == "O":  # Begin NE
            bio_tagged.append((token, "B-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag == tag:  # Inside NE
            bio_tagged.append((token, "I-"+tag))
            prev_tag = tag
        elif prev_tag != "O" and prev_tag != tag:  # Adjacent NE
            bio_tagged.append((token, "B-"+tag))
            prev_tag = tag
    return bio_tagged


# Parse named entities from tree
def structure_ne(ne_tree):
    ne = []
    for subtree in ne_tree:
            if type(subtree) == Tree:  # If subtree is a noun chunk, i.e. NE != "O"
                    ne_label = subtree.label()
                    ne_string = " ".join([token for token, pos in subtree.leaves()])
                    ne.append((ne_string, ne_label))
    return ne


def nltk_main():
    print(structure_ne(nltk_tagger(process_text())))
