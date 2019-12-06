import os
print("start")
for root, dirs, files in os.walk("../processed_inputs"):
    for filename in files:
        outputName = filename[:-2] + "out"
        outputPath = "../outputs/" + outputName
        if os.path.exists(outputPath) or filename[-2:] != 'in':
            pass
        else:
            os.system("python3 ../solver.py "+ filename + " " + "../outputs")
            print("processed")
    