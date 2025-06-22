#!/usr/bin/env python3
import json
import os
from datetime import datetime

import requests

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

year_counts = {}
for image in ifs_images:
    if image["exif"]["time"] is not None and image["exif"]["time"] > 1325416332000:
        new_date = datetime.fromtimestamp(int(image["exif"]["time"]) / 1000)

        if date is None or new_date > date:
            date = new_date

        year = date.year

        if year > last_year:
            year_counts[str(last_year)] = year_count
            last_year = year
            year_count = 0

    year_count += 1

year_counts[str(year)] = year_count

date = None
last_year = 0
year_count = 0
year = 0

print(year_counts)

for image in ifs_images:
    total += 1

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

    frontmatter_extra = '\n[extra]\n'
    frontmatter_extra += 'filename = "' + image["filename"] + '"\n'
    frontmatter_extra += '\n'

    frontmatter_extra += 'height = ' + str(image["height"]) + "\n"
    frontmatter_extra += 'width = ' + str(image["width"]) + "\n"

    frontmatter_extra += '\n'

    frontmatter_extra += 'file_uri = "' + ifs_url + "/" + image["filename"] + '"\n'
    frontmatter_extra += 'file_uri_300 = "' + ifs_url + "/.thumbs/300-" + image["filename"] + '"\n'
    frontmatter_extra += 'file_uri_750 = "' + ifs_url + "/.thumbs/750-" + image["filename"] + '"\n'
    frontmatter_extra += 'file_uri_1200 = "' + ifs_url + "/.thumbs/1200-" + image["filename"] + '"\n'

    frontmatter_extra += '\nog_title = "' + title + '"\n'

    frontmatter_extra += '\n'

    if total > 1:
        previous_id = int(ifs_images[total - 2]["filename"].split(".")[0])
        frontmatter_extra += ('previous = \"/images/ifs/{0}/IFS-{1}.md\"\n'
                              .format(str(year if year_count > 1 else (year - 1)), str(previous_id)))

    if total < len(ifs_images):
        next_id = int(ifs_images[total]["filename"].split(".")[0])

        frontmatter_extra += ('next = \"/images/ifs/{0}/IFS-{1}.md\"\n'
                              .format(str(year if year_count < year_counts[str(year)] else (year + 1)),
                                      str(next_id)))

    f = open("{0}/{1}/IFS-{2}.md".format(ifs_folder, str(year), image_id_str), "w")
    f.write(frontmatter)
    f.write('aliases = [\"/images/ifs/by-id/{0}\"]\n'.format(image_id_str))
    f.write(frontmatter_extra)
    f.write('+++\n')
    f.close()

    f = open("{0}/{1}/IFS-{2}.en.md".format(ifs_folder, str(year), image_id_str), "w")
    f.write(frontmatter)
    f.write('aliases = [\"/en/images/ifs/by-id/{0}\"]\n'.format(image_id_str))
    f.write(frontmatter_extra)
    f.write('+++\n')
    f.close()

    print("IFS markdown page for IFS {0} ({1} in year {2}) created".format(image_id_str, str(year_count), str(year)))

print("Created a total of {0} IFS markdown pages out of {1} entries".format(str(total), str(len(ifs_images))))
