# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_address_block[23-de-None-Nice-Addition] 1"
] = """David Moreno
Nice
Addition
060 Guerra Island
23
62422 Port Michaela
Äthiopien"""

snapshots[
    "test_address_block[23-de-None-None-None] 1"
] = """David Moreno
060 Guerra Island
23
62422 Port Michaela
Äthiopien"""

snapshots[
    "test_address_block[23-de-Some-Nice-Addition] 1"
] = """David Moreno
Some
Nice
Addition
060 Guerra Island
23
62422 Port Michaela
Äthiopien"""

snapshots[
    "test_address_block[23-de-Some-None-Addition] 1"
] = """David Moreno
Some
Addition
060 Guerra Island
23
62422 Port Michaela
Äthiopien"""

snapshots[
    "test_address_block[23-en-None-Nice-Addition] 1"
] = """David Moreno
Nice
Addition
060 Guerra Island
23
62422 Port Michaela
Ethiopia"""

snapshots[
    "test_address_block[23-en-None-None-None] 1"
] = """David Moreno
060 Guerra Island
23
62422 Port Michaela
Ethiopia"""

snapshots[
    "test_address_block[23-en-Some-Nice-Addition] 1"
] = """David Moreno
Some
Nice
Addition
060 Guerra Island
23
62422 Port Michaela
Ethiopia"""

snapshots[
    "test_address_block[23-en-Some-None-Addition] 1"
] = """David Moreno
Some
Addition
060 Guerra Island
23
62422 Port Michaela
Ethiopia"""

snapshots[
    "test_address_block[23-fr-None-Nice-Addition] 1"
] = """David Moreno
Nice
Addition
060 Guerra Island
23
62422 Port Michaela
Éthiopie"""

snapshots[
    "test_address_block[23-fr-None-None-None] 1"
] = """David Moreno
060 Guerra Island
23
62422 Port Michaela
Éthiopie"""

snapshots[
    "test_address_block[23-fr-Some-Nice-Addition] 1"
] = """David Moreno
Some
Nice
Addition
060 Guerra Island
23
62422 Port Michaela
Éthiopie"""

snapshots[
    "test_address_block[23-fr-Some-None-Addition] 1"
] = """David Moreno
Some
Addition
060 Guerra Island
23
62422 Port Michaela
Éthiopie"""

snapshots[
    "test_address_block[None-de-None-Nice-Addition] 1"
] = """David Moreno
Nice
Addition
060 Guerra Island
62422 Port Michaela
Äthiopien"""

snapshots[
    "test_address_block[None-de-None-None-None] 1"
] = """David Moreno
060 Guerra Island
62422 Port Michaela
Äthiopien"""

snapshots[
    "test_address_block[None-de-Some-Nice-Addition] 1"
] = """David Moreno
Some
Nice
Addition
060 Guerra Island
62422 Port Michaela
Äthiopien"""

snapshots[
    "test_address_block[None-de-Some-None-Addition] 1"
] = """David Moreno
Some
Addition
060 Guerra Island
62422 Port Michaela
Äthiopien"""

snapshots[
    "test_address_block[None-en-None-Nice-Addition] 1"
] = """David Moreno
Nice
Addition
060 Guerra Island
62422 Port Michaela
Ethiopia"""

snapshots[
    "test_address_block[None-en-None-None-None] 1"
] = """David Moreno
060 Guerra Island
62422 Port Michaela
Ethiopia"""

snapshots[
    "test_address_block[None-en-Some-Nice-Addition] 1"
] = """David Moreno
Some
Nice
Addition
060 Guerra Island
62422 Port Michaela
Ethiopia"""

snapshots[
    "test_address_block[None-en-Some-None-Addition] 1"
] = """David Moreno
Some
Addition
060 Guerra Island
62422 Port Michaela
Ethiopia"""

snapshots[
    "test_address_block[None-fr-None-Nice-Addition] 1"
] = """David Moreno
Nice
Addition
060 Guerra Island
62422 Port Michaela
Éthiopie"""

snapshots[
    "test_address_block[None-fr-None-None-None] 1"
] = """David Moreno
060 Guerra Island
62422 Port Michaela
Éthiopie"""

snapshots[
    "test_address_block[None-fr-Some-Nice-Addition] 1"
] = """David Moreno
Some
Nice
Addition
060 Guerra Island
62422 Port Michaela
Éthiopie"""

snapshots[
    "test_address_block[None-fr-Some-None-Addition] 1"
] = """David Moreno
Some
Addition
060 Guerra Island
62422 Port Michaela
Éthiopie"""

snapshots["test_address_block_missing_address 1"] = "David Moreno"

snapshots["test_fullname[de-None-None-dr-female] 1"] = "Frau Dr."

snapshots["test_fullname[de-None-None-dr-male] 1"] = "Herr Dr."

snapshots["test_fullname[de-None-None-dr-neutral] 1"] = "Dr."

snapshots["test_fullname[de-None-None-none-female] 1"] = "Frau"

snapshots["test_fullname[de-None-None-none-male] 1"] = "Herr"

snapshots["test_fullname[de-None-None-none-neutral] 1"] = ""

snapshots["test_fullname[de-None-None-pd-dr-female] 1"] = "Frau PD Dr."

snapshots["test_fullname[de-None-None-pd-dr-male] 1"] = "Herr PD Dr."

snapshots["test_fullname[de-None-None-pd-dr-neutral] 1"] = "PD Dr."

snapshots["test_fullname[de-None-None-prof-dr-female] 1"] = "Frau Prof. Dr."

snapshots["test_fullname[de-None-None-prof-dr-male] 1"] = "Herr Prof. Dr."

snapshots["test_fullname[de-None-None-prof-dr-neutral] 1"] = "Prof. Dr."

snapshots["test_fullname[de-None-None-prof-female] 1"] = "Frau Prof."

snapshots["test_fullname[de-None-None-prof-male] 1"] = "Herr Prof."

snapshots["test_fullname[de-None-None-prof-neutral] 1"] = "Prof."

snapshots["test_fullname[de-None-Winston-dr-female] 1"] = "Frau Dr. Winston"

snapshots["test_fullname[de-None-Winston-dr-male] 1"] = "Herr Dr. Winston"

snapshots["test_fullname[de-None-Winston-dr-neutral] 1"] = "Dr. Winston"

snapshots["test_fullname[de-None-Winston-none-female] 1"] = "Frau Winston"

snapshots["test_fullname[de-None-Winston-none-male] 1"] = "Herr Winston"

snapshots["test_fullname[de-None-Winston-none-neutral] 1"] = "Winston"

snapshots["test_fullname[de-None-Winston-pd-dr-female] 1"] = "Frau PD Dr. Winston"

snapshots["test_fullname[de-None-Winston-pd-dr-male] 1"] = "Herr PD Dr. Winston"

snapshots["test_fullname[de-None-Winston-pd-dr-neutral] 1"] = "PD Dr. Winston"

snapshots["test_fullname[de-None-Winston-prof-dr-female] 1"] = "Frau Prof. Dr. Winston"

snapshots["test_fullname[de-None-Winston-prof-dr-male] 1"] = "Herr Prof. Dr. Winston"

snapshots["test_fullname[de-None-Winston-prof-dr-neutral] 1"] = "Prof. Dr. Winston"

snapshots["test_fullname[de-None-Winston-prof-female] 1"] = "Frau Prof. Winston"

snapshots["test_fullname[de-None-Winston-prof-male] 1"] = "Herr Prof. Winston"

snapshots["test_fullname[de-None-Winston-prof-neutral] 1"] = "Prof. Winston"

snapshots["test_fullname[de-Smith-None-dr-female] 1"] = "Frau Dr. Smith"

snapshots["test_fullname[de-Smith-None-dr-male] 1"] = "Herr Dr. Smith"

snapshots["test_fullname[de-Smith-None-dr-neutral] 1"] = "Dr. Smith"

snapshots["test_fullname[de-Smith-None-none-female] 1"] = "Frau Smith"

snapshots["test_fullname[de-Smith-None-none-male] 1"] = "Herr Smith"

snapshots["test_fullname[de-Smith-None-none-neutral] 1"] = "Smith"

snapshots["test_fullname[de-Smith-None-pd-dr-female] 1"] = "Frau PD Dr. Smith"

snapshots["test_fullname[de-Smith-None-pd-dr-male] 1"] = "Herr PD Dr. Smith"

snapshots["test_fullname[de-Smith-None-pd-dr-neutral] 1"] = "PD Dr. Smith"

snapshots["test_fullname[de-Smith-None-prof-dr-female] 1"] = "Frau Prof. Dr. Smith"

snapshots["test_fullname[de-Smith-None-prof-dr-male] 1"] = "Herr Prof. Dr. Smith"

snapshots["test_fullname[de-Smith-None-prof-dr-neutral] 1"] = "Prof. Dr. Smith"

snapshots["test_fullname[de-Smith-None-prof-female] 1"] = "Frau Prof. Smith"

snapshots["test_fullname[de-Smith-None-prof-male] 1"] = "Herr Prof. Smith"

snapshots["test_fullname[de-Smith-None-prof-neutral] 1"] = "Prof. Smith"

snapshots["test_fullname[de-Smith-Winston-dr-female] 1"] = "Frau Dr. Winston Smith"

snapshots["test_fullname[de-Smith-Winston-dr-male] 1"] = "Herr Dr. Winston Smith"

snapshots["test_fullname[de-Smith-Winston-dr-neutral] 1"] = "Dr. Winston Smith"

snapshots["test_fullname[de-Smith-Winston-none-female] 1"] = "Frau Winston Smith"

snapshots["test_fullname[de-Smith-Winston-none-male] 1"] = "Herr Winston Smith"

snapshots["test_fullname[de-Smith-Winston-none-neutral] 1"] = "Winston Smith"

snapshots[
    "test_fullname[de-Smith-Winston-pd-dr-female] 1"
] = "Frau PD Dr. Winston Smith"

snapshots["test_fullname[de-Smith-Winston-pd-dr-male] 1"] = "Herr PD Dr. Winston Smith"

snapshots["test_fullname[de-Smith-Winston-pd-dr-neutral] 1"] = "PD Dr. Winston Smith"

snapshots[
    "test_fullname[de-Smith-Winston-prof-dr-female] 1"
] = "Frau Prof. Dr. Winston Smith"

snapshots[
    "test_fullname[de-Smith-Winston-prof-dr-male] 1"
] = "Herr Prof. Dr. Winston Smith"

snapshots[
    "test_fullname[de-Smith-Winston-prof-dr-neutral] 1"
] = "Prof. Dr. Winston Smith"

snapshots["test_fullname[de-Smith-Winston-prof-female] 1"] = "Frau Prof. Winston Smith"

snapshots["test_fullname[de-Smith-Winston-prof-male] 1"] = "Herr Prof. Winston Smith"

snapshots["test_fullname[de-Smith-Winston-prof-neutral] 1"] = "Prof. Winston Smith"

snapshots["test_fullname[en-None-None-dr-female] 1"] = "Mrs. Dr."

snapshots["test_fullname[en-None-None-dr-male] 1"] = "Mr. Dr."

snapshots["test_fullname[en-None-None-dr-neutral] 1"] = "Dr."

snapshots["test_fullname[en-None-None-none-female] 1"] = "Mrs."

snapshots["test_fullname[en-None-None-none-male] 1"] = "Mr."

snapshots["test_fullname[en-None-None-none-neutral] 1"] = ""

snapshots["test_fullname[en-None-None-pd-dr-female] 1"] = "Mrs. PD Dr."

snapshots["test_fullname[en-None-None-pd-dr-male] 1"] = "Mr. PD Dr."

snapshots["test_fullname[en-None-None-pd-dr-neutral] 1"] = "PD Dr."

snapshots["test_fullname[en-None-None-prof-dr-female] 1"] = "Mrs. Prof. Dr."

snapshots["test_fullname[en-None-None-prof-dr-male] 1"] = "Mr. Prof. Dr."

snapshots["test_fullname[en-None-None-prof-dr-neutral] 1"] = "Prof. Dr."

snapshots["test_fullname[en-None-None-prof-female] 1"] = "Mrs. Prof."

snapshots["test_fullname[en-None-None-prof-male] 1"] = "Mr. Prof."

snapshots["test_fullname[en-None-None-prof-neutral] 1"] = "Prof."

snapshots["test_fullname[en-None-Winston-dr-female] 1"] = "Mrs. Dr. Winston"

snapshots["test_fullname[en-None-Winston-dr-male] 1"] = "Mr. Dr. Winston"

snapshots["test_fullname[en-None-Winston-dr-neutral] 1"] = "Dr. Winston"

snapshots["test_fullname[en-None-Winston-none-female] 1"] = "Mrs. Winston"

snapshots["test_fullname[en-None-Winston-none-male] 1"] = "Mr. Winston"

snapshots["test_fullname[en-None-Winston-none-neutral] 1"] = "Winston"

snapshots["test_fullname[en-None-Winston-pd-dr-female] 1"] = "Mrs. PD Dr. Winston"

snapshots["test_fullname[en-None-Winston-pd-dr-male] 1"] = "Mr. PD Dr. Winston"

snapshots["test_fullname[en-None-Winston-pd-dr-neutral] 1"] = "PD Dr. Winston"

snapshots["test_fullname[en-None-Winston-prof-dr-female] 1"] = "Mrs. Prof. Dr. Winston"

snapshots["test_fullname[en-None-Winston-prof-dr-male] 1"] = "Mr. Prof. Dr. Winston"

snapshots["test_fullname[en-None-Winston-prof-dr-neutral] 1"] = "Prof. Dr. Winston"

snapshots["test_fullname[en-None-Winston-prof-female] 1"] = "Mrs. Prof. Winston"

snapshots["test_fullname[en-None-Winston-prof-male] 1"] = "Mr. Prof. Winston"

snapshots["test_fullname[en-None-Winston-prof-neutral] 1"] = "Prof. Winston"

snapshots["test_fullname[en-Smith-None-dr-female] 1"] = "Mrs. Dr. Smith"

snapshots["test_fullname[en-Smith-None-dr-male] 1"] = "Mr. Dr. Smith"

snapshots["test_fullname[en-Smith-None-dr-neutral] 1"] = "Dr. Smith"

snapshots["test_fullname[en-Smith-None-none-female] 1"] = "Mrs. Smith"

snapshots["test_fullname[en-Smith-None-none-male] 1"] = "Mr. Smith"

snapshots["test_fullname[en-Smith-None-none-neutral] 1"] = "Smith"

snapshots["test_fullname[en-Smith-None-pd-dr-female] 1"] = "Mrs. PD Dr. Smith"

snapshots["test_fullname[en-Smith-None-pd-dr-male] 1"] = "Mr. PD Dr. Smith"

snapshots["test_fullname[en-Smith-None-pd-dr-neutral] 1"] = "PD Dr. Smith"

snapshots["test_fullname[en-Smith-None-prof-dr-female] 1"] = "Mrs. Prof. Dr. Smith"

snapshots["test_fullname[en-Smith-None-prof-dr-male] 1"] = "Mr. Prof. Dr. Smith"

snapshots["test_fullname[en-Smith-None-prof-dr-neutral] 1"] = "Prof. Dr. Smith"

snapshots["test_fullname[en-Smith-None-prof-female] 1"] = "Mrs. Prof. Smith"

snapshots["test_fullname[en-Smith-None-prof-male] 1"] = "Mr. Prof. Smith"

snapshots["test_fullname[en-Smith-None-prof-neutral] 1"] = "Prof. Smith"

snapshots["test_fullname[en-Smith-Winston-dr-female] 1"] = "Mrs. Dr. Winston Smith"

snapshots["test_fullname[en-Smith-Winston-dr-male] 1"] = "Mr. Dr. Winston Smith"

snapshots["test_fullname[en-Smith-Winston-dr-neutral] 1"] = "Dr. Winston Smith"

snapshots["test_fullname[en-Smith-Winston-none-female] 1"] = "Mrs. Winston Smith"

snapshots["test_fullname[en-Smith-Winston-none-male] 1"] = "Mr. Winston Smith"

snapshots["test_fullname[en-Smith-Winston-none-neutral] 1"] = "Winston Smith"

snapshots[
    "test_fullname[en-Smith-Winston-pd-dr-female] 1"
] = "Mrs. PD Dr. Winston Smith"

snapshots["test_fullname[en-Smith-Winston-pd-dr-male] 1"] = "Mr. PD Dr. Winston Smith"

snapshots["test_fullname[en-Smith-Winston-pd-dr-neutral] 1"] = "PD Dr. Winston Smith"

snapshots[
    "test_fullname[en-Smith-Winston-prof-dr-female] 1"
] = "Mrs. Prof. Dr. Winston Smith"

snapshots[
    "test_fullname[en-Smith-Winston-prof-dr-male] 1"
] = "Mr. Prof. Dr. Winston Smith"

snapshots[
    "test_fullname[en-Smith-Winston-prof-dr-neutral] 1"
] = "Prof. Dr. Winston Smith"

snapshots["test_fullname[en-Smith-Winston-prof-female] 1"] = "Mrs. Prof. Winston Smith"

snapshots["test_fullname[en-Smith-Winston-prof-male] 1"] = "Mr. Prof. Winston Smith"

snapshots["test_fullname[en-Smith-Winston-prof-neutral] 1"] = "Prof. Winston Smith"

snapshots["test_fullname[fr-None-None-dr-female] 1"] = "Madame Dr"

snapshots["test_fullname[fr-None-None-dr-male] 1"] = "Monsieur Dr"

snapshots["test_fullname[fr-None-None-dr-neutral] 1"] = "Dr"

snapshots["test_fullname[fr-None-None-none-female] 1"] = "Madame"

snapshots["test_fullname[fr-None-None-none-male] 1"] = "Monsieur"

snapshots["test_fullname[fr-None-None-none-neutral] 1"] = ""

snapshots["test_fullname[fr-None-None-pd-dr-female] 1"] = "Madame PD Dr"

snapshots["test_fullname[fr-None-None-pd-dr-male] 1"] = "Monsieur PD Dr"

snapshots["test_fullname[fr-None-None-pd-dr-neutral] 1"] = "PD Dr"

snapshots["test_fullname[fr-None-None-prof-dr-female] 1"] = "Madame Prof. Dr"

snapshots["test_fullname[fr-None-None-prof-dr-male] 1"] = "Monsieur Prof. Dr"

snapshots["test_fullname[fr-None-None-prof-dr-neutral] 1"] = "Prof. Dr"

snapshots["test_fullname[fr-None-None-prof-female] 1"] = "Madame Prof."

snapshots["test_fullname[fr-None-None-prof-male] 1"] = "Monsieur Prof."

snapshots["test_fullname[fr-None-None-prof-neutral] 1"] = "Prof."

snapshots["test_fullname[fr-None-Winston-dr-female] 1"] = "Madame Dr Winston"

snapshots["test_fullname[fr-None-Winston-dr-male] 1"] = "Monsieur Dr Winston"

snapshots["test_fullname[fr-None-Winston-dr-neutral] 1"] = "Dr Winston"

snapshots["test_fullname[fr-None-Winston-none-female] 1"] = "Madame Winston"

snapshots["test_fullname[fr-None-Winston-none-male] 1"] = "Monsieur Winston"

snapshots["test_fullname[fr-None-Winston-none-neutral] 1"] = "Winston"

snapshots["test_fullname[fr-None-Winston-pd-dr-female] 1"] = "Madame PD Dr Winston"

snapshots["test_fullname[fr-None-Winston-pd-dr-male] 1"] = "Monsieur PD Dr Winston"

snapshots["test_fullname[fr-None-Winston-pd-dr-neutral] 1"] = "PD Dr Winston"

snapshots["test_fullname[fr-None-Winston-prof-dr-female] 1"] = "Madame Prof. Dr Winston"

snapshots["test_fullname[fr-None-Winston-prof-dr-male] 1"] = "Monsieur Prof. Dr Winston"

snapshots["test_fullname[fr-None-Winston-prof-dr-neutral] 1"] = "Prof. Dr Winston"

snapshots["test_fullname[fr-None-Winston-prof-female] 1"] = "Madame Prof. Winston"

snapshots["test_fullname[fr-None-Winston-prof-male] 1"] = "Monsieur Prof. Winston"

snapshots["test_fullname[fr-None-Winston-prof-neutral] 1"] = "Prof. Winston"

snapshots["test_fullname[fr-Smith-None-dr-female] 1"] = "Madame Dr Smith"

snapshots["test_fullname[fr-Smith-None-dr-male] 1"] = "Monsieur Dr Smith"

snapshots["test_fullname[fr-Smith-None-dr-neutral] 1"] = "Dr Smith"

snapshots["test_fullname[fr-Smith-None-none-female] 1"] = "Madame Smith"

snapshots["test_fullname[fr-Smith-None-none-male] 1"] = "Monsieur Smith"

snapshots["test_fullname[fr-Smith-None-none-neutral] 1"] = "Smith"

snapshots["test_fullname[fr-Smith-None-pd-dr-female] 1"] = "Madame PD Dr Smith"

snapshots["test_fullname[fr-Smith-None-pd-dr-male] 1"] = "Monsieur PD Dr Smith"

snapshots["test_fullname[fr-Smith-None-pd-dr-neutral] 1"] = "PD Dr Smith"

snapshots["test_fullname[fr-Smith-None-prof-dr-female] 1"] = "Madame Prof. Dr Smith"

snapshots["test_fullname[fr-Smith-None-prof-dr-male] 1"] = "Monsieur Prof. Dr Smith"

snapshots["test_fullname[fr-Smith-None-prof-dr-neutral] 1"] = "Prof. Dr Smith"

snapshots["test_fullname[fr-Smith-None-prof-female] 1"] = "Madame Prof. Smith"

snapshots["test_fullname[fr-Smith-None-prof-male] 1"] = "Monsieur Prof. Smith"

snapshots["test_fullname[fr-Smith-None-prof-neutral] 1"] = "Prof. Smith"

snapshots["test_fullname[fr-Smith-Winston-dr-female] 1"] = "Madame Dr Winston Smith"

snapshots["test_fullname[fr-Smith-Winston-dr-male] 1"] = "Monsieur Dr Winston Smith"

snapshots["test_fullname[fr-Smith-Winston-dr-neutral] 1"] = "Dr Winston Smith"

snapshots["test_fullname[fr-Smith-Winston-none-female] 1"] = "Madame Winston Smith"

snapshots["test_fullname[fr-Smith-Winston-none-male] 1"] = "Monsieur Winston Smith"

snapshots["test_fullname[fr-Smith-Winston-none-neutral] 1"] = "Winston Smith"

snapshots[
    "test_fullname[fr-Smith-Winston-pd-dr-female] 1"
] = "Madame PD Dr Winston Smith"

snapshots[
    "test_fullname[fr-Smith-Winston-pd-dr-male] 1"
] = "Monsieur PD Dr Winston Smith"

snapshots["test_fullname[fr-Smith-Winston-pd-dr-neutral] 1"] = "PD Dr Winston Smith"

snapshots[
    "test_fullname[fr-Smith-Winston-prof-dr-female] 1"
] = "Madame Prof. Dr Winston Smith"

snapshots[
    "test_fullname[fr-Smith-Winston-prof-dr-male] 1"
] = "Monsieur Prof. Dr Winston Smith"

snapshots[
    "test_fullname[fr-Smith-Winston-prof-dr-neutral] 1"
] = "Prof. Dr Winston Smith"

snapshots[
    "test_fullname[fr-Smith-Winston-prof-female] 1"
] = "Madame Prof. Winston Smith"

snapshots[
    "test_fullname[fr-Smith-Winston-prof-male] 1"
] = "Monsieur Prof. Winston Smith"

snapshots["test_fullname[fr-Smith-Winston-prof-neutral] 1"] = "Prof. Winston Smith"
