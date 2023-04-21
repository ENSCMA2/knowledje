import csv
import nltk
import json
nltk.download("punkt")
from nltk.tokenize import word_tokenize

def edits1(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]  
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces   = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts) 

def editsl1(words):
    return set.union(*[edits1(w) for w in words])

def edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

def editsl2(words):
    return set.union(*[edits2(w) for w in words])

def editslu2(words):
    return set.union(editsl1(words), editsl2(words))

def edits3(word):
    return set(e3 for e2 in edits2(word) for e3 in edits1(e2))

def editsl3(words):
    return set.union(*[edits3(w) for w in words])

def editslu3(words):
    return set.union(editslu2(words), editsl3(words))

def edits4(word):
    return set(e4 for e3 in edits3(word) for e4 in edits1(e3))

def editsl4(words):
    return set.union(*[edits4(w) for w in words])

def editslu4(words):
    return set.union(editslu3(words), editsl4(words))

def edits5(word):
    return set(e5 for e4 in edits4(word) for e5 in edits1(e4))

def editsl5(words):
   return set.union(*[edits5(w) for w in words])

def editslu5(words):
   return set.union(editslu4(words), editsl5(words))

def get_ngrams(post):
    unigrams = word_tokenize(post)
    bigrams = [unigrams[i] + " " + unigrams[i + 1] for i in range(len(unigrams) - 1)]
    trigrams = [unigrams[i] + " " + unigrams[i + 1] + " " + unigrams[i + 2] for i in range(len(unigrams) - 2)]
    # fourgrams = [" ".join(unigrams[i:i + 4]) for i in range(len(unigrams) - 3)]
    # fivegrams = [" ".join(unigrams[i:i + 5]) for i in range(len(unigrams) - 4)]
    allgrams = set.union(set(unigrams), # editsl1(unigrams) if len(unigrams) > 0 else set(), 
                         set(bigrams), # editsl1(bigrams) if len(bigrams) > 0 else set(), 
                         set(trigrams)) # , editsl1(trigrams) if len(trigrams) > 0 else set()) #, 
                         # fourgrams, editslu4(fourgrams), 
                         # fivegrams, editslu5(fivegrams))
    return allgrams

def get_context(post, kg):
    ngrams = get_ngrams(post)
    context = ""
    with open(kg, "rb") as kg_file:
        knowledge = json.load(kg_file)
    for ngram in ngrams:
        try:
            info = knowledge[ngram.lower()]
            if info["type"] == "event":
                context += "event name: " + ngram.lower() + ", event description: " + info["description"] + " "
            elif info["type"] == "person":
                context += "person name: " + ngram.lower() + ", person description: " + info["description"] + " "
            elif info["type"] == "place":
                context += "place name: " + ngram.lower() + ", "
                for event in info["events"]:
                    try:
                        event_info = knowledge[event]
                        if event_info["type"] == "event":
                            context += "event name: " + event + ", event description: " + event_info["description"] + " "
                        else:
                            print("forgot to account for " + event_info["type"] + " in " + ngram.lower())
                    except:
                        print("forgot to put in " + event + " under " + str(info))
            elif info["type"] == "slur":
                context += "slur name: " + ngram.lower() + ", slur description: " + info["description"] + " "
            elif info["type"] == "publication":
                context += "publication name: " + ngram.lower() + ", publication description: " + info["description"] + " "
            elif info["type"] == "date":
                context += "date: " + ngram.lower() + ", "
                for event in info["events"]:
                    try:
                        event_info = knowledge[event]
                        if event_info["type"] == "event":
                            context += "event name: " + event + ", event description: " + event_info["description"] + " "
                        elif event_info["type"] == "publication":
                            context += "publication name: " + event + ", publication description: " + event_info["description"] + " "
                        elif event_info["type"] == "organization":
                            context += "organization name: " + event + ", organization description: " + event_info["description"] + " "
                        else:
                            print("forgot to account for " + event_info["type"] + " in " + ngram.lower())
                    except:
                        print("forgot to put in " + event + " under " + str(info))
            elif info["type"] == "organization":
                context += "organization name: " + ngram.lower() + ", organization description: " + info["description"] + " "
            elif info["type"] == "product":
                context += "product name: " + ngram.lower() + ", product description: " + info["description"] + " "
            else:
                print("forgot to account for", info["type"])
        except:
            continue
    if len(context) > 0 and len(context) < 1500:
        print(context)
    return context

def get_augmented_post(post, kg):
    return get_context(post, kg) + "[SEP]  " + post

def get_final_dataset(data_file, kg, out_file, id_first = False):
    with open(data_file, "r+") as o:
        rows = list(csv.reader(o, delimiter = "\t"))
        if id_first:
            posts = [row[1] for row in rows][1:]
            labels = [row[2] for row in rows][1:]
            ids = [row[0] for row in rows][1:]
        else:
            posts = [row[0] for row in rows][1:]
            labels = [row[1] for row in rows][1:]
        print("there are", len(posts), "posts for", data_file)
        augmented_posts = [get_augmented_post(post, kg) for post in posts]
        with open(out_file, "w") as o:
            writer = csv.writer(o, delimiter = "\t")
            writer.writerow(rows[0])
            for i in range(len(augmented_posts)):
                if id_first:
                    writer.writerow([ids[i], augmented_posts[i], labels[i]])
                else:
                    writer.writerow([augmented_posts[i], labels[i]])

get_final_dataset("/n/home04/khalevy/hate_speech_detection/data/post_level/echo_posts_2_labels.tsv", 
                  "/n/home04/khalevy/hate_speech_detection/data/post_level/kg.json",
                  "/n/home04/khalevy/hate_speech_detection/data/post_level/echo_kg_sep.tsv", False)
