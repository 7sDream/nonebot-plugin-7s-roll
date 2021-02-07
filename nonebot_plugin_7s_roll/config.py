from pydantic import BaseSettings


class Config(BaseSettings):
    i7s_roll_command: str = "roll"
    i7s_roll_trigger: str = "roll"

    class Config:
        extra = "ignore"
