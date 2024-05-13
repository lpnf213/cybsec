import re

class RegexParser:

    @staticmethod
    def findall(pattern: str, string: str, replace_expression: list = []):
        result: list = []
        found_strings: list = re.findall(pattern, str(string))
        for string_val in found_strings:
            for replace in replace_expression:
                string_val = string_val.replace(replace[0], replace[1])
            string_val.replace("b'", "")
            if len(string_val) > 0:
                result.append(string_val)
        return result
