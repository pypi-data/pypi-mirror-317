#!/usr/bin/env python3

"""get-def

Usage:
    get-def (WORD)
    get-def -h

Examples:
    get-def hello

Options:
    -h, --help      show this help message and exit
"""

import requests
from docopt import docopt
from rich import box, print
from rich.console import Console
from rich.padding import Padding
from rich.table import Table
from rich.text import Text


def main():
    args = docopt(__doc__)

    api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    word_url = api_url + args["WORD"]

    response = requests.get(word_url, timeout=60)

    word = response.json()[0].get("word")

    phonetics = response.json()[0].get("phonetics")
    phonetics_dict = {}
    if len(phonetics) > 0:
        for i in range(len(phonetics)):
            if phonetics[i].get("text"):
                phonetics_dict.update({f"Phonetic {i+1}": phonetics[i].get("text")})
            if phonetics[i].get("audio"):
                phonetics_dict.update(
                    {f"Phonetic audio {i+1}": phonetics[i].get("audio")}
                )

    phonetics_table = Table(box=box.SQUARE)
    phonetics_table.add_column("Phonetic Text", style="cyan")
    phonetics_table.add_column("Phonetic Audio")
    if len(phonetics) > 0:
        for item in phonetics:
            text = item.get("text") if item.get("text") else "None"
            audio = item.get("audio") if item.get("audio") else "None"
            phonetics_table.add_row(text, audio)

    meanings = response.json()[0].get("meanings")

    console = Console(width=100)
    print()
    console.rule()
    print()
    print(" :arrow_forward: ", Text(word, style="bold red", justify="center"))
    print()

    console.print(phonetics_table)

    print(
        "Click to view [link=https://www.internationalphoneticassociation.org/IPAcharts/inter_chart_2018/IPA_2018.html]Interactive IPA chart[/link]"
    )
    print()

    # console.rule()
    for item in meanings:
        print(f"[bold]{meanings.index(item) + 1}. [underline]{item["partOfSpeech"]}")
        for definition in item["definitions"]:
            print(
                Padding(
                    f"[bold blue]Definition:[/bold blue] {definition.get("definition")}",
                    (0, 0, 0, 3),
                )
            )
            if definition.get("example") is not None:
                print(
                    Padding(
                        f"[bold magenta]Example:[/bold magenta] {definition.get("example")}",
                        (0, 0, 0, 3),
                    )
                )
            if definition.get("synonyms"):
                print(
                    Padding(
                        f"[bold yellow]Synonyms:[/bold yellow] "
                        + ", ".join(definition.get("synonyms")),
                        (0, 0, 0, 3),
                    )
                )
            if definition.get("antonyms"):
                print(
                    Padding(
                        f"[bold yellow]Antonyms:[/bold yellow] "
                        + ", ".join(definition.get("antonyms")),
                        (0, 0, 0, 3),
                    )
                )
            print()


if __name__ == "__main__":
    main()
