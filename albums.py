#!/usr/bin/env python3
import json
import os
import requests
import tempfile
from os.path import join as join_path
from slugify import slugify
from datetime import datetime
from threading import Thread

albums_path = "content/images/albums"
albums_url = "https://www.mainframe.io/media/album-images"

tmp_folder = tempfile.mkdtemp(prefix="ktt_ol_albums")
print(tmp_folder)


def get_url_metadata(folder) -> dict:
    url = albums_url + "/" + folder + "/meta.json"
    print("Fetching meta from: " + url)
    folder_data = json.loads(requests.get(url).text)
    return folder_data


def create_index_md(base_uri: str, folder_path: str, folder: dict, lang: str, created: datetime) -> None:
    title = folder["title"]

    title.replace('"', '\"')

    header = "+++\n"
    header += 'title = "' + lang + title + '"\n'
    header += 'template = "album/album-list.html"\n'
    header += '[extra]\n'
    header += 'display_name = "' + title + '"\n'
    header += 'image_count = ' + str(folder["imageCount"]) + '\n'

    if "cover" in folder and folder["cover"] is not None:
        header += 'cover = "' + albums_url + "/" + base_uri + "/" + folder["cover"] + '"\n'

    if created is not None:
        header += 'date = "' + created.strftime("%Y-%m-%dT%H:%M:%S") + '"\n'

    header += "+++\n"

    if lang != "":
        lang = "." + lang

    f = open(join_path(folder_path, "_index" + lang + ".md"), "w")
    f.write(header)
    f.close()


def create_image_md(base_uri: str, folder_path: str, image_metadata: dict, lang: str) -> None:
    filename = image_metadata["filename"]
    filename = filename.replace('"', '\"')
    slug_name = slugify(filename)

    if lang != "":
        lang = "." + lang

    image_file = open(join_path(folder_path, slug_name + lang + ".md"), "w")

    image_file.write("+++\n")
    image_file.write('title = "' + filename + '"\n')
    image_file.write('template = "album/album-single.html"\n')

    image_file.write('[extra]\n')
    image_file.write('height = ' + str(image_metadata["height"]) + "\n")
    image_file.write('width = ' + str(image_metadata["width"]) + "\n")
    image_file.write('file_uri = "' + albums_url + "/" + base_uri + "/" + filename + '"\n')
    image_file.write('file_uri_300 = "' + albums_url + "/" + base_uri + "/.thumbs/300-" + filename + '"\n')
    # Albums do not have 750 pixel thumbnail, use 1200 instead
    image_file.write('file_uri_750 = "' + albums_url + "/" + base_uri + "/.thumbs/1200-" + filename + '"\n')
    image_file.write('file_uri_1200 = "' + albums_url + "/" + base_uri + "/.thumbs/1200-" + filename + '"\n')
    image_file.write("+++\n")
    image_file.close()


def create_album_folder(base_uri: str, base_path: str, album_metadata: dict) -> None:
    base_uri = base_uri + "/" + album_metadata["foldername"]
    directory_metadata = get_url_metadata(base_uri)

    if 'time' in directory_metadata:
        date = datetime.fromtimestamp(int(directory_metadata["time"]) / 1000)
    else:
        date = None

    album_folder_slug = slugify(album_metadata["foldername"])
    album_folder = join_path(base_path, album_folder_slug)
    os.makedirs(album_folder)

    create_index_md(base_uri, album_folder, album_metadata, "", date)
    create_index_md(base_uri, album_folder, album_metadata, "en", date)

    for image_metadata in directory_metadata["images"]:
        create_image_md(base_uri, album_folder, image_metadata, "")
        create_image_md(base_uri, album_folder, image_metadata, "en")

    sub_threads = []
    for sub_directory in directory_metadata["subDirs"]:
        sub_thread = Thread(target=create_album_folder, args=(base_uri, album_folder, sub_directory))
        sub_thread.start()
        sub_threads.append(sub_thread)

    for sub_thread in sub_threads:
        sub_thread.join()


current_path = tmp_folder
base_metadata = get_url_metadata("")

threads = []
for directory in base_metadata["subDirs"]:
    thread = Thread(target=create_album_folder, args=("", current_path, directory))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()


index_file = open(join_path(tmp_folder, "_index.md"), "w")
index_file.write("+++\n")
index_file.write("title = 'Fotoalben'\n")
index_file.write("template = 'album/album-list.html'\n")
index_file.write("+++\n")
index_file.close()

index_file = open(join_path(tmp_folder, "_index.en.md"), "w")
index_file.write("+++\n")
index_file.write("title = 'Albums'\n")
index_file.write("template = 'album/album-list.html'\n")
index_file.write("+++\n")
index_file.close()

os.rename(tmp_folder, albums_path)
