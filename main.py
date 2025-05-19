import json
import re
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from models import ModelManager
from utils import mask_pii

app = FastAPI()

# Initialize model manager
model_manager = ModelManager()
try:
    model_manager.load_models()
except Exception as e:
    raise RuntimeError(f"Error loading models: {e}")

# Helper class for marking lists that need compact JSON representation
class CompactListWrapper:
    def __init__(self, data_list):
        self.data = data_list

# Custom JSON Encoder (used by CustomFormattedJSONResponse)
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, CompactListWrapper):
            return f"__COMPACT_LIST_PLACEHOLDER__{json.dumps(o.data, separators=(',',':'))}__END_PLACEHOLDER__"
        return super().default(o)

# Custom JSONResponse class for specific formatting
class CustomFormattedJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        # content is the dictionary passed to the response instance
        json_string_with_placeholders = json.dumps(
            content, 
            indent=2, 
            cls=CustomJsonEncoder # Our encoder that inserts placeholders
        )
        
        # Replace the quoted placeholders with their unquoted compact list content
        final_json_string = re.sub(
            r'"__COMPACT_LIST_PLACEHOLDER__(.*?)__END_PLACEHOLDER__"',
            r'\1',
            json_string_with_placeholders
        )
        
        return final_json_string.encode("utf-8")

class EmailInput(BaseModel):
    input_email_body: str

@app.post("/classify")
async def classify_email(email_input: EmailInput):
    try:
        # Mask PII in the email
        masked_email_str, masked_entities_list_of_dicts = mask_pii(
            email_input.input_email_body,
            model_manager.ner_pipeline
        )

        # Classify the masked email
        predicted_category_str = model_manager.predict(masked_email_str)

        # Prepare data, wrapping 'position' lists in CompactListWrapper
        processed_masked_entities = []
        for entity_dict in masked_entities_list_of_dicts:
            # Create a new dict to avoid modifying original from mask_pii if it's reused
            processed_entity = entity_dict.copy()
            if "position" in processed_entity and isinstance(processed_entity["position"], list):
                processed_entity["position"] = CompactListWrapper(processed_entity["position"])
            processed_masked_entities.append(processed_entity)

        response_data = {
            "input_email_body": email_input.input_email_body,
            "list_of_masked_entities": processed_masked_entities,
            "masked_email": masked_email_str,
            "category_of_the_email": predicted_category_str
        }

        # Use the custom response class
        return CustomFormattedJSONResponse(content=response_data)
    except Exception as e:
        # It's good practice to log the actual exception for debugging on the server
        # import traceback
        # print(f"Error in classify_email: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)