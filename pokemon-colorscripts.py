#!/usr/bin/env python3

import sys
import argparse
import os
import random

PROGRAM = os.path.realpath(__file__)
PROGRAM_DIR = os.path.dirname(PROGRAM)
POKEART_DIR = f"{PROGRAM_DIR}/colorscripts"
POKEART_REGULAR_DIR = f"{POKEART_DIR}/regular"
POKEART_SHINY_DIR = f"{POKEART_DIR}/shiny"
SHINY_RATE = 1/128
GENERATIONS = {"1": (1, 151), "2": (152, 251), "3": (252, 386), "4": (387, 493),
               "5": (494, 649), "6": (650, 721), "7": (722, 809), "8": (810, 898)}


def cat(filepath: str):
    with open(filepath, "r") as f:
        print(f.read())


def list_pokemon_names():
    cat(f"{PROGRAM_DIR}/nameslist.txt")


def show_pokemon_by_name(name: str, title: bool, shiny: bool):
    base_path = POKEART_SHINY_DIR if shiny else POKEART_REGULAR_DIR
    pokemon = f"{base_path}/{name}.txt"
    if not os.path.isfile(pokemon):
        print(f"Invalid pokemon '{name}'")
        sys.exit(1)
    if title:
        if shiny:
            print(f"{name} (shiny)")
        else:
            print(name)
    cat(pokemon)


def show_random_pokemon(generations: str, title: bool):
    # Generation list
    if len(generations.split(",")) > 1:
        input_gens = generations.split(",")
        start_gen = random.choice(input_gens)
        end_gen = start_gen
    # Generation range
    elif len(generations.split("-")) > 1:
        start_gen, end_gen = generations.split("-")
    # Single generation
    else:
        start_gen = generations
        end_gen = start_gen

    with open(f"{PROGRAM_DIR}/nameslist.txt", "r") as f:
        pokemon = [l.strip() for l in f.readlines()]
    try:
        start_idx = GENERATIONS[start_gen][0]
        end_idx = GENERATIONS[end_gen][1]
        random_idx = random.randint(start_idx, end_idx)
        random_pokemon = pokemon[random_idx - 1]
        shiny = random.random() <= SHINY_RATE
        show_pokemon_by_name(random_pokemon, title, shiny)
    except KeyError:
        print(f"Invalid generation '{generations}'")
        sys.exit(1)


def main(arguments):
    parser = argparse.ArgumentParser(prog="pokemon-colorscripts",
                                     description="CLI utility to print out unicode image of a pokemon in your shell",
                                     usage="pokemon-colorscripts [OPTION] [POKEMON NAME]",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     add_help=False)

    parser.add_argument("-h", "--help", action="help",
                        help="Show this help message and exit")
    parser.add_argument(
        "-l", "--list", help="Print list of all pokemon", action="store_true")
    parser.add_argument("-n", "--name", type=str,
                        help="""Select pokemon by name. Generally spelled like in the games.
                        a few exceptions are nidoran-f, nidoran-m, mr-mime, farfetchd, flabebe
                        type-null etc. Perhaps grep the output of --list if in
                        doubt.""")
    parser.add_argument("--no-title", action="store_false",
                        help="Do not display pokemon name")
    parser.add_argument("-s", "--shiny", action="store_true",
                        help="Show the shiny version of the pokemon instead")
    parser.add_argument("-r", "--random", type=str, const="1-8", nargs="?",
                        help="""Show a random pokemon. This flag can optionally be
                        followed by a generation number or range (1-8) to show random
                        pokemon from a specific generation or range of generations.
                        The generations can be provided as a continuous range (eg. 1-3)
                        or as a list of generations (1,3,6)""")

    args = parser.parse_args(arguments)

    if args.list:
        list_pokemon_names()
    elif args.name:
        show_pokemon_by_name(args.name, args.no_title, args.shiny)
    elif args.random:
        show_random_pokemon(args.random, args.no_title)
    else:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
