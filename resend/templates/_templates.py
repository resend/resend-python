"""Templates API operations."""

from typing import Any, Dict, List, Optional, Union, cast

from typing_extensions import NotRequired, TypedDict

from resend import request
from resend._base_response import BaseResponse
from resend.pagination_helper import PaginationHelper

from ._template import Template, TemplateListItem, Variable

# Use functional TypedDict syntax to support reserved keyword "from"
_CreateParamsFrom = TypedDict(
    "_CreateParamsFrom",
    {
        "from": NotRequired[str],
    },
)


class Templates:
    """Templates API resource.

    The Templates API allows you to create, manage, and publish email templates
    with optional variables.
    """

    class CreateParams(_CreateParamsFrom):
        """Parameters for creating a template.

        Attributes:
            name (str): The name of the template (required).
            alias (str): The alias of the template.
            from (str): Sender email address. To include a friendly name, use the format
                "Your Name <sender@domain.com>". If provided, this value can be overridden
                when sending an email using the template.
            subject (str): Email subject. If provided, this value can be overridden when
                sending an email using the template.
            reply_to (Union[List[str], str]): Reply-to email address(es). For multiple
                addresses, send as an array of strings. If provided, this value can be
                overridden when sending an email using the template.
            html (str): The HTML version of the template (required).
            text (str): The plain text version of the message. If not provided, the HTML
                will be used to generate a plain text version. You can opt out of this
                behavior by setting value to an empty string.
            variables (List[Variable]): The array of variables used in the template.
                Each template may contain up to 20 variables.
        """

        name: str
        """The name of the template."""

        html: str
        """The HTML version of the template."""

        alias: NotRequired[str]
        """The alias of the template."""

        subject: NotRequired[str]
        """Email subject."""

        reply_to: NotRequired[Union[List[str], str]]
        """Reply-to email address(es)."""

        text: NotRequired[str]
        """The plain text version of the message."""

        variables: NotRequired[List[Variable]]
        """The array of variables used in the template."""

    class CreateResponse(BaseResponse):
        """Response from creating a template.

        Attributes:
            id (str): The Template ID.
            object (str): The object type (always "template").
        """

        id: str
        """The Template ID."""

        object: str
        """The object type (always "template")."""

    class UpdateParams(_CreateParamsFrom):
        """Parameters for updating a template.

        Attributes:
            id (str): The Template ID (required).
            name (str): The name of the template.
            alias (str): The alias of the template.
            from (str): Sender email address.
            subject (str): Email subject.
            reply_to (Union[List[str], str]): Reply-to email address(es).
            html (str): The HTML version of the template.
            text (str): The plain text version of the message.
            variables (List[Variable]): The array of variables used in the template.
        """

        id: str
        """The Template ID."""

        name: NotRequired[str]
        """The name of the template."""

        alias: NotRequired[str]
        """The alias of the template."""

        subject: NotRequired[str]
        """Email subject."""

        reply_to: NotRequired[Union[List[str], str]]
        """Reply-to email address(es)."""

        html: NotRequired[str]
        """The HTML version of the template."""

        text: NotRequired[str]
        """The plain text version of the message."""

        variables: NotRequired[List[Variable]]
        """The array of variables used in the template."""

    class UpdateResponse(BaseResponse):
        """Response from updating a template.

        Attributes:
            id (str): The Template ID.
            object (str): The object type (always "template").
        """

        id: str
        """The Template ID."""

        object: str
        """The object type (always "template")."""

    class ListParams(TypedDict):
        """Parameters for listing templates.

        Attributes:
            limit (int): The number of templates to return (max 100).
            after (str): Return templates after this cursor.
            before (str): Return templates before this cursor.
        """

        limit: NotRequired[int]
        """The number of templates to return (max 100)."""

        after: NotRequired[str]
        """Return templates after this cursor."""

        before: NotRequired[str]
        """Return templates before this cursor."""

    class ListResponse(BaseResponse):
        """Response from listing templates.

        Attributes:
            object (str): The object type (always "list").
            data (List[TemplateListItem]): Array of template list items with a subset of template properties.
            has_more (bool): Whether there are more results available.
        """

        object: str
        """The object type (always "list")."""

        data: List[TemplateListItem]
        """Array of template list items with a subset of template properties."""

        has_more: bool
        """Whether there are more results available."""

    class PublishResponse(BaseResponse):
        """Response from publishing a template.

        Attributes:
            id (str): The Template ID.
            object (str): The object type (always "template").
        """

        id: str
        """The Template ID."""

        object: str
        """The object type (always "template")."""

    class DuplicateResponse(BaseResponse):
        """Response from duplicating a template.

        Attributes:
            id (str): The Template ID of the duplicated template.
            object (str): The object type (always "template").
        """

        id: str
        """The Template ID of the duplicated template."""

        object: str
        """The object type (always "template")."""

    class RemoveResponse(BaseResponse):
        """Response from removing a template.

        Attributes:
            id (str): The Template ID.
            object (str): The object type (always "template").
            deleted (bool): Whether the template was deleted.
        """

        id: str
        """The Template ID."""

        object: str
        """The object type (always "template")."""

        deleted: bool
        """Whether the template was deleted."""

    @classmethod
    def create(cls, params: CreateParams) -> CreateResponse:
        """Create a new template.

        Before you can use a template, you must publish it first. To publish a template,
        use the Templates dashboard or publish() method.

        Args:
            params: The template creation parameters.

        Returns:
            CreateResponse: The created template response with ID and object type.
        """
        path = "/templates"
        resp = request.Request[Templates.CreateResponse](
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def get(cls, template_id: str) -> Template:
        """Retrieve a template by ID.

        Args:
            template_id: The Template ID.

        Returns:
            Template: The template object.
        """
        path = f"/templates/{template_id}"
        resp = request.Request[Template](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def list(cls, params: Optional[ListParams] = None) -> ListResponse:
        """List all templates with pagination support.

        Args:
            params: Optional pagination parameters (limit, after, before).

        Returns:
            ListResponse: The paginated list of templates.
        """
        base_path = "/templates"
        query_params = cast(Dict[Any, Any], params) if params else None
        path = PaginationHelper.build_paginated_path(base_path, query_params)
        resp = request.Request[Templates.ListResponse](
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    @classmethod
    def update(cls, params: UpdateParams) -> UpdateResponse:
        """Update an existing template.

        Args:
            params: The template update parameters (must include id).

        Returns:
            UpdateResponse: The updated template response with ID and object type.
        """
        template_id = params["id"]
        path = f"/templates/{template_id}"
        # Remove 'id' from params before sending
        update_params = {k: v for k, v in params.items() if k != "id"}
        resp = request.Request[Templates.UpdateResponse](
            path=path, params=cast(Dict[Any, Any], update_params), verb="patch"
        ).perform_with_content()
        return resp

    @classmethod
    def publish(cls, template_id: str) -> PublishResponse:
        """Publish a template to make it available for use.

        Before you can use a template to send emails, you must publish it first.

        Args:
            template_id: The Template ID.

        Returns:
            PublishResponse: The published template response with ID and object type.
        """
        path = f"/templates/{template_id}/publish"
        resp = request.Request[Templates.PublishResponse](
            path=path, params={}, verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def duplicate(cls, template_id: str) -> DuplicateResponse:
        """Duplicate a template.

        Creates a copy of the specified template with all its properties and variables.

        Args:
            template_id: The Template ID to duplicate.

        Returns:
            DuplicateResponse: The duplicated template response with new ID and object type.
        """
        path = f"/templates/{template_id}/duplicate"
        resp = request.Request[Templates.DuplicateResponse](
            path=path, params={}, verb="post"
        ).perform_with_content()
        return resp

    @classmethod
    def remove(cls, template_id: str) -> RemoveResponse:
        """Delete a template.

        Args:
            template_id: The Template ID.

        Returns:
            RemoveResponse: The deletion response with ID, object type, and deleted status.
        """
        path = f"/templates/{template_id}"
        resp = request.Request[Templates.RemoveResponse](
            path=path, params={}, verb="delete"
        ).perform_with_content()
        return resp
