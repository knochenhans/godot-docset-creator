import json
import os
import subprocess

from bs4 import BeautifulSoup, Tag

langcode = "en"
version = "4.2"


def process_html_file(file_path):
    with open(file_path, "r") as file:
        html = file.read()
        soup = BeautifulSoup(html, "html.parser")

        elem = soup.find("nav")

        if isinstance(elem, Tag):
            elem.decompose()

        elem = soup.find("title")
        if isinstance(elem, Tag):
            elem.string = elem.string.replace(
                f" — Godot Engine ({version}) documentation in English", ""
            )

        elem = soup.find("div", class_="rst-versions")

        if isinstance(elem, Tag):
            elem.decompose()

        elem = soup.find("div", class_="admonition-grid")

        if isinstance(elem, Tag):
            elem.decompose()

        elem = soup.find("div", attrs={"role": "navigation"})

        if isinstance(elem, Tag):
            elem.decompose()

        # Save the modified HTML back to the file
        with open(file_path, "w") as modified_file:
            modified_file.write(str(soup))


def process_html_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for i, file in enumerate(files):
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                process_html_file(file_path)
                print(f"Processed file {i+1}/{len(files)}: {file_path}")


def editDashingJSON():
    # Open the dashing.json file
    with open("dashing.json", "r") as file:
        data = json.load(file)

    # Modify the title selector to match the new title with version info
    version_string = version.replace(".", "\\.")

    data["selectors"]["title"][
        "regexp"
    ] = f" — Godot Engine \\({version_string}\\) documentation in English"

    # Save the modified data back to the file
    with open("dashing.json", "w") as file:
        json.dump(data, file, indent=4)


command = f"wget --no-parent -r -c -w 0.1 https://docs.godotengine.org/{langcode}/{version}/ -nH --cut-dirs=2"
subprocess.run(command, shell=True)

editDashingJSON()

command = "dashing build mydocs"
subprocess.run(command, shell=True)

process_html_files_in_folder("godot.docset")
