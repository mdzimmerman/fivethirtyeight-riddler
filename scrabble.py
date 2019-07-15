from deap import base, creator, tools
import numpy as np
import re
import random

class Scrabble(object):
    LETTERS_VALUES_FREQS = {
        0:  {'?': 2},
        1:  {'E': 12, 'A': 9, 'I': 9, 'O': 8, 'N': 6, 'R': 6, 'T': 6, 'L': 4, 'S': 4, 'U': 4},
        2:  {'D': 4, 'G': 3},
        3:  {'B': 2, 'C': 2, 'M': 2, 'P': 2},
        4:  {'F': 2, 'H': 2, 'V': 2, 'W': 2, 'Y': 2},
        5:  {'K': 1},
        8:  {'J': 1, 'X': 1},
        10: {'Q': 1, 'Z': 1}
    }

    def __init__(self):
        self.values, self.letters = self._set_values()
        self.words = self._set_words()
        self.re_blank = re.compile('\?')

    def _set_values(self):
        values = {}
        l = []
        for value, freq in Scrabble.LETTERS_VALUES_FREQS.items():
            for letter, count in freq.items():
                letter = letter.lower()
                values[letter] = value
                for _ in range(count):
                    l.append(letter)
            letters = "".join(np.array(l))
        return values, letters

    def _set_words(self):
        words = {}
        with open('enable1.txt') as fh:
            for line in fh:
                w = line.strip()
                r = re.compile("".join(["["+l+"?]" for l in w]))
                words[w] = r
        return words

    def score_word(self, word):
        return sum([self.values[l] for l in word])

    def letter2i(self, l):
        return ord(l)-ord('a')

    def shuffle(self, s):
        w = list(s)
        random.shuffle(w)
        return "".join(w)

    def create_random(self):
        return self.shuffle(self.letters)

    def calc_score(self, s):
        s="".join(s)
        bpos=[]
        for b in self.re_blank.finditer(s):
            bpos.append(b.start(0))
        bpos.sort()
        #print(bpos)

        scores = np.zeros(shape=(26,26))

        for w, r in self.words.items():
            matches = r.finditer(s)
            for m in matches:
                wm = m.group(0)
                wi = m.start(0)
                wv = self.score_word(wm)
                #print("%s %s pos=%d value=%d" % (w, wm, wi, wv))
                blanks = self.re_blank.finditer(wm)
                bi_local = []
                bl_local = []
                for b in blanks:
                    bi = b.start(0)
                    tbi = wi + bi
                    bl = w[bi:bi+1]
                    #print ("    ", tbi, bl)
                    bi_local.append(tbi)
                    bl_local.append(bl)
                #print("    ",bi_local)
                #print("    ",bl_local)
                bi_local_len = len(bi_local)

                if bi_local_len == 0:
                    scores[:,:] += wv
                elif len(bi_local) == 1:
                    if bi_local[0] == bpos[0]:
                        scores[self.letter2i(bl_local[0]),:] += wv
                    elif bi_local[0] == bpos[1]:
                        scores[:,self.letter2i(bl_local[0])] += wv
                elif len(bi_local) == 2:
                    scores[self.letter2i(bl_local[0]),self.letter2i(bl_local[1])] += wv

        #print(scores)
        return scores.max()

s = Scrabble()
for _ in range(10):
    x = s.shuffle(s.letters)
    print(x)
    print(s.calc_score(x))
#
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
#
toolbox = base.Toolbox()

toolbox.register("letters", random.sample, s.letters, len(s.letters))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.letters)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", s.calc_score)

#toolbox.evaluate(x[0])

toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.01)
toolbox.register("select", tools.selTournament, tournsize=10)