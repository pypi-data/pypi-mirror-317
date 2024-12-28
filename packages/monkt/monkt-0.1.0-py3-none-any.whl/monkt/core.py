from pathlib import Path
from typing import Literal, Union

def convert(
    file_path: Union[str, Path],
    output_format: Literal["markdown", "json"] = "markdown",
) -> str:
    """
    Convert a document to markdown or JSON format.
    
    Args:
        file_path: Path to the input document
        output_format: Desired output format ("markdown" or "json")
        
    Returns:
        str: Converted document content
    """
    raise NotImplementedError("Conversion not yet implemented")
