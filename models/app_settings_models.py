from pydantic import BaseModel


class Setting(BaseModel):
    key: str
    value: int | str | bool


class AppSettingsBase(BaseModel):
    theme_mode: str
    theme_color: str


class AppSettingsCreate(AppSettingsBase):
    pass


class AppSettings(AppSettingsBase):
    id: int

    class Config:
        from_attributes = True
