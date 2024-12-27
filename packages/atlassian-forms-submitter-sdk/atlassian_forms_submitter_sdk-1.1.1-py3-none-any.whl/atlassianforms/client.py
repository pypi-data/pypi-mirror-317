from typing import Any, Dict

from atlassianforms.form.manager import ServiceDeskFormManager
from atlassianforms.form.parser import ServiceDeskFormParser
from atlassianforms.manager import ServiceDeskManager
from atlassianforms.models.response import CreateRequestResponseParser

FORM_DIDNT_FETCH_ERROR = (
    "Form has not been fetched and parsed. Please run `fetch_and_parse_form` first."
)


class ServiceDeskFormClient:
    """
    A client class for interacting with Atlassian Service Desk forms.

    This class provides utilities to fetch forms, parse them, manage form fields, and create service desk requests.

    Attributes
    ----------
    base_url : str
        The base URL of the Atlassian Service Desk.
    username : str
        The username used for authentication.
    auth_token : str
        The authentication token.
    service_desk_manager : ServiceDeskManager
        An instance of ServiceDeskManager for managing service desk requests.
    form_manager : ServiceDeskFormManager
        An instance of ServiceDeskFormManager for managing form fields and values.

    Methods
    -------
    fetch_and_parse_form(portal_id: int, request_type_id: int) -> None
        Fetches and parses the form for the given portal and request type ID.
    list_fields() -> None
        Lists all fields in the form.
    list_field_values(field_name: str) -> None
        Lists possible values for a specific field in the form.
    set_form_values(values: Dict[str, Any]) -> Dict[str, Any]
        Sets the values for the form fields.
    create_request(filled_values: Dict[str, Any]) -> CreateRequestResponseParser
        Creates a service desk request with the filled form values.
    """

    def __init__(self, base_url: str, username: str, auth_token: str) -> None:
        """
        Initializes the ServiceDeskFormClient with the provided credentials.

        Parameters
        ----------
        base_url : str
            The base URL of the Atlassian Service Desk.
        username : str
            The username used for authentication.
        auth_token : str
            The authentication token.
        """
        self.base_url = base_url
        self.username = username
        self.auth_token = auth_token
        self.service_desk_manager = ServiceDeskManager(
            base_url=self.base_url, username=self.username, auth_token=self.auth_token
        )

    def fetch_and_parse_form(
        self, portal_id: int, request_type_id: int
    ) -> ServiceDeskFormManager:
        """
        Fetches and parses the form for the given portal and request type ID.

        Parameters
        ----------
        portal_id : int
            The ID of the service desk portal.
        request_type_id : int
            The ID of the request type.
        """
        form = self.service_desk_manager.fetch_form(
            portal_id=portal_id, request_type_id=request_type_id
        )
        form_obj = ServiceDeskFormParser.parse(form)
        return ServiceDeskFormManager(form_obj)

    def create_request(
        self, filled_values: Dict[str, Any]
    ) -> CreateRequestResponseParser:
        """
        Creates a service desk request with the filled form values.

        Parameters
        ----------
        filled_values : Dict[str, Any]
            The filled form values.

        Returns
        -------
        CreateRequestResponseParser
            The response of the create request parsed into a CreateRequestResponseParser object.
        """
        response_dict = self.service_desk_manager.create_request(filled_values)
        return CreateRequestResponseParser.parse(response_dict)
