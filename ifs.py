#!/usr/bin/env python3
import json
from typing import Optional
import requests
import os
from datetime import datetime

languages = ["de", "en"]

ifs_url = "https://mainframe.io/media/ifs-images/meta.json"
ifs_image_path = "content/images/ifs"

frontmatter_template_ifs = """+++
title = "IFS {0}"
slug = "{0}"
weight = {0}
template = "album/album-single.html"
in_search_index = false
date = {5}
aliases = ["/{4}images/ifs/by-id/{0}"]

[extra]
filename = "{1}"

height = {2}
width = {3}

file_uri = "https://mainframe.io/media/ifs-images/{1}"
file_uri_300 = "https://mainframe.io/media/ifs-images/.thumbs/300-{1}"
file_uri_750 = "https://mainframe.io/media/ifs-images/.thumbs/750-{1}"
file_uri_1200 = "https://mainframe.io/media/ifs-images/.thumbs/1200-{1}"

og_title = "IFS {0}"
"""

frontmatter_template_index = """+++
title = "Images From Space {0}"
sort_by = "weight"
template = "album/album-list.html"
weight = {0}
in_search_index = false
[extra]
display_name = "{0}"
+++
"""


class IfsImage:
    def __init__(self, image: dict, date: datetime):
        self.ifs_id = int(image["filename"].split(".")[0])
        self.filename = image["filename"]
        self.height = image["height"]
        self.width = image["width"]
        self.date = date


def generate_frontmatter(lang: str, current: IfsImage, previous: Optional[IfsImage], next: Optional[IfsImage]) -> str:
    frontmatter = frontmatter_template_ifs.format(
        current.ifs_id,
        current.filename,
        current.height,
        current.width,
        lang + "/",
        current.date.strftime("%Y-%m-%dT%H:%M:%S"),
        current.date.strftime("%Y")
    )

    if previous is not None:
        frontmatter += '\nprevious = "/images/ifs/{0}/IFS-{1}.md"'.format(previous.date.year, previous.ifs_id)

    if next is not None:
        frontmatter += '\nnext = "/images/ifs/{0}/IFS-{1}.md"'.format(next.date.year, next.ifs_id)

    frontmatter += "\n+++\n"

    return frontmatter


def generate_ifs_document(path: str, lang: str, current: IfsImage, previous: IfsImage, next: IfsImage):
    frontmatter = generate_frontmatter(lang, current, previous, next)

    if lang == "de":
        filepath = "{0}/{1}/IFS-{2}.md".format(path, current.date.strftime("%Y"), current.ifs_id)
    else:
        filepath = "{0}/{1}/IFS-{2}.{3}.md".format(path, current.date.strftime("%Y"), current.ifs_id, lang)

    with open(filepath, "w") as f:
        f.write(frontmatter)


def fetch_ifs_data(url: str) -> list:
    ifs_data = json.loads(requests.get(url).text)
    ifs_data = ifs_data["images"][::-1]

    current_date = None

    entries = []

    for image in ifs_data:
        if image["exif"]["time"] is not None and image["exif"]["time"] > 1325416332000:
            new_date = datetime.fromtimestamp(int(image["exif"]["time"]) / 1000)

            if current_date is None or new_date > current_date:
                current_date = new_date

        entries.append(IfsImage(image, current_date))

    return entries


def create_year_sections(path: str, images):
    year_counts = {}

    for image in images:
        year = str(image.date.year)
        year_counts[year] = year_counts.get(year, 0) + 1

    for year in year_counts:
        frontmatter = frontmatter_template_index.format(year)

        ifs_year_folder = path + "/" + str(year)

        if not os.path.exists(ifs_year_folder):
            os.mkdir(ifs_year_folder)

        for lang in languages:
            if lang == "de":
                filepath = os.path.join(ifs_year_folder, "_index.md")
            else:
                filepath = os.path.join(ifs_year_folder, "_index.{0}.md".format(lang))

            with open(filepath, "w") as f:
                f.write(frontmatter)


def create_ifs_markdown_pages(path: str, images: list):
    for i in range(0, len(images)):
        for lang in languages:
            generate_ifs_document(
                path,
                lang,
                images[i],
                images[(i - 1) % len(images)],
                images[(i + 1) % len(images)]
            )


ifs_images = fetch_ifs_data(ifs_url)

create_year_sections(ifs_image_path, ifs_images)

create_ifs_markdown_pages(ifs_image_path, ifs_images)

print("Created a total of {0} IFS markdown pages ".format(len(ifs_images)))
