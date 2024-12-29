#    ____   # -------------------------------------------------- #
#   | ^  |  # EPICClient for AUMC               				 #
#   \  --   # o.m.vandermeer@amsterdamumc.nl        			 #
# \_| ﬤ| ﬤ  # If you like this code, treat him to a coffee! ;)	 #
#   |_)_)   # -------------------------------------------------- #

from json import dumps
import base64
from datetime import datetime


class FHIRBase:
    def __init__(self, epic_client):
        self.epic_client = epic_client
        self.post = self.epic_client.post
        self.get = self.epic_client.get
        self.put = self.epic_client.put
        self.delete = self.epic_client.delete
        self.patch = self.epic_client.patch
        self.base_url = self.epic_client.base_url

    def get_metadata(self, version="R4"):
        if version not in ["DSTU2", "STU3", "R4"]:
            raise ValueError(
                "Invalid version. Please specify either 'DSTU2', 'STU3' or 'R4'."
            )

        endpoint = f"/api/FHIR/{version}/metadata"
        endpoint = self.base_url + endpoint
        response = self.get(endpoint)
        print("GET response:", response)

        return response

    def get_resource(
        self, resource_type, resource_id=None, version="R4", **optional_params
    ):
        """
        Get a FHIR resource with mandatory and optional parameters.

        :param resource_type: str, the type of the FHIR resource (e.g., 'Patient', 'Encounter')
        :param resource_id: str, the ID of the resource
        :param optional_params: dict, optional query parameters to be added to the URL

        :return: dict, the response from the FHIR server
        """
        base_url = f"api/FHIR/{version}/{resource_type}"

        if resource_id:
            base_url += f"/{resource_id}"

        if optional_params:
            # Append optional query parameters to the URL
            for key, value in optional_params.items():
                if value != None:
                    qlist = [f"{key}={value}"]
            query_string = "&".join(qlist)
            url = f"{base_url}?{query_string}"
        else:
            url = base_url

        return self.get(url)

    def patient_read(self, patient_id):
        """Retrieve patient information by patient ID."""
        return self.get_resource("Patient", patient_id)

    def patient_search(
        self,
        address=None,
        address_city=None,
        address_postalcode=None,
        address_state=None,
        birthdate=None,
        family=None,
        gender=None,
        given=None,
        identifier=None,
        name=None,
        own_name=None,
        own_prefix=None,
        partner_name=None,
        partner_prefix=None,
        telecom=None,
        legal_sex=None,
        active=None,
        address_use=None,
        death_date=None,
        email=None,
        general_practitioner=None,
        language=None,
        link=None,
        organization=None,
        phone=None,
        phonetic=None,
    ):
        # Build query parameters
        params = {
            "address": address,
            "address-city": address_city,
            "address-postalcode": address_postalcode,
            "address-state": address_state,
            "birthdate": birthdate,
            "family": family,
            "gender": gender,
            "given": given,
            "identifier": identifier,
            "name": name,
            "own-name": own_name,
            "own-prefix": own_prefix,
            "partner-name": partner_name,
            "partner-prefix": partner_prefix,
            "telecom": telecom,
            "legal-sex": legal_sex,
            "active": active,
            "address-use": address_use,
            "death-date": death_date,
            "email": email,
            "general-practitioner": general_practitioner,
            "language": language,
            "link": link,
            "organization": organization,
            "phone": phone,
            "phonetic": phonetic,
        }

        # Remove any parameters that are None (not provided)
        params = {key: value for key, value in params.items() if value is not None}

        # Send GET request with the constructed parameters
        return self.get_resource("Patient", params=params)

    def encounter_read(self, encounter_id):
        """Retrieve encounter information by patient ID."""
        return self.get_resource("Encounter", encounter_id)

    def encounter_search(self, patient_id):
        """Retrieve encounters by patient ID."""
        return self.get_resource("Encounter", patient=patient_id)

    def document_reference_read(self, document_reference_id):
        """Retrieve document_reference information by document_reference_id."""
        return self.get_resource("DocumentReference", document_reference_id)

    def document_reference_search(
        self,
        category=None,
        date=None,
        docstatus=None,
        encounter=None,
        patient=None,
        period=None,
        subject=None,
        d_type=None,
    ):
        """Retrieve encounters by patient ID."""
        if not (subject or patient):
            raise ValueError("At least one of subject or patient must be provided")
        if not (category or d_type):
            category = "clinical-note"
        return self.get_resource(
            "DocumentReference",
            category=category,
            date=date,
            docstatus=docstatus,
            encounter=encounter,
            patient=patient,
            period=period,
            subject=subject,
            type=d_type,
        )

    def observation_create(self, patient_id, encounter_id, flowsheet_id, name, value):
        """Create observation. For now only 1 entry per call is supported"""
        url = "/api/FHIR/R4/Observation"
        observation = {
            "resourceType": "Observation",
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/observation-category",
                            "code": "vital-signs",
                            "display": "Vital Signs",
                        }
                    ],
                    "text": "Vital Signs",
                }
            ],
            "code": {
                "coding": [
                    {
                        "system": "http://open.epic.com/FHIR/StructureDefinition/observation-flowsheet-id",  # urn:oid:2.16.840.1.113883.6.88
                        "code": flowsheet_id,
                        "display": name,
                    }
                ],
                "text": name,
            },
            "subject": {
                "reference": "Patient/" + patient_id,
                # "display": "Meiko Lufhir"
            },
            "encounter": {"reference": "Encounter/" + encounter_id},
            "effectiveDateTime": datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),  # "2019-09-05T20:00:00Z",
            "valueQuantity": {
                "value": value,
                # "unit": "",
                # "system": "http://unitsofmeasure.org",
                # "code": "%"
            },
            "status": "final",
        }
        return self.post(url, json=observation)

    def document_reference_create(
        self,
        patient_id,
        encounter_id,
        note_text,
        note_type="Consultation Note",
        doc_status="final",
        prefer="return=representation",
    ):
        """
        Create a DocumentReference resource in the FHIR server.

        :param patient_id: str, the ID of the patient
        :param encounter_id: str, the ID of the encounter
        :param note_text: str, the plain text of the note
        :param note_type: str, the type of the note, default is "Consultation Note"
        :param doc_status: str, the status of the document, default is "final"
        :param prefer: str, the prefer header to control the response, default is "return=representation"

        :return: dict, the response from the FHIR server
        """
        url = "/api/FHIR/R4/DocumentReference"
        headers = {"Content-Type": "application/fhir+json", "Prefer": prefer}

        document_reference = {
            "resourceType": "DocumentReference",
            "docStatus": doc_status,
            "type": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "11488-4",
                        "display": note_type,
                    }
                ],
                "text": note_type,
            },
            "subject": {"reference": f"Patient/{patient_id}"},
            "content": [
                {
                    "attachment": {
                        "contentType": "text/plain",
                        "data": base64.b64encode(note_text.encode("utf-8")).decode(
                            "utf-8"
                        ),
                    }
                }
            ],
            "context": {"encounter": [{"reference": f"Encounter/{encounter_id}"}]},
        }

        return self.post(url, extra_headers=headers, data=dumps(document_reference))
