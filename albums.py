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
cover_path = "album_covers"
albums_url = "https://www.mainframe.io/media/album-images"


def join_folder_path(path_components: list[str]) -> str:
    slugged_path_components = list()

    for component in path_components:
        slugged_path_components.append(slugify(component))

    return os.path.sep.join(slugged_path_components)


def join_web_path(path_components: list[str]) -> str:
    return '/'.join(path_components)


def get_url_metadata(path_components: list[str]) -> dict:
    url = albums_url + "/" + join_web_path(path_components) + "/meta.json"
    print("Fetching meta from: " + url)
    folder_data = json.loads(requests.get(url).text)
    return folder_data


def get_cover_image(path_components: list[str], tmp_folder_covers: str, image_filename: str) -> str:
    url = albums_url + "/" + join_web_path(path_components) + "/" + image_filename

    joined_components = join_folder_path(path_components)
    img_folder_path = join_path(tmp_folder_covers, joined_components)
    img_file_path = join_path(img_folder_path, image_filename)

    if not os.path.exists(img_folder_path):
        os.makedirs(img_folder_path)

    if os.path.exists(img_file_path) and os.path.isfile(img_file_path):
        return join_path(joined_components, image_filename)

    img_data = requests.get(url).content
    img_file = open(img_file_path, "wb")
    img_file.write(img_data)
    img_file.close()

    return join_path(joined_components, image_filename)


def create_index_md(path_components: list[str], tmp_folder_albums: str, tmp_folder_covers: str, metadata: dict,
                    lang: str) -> None:
    if 'time' in metadata and metadata['time'] is not None:
        date = datetime.fromtimestamp(int(metadata["time"]) / 1000)
    else:
        date = None

    title = metadata["title"]
    title = title.replace('"', '\"')

    if lang != "":
        lang = "." + lang

    f = open(join_path(tmp_folder_albums, join_folder_path(path_components), "_index" + lang + ".md"), "w")
    f.write("+++\n")
    f.write('title = "' + title + '"\n')
    f.write('template = "album/album-list.html"\n')

    if date is not None:
        f.write('date = "' + date.strftime("%Y-%m-%dT%H:%M:%S") + '"\n')

    f.write('[extra]\n')
    f.write('display_name = "' + title + '"\n')
    f.write('image_count = ' + str(metadata["imageCount"]) + '\n')

    if "cover" in metadata and metadata["cover"] is not None:
        f.write('cover = "' + join_path(cover_path, get_cover_image(path_components, tmp_folder_covers, metadata["cover"]) + '"\n'))

    f.write("+++\n")
    f.close()


def create_image_md(path_components: list[str], tmp_folder_albums: str, metadata: dict, lang: str) -> None:
    filename = metadata["filename"]
    filename = filename.replace('"', '\"')

    if lang != "":
        lang = "." + lang

    slug_name = slugify(filename)

    base_uri = join_web_path(path_components)

    image_file_path = join_path(tmp_folder_albums, join_folder_path(path_components), slug_name + lang + ".md")
    image_file = open(image_file_path, "w")

    image_file.write("+++\n")
    image_file.write('title = "' + filename + '"\n')
    image_file.write('template = "album/album-single.html"\n')
    image_file.write('sort_by = "title"\n')

    image_file.write('[extra]\n')
    image_file.write('height = ' + str(metadata["height"]) + "\n")
    image_file.write('width = ' + str(metadata["width"]) + "\n")
    image_file.write('file_uri = "' + albums_url + "/" + base_uri + "/" + filename + '"\n')
    image_file.write('file_uri_300 = "' + albums_url + "/" + base_uri + "/.thumbs/300-" + filename + '"\n')

    # Albums do not have 750 pixel thumbnail, use 1200 instead
    image_file.write('file_uri_750 = "' + albums_url + "/" + base_uri + "/.thumbs/1200-" + filename + '"\n')
    image_file.write('file_uri_1200 = "' + albums_url + "/" + base_uri + "/.thumbs/1200-" + filename + '"\n')
    image_file.write("+++\n")
    image_file.close()


def create_album_folder(path_components: list[str], tmp_folder_albums: str, tmp_folder_covers: str,
                        metadata: dict) -> None:
    path_components = path_components.copy()
    path_components.append(metadata["foldername"])
    joined_path = join_folder_path(path_components)

    album_folder = join_path(tmp_folder_albums, joined_path)
    os.makedirs(album_folder)

    create_index_md(path_components, tmp_folder_albums, tmp_folder_covers, metadata, "")
    create_index_md(path_components, tmp_folder_albums, tmp_folder_covers, metadata, "en")

    current_metadata = get_url_metadata(path_components)
    for image_metadata in current_metadata["images"]:
        create_image_md(path_components, tmp_folder_albums, image_metadata, "")
        create_image_md(path_components, tmp_folder_albums, image_metadata, "en")

    sub_threads = []

    for sub_directory in current_metadata["subDirs"]:
        sub_thread = Thread(target=create_album_folder,
                            args=(path_components, tmp_folder_albums, tmp_folder_covers, sub_directory))
        sub_thread.start()
        sub_threads.append(sub_thread)

    for sub_thread in sub_threads:
        sub_thread.join()


base_metadata = get_url_metadata([])

tmp_ktt_ol_albums = tempfile.mkdtemp(prefix="ktt_ol_albums")
tmp_ktt_ol_cover = tempfile.mkdtemp(prefix="ktt_ol_cover")

threads = []
for directory in base_metadata["subDirs"]:
    thread = Thread(target=create_album_folder,
                    args=([], tmp_ktt_ol_albums, tmp_ktt_ol_cover, directory)
                    )
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

index_file = open(join_path(tmp_ktt_ol_albums, "_index.md"), "w")
index_file.write("+++\n")
index_file.write("title = 'Fotoalben'\n")
index_file.write("template = 'album/album-list.html'\n")
index_file.write("+++\n")
index_file.close()

index_file = open(join_path(tmp_ktt_ol_albums, "_index.en.md"), "w")
index_file.write("+++\n")
index_file.write("title = 'Albums'\n")
index_file.write("template = 'album/album-list.html'\n")
index_file.write("+++\n")
index_file.close()

os.rename(tmp_ktt_ol_albums, albums_path)
os.rename(tmp_ktt_ol_cover, cover_path)
