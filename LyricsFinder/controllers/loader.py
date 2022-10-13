import math

class Loader:

    def __init__(self, current=0, label="Loading", bars = 20, bar = "="):
        # Starting value of the loader
        self.current = current # Maximum value is 1
        self.label = label
        self.bars = bars
        self.bar = bar

    def print(self, end="\r"):
        # Prints the loader

        bars = math.floor(self.current * self.bars)

        print(" ", self.label, f"[{self.bar * bars}{' ' * (self.bars - bars)}] {round(self.current*100, 1)}%", end=end)

    def start(self):
        # start the loader
        self.print()

    def update(self, newValue, newLabel=None):
        self.current = newValue
        
        if newLabel != None:
            self.label = newLabel

        # Update current
        self.print()
    
    def close(self):
        # Close the loader
        self.print("\n")

    

        
