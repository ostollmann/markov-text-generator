from __future__ import division, with_statement
from collections import Counter
from random import uniform, randint

from numpy import array, float32
import nltk

def learn_from_text_file(file_path):
    pass

def learn_from_text_files(dir_path):
    pass

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def tokenize(_str):
    tokens = nltk.word_tokenize(_str)
    tokens = tokenize_dots(tokens)
    tokens = filter(is_clean, tokens)
    tokens = map(lambda x: x.lower(), tokens)
    return tokens
    

def tokenize_dots(tokens):
    i = 0
    while i < len(tokens):
        ct = tokens[i]
        if ct != '.' and ct[-1] == '.':
            tokens[i] = ct[:-1]
            tokens.insert(i+1, '.') 
        i += 1
    return tokens

def is_clean(_str):
    if _str[0] in ('/', '\\'):
        return False
    if any(ord(c) > 127 for c in _str):
        return False
    if str in ("'", '"', '(', ')'):
        return False
    if "'" in _str:
        return False
    if '"' in _str:
        return False
    return True

def extract_tp(text, states=None, max_num_states_factor=0.4):
    
    if max_num_states_factor == 0:
        raise ValueError("max_num_states_factor cannot be 0.")
    
    if not states:
        must_learn_states = True
    
    tokens = tokenize(text)    
    
    if must_learn_states:
        count = Counter(tokens)
        num_states = int(len(count) * max_num_states_factor)
    
        states = count.most_common(num_states)    
        states = map(lambda x: x[0], states)
    else:
        num_states = len(states)
    
    # create empty transition probability matrix
    tp = array([[0]], dtype=float32)
    tp.resize(num_states,num_states) 
    
    num_tokens = len(tokens)
    i = 0
    while i < num_tokens-1:
        this_token = tokens[i]
        next_token = tokens[i+1]
        if this_token in states and next_token in states:
            tp[states.index(this_token), states.index(next_token)] += 1
        i += 1
    
    for i in xrange(len(tp)):
        s = sum(tp[i])
        if s != 0:
            tp[i] = tp[i] / sum(tp[i])
        
    
    return (states, tp)

# Text Generator

def generate(states, tp, num_words, first_word=None):
    r_min = 0.0000000000000001
    r_max = 0.9999999999999999 
    first_word = first_word.lower()
    if not first_word:
        first_word = states[randint(0,len(states)-1)]
    elif first_word not in states:
        print "First word '%s' not in states!" % first_word
        import sys
        sys.exit()
        
    text = [first_word]
    
    num_states = len(states)

    for n in xrange(num_words-1):
        r = uniform(r_min, r_max)
        cword = text[-1]
        tp_row = tp[states.index(cword)]
        ptotal = 0
        for m in xrange(num_states):
            ptotal += tp_row[m]
            if r <= ptotal:
                text.append(states[m])
                break
    return text
        

def make_nice_text(words, make_paragraphs=False, paragraph_prob=0.3):
    text = ''
    eos = True
    
    for i in xrange(len(words)):
        word = words[i]
        if eos:
            word = word.capitalize()
            if uniform(0,1) < paragraph_prob:
                word = '\n' + '\n' + word
            
        if word == 'i':
            word = 'I'
        if word in ('?', '!', '.', ';'):
            text += word
            eos = True
        elif word in ("'", ':', ','):
            text += word
            eos = False
        else:
            text += (' ' + word)
            eos = False
    
    return text[1:]

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    num_words = int(sys.argv[3])
    num_states_factor = float(sys.argv[4])

    print "Extracting transition probabilities from learning text '%s' (this may take a long time...)" % input_file
    states, tp = extract_tp(read_file(input_file), None, num_states_factor)

    print "Generating text (%s words)" % num_words
    text = make_nice_text(generate(states, tp, num_words, "The"), True, 0.2)
    
    if output_file != '-':
        print "Writing data to file '%s'" % output_file
        with open(output_file, 'w+') as file:
            file.write(text)
    else:
        print text
    
    
            
        
