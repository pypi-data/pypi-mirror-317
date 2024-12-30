from pathlib import Path
import re
from typing import Optional, TypeVar
from pydantic import BaseModel, Field, ConfigDict, computed_field
from abc import ABC, abstractmethod
import numpy as np
import yaml
import hashlib

from yaml import YAMLObject, Dumper

class BugFixDumper(Dumper):
    def represent_str(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    
class Document(BaseModel):
    text: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
    vectors: dict[str, list[float]] = Field(default_factory=dict, alias='_vectors')
    token_count: Optional[int] = Field(default=None)
    source: Optional[str] = Field(default=None)
    
    model_config = ConfigDict(
        populate_by_name=True,  # Allows both alias and original name to work
        exclude_none=True,      # Don't include None values in serialization
        json_by_alias=True      # Always use aliases in JSON serialization
    )

    @property
    def content(self) -> Optional[str]:
        """Returns the text value"""
        return self.text
    
    @computed_field
    def hash(self) -> Optional[str]:
        """Returns MD5 hash of the text"""
        if self.text is None:
            return None
        return hashlib.md5(self.text.encode('utf-8')).hexdigest()
    
    def with_vector(self, embedder_name: str | None, vector: list[float] | np.ndarray | None):
        """Add a vector to the document
        
        Args:
            embedder_name: Name of the embedder used to generate the vector
            vector: Vector to add, can be list of floats or numpy array
        """
        if embedder_name is None or vector is None:
            return self
        
        if isinstance(vector, np.ndarray):
            vector = vector.tolist()
        self.vectors[embedder_name] = vector
        return self

   
    def save_to_yaml(self, path: Path) -> Path:
        """Save document to a YAML file"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            yaml.dump(
                self.model_dump(by_alias=True),
                f,
                sort_keys=False,
                allow_unicode=True,
                default_flow_style=False,
                Dumper=BugFixDumper
            )
        return path

    
IDocument = TypeVar('IDocument', bound=Document)  # Document type that must inherit from Document class

class ArticleDocument(Document):

    """Represents a document or document fragment with its metadata"""
    title: str | None
    abstract: str | None
    fragment_num: int
    total_fragments: int

    @computed_field
    def content(self) -> Optional[str]:
       return self.to_formatted_string()
    
        
    @computed_field
    def hash(self) -> Optional[str]:
        """Returns MD5 hash of the text"""
        if self.text is None:
            return None
        return hashlib.md5(self.to_formatted_string().encode('utf-8')).hexdigest()
   
    

    def to_formatted_string(self, mention_splits: bool = True) -> str:
        """
        Convert the document to a formatted string representation.
        
        Args:
            mention_splits: Whether to include fragment information
        
        Returns:
            Formatted string with metadata and content
        """
        parts = []
        
        if self.title:
            parts.append(f"TITLE: {self.title}\n")
        if self.abstract:
            parts.append(f"ABSTRACT: {self.abstract}\n")
            
        has_multiple_fragments = self.total_fragments > 1
        if has_multiple_fragments:
            parts.append("TEXT_FRAGMENT: ")
        
        parts.append(self.text)
        
        parts.append(f"\n\nSOURCE: {self.source}")
        if mention_splits and has_multiple_fragments:
            parts.append(f"\tFRAGMENT: {self.fragment_num}/{self.total_fragments}")
        
        parts.append("\n")
        
        return "\n".join(parts)
    

    @staticmethod
    def calculate_adjusted_chunk_size(
        tokenizer,
        max_chunk_size: int,
        title: str | None = None,
        abstract: str | None = None,
        source: str | None = None
    ) -> int:
        """
        Calculate the adjusted chunk size accounting for metadata tokens.
        
        Args:
            tokenizer: The tokenizer to use for token counting
            max_chunk_size: Original maximum chunk size
            title: Optional title text
            abstract: Optional abstract text
            source: Optional source identifier
            
        Returns:
            Adjusted maximum chunk size accounting for metadata
        """
        # Build sample metadata text
        metadata_text = ""
        if title:
            metadata_text += f"TITLE: {title}\n"
        if abstract:
            metadata_text += f"ABSTRACT: {abstract}\n"
        if source:
            metadata_text += f"\n\nSOURCE: {source}"
        metadata_text += "\tFRAGMENT: 999/999\n"  # Account for worst-case fragment notation
        
        # Calculate tokens for metadata
        metadata_tokens = len(tokenizer.tokenize(metadata_text))
        
        # Return adjusted size
        return max_chunk_size - metadata_tokens