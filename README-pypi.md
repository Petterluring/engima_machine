
## The Engima Mahcine

The enigma machine is an analog cipher device invented by German engineer Arthur Scherbius in 1918. It is most famous for being used by Nazi Germany during WWII to encrypt secret messages. The enigma was broken by the Polish who decrypted enigma traffic on a continuous basis before being invaded 1939. The British (and the French) continued and reproduced the work of the Polish by building the Bombe machine at Bletchley Park to decipher enigma messages, effectively shortening the war by years.

Sources:   
https://en.wikipedia.org/wiki/Enigma_machine   
https://en.wikipedia.org/wiki/Bombe

## Project info

GitHub repo: https://github.com/Petterluring/enigma_machine   
License: MIT   
Contact info: petter.gustafsson1998@gmail.com


## Quick start

#### enigma_machine
Root package containing the enigma machine implementation. Use the EnigmaMachine class as the main entrypoint to build a new machine.
```python
from enigma_machine import EnigmaMachine
```

#### alphabet
Package containing an enum class named Alphabet. Defines the sets of alphabetic letters that can be used as input in the machine.
```python
class Alphabet(Enum):
    LATIN_ALPHABET   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    GERMAN_ALPHABET  = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ"
```

#### plugboard
Package for plugboard related functionality. Allows the user to configure a plugboard to be used in the machine using the Plugboard class. 

```python
from enigma_machine.plugboard import Plugboard
from enigma_machine.alphabet import Alphabet

plugboard = Plugboard(
        # Cords
        ("A", "B"),
        ("C", "D"),
        alphabet=Alphabet.LATIN_ALPHABET # Plugboard validates against the latin alphabet when adding cords for instance. Prevents user to add a cord such as (A, !).
)
```

#### rotor
Package for rotor related functionality. Allows the user to configure a rotor to be used in the machine using the Rotor class.

```python
from enigma_machine.rotor import Rotor

rotor = Rotor(
    wiring="EKMFLGDQVZNTOWYHXUSPAIBRCJ", # Permutation of latin alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ. Alphabet is infered by the initializer.
    position=1,
    turnover=1
)
```

#### Example configuration
The user can build a machine using the described components, Rotors class, and a reflector wiring: 

```python
from enigma_machine.plugboard import Plugboard
from enigma_machine.rotor import Rotor, Rotors
from enigma_machine import EnigmaMachine
from enigma_machine.alphabet import Alphabet


rotor_1 = Rotor(
    wiring="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    position=1,
    turnover=1,
)

rotor_2 = Rotor(
    wiring="AJDKSIRUXBLHWTMCQGZNPYFVOE",
    position=1,
    turnover=1,
)

rotor_3 = Rotor(
    wiring="BDFHJLCPRTXVZNYEIWGAKMUSQO",
    position=1,
    turnover=1,
)


plugboard = Plugboard(
        # Cords
        ("A", "B"),
        ("C", "D"),
        alphabet=Alphabet.LATIN_ALPHABET
)

device = EnigmaMachine(
    rotors=Rotors(rotor_1, rotor_2, rotor_3),
    reflector="YRUHQSLDPXNGOKMIEBFZCWVJAT",
    plugboard=plugboard,
)

```

#### factory
Package for storing pre-configured enigma machines. Instead of building a machine from scratch, import factory functions that builds one for you.

```python
from enigma_machine.factory import create_enigma_i_machine

machine = create_enigma_i_machine()
```

### Example usage
The following code snippet show how the EnigmaMachine class can be used to encrypt and decrypt messages. Remark how Rotors and Plugboard objects are initialized more conveniently compared to previous section.
```python
from enigma_machine import EnigmaMachine

machine = EnigmaMachine(
    rotors=(
        "WBOSQNZJHEAMFYKTRUIDCGXLVP",
        "HFQATKXPNYVCLIZRSEUGMBWODJ",
        "QJXRMPLVOGSIBZTEWCKUYAFNDH",
    ),
    reflector="LCYUGRWPAZFVDJQIXSOBETNMHK",
    plugboard=[ # Assumes latin alphabetic letters 
        ("A", "D"),
        ("B", "Q"),
        ("C", "M"),
        ("E", "Z"),
        ("F", "L"),
        ("G", "X"),
        ("H", "P"),
        ("I", "T"),
        ("J", "N"),
        ("K", "W"),
    ]
)

message = "Hello there."

machine.rotor_setting = (1, 2, 3)
encoded_message = machine.encode_message(message)

machine.rotor_setting = (1, 2, 3)
decoded_message = machine.encode_message(encoded_message)

print(f"Original message: {message}")        # Hello there.
print(f"Encoded message: {encoded_message}") # JJICQOLJAI
print(f"Decoded message: {decoded_message}") # HELLOTHERE
```

Using a factory function:
```python
from enigma_machine.factory import create_enigma_i_machine

message = "Hello there."

enigma_i = create_enigma_i_machine()

enigma_i.rotor_setting = (3, 4, 2)
encoded_message = enigma_i.encode_message(message)

enigma_i.rotor_setting = (3, 4, 2)
decoded_message = enigma_i.encode_message(encoded_message)

print(f"\nOriginal message: {message}")      # Hello there.
print(f"Encoded message: {encoded_message}") # KPNDFJRFMA
print(f"Decoded message: {decoded_message}") # HELLOTHERE
```