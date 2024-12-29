#    ____   # -------------------------------------------------- #
#   | ^  |  # EPICClient for AUMC               				 #
#   \  --   # o.m.vandermeer@amsterdamumc.nl        			 #
# \_| ﬤ| ﬤ  # If you like this code, treat him to a coffee! ;)	 #
#   |_)_)   # -------------------------------------------------- #

from json import dumps
import uuid


class InternalBase:

    def __init__(self, epic_client):
        self.epic_client = epic_client
        self.post = self.epic_client.post
        self.get = self.epic_client.get
        self.put = self.epic_client.put
        self.delete = self.epic_client.delete
        self.patch = self.epic_client.patch
        self.base_url = self.epic_client.base_url

    def set_smart_data_values(
        self,
        context_name,
        entity_id,
        entity_id_type,
        user_id,
        user_id_type,
        smart_data_values,
        contact_id=None,
        contact_id_type="DAT",
        source="Web Service",
        extra_headers={},
    ):
        """
        Sets raw values for SmartData elements.

        Args:
            context_name (str): Name of the context associated with SmartData elements (e.g., PATIENT, ENCOUNTER).
            entity_id (str): ID for the entity associated with the context.
            entity_id_type (str): Type of the provided entity ID (e.g., Internal, External, CID).
            user_id (str): User ID used for auditing.
            user_id_type (str): Type of the provided User ID (e.g., Internal, External).
            smart_data_values (list): List of dictionaries representing SmartData values to set.
                Each dictionary should contain keys `Comments`, `SmartDataID`, `SmartDataIDType`, and `Values`.
            contact_id (str, optional): Contact date for the ENCOUNTER context.
            contact_id_type (str, optional): Type for the provided contact date. Defaults to "DAT".
            source (str, optional): Source setting the values. Defaults to "Web Service".
            extra_headers (dict, optional): Additional headers to include in the request.

        Returns:
            dict: Parsed response from the API.
        """
        endpoint = "api/epic/2013/Clinical/Utility/SETSMARTDATAVALUES/SmartData/Values"

        payload = {
            "SetSmartDataValues": {
                "@xmlns": "urn:Epic-com:Clinical.2012.Services.Utility",
                "ContextName": context_name,
                "EntityID": entity_id,
                "EntityIDType": entity_id_type,
                "UserID": user_id,
                "UserIDType": user_id_type,
                "Source": source,
                "SmartDataValues": {
                    "Value": [
                        {
                            "Comments": {"string": [val["Comments"]]},
                            "SmartDataID": val["SmartDataID"],
                            "SmartDataIDType": val["SmartDataIDType"],
                            "Values": {"string": [val["Values"]]},
                        }
                        for val in smart_data_values
                    ]
                },
            }
        }

        # Include optional fields if provided
        if contact_id:
            payload["SetSmartDataValues"]["ContactID"] = contact_id
            payload["SetSmartDataValues"]["ContactIDType"] = contact_id_type

        return self.put(endpoint, json=payload, extra_headers=extra_headers)

    def get_smart_data_values(
        self,
        context_name,
        entity_id,
        entity_id_type,
        user_id,
        user_id_type,
        smart_data_ids=None,
        contact_id=None,
        contact_id_type="DAT",
        extra_headers={},
    ):
        """
        Retrieves raw values for SmartData elements.

        Args:
            context_name (str): Name of the context associated with SmartData elements (e.g., PATIENT, ENCOUNTER).
            entity_id (str): ID for the entity associated with the context.
            entity_id_type (str): Type of the provided entity ID (e.g., Internal, External, CID).
            user_id (str): User ID used for auditing.
            user_id_type (str): Type of the provided User ID (e.g., Internal, External).
            smart_data_ids (list, optional): List of dictionaries representing SmartData IDs to retrieve.
                Each dictionary should contain keys `ID` and `Type`.
            contact_id (str, optional): Contact date for the ENCOUNTER context.
            contact_id_type (str, optional): Type for the provided contact date. Defaults to "DAT".
            extra_headers (dict, optional): Additional headers to include in the request.

        Returns:
            dict: Parsed response from the API.
        """
        endpoint = "api/epic/2013/Clinical/Utility/GETSMARTDATAVALUES/SmartData/Values"

        payload = {
            "GetSmartDataValues": {
                "ContextName": context_name,
                "EntityID": entity_id,
                "EntityIDType": entity_id_type,
                "UserID": user_id,
                "UserIDType": user_id_type,
                "SmartDataIDs": (
                    {
                        "IDType": [
                            {"ID": val["ID"], "Type": val["Type"]}
                            for val in (smart_data_ids or [])
                        ]
                    }
                    if smart_data_ids
                    else None
                ),
            }
        }

        # Include optional fields if provided
        if contact_id:
            payload["GetSmartDataValues"]["ContactID"] = contact_id
            payload["GetSmartDataValues"]["ContactIDType"] = contact_id_type

        return self.post(endpoint, json=payload, extra_headers=extra_headers)

    def handle_external_model_scores(
        self,
        model_id,
        entity_ids,
        outputs,
        job_id=uuid.uuid4(),
        error_message=None,
        output_type="",
        raw=None,
        predictive_context={},
        ScoreDisplayed="",
    ):
        """
        Send predictive model scores back to the Epic Cognitive Computing Platform for filing.

        :param model_id: str, the ECCP model ID the scores are for
        :param job_id: str, the autogenerated job ID for the evaluation on ECCP
        :param output_type: str, the type of output for the predictive model
        :param server_version: str, the server version of the predictive context
        :param session_id: str, the session ID of the predictive context
        :param entity_ids: list, a list of dictionaries with ID and Type for the entity
        :param outputs: dict, the output values of the predictive model
        :param raw: dict, optional, raw features used to calculate the scores
        :param predictive_context: dict, optional, additional context information for the predictive model

        :return: dict, the response from the Epic Cognitive Computing Platform
        """
        print("Sending external model scores to ECCP with job ID: {}".format(job_id))
        url = f"/api/epic/2017/Reporting/Predictive/HANDLEEXTERNALMODELSCORES?modelId={model_id}&jobId={job_id}"
        headers = {"Content-Type": "application/json"}

        # Build the request payload
        request_body = {}

        request_body["OutputType"] = output_type

        request_body["PredictiveContext"] = predictive_context

        if error_message:
            request_body["Error"] = error_message

        request_body["ScoreDisplayed"] = ScoreDisplayed

        # Add entity IDs
        request_body["EntityId"] = [
            {"ID": entity["ID"], "Type": entity["Type"]} for entity in entity_ids
        ]

        # Add outputs and optional raw features
        request_body["Outputs"] = outputs
        if raw:
            request_body["Raw"] = raw

        # Send the request
        response = self.post(url, extra_headers=headers, data=dumps(request_body))

        return response
