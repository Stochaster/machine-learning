""Count words."""

def count_words(text):
    """Count how many times each unique word occurs in text."""
    counts = dict()  # dictionary of { <word>: <count> } pairs to return
    
    # TODO: Convert to lowercase
    textl = text.lower()
    
    # TODO: Split text into tokens (words), leaving out punctuation
    # (Hint: Use regex to split on non-alphanumeric characters)
    import re
    nop = re.sub(r'[^\w\s]','',textl)  #remove punctuation
    #cleantext = re.split('[ ]', nop)
    #cleantext = re.split('[^a-zA-Z0-9]', nop)
    cleantext = re.split('[ \t\n\r\f\v]', nop)
    #cleantext = re.findall('[a-zA-Z]', text)
    #cleantext = re.findall(r"\w+",text)
    #cleantext = re.sub(r"[^a-zA-Z0-9]", " ", text)
    print(cleantext)
    
    # TODO: Aggregate word counts using a dictionary
    words = text.split()
    countsagg = dict([(i, cleantext.count(i)) for i in set(cleantext)])
    print(countsagg)
    
    return countsagg


def test_run():
    with open("input.txt", "r") as f:
        text = f.read()
        #text = 'The hammer and the nail.'
        #text = 'Buffalo buffalo Buffalo, buffalo buffalo!'
        counts = count_words(text)
        sorted_counts = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
        
        print("10 most common words:\nWord\tCount")
        for word, count in sorted_counts[:10]:
            print("{}\t{}".format(word, count))
        
        print("\n10 least common words:\nWord\tCount")
        for word, count in sorted_counts[-10:]:
            print("{}\t{}".format(word, count))


if __name__ == "__main__":
    test_run()
