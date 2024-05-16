<b>Requirements</b>

 - Python 3
 
 
<b>Instructions</b>

- Extract the zipped file you are provided with.
- Install the required packages using `pip install -r requirements.txt`.
- Run the program using `python3 binary.py`.


<b>How it works:</b>

When the program is executed, the core handler is loaded serving the user with options to choose from.
These include:

- Generate: Generates binary files (`.bin` or `.img`) following variable starting addresses which are compliant with file sizes. The generated files are saved in the current working directory.

- Compare: Compares two binary files writing their differences to a `differences.txt` file if any. The supported binary files are of extension type `.bin` and `.img`. Others may work but have not been tested yet.


<b>Optional arguments:</b>

- `-o` or `--output` configures the output name for generated binary files.
- `-e` or `--extension` configures the file extension for generated binary files.


NOTE: Be patient when generating large binary files as the computation algorithm needs to process the bytes pattern.
A more recent CPU with some good memory would generally yield better performance.


<b>ENJOY!</b>
 