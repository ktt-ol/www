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

    frontmatter = '+++\n'
    frontmatter += 'title = "IFS ' + image_id_str + '"\n'
    frontmatter += 'weight = ' + str(ifs_count - image_id) + '\n'
    frontmatter += '[extra]\n'
    frontmatter += 'image_filename = "' + image["filename"] + '"'
    frontmatter += "\nwidth = " + str(image["width"])
    frontmatter += "\nheight = " + str(image["height"])
    frontmatter += '\n+++\n'

    content = "\n"
    content += "\n#### Image From Space " + image_id_str + ' {{ button(text="%replace_with_text%", location="/images/ifs/all/") }}'
    content += "\n"
    content += '{{ button(text="<<", location="/images/ifs/all/' + str(image_id + 1) + '", disabled="' + str(image_id + 1 >= (ifs_count-1)) + '") }}'
    content += '{{ ifs_image(filename="' + image["filename"] + '", height=' + str(image["height"]) + ', width=' + str(image["width"]) + ') }}'
    content += '{{ button(text=">>", location="/images/ifs/all/' + str(image_id - 1) + '", disabled="' + str(image_id - 1 < 0) + '") }}'

    f = open(ifs_folder_all + "/" + image_id_str + ".md", "w")
    f.write(frontmatter)
    f.write(content.replace("%replace_with_text%", "Alle Images From Space"))
    f.close()

    f = open(ifs_folder_all + "/" + image_id_str + ".en.md", "w")
    f.write(frontmatter)
    f.write(content.replace("%replace_with_text%", "All Images From Space"))
    f.close()

    print("IFS markdown page for " + image_id_str + " created")

    total += 1

print("Created a total of " + str(total) + " IFS markdown pages")
