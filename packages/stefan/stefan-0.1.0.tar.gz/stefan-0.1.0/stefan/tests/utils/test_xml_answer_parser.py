import pytest
from stefan.utils.xml_answer_parser import XMLAnswerParser

def test_parse_simple_answer():
    xml = """Some LLM thinking...
    <answer>
    <reasoning>Not very relevant function</reasoning>
    <score>0.3</score>
    <is_relevant>false</is_relevant>
    </answer>"""
    
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "reasoning": "Not very relevant function",
        "score": "0.3",
        "is_relevant": "false"
    }
    assert result.xml_text.strip() == """<answer>
    <reasoning>Not very relevant function</reasoning>
    <score>0.3</score>
    <is_relevant>false</is_relevant>
    </answer>""".strip()

def test_parse_nested_answer():
    xml = """<answer>
    <metadata>
        <timestamp>2024-03-20</timestamp>
        <version>1.0</version>
    </metadata>
    <result>
        <score>0.8</score>
        <confidence>high</confidence>
    </result>
    </answer>"""
    
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "metadata": {
            "timestamp": "2024-03-20",
            "version": "1.0"
        },
        "result": {
            "score": "0.8",
            "confidence": "high"
        }
    }

def test_answer_with_empty_values():
    xml = """<answer>
    <reasoning></reasoning>
    <score></score>
    </answer>"""
    
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "reasoning": "",
        "score": ""
    }

def test_answer_must_be_at_end():
    xml = """<answer>
    <score>0.8</score>
    </answer>
    Some text after"""
    
    with pytest.raises(ValueError, match="Answer must be at the end of the response"):
        XMLAnswerParser.parse_answer_xml(xml)

def test_parse_repeated_elements():
    xml = """<answer>
    <file>file1.txt</file>
    <file>file2.txt</file>
    <other>single value</other>
    </answer>"""
    
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "file": ["file1.txt", "file2.txt"],
        "other": "single value"
    }

def test_content_contains_invalid_xml_characters():
    xml = """
    <answer>
    <write_to_file>
    <file_path>calculator.py</file_path>
    <content>
    while i < len(tokens): & < > \" '
    </content>
    </write_to_file>
    </answer>
    """
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "write_to_file": {
            "file_path": "calculator.py",
            "content": "while i < len(tokens): & < > \" '",
        }
    }

def test_content_contains_xml_like_tags():
    xml = """
    <answer>
    <attempt_completion>
    <response>
    - Extends UseCase<LoginUseCase.Args, SignedInRedirect>
    </response>
    </attempt_completion>
    </answer>
    """
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "attempt_completion": {
            "response": "- Extends UseCase<LoginUseCase.Args, SignedInRedirect>"
        }
    }

def test_content_contains_xml_content():
    xml = """
    <answer>
    <create_file>
    <file_path>shared/resources/src/commonMain/moko-resources/base/strings.xml</file_path>
    <content><?xml version="1.0" encoding="utf-8"?>
    <resources>
        <!-- Previous content remains unchanged -->
        <!-- Profile -->
        <string name="profile_test_notification_button">Odeslat testovací notifikaci</string>
        <!-- Rest of the content remains unchanged -->
    </resources></content>
    </create_file>
    </answer>
    """

    expected_content = """<?xml version="1.0" encoding="utf-8"?>
    <resources>
        <!-- Previous content remains unchanged -->
        <!-- Profile -->
        <string name="profile_test_notification_button">Odeslat testovací notifikaci</string>
        <!-- Rest of the content remains unchanged -->
    </resources>"""

    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "create_file": {
            "file_path": "shared/resources/src/commonMain/moko-resources/base/strings.xml",
            "content": expected_content,
        }
    }

def test_content_contains_cdata():
    xml = """
    <answer>
    <content><![CDATA[Some text with & < > \" ' characters]]></content>
    </answer>
    """
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "content": "Some text with & < > \" ' characters",
    }

def test_multiple_answers_raises_error():
    xml = """<answer>first</answer>
    Some text
    <answer>second</answer>"""
    
    with pytest.raises(ValueError, match="Multiple answer tags found in response"):
        XMLAnswerParser.parse_answer_xml(xml)

def test_missing_answer_raises_error():
    xml = "Some text without answer tags"
    
    with pytest.raises(ValueError, match="No answer tag found in response"):
        XMLAnswerParser.parse_answer_xml(xml)

def test_invalid_xml_raises_error():
    xml = "<answer><invalid></answer>"
    
    with pytest.raises(ValueError, match="Invalid XML format"):
        XMLAnswerParser.parse_answer_xml(xml)

def test_empty_content():
    xml = "<answer><content></content></answer>"
    result = XMLAnswerParser.parse_answer_xml(xml)
    assert result.answer_dict == {
        "content": "",
    }
