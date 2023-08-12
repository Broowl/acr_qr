# A QR-Code generator and scanner
Both the scanner and the generator have a graphical user interface (GUI).
The generator creates digitally signed QR codes intended for e-tickets.
The scanner decodes the information in the generated QR codes and verifies the signature.

# Setup development environment

1. Install pipenv with `pip install --user pipenv`
2. Run `pipenv sync` to install the required dependencies
3. Open the project in VS Code
4. Install the recommended extensions
5. Select the *pipenv* as Python interpreter

# Distribution

To create executables for the generator and the scanner run `deploy.ps1`.
Afterwards you can find the packaged executables in the *dist* folder.