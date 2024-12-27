from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class JrdLink(BaseModel):
    """
    See [RFC 7033](https://www.rfc-editor.org/rfc/rfc7033.html).

    ``pycon
    >>> JrdLink(rel="self", href="http://test.example/actor").model_dump(exclude_none=True)
    {'rel': 'self', 'href': 'http://test.example/actor'}

    ```
    """

    model_config = ConfigDict(
        extra="allow",
    )
    rel: str | None = Field(None, examples=["self"])
    """
    rel
    """
    type: str | None = Field(None, examples=["application/activity+json"])
    """
    type
    """
    href: str | None = Field(None, examples=["http://test.example/actor"])
    """
    when used with the 'href' attribute, conveys a link relation between the host described by the document and a common target URI
    """
    titles: Optional[Dict[str, Any]] = None
    """
    titles
    """
    properties: Optional[Dict[str, Any]] = None
    """
    properties
    """
    template: Optional[str] = None
    """
    template attribute conveys a relation whose context is an individual resource within the host-meta document scope,
    """


class JrdData(BaseModel):
    """
    See [RFC 6415](https://www.packetizer.com/rfc/rfc6415/)

    ```pycon
    >>> JrdData(subject="acct:actor@test.example").model_dump(exclude_none=True)
    {'subject': 'acct:actor@test.example'}

    ```
    """

    model_config = ConfigDict(
        extra="allow",
    )
    subject: str | None = Field(None, examples=["acct:actor@test.example"])
    """
    The subject
    """
    expires: Optional[datetime] = None
    """
    expiration date time
    """
    aliases: List[str] | None = None
    """
    value a string array containing the values of each element in order
    """
    properties: Optional[Dict[str, Any]] = None
    """
    value an object with each element included as a name/value pair with the value of the type attribute as name, and element value included as a string value.
    """
    links: Optional[List[JrdLink]] = None
    """
     a single name/value pair with the name 'links', and value an array with each element included as an object
    """
