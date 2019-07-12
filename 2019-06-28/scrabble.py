import numpy as np
import re
import timeit

letter_values_freqs = {
    0:  {'?': 2},
    1:  {'E': 12, 'A': 9, 'I': 9, 'O': 8, 'N': 6, 'R': 6, 'T': 6, 'L': 4, 'S': 4, 'U': 4},
    2:  {'D': 4, 'G': 3},
    3:  {'B': 2, 'C': 2, 'M': 2, 'P': 2},
    4:  {'F': 2, 'H': 2, 'V': 2, 'W': 2, 'Y': 2},
    5:  {'K': 1},
    8:  {'J': 1, 'X': 1},
    10: {'Q': 1, 'Z': 1}
}

values = {}
l = []
for value, freq in letter_values_freqs.items():
    for letter, count in freq.items():
        letter = letter.lower()
        values[letter] = value
        for _ in range(count):
            l.append(letter)
letters = np.array(l)
np.random.shuffle(letters)
x = "".join(letters)

def count(wm):
    return sum([values[l] for l in wm])

def letter_to_i(l):
    return ord(l)-ord('a')


words = dict()
with open('enable1.txt') as fh:
    for line in fh:
        w = line.strip()
        r = re.compile("".join(["["+l+"?]" for l in w]))
        words[w] = r

re_blank = re.compile('\?')

def calc_score(x):
    blist=[]
    for b in re_blank.finditer(x):
        blist.append(b.start(0))
    blist.sort()
    print(blist)

    scores = np.zeros(shape=(26,26))

    for w, r in words.items():
        matches = r.finditer(x)
        for m in matches:
            wm = m.group(0)
            wi = m.start(0)
            wv = count(wm)
            #print("%s %s pos=%d value=%d" % (w, wm, wi, wv))
            blanks = re_blank.finditer(wm)
            bi_local = []
            bl_local = []
            for b in blanks:
                bi = b.start(0)
                tbi = wi + bi
                bl = w[bi:bi+1]
                print ("    ", tbi, bl)
                bi_local.append(tbi)
                bl_local.append(bl)
            #print("    ",bi_local)
            #print("    ",bl_local)
            bi_local_len = len(bi_local)

            if bi_local_len == 0:
                scores[:,:] += wv
            elif len(bi_local) == 1:
                if bi_local[0] == blist[0]:
                    scores[letter_to_i(bl_local[0]),:] += wv
                elif bi_local[0] == blist[1]:
                    scores[:,letter_to_i(bl_local[0])] += wv
            elif len(bi_local) == 2:
                scores[letter_to_i(bl_local[0]),letter_to_i(bl_local[1])] += wv

        print(scores)
        print(scores.max())

print(x)
timeit.timeit('calc_score(x)', globals=globals())