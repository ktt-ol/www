#!/usr/bin/env python3
import os, errno, json, requests

ifs_folder = os.environ["IFS_FOLDER"]
ifs_path = os.environ["IFS_PATH"]

ifs_meta_path = ifs_path + "/meta.json"
ifs_image_path = ifs_path

ifs_folder_all = ifs_folder + "/all"

ifs_data = json.loads(requests.get(ifs_meta_path).text)
ifs_images = ifs_data["images"]

ifs_count = len(ifs_images)
total = 0
for image in ifs_images:
    image_id = int(image["filename"].split(".")[0])
    image_id_str = str(image_id)
    title = 'IFS ' + image_id_str

    frontmatter = '+++\n'
    frontmatter += 'title = "' + title + '"\n'
    frontmatter += 'weight = ' + str(ifs_count - image_id) + '\n'
    frontmatter += 'template = "ifs/ifs-single.html"\n'
    frontmatter += '[extra]\n'
    frontmatter += 'image_filename = "' + image["filename"] + '"'
    frontmatter += "\nwidth = " + str(image["width"])
    frontmatter += "\nheight = " + str(image["height"])
    frontmatter += "\nimage_id = " + image_id_str
    frontmatter += '\nog_title = "' + title + '"'
    frontmatter += '\nog_description = "Random Image From Space of the hackspace oldenburg"'
    frontmatter += '\n+++\n'

    image_elem = '![' + title + '](' + ifs_image_path + '/.thumbs/750-' + image["filename"] +')'

    content = "\n"
    content += "\n#### " + title + ' {{ button(text="%replace_with_text%", location="/images/ifs/all/") }}'
    content += "\n"
    content += '{{ button(text="<<", location="/images/ifs/all/' + str(image_id + 1) + '", disabled="' + str(image_id + 1 >= (ifs_count)) + '") }}\n'
    content += '[' + image_elem + '](' + ifs_image_path + '/' + image["filename"] + ')\n'
    content += '{{ button(text=">>", location="/images/ifs/all/' + str(image_id - 1) + '", disabled="' + str(image_id - 1 <= 0) + '") }}\n'

    f = open(ifs_folder_all + "/" + image_id_str + ".md", "w")
    f.write(frontmatter)
    f.write(content.replace("%replace_with_text%", "Alle Images From Space"))
    f.close()

    f = open(ifs_folder_all + "/" + image_id_str + ".en.md", "w")
    f.write(frontmatter)
    f.write(content.replace("%replace_with_text%", "All Images From Space"))
    f.close()

    total += 1

    print("IFS markdown page for " + image_id_str + " created")


print("Created a total of " + str(total) + " IFS markdown pages")
