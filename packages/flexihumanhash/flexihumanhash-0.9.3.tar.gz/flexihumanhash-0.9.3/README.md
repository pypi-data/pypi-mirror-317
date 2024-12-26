## flexi-human-hash
There are lots of packages that convert big random numbers to something readable or create random strings from words, but none are as flexible as I wanted. I created this to be a highly controllable version of the other human hash packages.

Note that this package is well tested and fairly stable, so don't expect to see many changes unless new GitHub issues are opened.

## Usage
Install:
``` bash
pip install flexi-human-hash
```

Use
``` python
from flexihumanhash import FlexiHumanHash
fhh = FlexiHumanHash("{{adj}}-{{noun}}")
print(fhh.hash("hello world"))
# Expected output: "crookedest-valentines"
print(fhh.hash(42))
# Expected output: "worthiest-omelettes"
print(fhh.hash(bytes([0, 1, 3, 5])))
# Expected output: "manila-dive"
```

## Features:
* Multiple dictionaries: nouns, adjectives, verbs, first name, last name, city
* Full control over formatting: separators, spaces, additional words, upper case, lower case, numbers
* Random: You provide the source of randomness (hash, string, uuid, etc) or one will be provided for you
* Entropy reporting: understand how likely hash collisions are for your given format
* Extendable: add your own dictionaries and formatting transforms
* Jinja2-based templating for more features and control

## API Examples:
Simple hash converted into a string
``` python
fhh = FlexiHumanHash("{{adj}}-{{adj}}-{{noun}}-{{decimal(4)}}")
str(fhh.hash("hello world."))
# Expected output: "manuscript-anatomically-naps-5303"
```

Another format, random number provided for you
``` python
fhh = FlexiHumanHash("{{adj}}, {{adj}} {{noun}} {{hex(4)}}")
print(fhh.rand())
# Expected output: "frolicsome, intelligent mix 89d5"
```

Another format, md5 hash a string for random numbers, transform names to all caps
``` python
fhh = FlexiHumanHash("{{first-name|capitalize}}-{{last-name|capitalize}}-{{decimal(6)}}")
fhh.hash("this is my password...", alg="md5")
# Expected output: "CHARITY-ESMERELDA-903817"
# supported hash algorithms: blake2b (default), blake2s, shake128, shake256, md5, sha1, sha224, sha256, sha384, sha512, sha3-224, sha3-256, sha3-384, sha3-512
```

Report how much entropy is used for a format to help understand likelihood of collisions
``` python
fhh = FlexiHumanHash("{{first-name uppercase}}-{{last-name uppercase}}-{{decimal(6)}}")
print(fhh.entropy)
# Expected output (note BigInt): "70368744177664n"
print(f"Number of combinations: {fhh.entropy:,}")
# Expected output: "Number of combinations: 70,368,744,177,664"
print(f"Entropy: 2^${fhh.entropy_bits}")
# Expected output: "Entropy: 2^46"
```

Add a dictionary from a file
``` python
from pathlib import Path

FlexiTextDict.from_file(Path("./foo.txt")) # file contains one word per line
```

Add a dictionary programmatically
``` python
@register_dict("decimal")
class FlexiDecimalDict(FlexiDict):
    def __init__(self, size: int = 4) -> None:
        self.sz = size

    def get_entry(self, n: int) -> str:
        return f"{n:0{self.sz}d}" 

    @property
    def size(self) -> int:
        ret: int = 10 ** self.sz
        return ret

    def preprocess(self, args: tuple[Any, ...], kwargs: dict[str, Any]) -> FlexiDecimalDict:
        # this gets called if parameters are passed in to Jinja
        return FlexiDecimalDict(*args, **kwargs)
```

## Formats
* noun
    * 47,004 English nouns from [categorized-words](https://github.com/felixfischer/categorized-words)
* verb
    * 31,232 English verbs from [categorized-words](https://github.com/felixfischer/categorized-words)
* adjective
    * 14,903 English adjectives from [categorized-words](https://github.com/felixfischer/categorized-words)
* decimal
    * A decimal number (zero through 10), defaults to four digits long but can be a specified number of digits long
    * {{decimal}} = 2394
    * {{decimal(8)}} = 84258973
    * {{decimal(1)}} = 7
* hex
    * A hexidecimal number (zero through f), defaults to four nibbles / characters long but can be a specified number of digits long
    * {{hex}} = 3fa8
    * {{hex(8)}} = cb28f30d
    * {{hex(1)}} = e
* femalename
    * 4,951 English capitalized female first names / given names from [@stdlib](https://github.com/stdlib-js/datasets-female-first-names-en)
* malename
    * 3,898 English capitalized male first names / given names from [@stdlib](https://github.com/stdlib-js/datasets-male-first-names-en)
* firstname
    * 8,849 English capitalized first names / given names (female-name and male-name combined)
* lastname
    * 21,985 last names / family names from [uuid-readable](https://github.com/Debdut/uuid-readable)
* city
    * 138,398 city names from [all-the-cities](https://www.npmjs.com/package/all-the-cities)

## Transforms

* uppercase
    * Converts the first letter of a word to uppercase
    * e.g. "{{noun|upper}}" -> "Word"
* lowercase
    * Converts an entire word to lowercase
    * e.g. "{{noun|lower}}" -> "word"
* caps
    * Converts an entire word to uppercase
    * e.g. "{{noun|capitalize}}" -> "WORD"

Issues and pull requests always welcome, even if you're just saying hi. :)


Thank you to [@stdlib](https://www.npmjs.com/package/@stdlib/stdlib),
[categorized-words](https://www.npmjs.com/package/categorized-words),
[all-the-cities](https://www.npmjs.com/package/all-the-cities), and
[uuid-readable](https://www.npmjs.com/package/uuid-readable) for their word lists.