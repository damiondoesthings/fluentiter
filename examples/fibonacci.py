"""
You can even use fluentiter to make a very neat fibonacci one-liner ヽ(•‿•)ノ
"""
from fluentiter import iterator

if __name__ == "__main__":
    for e in iterator(range(10)).scan((0, 0), lambda s, x: ((s[1], sum(s) or x), sum(s) or x)):
        print(e)
