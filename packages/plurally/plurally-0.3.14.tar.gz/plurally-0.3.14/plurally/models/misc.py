import itertools
from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field, field_validator


class File(BaseModel): ...


def get_file_base_kls(name):

    ACCEPT = {
        "audio": "audio/*",
        "video": "video/*",
        "image": "image/*",
        "pdf": "application/pdf",
        "text": "text/*",
    }

    class FileKls(File):
        model_config = ConfigDict(
            json_schema_extra={
                "type-friendly": name.title(),
                "uiSchema": {"ui:options": {"label": False}},
            }
        )
        file: str = Field(
            title=f"Upload {name} file",
            description=f"Please select an {name} file to upload",
            json_schema_extra={
                "is-file": True,
                "uiSchema": {"ui:widget": "file"},
                "accept": ACCEPT.get(name, "*/*"),
            },
        )
        # will be filled later - not part of schema
        filename: str | None = Field(
            None,
            title="Filename",
            description=f"The name of the {name} file",
            json_schema_extra={
                "uiSchema": {"ui:widget": "hidden"},
            },
        )

        # will be filled later - not part of schema
        content: bytes | None = Field(
            None,
            title="Content",
            description=f"The content of the {name} file",
            json_schema_extra={
                "uiSchema": {"ui:widget": "hidden"},
            },
        )

    return FileKls


class AudioFile(get_file_base_kls("audio")): ...


class MicAudioFile(AudioFile):

    file: str = Field(
        min_length=1,
        title=AudioFile.model_fields["file"].title,
        description=AudioFile.model_fields["file"].description,
        json_schema_extra={
            **AudioFile.model_fields["file"].json_schema_extra,
            "uiSchema": {
                "ui:widget": "AudioRecorderWidget",
                "errorMessages": {
                    "minLength": "Please finish recording some audio first",
                },
            },
            "uiExampleSchema": AudioFile.model_fields["file"].json_schema_extra[
                "uiSchema"
            ],
        },
    )


class PdfFile(get_file_base_kls("pdf")): ...


class Table(BaseModel):
    data: List[Dict[str, str]]

    @field_validator("data", mode="before")
    def check_data(cls, value):
        # make sure everything is a string
        columns = set()
        value, other = itertools.tee(value)
        for row in value:
            for key, val in row.items():
                if not isinstance(val, str):
                    row[key] = str(val)
            columns.add(tuple(row))

        if len(columns) > 1:
            raise ValueError(f"All rows must have the same columns, got {columns}")

        return other

    def columns(self):
        return list(self.data[0]) if self.data else []

    def is_empty(self):
        return not bool(self.data)

    class Config:
        json_schema_extra = {
            "type-friendly": "Table",
        }
