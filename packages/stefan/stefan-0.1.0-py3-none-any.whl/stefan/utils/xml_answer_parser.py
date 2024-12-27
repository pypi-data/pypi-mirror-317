import xml.etree.ElementTree as ET
from typing import Dict, Any
from pydantic import BaseModel
import re

class XMLAnswer(BaseModel):
    xml_text: str
    answer_dict: Dict[str, Any]

class XMLAnswerParser:
    # Add these as class constants
    CDATA_WRAP_ATTRIBUTES = {'old_text', 'new_text', 'content'}

    @staticmethod
    def parse_answer_xml(text: str) -> XMLAnswer:
        try:
            return XMLAnswerParser._parse_answer_xml(text)
        except ValueError as e:
            raise ValueError(f"Answer XML parsing failed with error:\n\n{str(e)}\n\nfor value:\n\n{text}")

    @staticmethod
    def _parse_answer_xml(text: str) -> XMLAnswer:
        """
        Parse XML answer from LLM response, ensuring it's properly formatted and at the end of the message.
        
        Args:
            text: Full text response from LLM containing XML answer
            
        Returns:
            Dictionary containing parsed XML attributes
            
        Raises:
            ValueError: If answer tag is missing, multiple answers found, or answer is not at the end
        """
        # Find the last occurrence of <answer>
        answer_start = text.rfind("<answer>")
        if answer_start == -1:
            raise ValueError(f"No answer tag found in response: {text}")
            
        # Check there's only one answer tag
        if text.count("<answer>") > 1:
            raise ValueError(f"Multiple answer tags found in response: {text}")
            
        # Extract the XML part
        xml_text = text[answer_start:]
        
        # Check if there's any non-whitespace content after the closing tag
        end_tag = "</answer>"
        end_tag_pos = xml_text.rfind(end_tag)
        if end_tag_pos == -1 or xml_text[end_tag_pos + len(end_tag):].strip():
            raise ValueError(f"Answer must be at the end of the response: {text}")

        # Wrap specified attributes with CDATA before escaping
        xml_text = XMLAnswerParser._wrap_attributes_with_cdata(xml_text)
        
        # Preprocess the XML to escape special characters
        sanitized_xml = XMLAnswerParser._escape_xml_characters(xml_text)
        
        try:
            # Parse XML
            root = ET.fromstring(sanitized_xml)
            if root.tag != "answer":
                raise ValueError(f"Root element must be 'answer': {text}")
                
            def parse_element(element: ET.Element) -> Dict[str, Any]:
                result = {}
                child_counts = {}
                
                for child in element:
                    child_counts[child.tag] = child_counts.get(child.tag, 0) + 1
                    
                for child in element:
                    # Unescape the text content
                    text_content = XMLAnswerParser._unescape_xml_characters(child.text.strip() if child.text else "")
                    
                    if child_counts[child.tag] > 1:
                        if child.tag not in result:
                            result[child.tag] = []
                        if len(child) > 0:
                            result[child.tag].append(parse_element(child))
                        else:
                            result[child.tag].append(text_content)
                    else:
                        if len(child) > 0:
                            result[child.tag] = parse_element(child)
                        else:
                            result[child.tag] = text_content
                return result
                
            return XMLAnswer(xml_text=sanitized_xml, answer_dict=parse_element(root))
            
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format: {str(e)} for value: {text}")

    @staticmethod
    def _wrap_attributes_with_cdata(xml: str) -> str:
        """
        Wrap specified attributes content with CDATA sections.
        """
        for attr in XMLAnswerParser.CDATA_WRAP_ATTRIBUTES:
            pattern = f"<{attr}>(.*?)</{attr}>"
            
            def wrap_with_cdata(match):
                content = match.group(1)
                if not content.startswith('<![CDATA['):
                    return f"<{attr}><![CDATA[{content}]]></{attr}>"
                return match.group(0)
            
            xml = re.sub(pattern, wrap_with_cdata, xml, flags=re.DOTALL)
        
        return xml

    @staticmethod
    def _escape_xml_characters(xml: str) -> str:
        """
        Escape special XML characters within text nodes while preserving CDATA sections.
        """
        # First, temporarily replace CDATA sections with a placeholder
        cdata_sections = []
        
        def save_cdata(match):
            cdata_sections.append(match.group(1))
            return f"___CDATA_PLACEHOLDER_{len(cdata_sections)-1}___"
        
        xml = re.sub(r'<!\[CDATA\[(.*?)\]\]>', save_cdata, xml, flags=re.DOTALL)
        
        # Escape special characters
        escaped_text = (
            xml.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )
        
        # Restore XML tags
        pattern = re.compile(r"&lt;(\/?)([a-zA-Z][a-zA-Z0-9_\-\.]*)((?:\s+[a-zA-Z][a-zA-Z0-9_\-\.]*=\"[^\"]*\")*)\s*&gt;")
        escaped_text = pattern.sub(r"<\1\2\3>", escaped_text)
        
        # Restore CDATA sections
        for i, cdata in enumerate(cdata_sections):
            escaped_text = escaped_text.replace(
                f"___CDATA_PLACEHOLDER_{i}___",
                f"<![CDATA[{cdata}]]>"
            )
        
        return escaped_text
        
    @staticmethod
    def _unescape_xml_characters(text: str) -> str:
        """
        Unescape XML special characters in text.
        
        Args:
            text: The text containing escaped XML characters
            
        Returns:
            Text with XML special characters unescaped
        """
        return (
            text.replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", '"')
            .replace("&apos;", "'")
        )