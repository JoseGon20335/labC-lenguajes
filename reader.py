class reader:
    def __init__(self, yalName):
        self.yalName = yalName

    def startReader(self):
        self.readFile()

    def readFile(self):
        # Open the file for reading
        with open(self.yalName, "r") as file:
            # Loop over each line in the file
            for line in file:
                # Loop over each character in the line
                for char in line:
                    # Do something with the character (e.g. print it)
                    print(char)
