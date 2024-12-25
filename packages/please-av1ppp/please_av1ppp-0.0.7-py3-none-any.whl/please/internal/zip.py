import os
from pathlib import Path
from tarfile import open as open_tarfile
from zipfile import ZipFile
from typing import Union
from shutil import make_archive

StrOrPath = Union[str, Path]


def zip_dir(in_dir: StrOrPath, out_path: StrOrPath):
    make_archive(str(out_path), "zip", in_dir)
    #
    # with ZipFile(out_path, "w", ZIP_DEFLATED) as zipf:
    #     for root, dirs, files in os.walk(in_dir):
    #         root_path = Path(root)

    #         for dir in dirs:
    #             zipf.mkdir(dir, dir_mode)

    #     for root, dirs, files in os.walk(in_dir):
    #         root_path = Path(root)

    #         for file in files:
    #             file_path = root_path.joinpath(file)
    #             zipf.write(file_path, file_path.relative_to(in_dir))


def unzip(in_path: StrOrPath, out_path: StrOrPath):
    with ZipFile(in_path, "r") as zipf:
        zipf.extractall(out_path)


def targz_dir(in_dir: StrOrPath, out_path: StrOrPath):
    make_archive(str(out_path), "zip", in_dir)
    entries = os.listdir(in_dir)

    with open_tarfile(out_path, "w:gz") as tar:
        for entry in entries:
            tar.add(os.path.join(in_dir, entry), arcname=entry)
