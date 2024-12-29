Random name generator.
Random email generator.
Random age generator. 

## Doel van het programma
Als developer wil je soms je database populeren met gebruikers om testen uit te voeren of een MVP te demonstreren of je hebt simpelweg
gewoon een random voornaam, achternaam, gender, email of leeftijd nodig. Met dit programma kan je MySQL of SQLite database populeren met gebruikers of de module gebruiken om een eigen populatie programma te maken.

PyPi package: https://pypi.org/project/worldnames/

# Installation manual for the Populating program

1. Clone the repository (**required**)

```commandline
git clone https://github.com/ayoub-abdessadak/world-names.git
```

2. Create a python virtual environment (**optional**)
```commandline
python -m venv venvworldnames
```
3. Activate the python virtual environment (**optional**)
```commandline
source venvworldnames/bin/activate
```

3.1 If you're on windows you can activate the virtual environment as is (**optional**)
```commandline
.\venvworldnames\Scripts\activate
```

4. Navigate to the repository (world-names) and install the required packages (**required**)
```commandline
pip install -r requirments.txt
```
5. Run the population simulator 
```commandline
python -m worldnames.populate
```
Or use the worldnames module to populate you're database:

1. Install the worldnames module (**required**)
```commandline
pip install worldnames
```
2. Use the worldnames module in you're python program
```python
import worldnames

worldnames.full_name() # returns 'Ashanti Qjtkbyh' for example. Type is a string.

worldnames.first_name() # returns 'Teodor' for example. Type is a string.

worldnames.last_name() # returns 'Pmgnwzqls' for example. Type is a string.

worldnames.age() # returns 50 for example. Type is an int.

worldnames.gender() # returns male for example. Type is a string.

worldnames.email() # returns 'Ashanti.Qjtkbyh@gmail.com' for example. Type is a string.

worldnames.email('Ashanti', 'Qjtkby') # It is possible to pass a first_name and last_name to the email method.

worldnames.user() # Returns all the attributes above in a tuple, for example: ('Cuauhtémoc', 'Sfzn', 'Woman', 88, 'Cuauhtémoc.Sfzn@outlook.com'). Type is an tuple.
```

