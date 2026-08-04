
# Introduction

The enigma machine is an analog cipher device invented by German engineer Arthur Scherbius in 1918.

Mention:
- Usage in WW2
- Breaking the enigma

Sources:
https://en.wikipedia.org/wiki/Enigma_machine


# Enigma Machine Theory
This section describes the core components of the enigma machine and how these jointly operate to produce encrypted letters. The description emphasizes on the encryption logic in the device such that the reader can understand the source code better. The reader is referred to other sources on the internet regarding aspects not discussed here. One tip is the "How did the Enigma work?" youtube video (See sources below) that include a detailed describtion of the machine's electromechanics along with how letters are encoded.


!["Figure 1"](imgs/enimga_machine_labeled.jpg)
*Figure 1. Labeled Enigma machine.*

Figure 1 displays the complete enigma device highlighting some of its components. To encrypt a message, the user enters the letters on the keyboard, which sends a current through the device that activates one of the lamps on the lampboard, highlighting the encrypted letter. The user can save the encrypted letters by writing them down on a piece of paper that together represents the encrypted message.

To decrypt a message, the user must configure the plugboard and rotors identically to the state before the message was encrypted. The user then types the encrypted letters which inverts them to their original states, resulting in the original message.

The upcoming sections describes the encryption process that occurs between typing a letter to a letter being lit on the lampboard.


Sources:
Figure 1 - https://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma#/media/File:EnigmaMachineLabeled.jpg  
How did the Enigma work? - https://www.youtube.com/watch?v=ybkkiGtJmkM&t=443s  
Wiki page - https://en.wikipedia.org/wiki/Enigma_machine

## Plugboard

## Rotors

### Rotor wiring

## Reflector

## Encryption process

## Possible configurations

# Source code

The source code is organized in the following packages:
* enigma_machine - Root package containing the enigma machine implementation.
* _internals - Utility package containing tools that other packages can use.
* _reflector - Package for reflector related functionality.
* plugboard  - Package for plugboard related functionality.
* rotor      - Package for rotor related functionality.



## Example usage
The following code snippet show how you can build your own enigma machine and use it to encrypt and decrypt messages.
```python
from enigma_machine import Machine
from enigma_machine.plugboard import Plugboard
from enigma_machine.rotor import Rotor, Rotors

machine = Machine(
    rotors=Rotors(
        fast_rotor=Rotor(wiring="QJXRMPLVOGSIBZTEWCKUYAFNDH"),
        middle_rotor=Rotor(wiring="HFQATKXPNYVCLIZRSEUGMBWODJ"),
        slow_rotor=Rotor(wiring="WBOSQNZJHEAMFYKTRUIDCGXLVP"),
    ),
    reflector_wiring="LCYUGRWPAZFVDJQIXSOBETNMHK",
    plugboard=Plugboard(
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
    )
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

The reader can also use prepared enigma machines for convenience:
```python
# INSERT CODE
``` 

# AI usage

AI usage was very limited in this project as I like to rely on my own problem solving skills when working on programming projects as a hobby. I have occasionally used ChatGPT to clarify details of how the enigma machine operates and discuss design patterns. Apart from that, the source code is entirely produced by me, along with the unit tests, toml-file and this readme file.