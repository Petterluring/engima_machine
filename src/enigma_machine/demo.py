"""Demo script."""
from enigma_machine import EnigmaMachine
from enigma_machine.factory import create_enigma_i_machine


def run() -> None:
    """Main entrypoint."""
    # BUILDING YOUR OWN ENIGMA
    machine = EnigmaMachine(
        rotors=(
            "WBOSQNZJHEAMFYKTRUIDCGXLVP",
            "HFQATKXPNYVCLIZRSEUGMBWODJ",
            "QJXRMPLVOGSIBZTEWCKUYAFNDH",
        ),
        reflector="LCYUGRWPAZFVDJQIXSOBETNMHK",
        plugboard=[
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

    # USING EXISTING ENIGMA
    message = "Hello there."

    enimga_i = create_enigma_i_machine()

    enimga_i.rotor_setting = (3, 4, 2)
    encoded_message = enimga_i.encode_message(message)

    enimga_i.rotor_setting = (3, 4, 2)
    decoded_message = enimga_i.encode_message(encoded_message)

    print(f"\nOriginal message: {message}")      # Hello there.
    print(f"Encoded message: {encoded_message}") # KPNDFJRFMA
    print(f"Decoded message: {decoded_message}") # HELLOTHERE

if "__main__":
    run()
