from typing import List, Union, Tuple
from pathlib import Path, PurePosixPath
from datetime import datetime

from rest_framework.exceptions import NotFound, ValidationError
import rest_framework.exceptions as ex

from .serializers import FileInfoSerializer
from .models import FileInfo


class Storage:
    def __init__(self, path: str, full_disk_encryption: bool = False):
        print('Created!')
        self.__root_path = Path(path)
        self.__full_encryption = full_disk_encryption
        self.__cwd = Path(path)
        self.__content = set(self.__cwd.iterdir())

    @property
    def root(self):
        return self.__root_path

    def pwd(self) -> str:
        """get working directory"""
        path = PurePosixPath(self.__cwd.relative_to(self.__root_path))
        return str("/" / path)

    def cd(self, path: str) -> str:
        """change directory"""
        path = PurePosixPath(path)
        full_path = self.__root_path / path
        if full_path.resolve() == self.__cwd:
            return self.pwd()

        if path.is_absolute():
            new_wd = self.__root_path.joinpath(*path.parts[1:])
        else:
            new_wd = self.__cwd / path

        if new_wd.exists() and new_wd.is_dir():
            self.__cwd = new_wd.resolve()
        else:
            return "Directory does not exist"

        self.__content = set(self.__cwd.iterdir())
        return self.pwd()

    def ls(self) -> List[str]:
        """get current directory contents"""
        return [entry.name for entry in self.__content]

    def get_file_size(self, filename) -> int:
        """get the size of a file"""
        file = self.__cwd / filename
        if file in self.__content:
            stat = file.stat()
            return stat.st_size

    def get_owner(self, filename: str) -> str:
        file = self.__cwd / filename
        if file in self.__content:
            try:
                return file.owner()
            except:
                return 'unknown'

    def get_dates(self, filename: str) -> Tuple[datetime, datetime, datetime]:
        file = self.__cwd / filename
        if file in self.__content:
            stat = file.stat()
            return (datetime.fromtimestamp(stat.st_ctime),
                    datetime.fromtimestamp(stat.st_atime),
                    datetime.fromtimestamp(stat.st_mtime))

    def is_dir(self, filename: str) -> bool:
        file = self.__cwd / filename
        if file in self.__content:
            return file.is_dir()
        return False


storage = Storage(R"D:\Robert\Downloads\Studia\TAI")


def get_files(path: Union[Path, str]) -> List[FileInfo]:
    directory = storage.root / path
    if not directory.exists():
        raise NotFound('Directory does not exist!')
    elif not directory.is_dir():
        raise ValidationError('Path is not a directory!')
    else:
        paths = []
        storage.cd(path)
        for p in storage.ls():
            serializer = FileInfoSerializer(data={
                'name': p,
                'path': storage.pwd() + p,
                'is_dir': storage.is_dir(p),
                'size': storage.get_file_size(p),
                'owner': storage.get_owner(p),
                'creation_date': storage.get_dates(p)[0]
            })
            serializer.is_valid(raise_exception=True)
            paths.append(serializer.save())
        return paths
