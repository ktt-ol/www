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
        new_date = datetime.utcfromtimestamp(int(image["exif"]["time"]) / 1000)
        if(date == None or new_date > date):
            date = new_date

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
        frontmatter += 'in_search_index = true\n'
        frontmatter += 'transparent = false\n'
        frontmatter += '[extra]\n'
        frontmatter += 'year = ' + year + '\n'
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
    frontmatter += 'in_search_index = false\n'
    
    if image["exif"]["time"]:
        frontmatter += 'date = "' + datetime_str + '"\n'

    frontmatter_extra = '[extra]\n'
    frontmatter_extra += 'image_filename = "' + image["filename"] + '"'
    frontmatter_extra += "\nwidth = " + str(image["width"])
    frontmatter_extra += "\nheight = " + str(image["height"])
    frontmatter_extra += "\nimage_id = " + image_id_str
    frontmatter_extra += "\nimage_year = " + year
    frontmatter_extra += '\nog_title = "' + title + '"'
    frontmatter_extra += '\nog_description = "Random Image From Space of the hackspace oldenburg"'
    frontmatter_extra += '\n+++\n'

    image_elem = '![' + title + '](' + ifs_image_path + '/.thumbs/750-' + image["filename"] +')'

    f = open(ifs_folder_all + "/"  + year + "/" + "IFS-" + image_id_str + ".md", "w")
    f.write(frontmatter)
    f.write('aliases = ["/images/ifs/by-id/' + image_id_str + '"]\n')
    f.write(frontmatter_extra)
    f.close()

    f = open(ifs_folder_all + "/"  + year + "/" + "IFS-" + image_id_str + ".en.md", "w")
    f.write(frontmatter)
    f.write('aliases = ["/en/images/ifs/by-id/' + image_id_str + '"]\n')
    f.write(frontmatter_extra)
    f.close()

    total += 1

    print("IFS markdown page for IFS " + image_id_str + " created")


print("Created a total of " + str(total) + " IFS markdown pages")
