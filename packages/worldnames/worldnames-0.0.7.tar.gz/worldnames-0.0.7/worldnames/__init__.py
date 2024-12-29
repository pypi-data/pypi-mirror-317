# The init module for the package worldnames creates an instance of the class WorldNames and assigns
# the bounded methods to variables so they can be accessed while still being Polymorphisme (d)
# Making the class reusable without having separate functions and rather using object-oriented programming.

# Python imports
import random, json, site, os
# world-names imports
from worldnames.populatinghelpers import email_domains, letters, genders

class WorldNames:

    """
    This class holds static and non-static methods for generating a name, age, gender, email or a combination of them all.
    Most likely to be used for populating a database or running some tests.
    """

    def __init__(self, file: str = 'worldnames/worldnames.json'):
        """
        The initializer needs the file name and the package folder which holds the JSON file.
        :param file:
        """
        site_packages = site.getsitepackages()
        site_packages.append("")
        names_in_json = []
        for sp in site_packages:
            try:
                __file = open(os.path.join(sp, file))
                names_in_json = __file.readlines()[0]
                break
            except FileNotFoundError:
                pass
        if not names_in_json:
            message = (
                    "file worldnames.json not found. Looked in the following directories:\n "
                    + os.path.abspath("worldnames/worldnames.json")
                    + "\n "
                    + "\n".join(site_packages)
            )
            raise BaseException(message)
        self.names = json.loads(names_in_json)
        self.min, self.max = 0, len(self.names)-1
        self.min_gender, self.max_gender = 0, len(genders)-1
        self.min_domain, self.max_domain = 0, len(email_domains)-1

    def full_name(self) -> str:
        """
        Returns a random first and last name
        :return: str
        """
        return f"{self.first_name()} {self.last_name()}"

    def first_name(self) -> str:
        """
        Returns a random first name
        :return: str
        """
        random.shuffle(self.names)
        return self.names[random.randint(self.min, self.max)]

    @staticmethod
    def last_name() -> str:
        """
        returns a random last name
        :return: str
        """
        _max = random.randint(3, 12)
        random.shuffle(letters)
        _last_name = "".join(letters[0:_max])
        return f"{_last_name[0].upper()}{_last_name[1::].lower()}"

    @staticmethod
    def age() -> int:
        """
        Returns a random age between 0 and 120
        :return: int
        """
        return random.randint(0, 120)

    def gender(self) -> str:
        """
        Returns a random gender
        :return: str
        """
        random.shuffle(genders)
        return genders[random.randint(self.min_gender, self.max_gender)]

    def email(self, _first_name:str=None, _last_name:str=None) -> str:
        """
        Returns a random email
        :param _first_name:
        :param _last_name:
        :return: str
        """
        random.shuffle(email_domains)
        domain = email_domains[random.randint(self.min_domain, self.max_domain)]
        if not first_name or not last_name:
            return f"{self.first_name()}.{self.last_name()}@{domain}"
        else:
            return f"{_first_name}.{_last_name}@{domain}"

    def phone_number(self) -> str:
        """
        Returns:
            str: A random +31 number
        """
        number = [1,2,3,4,5,6,7,8,9]
        [random.shuffle(number) for _ in range(100)]
        number = [_.__str__() for _ in number]
        return "+316" + "".join(number[0:8])
        
    def user(self) -> tuple:
        """
        Returns a random user containing the first_name, last_name, age, gender and email in a tuple.
        :return: tuple
        """
        fn, ln = self.first_name(), self.last_name()
        return fn, ln, self.gender(), self.age(), self.email(fn, ln), self.phone_number()
    

world_names = WorldNames()
full_name = world_names.full_name
first_name = world_names.first_name
last_name = world_names.last_name
age = world_names.age
gender = world_names.gender
email = world_names.email
phone_number = world_names.phone_number
user = world_names.user