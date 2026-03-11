#!/usr/bin/env python3
import hashlib
import json
import os
import shutil
import tempfile
import time
from datetime import datetime, timedelta
from os.path import join as join_path
from threading import Thread

import requests
from slugify import slugify

albums_web_path = "images/albums"
albums_path = "content/images/albums"
cover_path = "album_covers"
albums_url = "https://www.mainframe.io/media/album-images"


def join_folder_path(path_components: list[str]) -> str:
    slugged_path_components = list()

    for component in path_components:
        slugged_path_components.append(slugify(component))

    return os.path.sep.join(slugged_path_components)


def join_web_path(path_components: list[str], use_slug: bool = False) -> str:
    if use_slug:
        slugged = []
        for component in path_components:
            slugged.append(slugify(component))

        path_components = slugged

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

    if metadata["cover"] is not None:
        cover_image_path = join_path(cover_path, get_cover_image(path_components, tmp_folder_covers, metadata["cover"]))
        cover_image_path = cover_image_path.replace("\\", "\\\\")
        f.write('cover = "' + cover_image_path + '"\n')

    f.write("+++\n")
    f.close()


def generate_image_filename(path_components: list[str], lang: str, index: int) -> str:
    filename = f"img{index:03d}" + lang + ".md"
    path = join_path(join_folder_path(path_components), filename)

    return path


def create_image_md(path_components: list[str], tmp_folder_albums: str, metadata: dict, created_at: datetime,
                    lang: str, index: int, image_count: int) -> None:
    if lang != "":
        lang = "." + lang

    base_uri = join_web_path(path_components)

    filename = generate_image_filename(path_components, lang, index)
    image_file_path = join_path(tmp_folder_albums, filename)

    if os.path.exists(image_file_path):
        raise FileExistsError(image_file_path)

    image_file = open(image_file_path, "w")

    image_file.write("+++\n")
    image_file.write('title = "' + metadata["filename"] + '"\n')
    image_file.write('template = "album/album-single.html"\n')
    image_file.write('date = "' + created_at.strftime("%Y-%m-%dT%H:%M:%S") + '"\n')

    # add old path as alias
    alias = "/".join([albums_web_path, join_web_path(path_components, True), slugify(metadata["filename"])])
    image_file.write('aliases = ["/' + alias + '"]\n')

    image_file.write('[extra]\n')
    image_file.write('filename = "' + metadata["filename"] + '"\n')
    image_file.write('height = ' + str(metadata["height"]) + "\n")
    image_file.write('width = ' + str(metadata["width"]) + "\n")
    image_file.write('file_uri = "' + albums_url + "/" + base_uri + "/" + metadata["filename"] + '"\n')

    # Albums do not have 750 pixel thumbnail, use 1200 instead
    thumbs_base = albums_url + "/" + base_uri + "/.thumbs/"
    image_file.write('file_uri_300 = "' + thumbs_base + "300-" + metadata["filename"] + '"\n')
    image_file.write('file_uri_750 = "' + thumbs_base + "1200-" + metadata["filename"] + '"\n')
    image_file.write('file_uri_1200 = "' + thumbs_base + "1200-" + metadata["filename"] + '"\n')

    if index > 0:
        prev_filename_web = generate_image_filename(path_components, lang, index - 1).replace(os.path.sep, "/")
        image_file.write(
            'previous = "/' + albums_web_path + "/" + prev_filename_web + '"\n')

    if (index + 1) < image_count:
        next_filename_web = generate_image_filename(path_components, lang, index + 1).replace(os.path.sep, "/")
        image_file.write(
            'next = "/' + albums_web_path + "/" + next_filename_web + '"\n')

    image_file.write("+++\n")
    image_file.close()


def normalize_images(image_metadata: list[dict]) -> list[tuple[dict, datetime]]:
    images = []
    current_date = None

    for image_metadata in image_metadata:
        if image_metadata["exif"]["time"] is not None:
            new_date = datetime.fromtimestamp(int(image_metadata["exif"]["time"]) / 1000)

            if current_date is None or new_date > current_date:
                current_date = new_date

        if current_date is None:
            image_created_at = datetime.fromtimestamp(0)
        else:
            image_created_at = current_date

        images.append((image_metadata, image_created_at))

    images.sort(key=lambda x: (x[1], x[0]["filename"]))

    return images


def normalize_folders(folder_metadata: list[dict]) -> list[tuple[dict, datetime]]:
    folders = []
    current_date = None

    for folder in folder_metadata:
        # Use folder["time"], fallback to 0 if missing
        folder_time = folder["time"]
        if folder_time is not None:
            new_date = datetime.fromtimestamp(int(folder_time) / 1000)
            if current_date is None or new_date > current_date:
                current_date = new_date
        if current_date is None:
            folder_created_at = datetime.fromtimestamp(0)
        else:
            folder_created_at = current_date

        folders.append((folder, folder_created_at))

    folders.sort(key=lambda x: (x[1], x[0]["foldername"]))

    # Ensure that each album has its own unique timestamp associated with it to allow unique stubs and
    # deterministic list outputs in zola as it does not support sorting by more than one property
    unique_folders = []
    last_timestamp = None
    for folder, ts in folders:
        if last_timestamp is not None and ts <= last_timestamp:
            new_ts = last_timestamp + timedelta(seconds=1)
            print("Adjusting '" + folder["foldername"] + "' from '" + str(ts) + "' to '" + str(new_ts) + "'")
            ts = new_ts
        unique_folders.append((folder, ts))
        last_timestamp = ts

    return unique_folders


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

    current_metadata = get_url_metadata(path_components)

    images = normalize_images(current_metadata["images"])

    for i, (image_metadata, image_created_at) in enumerate(images):
        create_image_md(path_components, tmp_folder_albums, image_metadata, image_created_at, "", i, len(images))

    sub_threads = []

    sub_folders = normalize_folders(current_metadata["subDirs"])

    for (sub_folder, timestamp) in sub_folders:
        sub_thread = Thread(target=create_album_folder,
                            args=(path_components, tmp_folder_albums, tmp_folder_covers, sub_folder))
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
index_file.write(
    "description = 'Hier findest du nach Themen sortierte Fotoalben, zum Beispiel zu bestimmten Events oder Dingen im Space.'\n")
index_file.write("template = 'album/album-list.html'\n")
index_file.write("weight = 30\n")
index_file.write('sort_by = "date"\n')
index_file.write("+++\n")
index_file.close()

shutil.copytree(tmp_ktt_ol_albums, albums_path)
shutil.copytree(tmp_ktt_ol_cover, cover_path)
