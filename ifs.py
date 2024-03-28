#!/usr/bin/env python3
import json
import os
import requests
from datetime import datetime

ifs_folder = "content/images/ifs"
ifs_url = "https://mainframe.io/media/ifs-images"

ifs_meta_path = ifs_url + "/meta.json"

ifs_data = json.loads(requests.get(ifs_meta_path).text)

ifs_images = ifs_data["images"][::-1]
ifs_count = len(ifs_images)

total = 0

date = None
ifs_year_folder = None
last_year = 0
year_count = 0
year = 0

for image in ifs_images:
    # check if time exists and is after IFS introduction year (2012)
    if image["exif"]["time"] is not None and image["exif"]["time"] > 1325416332000:
        new_date = datetime.fromtimestamp(int(image["exif"]["time"]) / 1000)

        if date is None or new_date > date:
            date = new_date

        year = date.year

        if year > last_year:
            last_year = year
            year_count = 0

        ifs_year_folder = ifs_folder + "/" + str(year)

        if not os.path.exists(ifs_year_folder):
            os.mkdir(ifs_year_folder)

    if image["exif"]["time"] is not None:
        datetime_str = datetime.fromtimestamp(int(image["exif"]["time"]) / 1000).strftime("%Y-%m-%dT%H:%M:%S")
    else:
        datetime_str = "1970-01-01T01:00:00"

    year_count += 1

    frontmatter = '+++\n'
    frontmatter += 'title = "Images From Space ' + str(year) + '"\n'
    frontmatter += 'sort_by = "weight"\n'
    frontmatter += 'template = "album/album-list.html"\n'
    frontmatter += 'weight = ' + str(year) + '\n'
    frontmatter += 'in_search_index = false\n'
    frontmatter += '[extra]\n'
    frontmatter += 'display_name = "' + str(year) + '"\n'
    frontmatter += 'image_count = ' + str(year_count) + '\n'
    frontmatter += '+++\n'

    f = open(ifs_year_folder + "/_index.md", "w")
    f.write(frontmatter)
    f.close()

    f = open(ifs_year_folder + "/_index.en.md", "w")
    f.write(frontmatter)
    f.close()

    image_id = int(image["filename"].split(".")[0])
    image_id_str = str(image_id)
    title = 'IFS ' + image_id_str

    frontmatter = '+++\n'
    frontmatter += 'title = "' + title + '"\n'
    frontmatter += 'slug = "' + image_id_str + '"\n'
    frontmatter += 'weight = ' + image_id_str + '\n'
    frontmatter += 'template = "album/album-single.html"\n'
    frontmatter += 'in_search_index = false\n'
    frontmatter += 'date = ' + datetime_str + '\n'

    frontmatter_extra = '[extra]\n'
    frontmatter_extra += 'filename = "' + image["filename"] + '"\n'
    frontmatter_extra += 'height = ' + str(image["height"]) + "\n"
    frontmatter_extra += 'width = ' + str(image["width"]) + "\n"
    frontmatter_extra += 'file_uri = "' + ifs_url + "/" + image["filename"] + '"\n'
    frontmatter_extra += 'file_uri_300 = "' + ifs_url + "/.thumbs/300-" + image["filename"] + '"\n'
    frontmatter_extra += 'file_uri_750 = "' + ifs_url + "/.thumbs/750-" + image["filename"] + '"\n'
    frontmatter_extra += 'file_uri_1200 = "' + ifs_url + "/.thumbs/1200-" + image["filename"] + '"\n'

    frontmatter_extra += "\nimage_id = " + image_id_str
    frontmatter_extra += "\nimage_year = " + str(year)
    frontmatter_extra += '\nog_title = "' + title + '"'
    frontmatter_extra += '\nog_description = "Random Image From Space of the hackspace oldenburg"'
    frontmatter_extra += '\n+++\n'

    image_elem = '![' + title + '](' + ifs_url + '/.thumbs/750-' + image["filename"] + ')'

    f = open(ifs_folder + "/" + str(year) + "/" + "IFS-" + image_id_str + ".md", "w")
    f.write(frontmatter)
    f.write('aliases = ["/images/ifs/by-id/' + image_id_str + '"]\n')
    f.write(frontmatter_extra)
    f.close()

    f = open(ifs_folder + "/" + str(year) + "/" + "IFS-" + image_id_str + ".en.md", "w")
    f.write(frontmatter)
    f.write('aliases = ["/en/images/ifs/by-id/' + image_id_str + '"]\n')
    f.write(frontmatter_extra)
    f.close()

    total += 1

    print("IFS markdown page for IFS " + image_id_str + " created")

print("Created a total of " + str(total) + " IFS markdown pages")
