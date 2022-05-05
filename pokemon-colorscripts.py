#!/usr/bin/env python3

import argparse
import os
import random
import sys

PROGRAM = os.path.realpath(__file__)
PROGRAM_DIR = os.path.dirname(PROGRAM)
COLORSCRIPTS_DIR = f"{PROGRAM_DIR}/colorscripts"

REGULAR_SUBDIR = "regular"
SHINY_SUBDIR = "shiny"

SHINY_RATE = 1 / 128
GENERATIONS = {
    "1": (1, 151),
    "2": (152, 251),
    "3": (252, 386),
    "4": (387, 493),
    "5": (494, 649),
    "6": (650, 721),
    "7": (722, 809),
    "8": (810, 898),
}


def print_file(filepath: str) -> None:
    with open(filepath, "r") as f:
        print(f.read())


def list_pokemon_names() -> None:
    print_file(f"{PROGRAM_DIR}/nameslist.txt")


def show_pokemon_by_name(name: str, show_title: bool, shiny: bool) -> None:
    base_path = COLORSCRIPTS_DIR
    color_subdir = SHINY_SUBDIR if shiny else REGULAR_SUBDIR
    pokemon = f"{base_path}/{color_subdir}/{name}.txt"
    if not os.path.isfile(pokemon):
        print(f"Invalid pokemon '{name}'")
        sys.exit(1)
    if show_title:
        if shiny:
            print(f"{name} (shiny)")
        else:
            print(name)
    print_file(pokemon)


def show_random_pokemon(generations: str, show_title: bool, shiny: bool) -> None:
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
        # if the shiny flag is not passed, set a small random chance for the
        # pokemon to be shiny. If the flag is set, always show shiny
        if not shiny:
            shiny = random.random() <= SHINY_RATE
        show_pokemon_by_name(random_pokemon, show_title, shiny)
    except KeyError:
        print(f"Invalid generation '{generations}'")
        sys.exit(1)


def main(arguments) -> None:
    parser = argparse.ArgumentParser(
        prog="pokemon-colorscripts",
        description="CLI utility to print out unicode image of a pokemon in your shell",
        usage="pokemon-colorscripts [OPTION] [POKEMON NAME]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit"
    )
    parser.add_argument(
        "-l", "--list", help="Print list of all pokemon", action="store_true"
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="""Select pokemon by name. Generally spelled like in the games.
                a few exceptions are nidoran-f, nidoran-m, mr-mime, farfetchd, flabebe
                type-null etc. Perhaps grep the output of --list if in
                doubt.""",
    )
    parser.add_argument(
        "--no-title", action="store_false", help="Do not display pokemon name"
    )
    parser.add_argument(
        "-s",
        "--shiny",
        action="store_true",
        help="Show the shiny version of the pokemon instead",
    )
    parser.add_argument(
        "-r",
        "--random",
        type=str,
        const="1-8",
        nargs="?",
        help="""Show a random pokemon. This flag can optionally be
                followed by a generation number or range (1-8) to show random
                pokemon from a specific generation or range of generations.
                The generations can be provided as a continuous range (eg. 1-3)
                or as a list of generations (1,3,6)""",
    )

    args = parser.parse_args(arguments)

    if args.list:
        list_pokemon_names()
    elif args.name:
        show_pokemon_by_name(args.name, args.no_title, args.shiny)
    elif args.random:
        show_random_pokemon(args.random, args.no_title, args.shiny)
    else:
        parser.print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
