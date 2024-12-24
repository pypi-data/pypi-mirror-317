import urllib.parse
from pathlib import Path

import cairosvg
import requests
import typer

app = typer.Typer()

files = Path("downloads")
files.mkdir(parents=True, exist_ok=True)


@app.command()
def run():
    user_input = input("Enter the URL: ")

    desired_sizes = [500, 1000, 2000]

    while user_input != "q":
        url, *arguments = user_input.split(" ")

        parsed_url = urllib.parse.urlparse(url)
        path = Path(parsed_url.path)
        response = requests.get(url)
        with open(files / path.name, "wb") as f:
            f.write(response.content)

        argument_to_modify = "output_width"
        if arguments:
            desired_sizes = [int(arguments[0])]

            if len(arguments) > 1:
                specification = arguments[1]

                if specification == "-h":
                    argument_to_modify = "output_height"

        for size in desired_sizes:

            cairosvg.svg2png(
                bytestring=response.content, write_to=f"{files / path.name}_{size}.png", **{argument_to_modify: size}
            )

        user_input = input("Enter the URL: ")


if __name__ == "__main__":

    app()
