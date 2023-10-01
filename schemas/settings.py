from pydantic import BaseModel


fake_settings_db = {"rick": {"username": "rick", "theme_mode": "dark"}}


class Setting(BaseModel):
    key: str
    value: int | str | bool


class SettingsBase(BaseModel):
    user_id: int
    theme_mode: str


class Settings(SettingsBase):
    class Config:
        from_attributes = True
