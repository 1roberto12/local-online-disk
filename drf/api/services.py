import hashlib, os, shutil, base64
from io import BytesIO
from typing import List, Union, Tuple
from pathlib import Path, PurePosixPath
from datetime import datetime
from cryptography.fernet import Fernet

from rest_framework.exceptions import NotFound, ValidationError
# import rest_framework.exceptions as ex

from .serializers import FileInfoSerializer
from .models import FileInfo


class Storage:
    def __init__(self, path: str, full_disk_encryption: bool = False):
        # print('Created!')
        self.__root_path = Path(path)
        self.__full_encryption = full_disk_encryption
        self.__cwd = Path(path)
        self.__content = set(self.__cwd.iterdir())

    @property
    def root(self):
        return self.__root_path

    def chroot(self, path: Union[Path, str]) -> None:
        """change root directory"""
        path = Path(path)
        if not path.is_absolute():
            path = self.root / path
        if path.exists() and path.is_dir():
            self.__root_path = path.resolve()
            self.__cwd = path.resolve()
            self.__content = set(self.__cwd.iterdir())

    @property
    def cur_dir(self):
        return self.__cwd

    @property
    def pwd(self) -> str:
        """get working directory"""
        path = PurePosixPath(self.__cwd.relative_to(self.__root_path))
        return str("/" / path)

    def cd(self, path: Union[PurePosixPath, str] = '/') -> str:
        """change directory"""
        path = PurePosixPath(path or '')
        # if path is None:
        #     new_wd = self.root
        if path.root == '/':
            new_wd = self.root.joinpath(*path.parts[1:])
        elif path.is_absolute():
            return "Absolute paths not allowed"
        elif path == PurePosixPath(''):
            return self.pwd
        else:
            new_wd = self.cur_dir / path

        if new_wd.resolve() == self.cur_dir:
            return self.pwd
        if new_wd.exists() and new_wd.is_dir():
            self.__cwd = new_wd.resolve()
        else:
            return "Directory does not exist"

        self.__content = set(self.__cwd.iterdir())
        return self.pwd

    def mkdir(self, dirname: Union[PurePosixPath, str]) -> None:
        """create new directory"""
        new_dir = self.cur_dir / dirname
        if not new_dir.exists():
            new_dir.mkdir(parents=True)

    def ls(self) -> List[str]:
        """get current directory contents"""
        return [entry.name for entry in self.__content]

    def get_file_size(self, filename) -> int:
        """get the size of a file"""
        file = self.__cwd / filename
        if file.exists():
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
        file = self.cur_dir / (filename or '')
        if file.exists():
            stat = file.stat()
            return (datetime.fromtimestamp(stat.st_ctime),
                    datetime.fromtimestamp(stat.st_atime),
                    datetime.fromtimestamp(stat.st_mtime))
        timestamp = 0
        for timestamp in range(0, 10000000, 86400):
            try:
                datetime.fromtimestamp(timestamp)
            except:
                pass
            else:
                break
        return (datetime.fromtimestamp(timestamp),
                datetime.fromtimestamp(timestamp),
                datetime.fromtimestamp(timestamp))

    def is_dir(self, filename: str) -> bool:
        file = self.__cwd / filename
        if file.exists():
            return file.is_dir()
        return False

    def rm(self, path: Union[PurePosixPath, str]):
        """delete file or directory from disk"""
        path = self.cur_dir / (path or '')
        if path.exists():
            if path.is_file():
                os.remove(path)
            elif path.is_dir():
                shutil.rmtree(path)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
storage = Storage(BASE_DIR)
storage.mkdir('Storage')
storage.chroot('Storage')


class FileStorageService:

    @staticmethod
    def get_dir_entry(path: Union[Path, str] = '', user: str = '') -> FileInfo:
        userpath = PurePosixPath('/', user or '')
        path = PurePosixPath(path or '')
        storage.cd(userpath)
        if path == PurePosixPath('/'):
            path = PurePosixPath('')
        elif str(path).startswith('//'):
            path = PurePosixPath(*path.parts[1:])
        elif path.root == '/':
            path = PurePosixPath(*path.parts[1:])
        entry = storage.cur_dir / path
        if not entry.exists():
            raise ValidationError('File or directory does not exist')
        serializer = FileInfoSerializer(data={
            'name': entry.name,
            'path': str(path),
            'is_dir': storage.is_dir(str(path)),
            'size': storage.get_file_size(path),
            'owner': user or 'unknown',
            'creation_date': storage.get_dates(str(path))[0]
        })
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def get_files(path: Union[Path, str] = '', user: str = '') -> List[FileInfo]:
        # path = path or ''
        userpath = PurePosixPath('/', user or '')
        path = PurePosixPath(path or '')
        storage.cd(userpath)
        if path == PurePosixPath('/'):
            path = PurePosixPath('')
        elif str(path).startswith('//'):
            path = PurePosixPath(*path.parts[1:])
        elif path.root == '/':
            path = PurePosixPath(*path.parts[1:])
        directory = storage.cur_dir / path
        if not directory.exists():
            raise NotFound('Directory does not exist!')
        elif not directory.is_dir():
            raise ValidationError('Path is not a directory!')
        else:
            paths = []
            storage.cd(path)
            filepath = PurePosixPath(storage.pwd)
            filepath = PurePosixPath(filepath.parts[0], *filepath.parts[2:])
            for p in storage.ls():
                serializer = FileInfoSerializer(data={
                    'name': p,
                    'path': str(filepath / p),
                    'is_dir': storage.is_dir(p),
                    'size': storage.get_file_size(p),
                    'owner': user or 'unknown',
                    'creation_date': storage.get_dates(p)[0]
                })
                serializer.is_valid(raise_exception=True)
                paths.append(serializer.save())
            return paths

    @staticmethod
    def get_filestream(path: Union[Path, str] = '', user: str = ''):
        # path = path or ''
        userpath = PurePosixPath('/', user or '')
        path = PurePosixPath(path or '')
        if str(path).startswith('//'):
            path = PurePosixPath(*path.parts[1:])
        elif path.root == '/':
            path = PurePosixPath(*path.parts[1:])
        storage.cd(userpath)
        file = storage.cur_dir / path
        if not file.exists():
            raise NotFound('File does not exist!')
        elif file.is_dir():
            raise ValidationError('Path is not a file!')
        else:
            return file.open('rb')

    @staticmethod
    def get_filename(path: Union[Path, str] = '', user: str = '') -> str:
        # path = path or ''
        userpath = PurePosixPath('/', user or '')
        path = PurePosixPath(path or '')
        storage.cd(userpath)
        file = storage.cur_dir / path
        if not file.exists():
            raise NotFound('File does not exist!')
        elif file.is_dir():
            raise ValidationError('Path is not a file!')
        else:
            return file.name

    @staticmethod
    def save_file(path: Union[Path, str], name: str, data: BytesIO, user: str = '') -> None:
        # path = path or ''
        userpath = PurePosixPath('/', user or '')
        path = PurePosixPath(path or '')
        if path.root == '/':
            path = PurePosixPath(*path.parts[1:])
        storage.cd(userpath)
        dest = storage.cur_dir / path
        file = dest / name
        if not dest.exists():
            raise NotFound('Path does not exist!')
        elif not dest.is_dir():
            raise ValidationError('Path is not a directory!')
        elif file.exists():
            raise ValidationError('File already exists!')
        try:
            file.write_bytes(data.read(-1))
        except:
            raise ValidationError('File could not be uploaded')

    @staticmethod
    def create_directory(path: Union[Path, str] = '', user: str = '') -> None:
        # path = path or ''
        userpath = PurePosixPath('/', user or '')
        path = PurePosixPath(path or '')
        if path.root == '/':
            path = PurePosixPath(*path.parts[1:])
        storage.cd(userpath)
        directory = storage.cur_dir / path
        if directory.exists():
            raise ValidationError('Directory already exists')
        storage.mkdir(path)

    @staticmethod
    def remove(path: Union[Path, str] = '', user: str = '') -> None:
        userpath = PurePosixPath('/', user or '')
        path = PurePosixPath(path or '')
        if path.root == '/':
            path = PurePosixPath(*path.parts[1:])
        storage.cd(userpath)
        file = storage.cur_dir / path
        if not file.exists():
            raise NotFound('File or directory does not exist!')
        else:
            storage.rm(path)

    @staticmethod
    def encrypt(file: FileInfo, password: str) -> None:
        hasher = hashlib.sha256()
        hasher.update(bytes(password, 'utf-8'))
        key = hasher.digest()
        crypter = Fernet(base64.b64encode(key))
        storage.cd()
        storage.cd(file.owner)
        full_path = storage.cur_dir / file.path
        with open(full_path, 'rb') as plain:
            encrypted = crypter.encrypt(plain.read())
        with open(str(full_path) + '~encrypted', 'wb') as new_encrypted:
            new_encrypted.write(encrypted)
        storage.rm(file.path)

    @staticmethod
    def decrypt(file: FileInfo, password: str) -> None:
        hasher = hashlib.sha256()
        hasher.update(bytes(password, 'utf-8'))
        key = hasher.digest()
        crypter = Fernet(base64.b64encode(key))
        storage.cd()
        storage.cd(file.owner)
        full_path = storage.cur_dir / file.path
        with open(full_path, 'rb') as encrypted:
            plain = crypter.decrypt(encrypted.read())
        name = str(full_path)[:-len('~encrypted')]
        with open(name, 'wb') as new_plain:
            new_plain.write(plain)
        storage.rm(file.path)
