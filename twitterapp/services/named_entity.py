import nltk
from nltk.tokenize import word_tokenize
from nltk.tree import Tree
from twitterapp.models.model import Tweet
from sqlalchemy import desc


# NLTK POS and NER taggers
def nltk_tagger(token_text):
    tagged_words = nltk.pos_tag(token_text)
    ne_tagged = nltk.ne_chunk(tagged_words)
    return(ne_tagged)


def process_text(label):
    if label is not None:
        raw_text = Tweet.query.order_by(desc(Tweet.id)).\
            filter(Tweet.sentiment == label)[:50]
    else:
        raw_text = Tweet.query.order_by(desc(Tweet.id)).all()[:50]

    token_text = []
    for t in raw_text:
        print(t.sentiment)
        token_text.extend(word_tokenize(t.tweet))
    return token_text


# tag tokens with standard nlp bio tags
def bio_tagger(ne_tagged):
    bio_tagged = []
    prev_tag = "o"
    for token, tag in ne_tagged:
        if tag == "o":
            bio_tagged.append((token, tag))
            prev_tag = tag
            continue
        if tag != "o" and prev_tag == "o":  # begin ne
            bio_tagged.append((token, "b-"+tag))
            prev_tag = tag
        elif prev_tag != "o" and prev_tag == tag:  # inside ne
            bio_tagged.append((token, "i-"+tag))
            prev_tag = tag
        elif prev_tag != "o" and prev_tag != tag:  # adjacent ne
            bio_tagged.append((token, "b-"+tag))
            prev_tag = tag
    return bio_tagged


# parse named entities from tree
def structure_ne(ne_tree):
    ne = []
    for subtree in ne_tree:
        if type(subtree) == Tree:
            ne_label = subtree.label()
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            ne.append((ne_string, ne_label))
    return ne


def nltk_main(label=None):
    texts = process_text(label)
    return structure_ne(nltk_tagger(texts))
