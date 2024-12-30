import typing as tp
import io
from dataclasses import dataclass
from fastapi import File, UploadFile


@dataclass
class Files:
    _file: tp.Optional[tp.Union[io.IOBase, UploadFile]] = None
    file_name: str = ""

    @property
    def filename(self) -> tp.Union[str, None]:
        return self._file.filename

    @filename.setter
    def filename(cls, filename: str):
        cls.file_name = filename
        return cls

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file: UploadFile):
        self._file = file.file

    @classmethod
    def set_file(cls, file: any):
        cls._file = io.BytesIO(file)
        return cls

    @classmethod
    async def to_BytesIO_format(cls):
        if cls._file:
            await cls._file.seek(0)  # Reset the file pointer
            return cls._file
        raise ValueError("File content is not set")

