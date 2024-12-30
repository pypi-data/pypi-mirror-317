import ast
import json
import re
from typing import Union

from llmabstractions.exceptions import ParsingError


def json_data_parser(llm_output: Union[str, dict, list]) -> dict:
    """
    Extracts dictionary or array content from an LLM response.

    There are cases where you ask from the LLMs to return an array
    or a dictionary, but you don't get a structured output.
    You can either relay on models supporting structured output,
    or parse the output yourself using this function.

    Parameters
    ----------
    llm_output: str, dict, list
        Raw LLM response. Expected as string. However, if a dictionary
        or list is passed, the same content will be returned as long as
        they can be JSON serialized.

    Returns
    -------
    dict or list:
        A dictionary or list content in the message.

    Raises
    ------
    ParsingError:
        If for any reason, the content cannot be extracted from the response.

    Examples
    --------
    Extract a dictionary embedded in text:

    >>> llm_response = '''
    ... Here is the response
    ...
    ... {
    ...     "key1": "value1",
    ...     "key2": "value2"
    ... }
    ...
    ... Is there something else?
    ... '''
    >>> json_data_parser(llm_response)
    {'key1': 'value1', 'key2': 'value2'}
    """
    parsed_response = None
    if isinstance(llm_output, dict) or isinstance(llm_output, list):
        parsed_response = json.loads(json.dumps(llm_output), strict=False)
    else:
        try:
            # case where the llm output is a JSON sting
            parsed_response = json.loads(llm_output, strict=False)
        except json.JSONDecodeError:
            # case where you have a code snippet
            if "```" in llm_output:
                pattern = r"```(?:\w+)?\n(.*?)\n```"
                matches = re.findall(pattern, llm_output, re.DOTALL)
                if len(matches) > 0:
                    parsed_response = json.loads(matches[0]) if matches else None
            else:
                # finally, if is a dictionary inside the text
                parsed_response = _extract_dict_or_array_from_text(llm_output)

    if parsed_response is None:
        raise ParsingError('Unable to parse LLM output.')

    return parsed_response


def _extract_dict_or_array_from_text(text: str) -> Union[dict, list, None]:
    """
    Extracts the dictionary present in the given text.
    """
    try:
        start_bracket = text.find('{')
        end_bracket = text.rfind('}')
        start_curly_bracket = text.find('[')
        end_curly_bracket = text.rfind(']')

        if start_bracket >= 0 and start_curly_bracket >= 0:
            if start_bracket < start_curly_bracket:
                start = start_bracket
            else:
                start = start_curly_bracket
        elif start_bracket >= 0:
            start = start_bracket
        elif start_curly_bracket >= 0:
            start = start_curly_bracket
        else:
            start = -1

        if end_bracket > 0 and end_curly_bracket > 0:
            if end_bracket > end_curly_bracket:
                end = end_bracket
            else:
                end = end_curly_bracket
        elif end_bracket > 0:
            end = end_bracket
        elif end_curly_bracket > 0:
            end = end_curly_bracket
        else:
            end = -1

        if start != -1 and end != -1:
            dict_or_array_str = text[start:end+1]
            return ast.literal_eval(dict_or_array_str)
    except (ValueError, SyntaxError):
        pass

    return None
