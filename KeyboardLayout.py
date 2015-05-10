from os import listdir
from os import path
from itertools import izip_longest


def loadLayouts(directory):
    files = listdir(directory)
    files = [f for f in files if path.splitext(f)[1] == ".txt"]
    return sorted([KeyboardLayout(f, directory) for f in files],
                  key=lambda x: (x.name != "native", x.name))


class KeyboardLayout:
    def __init__(self, filename, basepath):
        self.name = path.splitext(filename)[0]
        state = 0
        self.layout = []
        self.layout.append([])
        with open(path.join(basepath, filename)) as f:
            lines = f.readlines()
            for line in lines:
                if line == "\n":
                    state += 1
                    self.layout.append([])
                else:
                    self.layout[state].append(unicode(line[:-1], encoding="utf-8"))

    def convertTo(self, text, layout):
        conversion = dict()
        for srcLayer, dstLayer in izip_longest(self.layout, layout.layout):
            if srcLayer is not None and dstLayer is not None:
                for srcRow, dstRow in izip_longest(srcLayer, dstLayer):
                    if srcRow is not None and dstRow is not None:
                        for srcChar, dstChar in izip_longest(srcRow, dstRow):
                            if srcChar is not None and dstChar is not None:
                                conversion[dstChar] = srcChar

        return "".join([conversion[c] if c in conversion else c for c in text])
