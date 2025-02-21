# kyc_validator.py
import fireworks.client
import base64
import json
from datetime import datetime
from typing import Union, BinaryIO

class KYCValidator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        fireworks.client.api_key = api_key

    def encode_image(self, image_data: Union[str, bytes, BinaryIO]) -> str:
        """
        Encode image data to base64 string.
        
        Args:
            image_data: Can be either:
                - A file path (str)
                - Bytes object
                - File-like object (e.g., from FastAPI's UploadFile)
        
        Returns:
            base64 encoded string
        """
        try:
            # If image_data is a string, treat it as a file path
            if isinstance(image_data, str):
                with open(image_data, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode('utf-8')
            
            # If image_data is bytes, encode directly
            elif isinstance(image_data, bytes):
                return base64.b64encode(image_data).decode('utf-8')
            
            # If image_data is a file-like object, read and encode
            elif hasattr(image_data, 'read'):
                # If it's a file object, read it
                content = image_data.read()
                if isinstance(content, str):
                    content = content.encode('utf-8')
                return base64.b64encode(content).decode('utf-8')
            
            else:
                raise ValueError("Unsupported image data type")
                
        except Exception as e:
            raise ValueError(f"Error encoding image: {str(e)}")

    async def extract_document_info(self, image_data: Union[str, bytes, BinaryIO]) -> dict:
        """
        Extract information from the provided document image
        
        Args:
            image_data: Can be file path, bytes, or file-like object
            
        Returns:
            Dictionary containing extracted document information
        """
        try:
            image_base64 = self.encode_image(image_data)
            
            response = fireworks.client.ChatCompletion.create(
                model="accounts/fireworks/models/llama-v3p2-90b-vision-instruct",
                messages=[{
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": "Can you describe this image? Output the format in json in this format DOB, LN, FN, DL, EXP, Address, Sex, HGT, WGT, HAIR, EYES, ISS, type of document",
                    }, {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        },
                    }],
                }],
                response_format={"type": "json_object"},
                top_p=1,
                top_k=40,
                presence_penalty=0,
                frequency_penalty=0,
                temperature=0.6,
            )
            
            return json.loads(response.choices[0].message.content)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing LLM response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error processing document: {str(e)}")

    async def validate_user_data(self, user_data: dict, document_data: dict) -> dict:
        """
        Compare user-submitted data with document data
        
        Args:
            user_data: Dictionary containing user submitted data (name, dob, address)
            document_data: Dictionary containing extracted document data
            
        Returns:
            Dictionary containing validation results
        """
        try:
            validation_prompt = f"""
            Compare the user-submitted information with the document information and determine if they match.
            In the event of a passport, there will not be a full address but a region, determine if the address provided is in the region of the document.
            Respond with only two fields named "Result" with a value of pass or fail and "Feedback" with information why it failed, if it passed provide "none"

            User submitted information:
            Name: {user_data['name']}
            Date of Birth: {user_data['dob']}
            Address: {user_data['address']}

            Document information:
            Name: {document_data.get('FN', '')} {document_data.get('LN', '')}
            Date of Birth: {document_data.get('DOB', '')}
            Address: {document_data.get('Address', '')}
            Document Type: {document_data.get('type of document', '')}

            Analyze the following:
            1. Name matching (accounting for formatting differences, we just want to know if the full name is present)
            2. Date of birth matching
            3. Address matching (accounting for abbreviations and formatting)
            4. Document validity (check expiration if available)
            """

            response = fireworks.client.ChatCompletion.create(
                model="accounts/fireworks/models/llama-v3p1-405b-instruct",
                messages=[{
                    "role": "user",
                    "content": validation_prompt
                }],
                max_tokens=4096,
                top_p=1,
                top_k=40,
                presence_penalty=0,
                frequency_penalty=0,
                temperature=0.6,
                response_format={"type": "json_object"}
            )

            return json.loads(response.choices[0].message.content)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing LLM response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error validating data: {str(e)}")