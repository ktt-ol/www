#!/usr/bin/env python3
import os, errno, json, requests

ifs_folder = os.environ["IFS_FOLDER"]
ifs_path = os.environ["IFS_PATH"]

ifs_meta_path = ifs_path + "/meta.json"
ifs_image_path = ifs_path

ifs_folder_all = ifs_folder + "/all"

ifs_data = json.loads(requests.get(ifs_meta_path).text)
ifs_images = ifs_data["images"]

total = 0
for image in ifs_images:
    image_id = int(image["filename"].split(".")[0])
    image_id_str = str(image_id)

    frontmatter = "+++\n"
    frontmatter += "title = \"Image From Space " + image_id_str + "\"\n"
    frontmatter += "weight = " + image_id_str + "\n"
    frontmatter += "+++\n" 
    
    content = "\n"
    content += "![IFS Image Number " + image_id_str + "](" + ifs_image_path + "/" + image["filename"] + ")"
  
    f = open(ifs_folder_all + "/" + image_id_str + ".md", "w")
    f.write(frontmatter)
    f.write(content)
    f.close()

    print("IFS markdown page for " + image_id_str + " created")

    total += 1
    
print("Created a total of " + str(total) + " IFS markdown pages")