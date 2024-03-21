#!/usr/bin/env python3
import os, errno, json, requests
from datetime import datetime

ifs_folder = os.environ["IFS_FOLDER"]
ifs_path = os.environ["IFS_PATH"]

ifs_meta_path = ifs_path + "/meta.json"
ifs_image_path = ifs_path

ifs_folder_all = ifs_folder + "/all"

ifs_data = json.loads(requests.get(ifs_meta_path).text)

ifs_images = ifs_data["images"][::-1]
ifs_count = len(ifs_images)

total = 0

date = None
ifs_year_folder = None

for image in ifs_images:
    # check if time exists and is after IFS introduction year (2012)
    if image["exif"]["time"] and image["exif"]["time"] > 1325416332000:
        date = datetime.utcfromtimestamp(int(image["exif"]["time"]) / 1000)
        
        date_str = date.strftime("%Y-%m-%d")
        datetime_str = date_str + "T" + date.strftime("%H:%M:%S")
        
        year = date.strftime("%Y")
        
        ifs_year_folder = ifs_folder_all + "/" + year
        
        if not os.path.exists(ifs_year_folder):
            os.mkdir(ifs_year_folder)
            
            frontmatter = '+++\n'
            frontmatter += 'title = "Images From Space ' + year + '"\n'
            frontmatter += 'sort_by = "weight"\n'
            frontmatter += 'template = "ifs/ifs-all.html"\n'
            frontmatter += 'paginate_by = 100\n'
            frontmatter += 'weight = ' + year + '\n'
            frontmatter += 'transparent = true\n'
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
    frontmatter += 'weight = ' + str(ifs_count - image_id) + '\n'
    frontmatter += 'template = "ifs/ifs-single.html"\n'
    
    if image["exif"]["time"]:
        frontmatter += 'date = "' + datetime_str + '"\n'

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

    f = open(ifs_folder_all + "/"  + year + "/" + "IFS-" + image_id_str + ".md", "w")
    f.write(frontmatter)
    f.write(content.replace("%replace_with_text%", "Alle Images From Space"))
    f.close()

    f = open(ifs_folder_all + "/"  + year + "/" + "IFS-" + image_id_str + ".en.md", "w")
    f.write(frontmatter)
    f.write(content.replace("%replace_with_text%", "All Images From Space"))
    f.close()

    total += 1

    print("IFS markdown page for IFS " + image_id_str + " created")


print("Created a total of " + str(total) + " IFS markdown pages")
