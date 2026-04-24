"""
Tests for PathPilot RAG System modules.
"""
import pytest
import json
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.ingestion import DataIngestion, Document
from utils.json_parser import try_parse_json, validate_json_structure


class TestDataIngestion:
    """Test data ingestion module."""
    
    def test_load_careers(self):
        """Test loading career dataset."""
        ingestion = DataIngestion()
        careers = ingestion.load_json("careers.json")
        assert isinstance(careers, list)
        assert len(careers) > 0
        assert "title" in careers[0]
    
    def test_load_startups(self):
        """Test loading startup dataset."""
        ingestion = DataIngestion()
        startups = ingestion.load_json("startups.json")
        assert isinstance(startups, list)
        assert len(startups) > 0
        assert "title" in startups[0]
    
    def test_load_financial_data(self):
        """Test loading financial dataset."""
        ingestion = DataIngestion()
        financial = ingestion.load_json("financial_data.json")
        assert isinstance(financial, dict)
        assert "stocks" in financial
        assert len(financial["stocks"]) > 0
    
    def test_chunk_careers(self):
        """Test career chunking."""
        ingestion = DataIngestion()
        careers = ingestion.load_json("careers.json")
        documents = ingestion.chunk_careers(careers)
        
        assert len(documents) > len(careers)  # Multiple chunks per career
        assert all(isinstance(doc, Document) for doc in documents)
        assert all(hasattr(doc, "text") for doc in documents)
        assert all(hasattr(doc, "metadata") for doc in documents)
    
    def test_document_metadata(self):
        """Test document metadata structure."""
        ingestion = DataIngestion()
        careers = ingestion.load_json("careers.json")
        documents = ingestion.chunk_careers(careers)
        
        first_doc = documents[0]
        assert "type" in first_doc.metadata
        assert "chunk_type" in first_doc.metadata
        assert "title" in first_doc.metadata


class TestJSONParser:
    """Test JSON parsing utilities."""
    
    def test_parse_valid_json(self):
        """Test parsing valid JSON."""
        valid_json = '{"key": "value", "number": 42}'
        result = try_parse_json(valid_json)
        assert result is not None
        assert result["key"] == "value"
        assert result["number"] == 42
    
    def test_parse_json_with_markdown(self):
        """Test parsing JSON from markdown."""
        markdown_json = '```json\n{"key": "value"}\n```'
        result = try_parse_json(markdown_json)
        assert result is not None
        assert result["key"] == "value"
    
    def test_parse_json_object_in_text(self):
        """Test extracting JSON object from text."""
        text_with_json = 'Here is the result: {"name": "test", "score": 95}. Hope it helps!'
        result = try_parse_json(text_with_json)
        assert result is not None
        assert result["name"] == "test"
    
    def test_parse_invalid_json(self):
        """Test handling invalid JSON."""
        invalid_json = "This is not JSON at all"
        result = try_parse_json(invalid_json)
        assert result is None
    
    def test_validate_json_structure(self):
        """Test JSON structure validation."""
        data = {"recommendations": [], "status": "success"}
        assert validate_json_structure(data, ["recommendations"]) is True
        assert validate_json_structure(data, ["recommendations", "status"]) is True
        assert validate_json_structure(data, ["recommendations", "missing"]) is False


class TestDocumentStructure:
    """Test document structure and serialization."""
    
    def test_document_creation(self):
        """Test creating a document."""
        doc = Document(
            text="Test document content",
            metadata={"type": "test", "id": "1"}
        )
        assert doc.text == "Test document content"
        assert doc.metadata["type"] == "test"
    
    def test_document_to_dict(self):
        """Test document serialization."""
        doc = Document(
            text="Test content",
            metadata={"key": "value"}
        )
        doc_dict = doc.to_dict()
        assert "text" in doc_dict
        assert "metadata" in doc_dict
        assert doc_dict["text"] == "Test content"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
