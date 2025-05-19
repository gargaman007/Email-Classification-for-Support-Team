import re
from typing import Dict, List, Tuple


def mask_full_name(text: str, ner_pipeline) -> Tuple[str, List[Dict]]:
    """
    Mask full names in text using NER model.
    
    Args:
        text (str): Input text
        ner_pipeline: NER pipeline for name detection
        
    Returns:
        Tuple[str, List[Dict]]: Masked text and list of masked entities
    """
    entities = ner_pipeline(text)
    masked_entities = []
    for ent in sorted(entities, key=lambda x: x['start'], reverse=True):
        if ent['entity_group'] in ['PER', 'Person', 'full_name']:
            start, end = ent['start'], ent['end']
            original_entity = text[start:end]
            masked_entities.append({
                "position": [start, end],
                "classification": "full_name",
                "entity": original_entity
            })
            text = text[:start] + '[full_name]' + text[end:]
    return text, masked_entities

def mask_with_regex(text: str) -> Tuple[str, List[Dict]]:
    """
    Mask PII using regex patterns.
    
    Args:
        text (str): Input text
        
    Returns:
        Tuple[str, List[Dict]]: Masked text and list of masked entities
    """
    masked_entities = []
    
    # Email address
    emails = list(re.finditer(r'\b[\w.-]+?@\w+?\.\w+?\b', text))
    for match in reversed(emails):
        start, end = match.span()
        original_entity = text[start:end]
        masked_entities.append({
            "position": [start, end],
            "classification": "email",
            "entity": original_entity
        })
        text = text[:start] + '[email]' + text[end:]

    # Phone number
    phones = list(re.finditer(r'\b(?:(?:\+|0)91[\s.-]?)?\d{10}(?!\d)\b', text))
    for match in reversed(phones):
        start, end = match.span()
        original_entity = text[start:end]
        masked_entities.append({
            "position": [start, end],
            "classification": "phone_number",
            "entity": original_entity
        })
        text = text[:start] + '[phone_number]' + text[end:]

    # Date of Birth
    dobs = list(re.finditer(r'\b\d{2}[-/]\d{2}[-/]\d{4}\b|\b\d{4}[-/]\d{2}[-/]\d{2}\b', text))
    for match in reversed(dobs):
        start, end = match.span()
        original_entity = text[start:end]
        masked_entities.append({
            "position": [start, end],
            "classification": "dob",
            "entity": original_entity
        })
        text = text[:start] + '[dob]' + text[end:]

    # Credit/Debit card number
    cards = list(re.finditer(r'\b(?:\d[ -]*?){13,19}\b', text))
    for match in reversed(cards):
        start, end = match.span()
        original_entity = text[start:end]
        masked_entities.append({
            "position": [start, end],
            "classification": "credit_debit_no",
            "entity": original_entity
        })
        text = text[:start] + '[credit_debit_no]' + text[end:]
        
    # Aadhar number
    aadhars = list(re.finditer(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', text))
    for match in reversed(aadhars):
        start, end = match.span()
        original_entity = text[start:end]
        masked_entities.append({
            "position": [start, end],
            "classification": "aadhar_num",
            "entity": original_entity
        })
        text = text[:start] + '[aadhar_num]' + text[end:]

    # CVV number
    cvvs = list(re.finditer(r'\b\d{3}\b', text))
    for match in reversed(cvvs):
        start, end = match.span()
        original_entity = text[start:end]
        masked_entities.append({
            "position": [start, end],
            "classification": "cvv_no",
            "entity": original_entity
        })
        text = text[:start] + '[cvv_no]' + text[end:]

    # Card expiry date
    expiries = list(re.finditer(r'\b(0[1-9]|1[0-2])\/?([0-9]{2}|[0-9]{4})\b', text))
    for match in reversed(expiries):
        start, end = match.span()
        original_entity = text[start:end]
        masked_entities.append({
            "position": [start, end],
            "classification": "expiry_no",
            "entity": original_entity
        })
        text = text[:start] + '[expiry_no]' + text[end:]

    return text, masked_entities

def mask_pii(text: str, ner_pipeline) -> Tuple[str, List[Dict]]:
    """
    Mask all PII in text using both NER and regex patterns.
    
    Args:
        text (str): Input text
        ner_pipeline: NER pipeline for name detection
        
    Returns:
        Tuple[str, List[Dict]]: Masked text and list of all masked entities
    """
    text, ner_entities = mask_full_name(text, ner_pipeline)
    text, regex_entities = mask_with_regex(text)
    return text, ner_entities + regex_entities 