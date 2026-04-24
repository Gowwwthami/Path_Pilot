"""
Robust JSON parsing utilities for PathPilot RAG System.
Handles messy LLM outputs and extracts valid JSON.
"""
import json
import re
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def try_parse_json(text: str) -> Optional[Any]:
    """
    Attempt to parse JSON from potentially messy LLM output.
    
    Args:
        text: Raw text that may contain JSON
        
    Returns:
        Parsed JSON object or None if parsing fails
    """
    text = text.strip()
    
    # Try direct parsing first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON object in text
    try:
        # Match JSON object
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
    except Exception as e:
        logger.warning(f"Failed to parse JSON object: {e}")
    
    # Try to find JSON array in text
    try:
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
    except Exception as e:
        logger.warning(f"Failed to parse JSON array: {e}")
    
    # Try to fix common JSON issues
    try:
        # Remove trailing commas
        fixed_text = re.sub(r',\s*([}\]])', r'\1', text)
        return json.loads(fixed_text)
    except Exception as e:
        logger.warning(f"Failed to fix and parse JSON: {e}")
    
    logger.error("All JSON parsing attempts failed")
    return None


def extract_json_from_markdown(text: str) -> Optional[str]:
    """
    Extract JSON from markdown code blocks.
    
    Args:
        text: Text that may contain markdown code blocks with JSON
        
    Returns:
        Extracted JSON string or None
    """
    # Try to find JSON in code blocks
    pattern = r'```(?:json)?\s*\n(.*?)\n```'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    return None


def validate_json_structure(data: Any, required_keys: list) -> bool:
    """
    Validate that JSON has required keys.
    
    Args:
        data: Parsed JSON object
        required_keys: List of required top-level keys
        
    Returns:
        True if all required keys are present
    """
    if not isinstance(data, dict):
        return False
    
    return all(key in data for key in required_keys)
