"""Template and Variable type definitions."""

from typing import Any, List, Literal, Union

from typing_extensions import NotRequired, TypedDict


class Variable(TypedDict):
    """Template variable type.

    Attributes:
        key (str): The key of the variable. We recommend capitalizing the key (e.g. FIRST_NAME).
        type (Literal["string", "number", "boolean", "object", "list"]): The type of the variable.
        fallback_value (Any): The fallback value of the variable. Must match the type of the variable.
            If no fallback value is provided, you must provide a value for the variable when sending
            an email using the template. If object type is provided, you must include a fallback.
    """

    key: str
    """The key of the variable. We recommend capitalizing the key (e.g. FIRST_NAME)."""

    type: Literal["string", "number", "boolean", "object", "list"]
    """The type of the variable."""

    fallback_value: NotRequired[Any]
    """The fallback value of the variable. Must match the type of the variable."""


# Use functional TypedDict syntax to support reserved keyword "from"
_FromParam = TypedDict(
    "_FromParam",
    {
        "from": NotRequired[str],
    },
)


class Template(_FromParam):
    """Template type that wraps the template object.

    Attributes:
        id (str): The Template ID.
        object (str): The object type (always "template").
        name (str): The name of the template.
        alias (str): The alias of the template.
        status (str): The status of the template ("draft" or "published").
        from (str): Sender email address.
        subject (str): Email subject.
        reply_to (Union[List[str], str]): Reply-to email address(es).
        html (str): The HTML version of the template.
        text (str): The plain text version of the template.
        variables (List[Variable]): The array of variables used in the template.
        created_at (str): The timestamp when the template was created.
        updated_at (str): The timestamp when the template was last updated.
        published_at (str): The timestamp when the template was published.
    """

    id: str
    """The Template ID."""

    object: str
    """The object type (always "template")."""

    name: str
    """The name of the template."""

    alias: NotRequired[str]
    """The alias of the template."""

    status: NotRequired[Literal["draft", "published"]]
    """The status of the template."""

    subject: NotRequired[str]
    """Email subject."""

    reply_to: NotRequired[Union[List[str], str]]
    """Reply-to email address(es)."""

    html: str
    """The HTML version of the template."""

    text: NotRequired[str]
    """The plain text version of the template."""

    variables: NotRequired[List[Variable]]
    """The array of variables used in the template."""

    created_at: NotRequired[str]
    """The timestamp when the template was created."""

    updated_at: NotRequired[str]
    """The timestamp when the template was last updated."""

    published_at: NotRequired[str]
    """The timestamp when the template was published."""
