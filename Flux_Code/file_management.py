import os

# Passes over all files in directory with specified extension
def file_generator(directory,extension):
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            yield filename

# Correct sensor output data extensions in directory
def format_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".xls"):
            filename = directory+"/"+filename
            pre, ext = os.path.splitext(filename)
            os.rename(filename, pre + ".txt")
            print("proccesed filename: " + filename)
