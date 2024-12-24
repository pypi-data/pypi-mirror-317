from dataclasses import dataclass, field
from typing import Optional
import os
import requests

@dataclass
class Part:
    binary_content: Optional[bytes]
    text_content: Optional[str]
    
    @staticmethod
    def parse_part(part: str):
        if part.startswith('http://') or part.startswith('https://'):
            response = requests.get(part)
            return Part(binary_content=None, text_content=response.text)
        elif os.path.isfile(part):
            with open(part, 'rb') as file:
                return Part(binary_content=file.read(), text_content=None)
        else:
            return Part(binary_content=None, text_content=part)
    
    def draw_box(self, box):
        # assume binary_content is image
        pass
