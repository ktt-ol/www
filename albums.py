#!/usr/bin/env python3
import json
import os
import time
import requests
import tempfile
import hashlib
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
    folder_data = json.loads(requests.get(url).text)
    return folder_data


def get_cover_image(path_components: list[str], tmp_folder_covers: str, image_filename: str) -> str:
    url = albums_url + "/" + join_web_path(path_components) + "/" + image_filename

    img_data = requests.get(url).content

    filename, file_extension = os.path.splitext(image_filename)
    file_hash = hashlib.sha256(img_data).hexdigest()
    filename = slugify(filename) + "_" + file_hash + file_extension

    img_file_path = join_path(tmp_folder_covers, filename)

    if os.path.exists(img_file_path) and os.path.isfile(img_file_path):
        return filename

    img_file = open(img_file_path, "wb")
    img_file.write(img_data)
    img_file.close()

    return filename


def create_index_md(path_components: list[str], tmp_folder_albums: str, tmp_folder_covers: str, metadata: dict,
                    created_at: datetime, lang: str) -> None:
    title = metadata["title"]
    title = title.replace('"', '\"')

    if lang != "":
        lang = "." + lang

    f = open(join_path(tmp_folder_albums, join_folder_path(path_components), "_index" + lang + ".md"), "w")
    f.write("+++\n")
    f.write('title = "' + title + '"\n')
    f.write('template = "album/album-list.html"\n')
    f.write('sort_by = "date"\n')
    f.write('weight = ' + str(int(time.mktime(created_at.timetuple()))) + '\n')

    f.write('[extra]\n')
    f.write('display_name = "' + title + '"\n')
    f.write('image_count = ' + str(metadata["imageCount"]) + '\n')

    if metadata["cover"] is not None:
        cover_image_path = join_path(cover_path, get_cover_image(path_components, tmp_folder_covers, metadata["cover"]))
        cover_image_path = cover_image_path.replace("\\", "\\\\")
        f.write('cover = "' + cover_image_path + '"\n')

    f.write("+++\n")
    f.close()


def create_image_md(path_components: list[str], tmp_folder_albums: str, metadata: dict, created_at: datetime,
                    lang: str) -> None:
    if lang != "":
        lang = "." + lang

    base_uri = join_web_path(path_components)

    date_str = created_at.strftime("%Y-%m-%d")
    time_str = created_at.strftime("%H:%M:%S")

    page_filename = date_str + "-" + slugify(metadata["filename"]) + lang + ".md"
    image_file_path = join_path(tmp_folder_albums, join_folder_path(path_components), page_filename)

    if os.path.exists(image_file_path):
        raise FileExistsError(image_file_path)

    image_file = open(image_file_path, "w")

    image_file.write("+++\n")
    image_file.write('title = "' + metadata["filename"] + '"\n')
    image_file.write('template = "album/album-single.html"\n')
    image_file.write('sort_by = "title"\n')
    image_file.write('date = ' + date_str + "T" + time_str + '\n')

    image_file.write('[extra]\n')
    image_file.write('filename = "' + metadata["filename"] + '"\n')
    image_file.write('height = ' + str(metadata["height"]) + "\n")
    image_file.write('width = ' + str(metadata["width"]) + "\n")
    image_file.write('file_uri = "' + albums_url + "/" + base_uri + "/" + metadata["filename"] + '"\n')
    image_file.write('file_uri_300 = "' + albums_url + "/" + base_uri + "/.thumbs/300-" + metadata["filename"] + '"\n')

    # Albums do not have 750 pixel thumbnail, use 1200 instead
    image_file.write('file_uri_750 = "' + albums_url + "/" + base_uri + "/.thumbs/1200-" + metadata["filename"] + '"\n')
    image_file.write(
        'file_uri_1200 = "' + albums_url + "/" + base_uri + "/.thumbs/1200-" + metadata["filename"] + '"\n')
    image_file.write("+++\n")
    image_file.close()


def create_album_folder(path_components: list[str], tmp_folder_albums: str, tmp_folder_covers: str,
                        metadata: dict) -> None:
    path_components = path_components.copy()
    path_components.append(metadata["foldername"])

    if metadata['time'] is not None:
        album_created_at = datetime.fromtimestamp(int(metadata["time"]) / 1000)
    else:
        print("Album has no creation date: ", path_components)
        album_created_at = datetime.fromtimestamp(0)

    joined_path = join_folder_path(path_components)

    album_folder = join_path(tmp_folder_albums, joined_path)
    os.makedirs(album_folder)

    create_index_md(path_components, tmp_folder_albums, tmp_folder_covers, metadata, album_created_at, "")
    create_index_md(path_components, tmp_folder_albums, tmp_folder_covers, metadata, album_created_at, "en")

    current_metadata = get_url_metadata(path_components)
    for image_metadata in current_metadata["images"]:
        if image_metadata['exif']['time'] is not None:
            image_created_at = datetime.fromtimestamp(int(image_metadata['exif']['time']) / 1000)
        else:
            image_created_at = datetime.fromtimestamp(0)

        create_image_md(path_components, tmp_folder_albums, image_metadata, image_created_at, "")
        create_image_md(path_components, tmp_folder_albums, image_metadata, image_created_at, "en")

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
index_file.write('sort_by = "date"\n')
index_file.write("+++\n")
index_file.close()

index_file = open(join_path(tmp_ktt_ol_albums, "_index.en.md"), "w")
index_file.write("+++\n")
index_file.write("title = 'Albums'\n")
index_file.write("template = 'album/album-list.html'\n")
index_file.write('sort_by = "date"\n')
index_file.write("+++\n")
index_file.close()

os.rename(tmp_ktt_ol_albums, albums_path)
os.rename(tmp_ktt_ol_cover, cover_path)
