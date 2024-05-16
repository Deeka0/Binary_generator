
from os import system, remove
from os.path import dirname, join, isfile
from time import time, sleep
from sys import platform, exit
from argparse import ArgumentParser

try:
    from numpy import zeros, arange, uint8
    from numpy.random import randint
except (ImportError, ModuleNotFoundError):
    print("\nNumpy Module is not installed")
    exit("Without the quotes, run 'pip install numpy' in the terminal to install Numpy")

parser = ArgumentParser(
    prog="Binary Generator",
    description="Generates binary files",
    epilog="Let's demonize bytes",
)
parser.add_argument("-o", "--output")
parser.add_argument("-e", "--extension")
args = parser.parse_args()

output = "test" # Default file name
extension = "bin" # Default file extension

if args.output is not None:
    output = args.output # File name if -o argument is passed

if args.extension is not None:
    extension = args.extension # File extension if -e argument is passed

runtime_path = dirname(__file__)
bin_file = join(runtime_path, f"{output}.{extension}")
diff_file = join(runtime_path, "differences.txt")

if platform not in ("darwin", "linux", "win32"):
    exit("OS not available yet")

if platform == "win32":
    clear_arg = "cls"
    splitter = "\\"
else:
    clear_arg = "clear"
    splitter = "/"


def clear(command: str) -> None:
    """
    Clears the screen
    """
    return system(command)


class Binary:
    """
    Computes some random binary methods
    """
    def generate_data(self, length: int, start_value: int) -> bytes:
        """
        Generates incremental binary data while randomizing every fourth byte
        """
        chunk = zeros(length, dtype=uint8) # Creates an array of length bytes
        chunk[:] = (start_value + arange(length)) % 256 # Increments the starting values for each byte

        # Randomizes the fourth byte in each group of four
        random_indices = arange(3, length, 4)
        chunk[random_indices] = randint(0, 256, len(random_indices))
        return chunk


    def core_gen(self):
        # Get data size input from user
        try:
            clear(command=clear_arg)
            print("Press CTRL + C to exit")
            print()
            user_length = int(input("How much data (MB) do you want to generate? ").strip())
        except ValueError:
            print("\nERROR! Invalid data size")
            sleep(1)
            return self.core_gen()
        else:
            address = user_length // 1024
            data_length = 1048576 * user_length  # Computes the length of binary data
            CHUNK_SIZE = 536870912  # Chunk size in bytes (1024 ** 3) // 2
            print()
            print(f"* Generated file would be named '{output}.bin'")
            print(f"  - Starting address is 0{address}")
            print("  - Generating and writing binary data ...")

        # Generate binary data
        try:
            start = time()
            with open(bin_file, 'wb') as outfile:
                while data_length > 0:
                    chunk_size = min(data_length, CHUNK_SIZE)
                    binary_data = self.generate_data(length=chunk_size, start_value=address)
                    outfile.write(binary_data)

                    data_length -= chunk_size
                    address += chunk_size  # Increments the start value for next chunk 

            stop = time()
            print(f"  - Data written in {stop - start:.5f} second(s)") 

        except MemoryError:
            exit("\nERROR! Out of memory")
        except KeyboardInterrupt:
            remove(bin_file)
            exit("\nInterrupted by user")
        else:
            print("* Done")


    def compare(self, file1: str, file2: str) -> None:
        """
        Compares two binary files outputting their differences if any
        """
        with open(file1, "rb") as f1, open(file2, "rb") as f2:
            
            with open(diff_file, "w") as file:

                def check_if_identical(is_identical):
                    if is_identical:
                        print("- Files are identical")
                        remove(diff_file)
                    else:
                        print("- Files are not identical")

                identical = True
                while True:
                    byte1 = f1.read(1).hex()
                    byte2 = f2.read(1).hex()

                    # Checks if both files have reached EOF
                    if not byte1 and not byte2:
                        check_if_identical(is_identical=identical)
                        break

                    # Checks if only one file has reached EOF
                    elif not byte1 or not byte2:
                        if not byte1:
                            print(f"{file1.split(splitter)[-1]} ended.")
                        elif not byte2:
                            print(f"{file2.split(splitter)[-1]} ended.")
                        check_if_identical(is_identical=identical)
                        break

                    # Compares bytes
                    if byte1 != byte2:
                        identical = False
                        file.write(f"Difference found at address {hex(f1.tell() - 1)}: {byte1} vs {byte2}\n")

                print("* Read complete")


    def core_compare(self) -> None:
        clear(command=clear_arg)
        print("Press CTRL + C to exit")
        print()

        def strip_literals(file, literals = ["'", '"']):
            for i in literals:
                if file.startswith(i):
                    file = file.removeprefix(i)
                if file.endswith(i):
                    file = file.removesuffix(i)
            return file

        file1 = strip_literals(file=input("Input path to the first file: ").strip())
        file2 = strip_literals(file=input("Input path to the second file: ").strip())
        print()

        invalid = False
        for i in (file1, file2):
            if (not isfile(i)):
                print(f"Invalid file at {i}")
                invalid = True

        if invalid:
            sleep(2)
            return self.core_compare()
        
        print(f"* Comparing files ...")
        try:
            self.compare(file1=file1, file2=file2)
            exit(0)
        except MemoryError:
            exit("\nERROR! Out of memory")
        except KeyboardInterrupt:
            exit("\nInterrupted by user")


def run() -> None:
    """
    Core Handler
    """
    char = ('1','2','x')
    clear(command=clear_arg)

    print("\tChoose an option:\n")
    print("1. Generate")
    print("2. Compare")
    print()
    print("X. Exit")

    asker = input("\nEnter here: ").lower().strip()
    if asker not in char:
        print("Invalid option!")
        sleep(1)
        return run()
    
    elif asker == 'x':
        clear(command=clear_arg)
        exit("Exiting")
    
    bin = Binary()
    if asker == "1":
        bin.core_gen()
    elif asker == '2':
        bin.core_compare()




if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        exit("\nInterrupted by user!")


