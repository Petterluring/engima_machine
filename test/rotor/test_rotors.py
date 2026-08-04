"""Test module for Rotors class."""
import random

import pytest

from enigma_machine.rotor.rotor import Rotor, Rotors


@pytest.fixture
def rotors() -> Rotors:
    """Return a Rotors object that can be reused throughout tests."""
    return Rotors(
        Rotor("QJXRMPLVOGSIBZTEWCKUYAFNDH"),
        Rotor("HFQATKXPNYVCLIZRSEUGMBWODJ"),
        Rotor("WBOSQNZJHEAMFYKTRUIDCGXLVP"),
    )

def test_rotors_turn_correctly(rotors: Rotors) -> None:
    """Test if rotors turn as expected."""
    for slow_rotor in range(1, 26 + 1):
        for middle_rotor in range(1, 26 + 1):
            for fast_rotor in range(1, 26 + 1):
                assert rotors.setting == (slow_rotor, middle_rotor, fast_rotor)
                rotors.forward("A") # Random encoding to make rotors turn.
    assert rotors.setting == (1, 1, 1)


@pytest.mark.parametrize(
        "seed", [
            24,
            53,
            10,
            37,
            34,
            43,
            12,
            46,
            12,
        ]
)
def test_rotors_turn_correctly_from_different_starting_points(rotors: Rotors, seed: int) -> None:
    """Choose different starting points for the rotor settings and test if rotations progress correctly."""
    random.seed(seed)
    slow, middle, fast = random.randint(1, 26), random.randint(1, 26), random.randint(1, 26)
    rotors.setting = (slow, middle, fast)

    for slow_rotor in range(slow, 26 + 1):
        start_middle = middle if slow_rotor == slow else 1

        for middle_rotor in range(start_middle, 26 + 1):
            start_fast = fast if middle_rotor == middle and slow_rotor == slow else 1

            for fast_rotor in range(start_fast, 26 + 1):
                assert rotors.setting == (slow_rotor, middle_rotor, fast_rotor)
                rotors.forward("A") # Random encoding to make rotors turn.

def test_rotors_turn_correctly_using_different_turnovers(rotors: Rotors) -> None:
    """Test if rotors can turn correctly using different turnover values."""
    rotors.fast_rotor.turnover = 3
    rotors.middle_rotor.turnover = 3

    rotors.forward("A")
    assert rotors.setting == (1, 1, 2)

    rotors.forward("A") # middle rotor should turn to 2
    assert rotors.setting == (1, 2, 3)

    for _ in range(26 - 3):
        rotors.forward("A")
    assert rotors.setting == (1, 2, 26)

    rotors.forward("A")
    rotors.forward("A")
    assert rotors.setting == (1, 2, 2)

    rotors.forward("A") # slow rotor should turn to 2
    assert rotors.setting == (2, 3, 3)


def test_rotors_can_set_settings(rotors: Rotors) -> None:
    """Test if rotors can set its settings properly."""
    assert rotors.setting == (1, 1, 1)
    assert rotors.setting_alph == ("A", "A", "A")

    rotors.setting = (1, 2, 1)
    assert rotors.setting == (1, 2, 1)
    assert rotors.setting_alph == ("A", "B", "A")

    rotors.setting = (26, 5, 23)
    assert rotors.setting == (26, 5, 23)
    assert rotors.setting_alph == ("Z", "E", "W")

    rotors.setting = ("A", "B", "C") # type:ignore[assignment]
    assert rotors.setting == (1, 2, 3)
    assert rotors.setting_alph == ("A", "B", "C")

def test_rotors_can_set_turnovers(rotors: Rotors) -> None:
    """Test if rotors can set its settings properly."""
    assert rotors.turnover_setting == (1, 1, 1)
    assert rotors.turnover_setting_alph == ("A", "A", "A")

    rotors.turnover_setting = (1, 2, 1)
    assert rotors.turnover_setting == (1, 2, 1)
    assert rotors.turnover_setting_alph == ("A", "B", "A")

    rotors.turnover_setting = (26, 5, 23)
    assert rotors.turnover_setting == (26, 5, 23)
    assert rotors.turnover_setting_alph == ("Z", "E", "W")

    rotors.turnover_setting = ("A", "B", "C") # type:ignore[assignment]
    assert rotors.turnover_setting == (1, 2, 3)
    assert rotors.turnover_setting_alph == ("A", "B", "C")

def test_rotors_forward_letters_correctly(rotors: Rotors) -> None:
    """Test if forward method encodes letters correctly."""
    # EXAMPLE 1
    #     MACHINE CONTACTS
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ - Type letter A.
    # |
    # |
    # V   FAST ROTOR CONTACTS
    # BCDEFGHIJKLMNOPQRSTUVWXYZA - Fast rotor turns. Setting: (1, 1, 2)
    #                              A effectively becomes B.
    #
    #     FAST ROTOR WIRING
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    #  |
    #  V
    # QJXRMPLVOGSIBZTEWCKUYAFNDH - B is then wired to J. See wiring in rotors fixture.
    #
    #     FAST ROTOR CONTACTS
    # BCDEFGHIJKLMNOPQRSTUVWXYZA
    #         |
    #         |
    #    MACH V INE CONTACTS
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ - J effectively becomes I
    #         |
    #         |
    #    MIDD V LE ROTOR CONTACTS
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ - I effectively becomes I because middle position is 1.
    #
    #    MIDDLE ROTOR WIRING
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    #         |
    #         |
    #         V
    # HFQATKXPNYVCLIZRSEUGMBWODJ - I wires to N. See wiring in rotors fixture.
    #
    #    MIDDLE ROTOR CONTACTS
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    #              |
    #              |
    #    MACHINE C V ONTACTS
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ  - N effectively becomes N.
    #              |
    #              |
    #    SLOW ROTO V R CONTACTS
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ - N effectively becomes N because slow position is 1.
    #
    #    SLOW ROTOR WIRING
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    #              |
    #              |
    #              V
    # WBOSQNZJHEAMFYKTRUIDCGXLVP - N wires to Y. See wiring in rotors fixture.
    #
    #    SLOW ROTOR CONTACTS
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    #                         |
    #                         |
    #    MACHINE CONTACTS     V
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ - Y effectively becomes Y because slow position is 1.
    assert rotors.forward("A") == "Y"
    assert rotors.setting == (1, 1, 2)

    rotors.setting = (4, 3, 1)
    # EXAMPLE 2
    #     MACHINE CONTACTS
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ - Type letter C.
    #   |
    #   |
    #   V FAST ROTOR CONTACTS
    # BCDEFGHIJKLMNOPQRSTUVWXYZA - Fast rotor turns. Setting: (4, 3, 2)
    #                              C effectively becomes D.
    #
    #     FAST ROTOR WIRING
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    #    |
    #    V
    # QJXRMPLVOGSIBZTEWCKUYAFNDH - D wires to R. See wiring in rotors fixture.
    #
    #     FAST ROTOR CONTACTS
    # BCDEFGHIJKLMNOPQRSTUVWXYZA
    #                 |
    #    MACHINE CONT V ACTS
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ - R effectively becomes Q
    #                 |
    #                 |
    #    MIDDLE ROTOR V CONTACTS
    # CDEFGHIJKLMNOPQRSTUVWXYZAB - Q effectively becomes S because middle position is 3.
    #
    #    MIDDLE ROTOR WIRING
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    #                   |
    #                   |
    #                   V
    # HFQATKXPNYVCLIZRSEUGMBWODJ - S wires to U. See wiring in rotors fixture.
    #
    #    MIDDLE ROTOR CONTACTS
    # CDEFGHIJKLMNOPQRSTUVWXYZAB
    #                   |
    #                   |
    #    MACHINE CONTAC V TS
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ  - U effectively becomes S.
    #                   |
    #                   |
    #    SLOW ROTOR CON V TACTS
    # DEFGHIJKLMNOPQRSTUVWXYZABC - S effectively becomes V because slow position is 4.
    #
    #    SLOW ROTOR WIRING
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    #                      |
    #                      |
    #                      V
    # WBOSQNZJHEAMFYKTRUIDCGXLVP - V wires to G. See wiring in rotors fixture.
    #
    #    SLOW ROTOR CONTACTS
    # DEFGHIJKLMNOPQRSTUVWXYZABC
    #    |
    #    |
    #    V MACHINE CONTACTS
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ - G effectively becomes D because slow position is 4.
    assert rotors.forward("C") == "D"
    assert rotors.setting == (4, 3, 2)


def test_rotors_backward_letters_correctly(rotors: Rotors) -> None:
    """Test if backward method backwards letters correctly.

    Remark that we reuse the examples from test_rotors_forward_letters_correctly
    and inspect if the encoded letter is reversed to the original input letter.
    """
    rotors.setting = (1, 1, 2)
    assert rotors.backward("Y") == "A"

    rotors.setting = (4, 3, 2)
    assert rotors.backward("D") == "C"

