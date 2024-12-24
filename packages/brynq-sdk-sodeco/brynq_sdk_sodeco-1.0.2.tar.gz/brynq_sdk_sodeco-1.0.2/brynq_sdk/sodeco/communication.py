from typing import Optional
import pandas as pd
from datetime import datetime

from .base import SodecoBase
from .schemas.communication import CommunicationSchema
from brynq_sdk.functions import Functions

class Communications(SodecoBase):
    """Class for managing communications in Sodeco."""

    def __init__(self, sodeco):
        super().__init__(sodeco)
        self.url = f"{self.sodeco.base_url}worker"

    def get(self, worker_id: str) -> pd.DataFrame:
        """
        Get communication information for a worker.
        
        Args:
            worker_id: The worker ID to get communication for
            
        Returns:
            pd.DataFrame: DataFrame containing the communication information
        """
        url = f"{self.url}/{worker_id}/communication"
        data = self._make_request_with_polling(url)
        return pd.DataFrame(data)

    def create(self, worker_id: str, payload: dict, debug: bool = False) -> dict:
        """
        Create a communication entry for a worker.
        The payload must adhere to the structure defined by the CommunicationSchema.
        
        Args:
            worker_id: The ID of the worker to create a communication for
            payload: The communication data to create
            debug: If True, prints detailed validation errors
            
        Returns:
            dict: The created communication data
            
        Raises:
            ValueError: If the payload is invalid
        """
        url = f"{self.url}/{worker_id}/communication"
        
        # Convert payload to DataFrame and validate
        df = pd.DataFrame([payload])
        valid_data, invalid_data = Functions.validate_data(df, CommunicationSchema, debug=debug)

        if len(invalid_data) > 0:
            error_msg = "Invalid communication payload"
            if debug:
                error_msg += f": {invalid_data.to_dict(orient='records')}"
            raise ValueError(error_msg)

        # Send the POST request to create the communication
        headers, data = self._prepare_raw_request(valid_data.iloc[0].to_dict())
        data = self._make_request_with_polling(
            url,
            method='POST',
            headers=headers,
            data=data
        )
        return data
