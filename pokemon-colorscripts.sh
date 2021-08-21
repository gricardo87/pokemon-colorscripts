#!/bin/sh

# Checking the OS so as to use mac specific utilities on MacOS
OS=$(uname)
if [ $OS = 'Darwin' ]
then
    PROGRAM=$(greadlink -f "$0")
else
    PROGRAM=$(readlink -f "$0")
fi

PROGRAM_DIR=$(dirname "$PROGRAM")
# directory where all the art files exist
POKEART_DIR="$PROGRAM_DIR/colorscripts"
# formatting for the help strings
fmt_help="  %-20s\t%-54s\n"


_help(){
    #Function that prints out the help text

    echo "Description: CLI utility to print out unicode image of a pokemon in your shell"
    echo ""
    echo "Usage: pokemon-colorscripts [OPTION] [POKEMON NAME]"
    printf "${fmt_help}" \
        "-h, --help, help" "Print this help." \
        "-l, --list, list" "Print list of all pokemon"\
        "-r, --random, random" "Show a random pokemon. This flag can optionally be
                        followed by a generation number (1-8) to show random
                        pokemon from a specific generation."\
        "-n, --name" "Select pokemon by name. Generally spelled like in the games.
                        a few exceptions are nidoran-f,nidoran-m,mr-mime,farfetchd,flabebe
                        type-null etc. Perhaps grep the output of --list if in
                        doubt"
    echo "Example: 'pokemon-colorscripts --name pikachu'"
}


# Index values where the different generations are seperated in the names list
# Cannot think of a better way to do arrays with narrow POSIX compliance
# 0-151 gen 1, 810-898 gen 8
indices="1 152 251 387 494 650 722 810 898"

_show_random_pokemon(){
    #selecting a random art file from the whole set

    # total number of art files present
    NUM_ART=$(ls -1 "$POKEART_DIR"|wc -l)

    # if there are no arguments show across all generations
    if [ $# = 0 ]; then
        start_index=1
        end_index=$NUM_ART
    elif [ $# = 1 ]; then
        start_index=$(_get_start_index $1)
        end_index=$(_get_end_index $1)
    fi

    # getting a random index (using shuf instead of $RANDOM for POSIX compliance)
    # Using mac coreutils if on MacOS
    if [ $OS = 'Darwin' ]
    then
        random_index=$(gshuf -i "$start_index"-"$end_index" -n 1)
    else
        random_index=$(shuf -i "$start_index"-"$end_index" -n 1)
    fi

    random_pokemon=$(sed $random_index'q;d' "$PROGRAM_DIR/nameslist.txt")
    echo $random_pokemon

    # print out the pokemon art for the pokemon
    gunzip -c "$POKEART_DIR/$random_pokemon.txt.gz"
}

_get_end_index(){
    local i=0
    local gen=$1
    for index in $indices; do
        if [ "$i" = "$gen" ]; then
            echo $index
            break
        fi
        i=$((i + 1))
    done
}

_get_start_index(){
    local i=0
    local gen=$1
    for index in $indices; do
        if [ "$i" = "$((gen-1))" ]; then
            echo $index
            break
        fi
        i=$((i + 1))
    done
}
_show_pokemon_by_name(){
    pokemon_name=$1
    echo $pokemon_name
    # Error handling. Can't think of a better way to do it
    gunzip -c "$POKEART_DIR/$pokemon_name.txt.gz" 2>/dev/null || echo "Invalid pokemon"
}

_list_pokemon_names(){
    cat "$PROGRAM_DIR/nameslist.txt"|less
}

# Handling command line arguments
case "$#" in
    0)
        # display help if no arguments are given
        _help
        ;;
    1)
        # Check flag and show appropriate output
        case $1 in
            -h | --help | help)
                _help
                ;;
            -r | --random | random)
                _show_random_pokemon
                ;;
            -l | --list | list)
                _list_pokemon_names
                ;;
            *)
                echo "Input error."
                exit 1
                ;;
        esac
        ;;

    2)
        if [ "$1" = '-n' ]||[ "$1" = '--name' ]||[ "$1" = 'name' ]; then
            _show_pokemon_by_name "$2"
        elif [ "$1" = -r ]||[ "$1" = '--random' ]||[ "$1" = 'random' ]; then
            if [ "$2" -le 8 ]&&[ "$2" -ge 1 ]; then
                _show_random_pokemon "$2"
            else
                echo "Invalid generation"
                exit 1
            fi
        else
            echo "Input error"
            exit 1
        fi
        ;;
    *)
        echo "Input error, too many arguments."
        exit 1
        ;;
esac
