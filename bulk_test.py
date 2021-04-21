import json
from os import listdir
from os.path import isfile, join
# from tkinter import filedialog
from pycfg_ex import generate_cfg
from test import compare
from collapse_test import collapse

class Result:
    def __init__(self, filename, examplefile, results):
        self.filename = filename
        self.examplefile = examplefile
        self.results = results

class CompareResult:
    def __init__(self, nim, score, diff, details):
        self.nim = nim
        self.score = score
        self.diff = diff
        self.details = details

# root = tk.Tk()
# root.withdraw()

filename = "segiempat.py"
# print(filename)
dir = "../4661 Praktikum 3 Shift 4 - 15.45-17.45"
# print(dir)
# filename = input("Enter filename: ")
# examplefile = input("Enter path to example file: ")
names = [f for f in listdir(dir)]
# print(names)

examplefile = dir + '/' + names[0] + '/' + filename
example_graph = collapse(generate_cfg(examplefile))
results = []

for i in range(len(names)):
    nim = names[i].split()[0]
    try:
        test_file = dir +'/' + names[i] + '/' + filename
        test_graph = collapse(generate_cfg(test_file))
        score, diff, details = compare(example_graph, test_graph)
        
    except FileNotFoundError:
        score = 0
        diff = '-'
        details = "File not found"

    except:
        score = 0
        diff = '-'
        details = "Something went wrong"
    
    finally:
        result = CompareResult(nim, score, diff, details)
        results.append(json.dumps(result.__dict__))

    print(names[i])

final_result = Result(filename, examplefile, results)

with open('result.json', 'w') as output:
    json.dump(final_result.__dict__, output, ensure_ascii=False, indent=4)

output.close()

