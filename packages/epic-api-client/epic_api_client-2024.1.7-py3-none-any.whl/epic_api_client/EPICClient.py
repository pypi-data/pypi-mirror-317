#    ____   # -------------------------------------------------- #
#   | ^  |  # EPICClient for AUMC               				 #
#   \  --   # o.m.vandermeer@amsterdamumc.nl        			 #
# \_| ﬤ| ﬤ  # If you like this code, treat him to a coffee! ;)	 #
#   |_)_)   # -------------------------------------------------- #

from json import dumps
from epic_api_client.SimpleHttpClient import SimpleHttpClient
from epic_api_client.FHIRExtension import FHIRExtension
from epic_api_client.InternalExtension import InternalExtension
import requests
import warnings


class EPICClient(SimpleHttpClient):
    def __init__(self, base_url=None, headers=None, client_id=None, jwt_generator=None):
        super().__init__(base_url, headers)
        # Pass `self` to extensions
        self.fhir = FHIRExtension(self)
        self.internal = InternalExtension(self)
        self.set_header("Epic-Client-ID", client_id)
        if not self.base_url:
            print("No base URL provided, using sandbox URL")
            self.base_url = (
                "https://vendorservices.epic.com/interconnect-amcurprd-oauth"
            )
        else:
            print("base url: ", self.base_url)
        self.jwt_generator = jwt_generator
        self.client_id = client_id
        self.dino = "Mrauw!"

    def set_token(self, token):
        self.set_header("Authorization", f"Bearer {token}")
        self.set_header("Accept", "application/fhir+json")

    def obtain_access_token(self):
        print("obtaining access token...")
        token_endpoint = self.base_url + "/oauth2/token"
        # Generate JWT
        jwt_token = self.jwt_generator.create_jwt(self.client_id, token_endpoint)

        # Set up the POST request data
        data = {
            "grant_type": "client_credentials",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": jwt_token,
        }

        # POST the JWT to the token endpoint
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(token_endpoint, data=data, headers=headers)
        response_data = response.json()
        # Check for successful response
        if response.status_code == 200:
            print("authentication successful")
            self.access_token = response_data.get("access_token")
            self.set_token(self.access_token)
            # self.set_header('prefer', 'return=representation')
            if "scope" in response_data:
                print("scope of client id: ", response_data["scope"])
            else:
                print("no scope of client id available")
            return response.json()  # Returns the access token and other data
        else:
            print("Response Status Code:", response.status_code)
            print("Response Text:", response.text)
            response.raise_for_status()

    def print_json(self, json_object):
        """
        Prints a JSON object in a readable, formatted way.

        Args:
        json_object (dict): The JSON object to be printed.
        """
        formatted_json = dumps(json_object, indent=2, sort_keys=True)
        print(formatted_json)

    # deprecated / relocated functions
    def get_metadata(self, *args, **kwargs):
        warnings.warn(
            "get_metadata has been relocated to fhir. "
            "Please update your code to use fhir.get_metadata instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.fhir.get_metadata(*args, **kwargs)

    def get_resource(self, *args, **kwargs):
        warnings.warn(
            "get_resource has been relocated to fhir. "
            "Please update your code to use fhir.get_resource instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.fhir.get_resource(*args, **kwargs)

    def patient_read(self, *args, **kwargs):
        warnings.warn(
            "patient_read has been relocated to fhir. "
            "Please update your code to use fhir.patient_read instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.fhir.patient_read(*args, **kwargs)

    def patient_search_MRN(self, *args, **kwargs):
        warnings.warn(
            "patient_search_MRN has been relocated to fhir. "
            "Please update your code to use fhir.patient_search_MRN instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.fhir.patient_search_MRN(*args, **kwargs)

    def mrn_to_FHIRid(self, *args, **kwargs):
        warnings.warn(
            "mrn_to_FHIRid has been relocated to fhir. "
            "Please update your code to use fhir.mrn_to_FHIRid instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.fhir.mrn_to_FHIRid(*args, **kwargs)

    def encounter_read(self, *args, **kwargs):
        warnings.warn(
            "encounter_read has been relocated to fhir. "
            "Please update your code to use fhir.encounter_read instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.fhir.encounter_read(*args, **kwargs)

    def encounter_search(self, *args, **kwargs):
        warnings.warn(
            "encounter_search has been relocated to fhir. "
            "Please update your code to use fhir.encounter_search instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.fhir.encounter_search(*args, **kwargs)

    def document_reference_read(self, *args, **kwargs):
        warnings.warn(
            "document_reference_read has been relocated to fhir. "
            "Please update your code to use fhir.document_reference_read instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.fhir.document_reference_read(*args, **kwargs)

    def document_reference_search(self, *args, **kwargs):
        warnings.warn(
            "document_reference_search has been relocated to fhir. "
            "Please update your code to use fhir.document_reference_search instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.fhir.document_reference_search(*args, **kwargs)

    def observation_create(self, *args, **kwargs):
        warnings.warn(
            "observation_create has been relocated to fhir. "
            "Please update your code to use fhir.observation_create instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.fhir.observation_create(*args, **kwargs)

    def document_reference_create(self, *args, **kwargs):
        warnings.warn(
            "document_reference_create has been relocated to fhir. "
            "Please update your code to use fhir.document_reference_create instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.fhir.document_reference_create(*args, **kwargs)

    def handle_external_model_scores(self, *args, **kwargs):
        warnings.warn(
            "handle_external_model_scores has been relocated to internal. "
            "Please update your code to use internal.handle_external_model_scores instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self.internal.handle_external_model_scores(*args, **kwargs)
