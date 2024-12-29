from pydantic import BaseModel, ConfigDict

from gwproto.utils import snake_to_camel

DEFAULT_WEB_SERVER_NAME = "default"


class WebServerGt(BaseModel):
    Name: str = DEFAULT_WEB_SERVER_NAME
    Host: str = "localhost"
    Port: int = 8080
    Enabled: bool = True
    Kwargs: dict = {}
    model_config = ConfigDict(
        extra="allow", alias_generator=snake_to_camel, populate_by_name=True
    )
