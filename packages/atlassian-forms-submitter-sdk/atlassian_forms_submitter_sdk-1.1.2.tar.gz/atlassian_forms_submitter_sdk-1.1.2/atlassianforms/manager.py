import base64
from typing import Any, Dict, List, Optional, Union

import requests
from atlassian import Jira, ServiceDesk

from atlassianforms.form.manager import ServiceDeskFormFilled


class ServiceDeskRequestError(Exception):
    """
    Custom exception class for errors related to Service Desk requests.

    Attributes
    ----------
    status_code : int
        The HTTP status code returned by the failed request.
    error_message : str
        The error message returned by the failed request.

    Methods
    -------
    __str__():
        Returns a formatted string representation of the error.
    """

    def __init__(self, status_code: int, error_message: str):
        """
        Initializes the ServiceDeskRequestError with the status code and error message.

        Parameters
        ----------
        status_code : int
            The HTTP status code returned by the failed request.
        error_message : str
            The error message returned by the failed request.
        """
        self.status_code = status_code
        self.error_message = error_message
        super().__init__(self.__str__())

    def __str__(self):
        """
        Returns a formatted string representation of the error.

        Returns
        -------
        str
            A string representation of the error.
        """
        return f"ServiceDeskRequestError: {self.status_code} - {self.error_message}"


def remove_disposable_keys(data, disposable_keys):
    """
    Recursively removes the disposable keys from a dictionary or list.

    Parameters
    ----------
    data : dict or list
        The JSON data (as a dict or list) from which keys should be removed.
    disposable_keys : list
        A list of keys to be removed from the data.

    Returns
    -------
    dict or list
        The cleaned-up data with disposable keys removed.
    """
    if isinstance(data, dict):
        return {
            k: remove_disposable_keys(v, disposable_keys)
            for k, v in data.items()
            if k not in disposable_keys
        }
    elif isinstance(data, list):
        return [remove_disposable_keys(item, disposable_keys) for item in data]
    else:
        return data


def clean_response(response):
    """
    Cleans up the JSON response by removing unnecessary keys.

    Parameters
    ----------
    response : dict
        The JSON response to clean.

    Returns
    -------
    dict
        The cleaned response.
    """
    disposable_keys = [
        "key",
        "portalBaseUrl",
        "onlyPortal",
        "createPermission",
        "portalAnnouncement",
        "canViewCreateRequestForm",
        "isProjectSimplified",
        "mediaApiUploadInformation",
        "userLanguageHeader",
        "userLanguageMessageWiki",
        "defaultLanguageHeader",
        "defaultLanguageMessage",
        "defaultLanguageDisplayName",
        "isUsingLanguageSupport",
        "translations",
        "callToAction",
        "intro",
        "instructions",
        "icon",
        "iconUrl",
        "userOrganisations",
        "canBrowseUsers",
        "requestCreateBaseUrl",
        "requestValidateBaseUrl",
        "calendarParams",
        "kbs",
        "canRaiseOnBehalf",
        "canSignupCustomers",
        "canCreateAttachments",
        "attachmentRequiredField",
        "hasGroups",
        "canSubmitWithEmailAddress",
        "showRecaptcha",
        "siteKey",
        "hasProformaForm",
        "linkedJiraFields",
        "portalWebFragments",
        "headerPanels",
        "subheaderPanels",
        "footerPanels",
        "pagePanels",
        "localId",
    ]

    return remove_disposable_keys(response, disposable_keys)


class ServiceDeskManager:
    """
    A class to manage interactions with the Atlassian Service Desk API and to fetch
    request parameters necessary for creating service desk requests.

    Attributes
    ----------
    base_url : str
        The base URL for the Atlassian account.
    username : str
        The username for authentication.
    auth_token : str
        The authentication token or password.
    service_desk : ServiceDesk
        An instance of the Atlassian ServiceDesk client.
    jira : Jira
        An instance of the Atlassian Jira client.

    Methods
    -------
    get_service_desks() -> List[Dict]:
        Fetches and returns all service desk projects.
    get_request_types(portal_id: int) -> List[Dict]:
        Fetches and returns all request types for a specific service desk project.
    fetch_form(portal_id: int, request_type_id: int) -> Dict:
        Fetches the fields and parameters for the specified service desk request type.
    validate_field_data(portal_id: int, request_type_id: int, field_data: dict) -> bool:
        Validates the provided field data against the required fields from the request parameters.
    create_service_desk_request(request_type: str, reporter_email: str,
                                field_data: dict, portal_id: str) -> Dict:
        Creates a service desk request with the specified parameters.
    """

    def __init__(self, base_url: str, username: str, auth_token: str):
        """
        Initialize ServiceDeskManager with authentication details and headers.

        Parameters
        ----------
        base_url : str
            The base URL for the Atlassian account.
        username : str
            The username for authentication.
        auth_token : str
            The authentication token or password.

        Notes
        -----
        Sets up required headers for both old and new API endpoints, including:
        - Basic authentication
        - Content type headers
        - Experimental API headers
        """
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.auth_token = auth_token

        self.auth_header = {
            "Authorization": f"Basic {base64.b64encode(f'{username}:{auth_token}'.encode()).decode()}",
            "X-Atlassian-Token": "no-check",
            "X-ExperimentalApi": "opt-in",
        }
        self.default_headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "x-requested-with": "XMLHttpRequest",
        }
        self.all_headers = {**self.default_headers, **self.auth_header}
        self.service_desk = ServiceDesk(
            url=base_url, username=username, password=auth_token
        )
        self.jira = Jira(url=base_url, username=username, password=auth_token)

    def _fetch_cloud_id(self) -> Optional[str]:
        """
        Fetch the cloud ID required for making API calls.

        Returns
        -------
        Optional[str]
            The cloud ID if successfully retrieved, None otherwise.

        Raises
        ------
        requests.exceptions.HTTPError
            If the API request fails.

        Notes
        -----
        Cloud ID is required for accessing the new Atlassian Cloud API endpoints.
        """
        url = f"{self.base_url}/_edge/tenant_info"
        response = requests.get(url, headers=self.all_headers)
        response.raise_for_status()
        return response.json().get("cloudId")

    def _fetch_form_template(
        self, cloud_id: str, service_desk_id: str, request_type_id: str
    ) -> Dict:
        """
        Fetch form template data from the new API.

        Parameters
        ----------
        cloud_id : str
            The Atlassian cloud instance ID.
        service_desk_id : str
            The ID of the service desk project.
        request_type_id : str
            The ID of the request type.

        Returns
        -------
        Dict
            The form template data including design, settings, and fields.

        Raises
        ------
        requests.exceptions.HTTPError
            If the API request fails.
        """
        url = f"https://api.atlassian.com/jira/forms/cloud/{cloud_id}/servicedesk/{service_desk_id}/requesttype/{request_type_id}/form"
        response = requests.get(url, headers=self.all_headers)
        response.raise_for_status()
        return response.json()

    def _fetch_form_external_data(
        self, cloud_id: str, service_desk_id: str, request_type_id: str
    ) -> Dict:
        """
        Fetch external data for form fields from the new API.

        Parameters
        ----------
        cloud_id : str
            The Atlassian cloud instance ID.
        service_desk_id : str
            The ID of the service desk project.
        request_type_id : str
            The ID of the request type.

        Returns
        -------
        Dict
            External data including field choices and configurations.

        Raises
        ------
        requests.exceptions.HTTPError
            If the API request fails.
        """
        url = f"https://api.atlassian.com/jira/forms/cloud/{cloud_id}/servicedesk/{service_desk_id}/requesttype/{request_type_id}/form/externaldata"
        response = requests.get(url, headers=self.all_headers)
        response.raise_for_status()
        return response.json()

    def get_service_desks(self) -> List[Dict]:
        """
        Fetches and returns all service desk projects.

        Returns
        -------
        List[Dict]
            A list of dictionaries containing service desk project details.
        """
        return self.service_desk.get_service_desks()

    def get_request_types(self, service_desk_id: int, group_id: int) -> List[Dict]:
        """
        Fetches and returns all request types for a specific service desk project.

        Parameters
        ----------
        service_desk_id : int
            The ID of the service desk project.
        group_id : int
            The ID of the group.

        Returns
        -------
        List[Dict]
            A list of dictionaries containing request type details.
        """
        return self.service_desk.get_request_types(
            service_desk_id=service_desk_id, group_id=group_id
        )

    def fetch_form(self, portal_id: int, request_type_id: int) -> Dict:
        """
        Fetch complete form data using new API endpoints while maintaining backward compatibility.

        Parameters
        ----------
        portal_id : int
            The ID of the service desk portal.
        request_type_id : int
            The ID of the request type.

        Returns
        -------
        Dict
            Form data in the original format for backward compatibility.

        Raises
        ------
        Exception
            If cloud ID cannot be fetched or if any required data is missing.
        requests.exceptions.HTTPError
            If any API request fails.

        Notes
        -----
        This method aggregates data from multiple new API endpoints and converts
        it to match the original response format for backward compatibility.
        """
        cloud_id = self._fetch_cloud_id()
        if not cloud_id:
            raise Exception("Could not fetch cloud ID")

        form_data = self._fetch_form_template(
            cloud_id, str(portal_id), str(request_type_id)
        )
        external_data = self._fetch_form_external_data(
            cloud_id, str(portal_id), str(request_type_id)
        )

        service_desk_data = self._fetch_service_desk_models(portal_id, request_type_id)

        converted_data = {
            "portal": {
                "id": form_data["id"],
                "serviceDeskId": str(portal_id),
                "projectId": str(service_desk_data["reqCreate"]["projectId"]),
                "name": service_desk_data["reqCreate"]["form"]["name"],
                "description": service_desk_data["reqCreate"]["form"][
                    "descriptionHtml"
                ],
            },
            "reqCreate": {
                "id": str(request_type_id),
                "form": {
                    "name": form_data["design"]["settings"]["name"],
                    "descriptionHtml": form_data["design"]["settings"].get(
                        "descriptionHtml", ""
                    ),
                },
                "fields": self._convert_fields(
                    form_data, external_data, service_desk_data
                ),
                "proformaTemplateForm": {
                    "updated": form_data.get("updated"),
                    "design": {
                        "settings": {
                            "templateId": service_desk_data["reqCreate"]
                            .get("proforma", {})
                            .get("formTemplateData", {})
                            .get("design", {})
                            .get("settings", {})
                            .get("templateId"),
                            "templateFormUuid": service_desk_data["reqCreate"]
                            .get("proforma", {})
                            .get("formTemplateData", {})
                            .get("uuid"),
                        }
                    },
                },
            },
            "xsrfToken": service_desk_data.get("xsrfToken"),
        }
        return converted_data

    def _convert_fields(
        self, form_data: Dict, external_data: Dict, service_desk_data: Dict
    ) -> List[Dict]:
        """
        Convert fields from new API format to the original format.

        Parameters
        ----------
        form_data : Dict
            Form template data from the new API.
        external_data : Dict
            External field data from the new API.
        service_desk_data : Dict
            Service desk data from the existing endpoint.

        Returns
        -------
        List[Dict]
            List of converted fields in the original format.

        Notes
        -----
        Handles both regular fields and proforma fields, maintaining all field
        properties and relationships from the original format.
        """
        fields = []
        for field_data in service_desk_data["reqCreate"].get("fields", []):
            field_id = field_data.get("fieldId")
            field_type = field_data.get("fieldType")

            converted_field = {
                "fieldType": field_type,
                "fieldId": field_id,
                "fieldConfigId": field_data.get("fieldConfigId", ""),
                "label": field_data.get("label"),
                "description": field_data.get("description", ""),
                "descriptionHtml": field_data.get("descriptionHtml", ""),
                "required": field_data.get("required", False),
                "displayed": field_data.get("displayed", False),
                "values": field_data.get("values", []),
                "rendererType": field_data.get("rendererType"),
                "autoCompleteUrl": field_data.get("autoCompleteUrl"),
            }
            fields.append(converted_field)

        proforma_questions = form_data.get("design", {}).get("questions", {})
        proforma_linked_fields = (
            service_desk_data["reqCreate"]
            .get("proforma", {})
            .get("linkedJiraFields", [])
        )
        external_fields = external_data.get("fields", {})

        for question_id, question_data in proforma_questions.items():
            jira_field = question_data.get("jiraField")
            if jira_field in proforma_linked_fields:
                external_field_data = external_fields.get(question_id, {})
                if external_field_data:
                    converted_field = {
                        "fieldType": question_data.get("type"),
                        "fieldId": jira_field,
                        "fieldConfigId": external_field_data.get("jiraField", {}).get(
                            "configId", ""
                        ),
                        "label": question_data.get("label"),
                        "description": question_data.get("description", ""),
                        "descriptionHtml": "",
                        "required": question_data.get("validation", {}).get(
                            "rq", False
                        ),
                        "displayed": True,
                        "isProformaField": True,
                        "proformaQuestionId": str(question_id),
                        "values": self._convert_choices(
                            external_field_data.get("choices", [])
                        ),
                    }
                    fields.append(converted_field)

        return fields

    def _convert_choices(self, choices: List[Dict]) -> List[Dict]:
        """
        Convert field choices from new API format to original format.

        Parameters
        ----------
        choices : List[Dict]
            List of choices from the new API.

        Returns
        -------
        List[Dict]
            Converted choices in the original format.

        Notes
        -----
        Ensures backward compatibility by maintaining the same choice structure
        used in the original API.
        """
        return [
            {
                "value": choice.get("id", ""),
                "label": choice.get("name", ""),
                "selected": False,
            }
            for choice in choices
        ]

    def _fetch_service_desk_models(
        self, service_desk_id: Union[str, int], request_type_id: int
    ) -> Dict:
        """
        Fetches service desk models using the customer endpoint.

        Parameters
        ----------
        service_desk_id : Union[str, int]
            The ID of the service desk
        request_type_id : int
            The ID of the request type

        Returns
        -------
        Dict
            The JSON response containing models data
        """
        url = f"{self.base_url}/rest/servicedesk/1/customer/models"

        payload = {
            "options": {
                "reqCreate": {"portalId": int(service_desk_id), "id": request_type_id},
                "portalId": int(service_desk_id),
            },
            "models": ["xsrfToken", "reqCreate"],
            "context": {
                "helpCenterAri": "ari:cloud:help::help-center/023eca6c-913d-41af-a182-61e86fd72ccc/de1070f9-b9dd-460c-b02f-104fc367db40",
                "clientBasePath": f"{self.base_url}/servicedesk/customer",
            },
        }

        try:
            response = requests.post(url, headers=self.all_headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error fetching service desk models: {e}")
            return {}

    def create_request(self, form_filled: ServiceDeskFormFilled) -> Dict:
        """
        Creates a service desk request with the specified parameters.

        Parameters
        ----------
        form_filled : ServiceDeskFormFilled
            An instance of ServiceDeskFormFilled containing validated user input.
        reporter_email : str
            The email of the reporter.

        Returns
        -------
        Dict
            The response from the API after creating the request.
        """
        field_data = form_filled.to_request_payload()

        portal_id = form_filled.form.service_desk_id
        request_type_id = form_filled.form.request_type_id

        url = f"{self.base_url}/servicedesk/customer/portal/{portal_id}/create/{request_type_id}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            **self.auth_header,
        }
        params = requests.models.RequestEncodingMixin._encode_params(field_data)
        response = requests.post(url, headers=headers, data=params)

        if response.status_code in (201, 200):
            return response.json()
        else:
            raise ServiceDeskRequestError(response.status_code, response.text)
