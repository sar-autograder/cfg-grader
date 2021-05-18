import json
from os import listdir
from os.path import isfile, join
# from tkinter import filedialog
from pycfg_ex import generate_cfg
from test import compare
from collapse_test import collapse
from blackbox import blackbox
import xlsxwriter

class Result:
    def __init__(self, filename, examplefile, results):
        self.filename = filename
        self.examplefile = examplefile
        self.results = results

# class CompareResult:
#     def __init__(self, nim, whitescore, blackscore, whitediff, details):
#         self.nim = nim
#         self.whitescore = whitescore
#         self.blackscore = blackscore
#         self.diff = diff
#         self.details = details

# root = tk.Tk()
# root.withdraw()

filename = "segiempat.py"
testcasepath = "testcase/segiempat/"
# print(filename)
dir = "../4661 Praktikum 3 Shift 4 - 15.45-17.45"
# print(dir)
# filename = input("Enter filename: ")
# examplefile = input("Enter path to example file: ")
names = [f for f in listdir(dir)]
# print(names)

examplefile = "segiempatcontoh.py"
example_graph = collapse(generate_cfg(examplefile))
results = []

for i in range(len(names)):
    nim = names[i].split()[0]
    test_file = dir +'/' + names[i] + '/' + filename
    try:
        test_graph = collapse(generate_cfg(test_file))
        whitescore, diff, details = compare(example_graph, test_graph)
        
    except FileNotFoundError:
        whitescore = 0
        diff = '-'
        details = "File not found"

    except:
        whitescore = 0
        diff = '-'
        details = "Something went wrong"
    
    finally:
        blackscore = blackbox(testcasepath, test_file, 50)
        result = {
            "nim" : nim,
            "whitescore" : whitescore,
            "blackscore" : blackscore,
            "diff" : diff,
            "details" : details
        }
        results.append(result)

    print(names[i])

# final_result = Result(filename, examplefile, results)

# with open('result.json', 'w') as output:
#     json.dump(final_result.__dict__, output, ensure_ascii=False, indent=4)

# output.close()

workbook = xlsxwriter.Workbook('results/' + filename[:-3] + '.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, "NIM")
worksheet.write(0, 1, "Whitescore")
worksheet.write(0, 2, "Blackscore")
worksheet.write(0, 3, "Total Cost")
worksheet.write(0, 4, "Details")

for i in range(len(results)):
    result = results[i]
    worksheet.write(i+1, 0, result['nim'])
    worksheet.write(i+1, 1, result['whitescore'])
    worksheet.write(i+1, 2, result['blackscore'])
    worksheet.write(i+1, 3, result['diff'])
    worksheet.write(i+1, 4, str(result['details']))

workbook.close()