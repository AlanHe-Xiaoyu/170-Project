import os
for root, dirs, files in os.walk("."):
    for filename in files:
        inputName = filename[:-3]+"in"
        inputPath = "./inputs/"+inputName
        if os.path.exists(inputPath):
            os.system("mv "+ inputPath + " " + "./processed_inputs/")
            print("removed")
    