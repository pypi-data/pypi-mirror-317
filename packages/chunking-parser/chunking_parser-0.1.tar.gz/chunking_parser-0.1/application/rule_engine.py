from dataclasses import dataclass
import re
import typing as tp


@dataclass
class ClauseBreakPointRules:
    period = r"[.]\s*$"  # .
    semicolon = r"[\u037e\;]\s+$"  # ;
    colon = r":\s*$"  # :
    start_double_quotes = r"^\s*”"
    end_double_quotes = r"“\s*$"
    semicolonand = r";\s*and$"  # ; and
    semicolonor = r";\s*or$"  # :
    integers_regex = r"^\d+\s+"  # 1, 2, 3
    integers_with_period_regex = r"^\d+\.\s*"  # 1., 2., 3., 4.
    integers_with_braces_regex = r"^\(\d+\)\s+"  # (1), (2), (3)
    decimal_numbers_regex = r"^\d+\.\d+\s*"  # 1.2, 3.4, 3.2
    decimal_numbers_with_period_regex = r"^\d+\.\d+\.\s*"  # 1.2., 1.3.
    two_points_numbers_regex = r"^\d+\.\d+\.\d+\s*"  # 1.2.1, 2.4.5, 5.6.3
    three_points_numbers_regex = r"^\d+\.\d+\.\d+\.\d+\s*"  # 1.2.1.3
    two_points_numbers_with_period_regex = r"^\d+\.\d+\.\d+\.\s*"  # 1.2.1., 1.2.3.
    three_points_numbers_with_period_regex = r"^\d+\.\d+\.\d+\.\d+\.\s*"  # 1.2.1.1.,
    roman_numbers_regex = r"^[ivxlcdmIVXLCDM]+(?=\s+)"  # i, ii, iii, iv
    roman_numbers_in_braces_regex = r"^\([ivxlcdmIVXLCDM]+\)(?=\s+)"  # (i), (ii), (iii)
    alphabets_regex = r"^[a-zA-Z](?=\s+)"  # a, b, c
    alphabets_with_period_regex = r"^[a-z]\.(?=\s*)"  # a., b. c.
    uppercase_alphabets_with_period_regex = r"^[A-Z]\.(?=\s*)"  # A., B., C.
    alphabets_in_braces_regex = r"^\([a-z]\)\s*"  # (a), (b), (c)
    uppdercase_alphabets_in_braces_regex = r"^\([A-Z]\)\s*"  # (A), (B), (C)
    alphabets_with_ending_braces_regex = r"^[a-z]\)\s+"  # a), b), c)
    uppercase_alphabets_with_ending_braces_regex = r"^[A-Z]\)\s+"  # A), B), C)
    roman_values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    @staticmethod
    def check_decimal_numbers_with_period_as_starting_char(
        line: str,
    ) -> tp.Tuple[str, str]:
        two_point_no, two_point_regex = (
            ClauseBreakPointRules.check_two_points_numbers_with_period(line)
        )
        decimal_with_period, decimal_with_period_regex = (
            ClauseBreakPointRules.check_decimal_numbers_with_period(line)
        )
        integers_with_period, integer_regex = ClauseBreakPointRules.check_integers_with_period(line)
        decimal_numbers, decimal_regex = ClauseBreakPointRules.check_decimal_numbers(
            line
        )
        # if decimal_with_period and not two_point_no:
        #     return decimal_with_period, decimal_regex
        if integers_with_period and not decimal_with_period and not decimal_numbers:
            return integers_with_period, integer_regex
        return None, None

    @staticmethod
    def check_starting_char(line: str) -> tp.Tuple[str, str]:
        roman_number_in_braces, regex = (
            ClauseBreakPointRules.check_roman_numbers_in_braces(line)
        )
        if roman_number_in_braces:
            return roman_number_in_braces, regex
        roman_number, regex = ClauseBreakPointRules.check_roman_numbers(line)
        if roman_number:
            return roman_number, regex
        integers_with_braces, regex = ClauseBreakPointRules.check_integers_with_braces(
            line
        )
        if integers_with_braces:
            return integers_with_braces, regex
        three_points_number_with_period, regex = (
            ClauseBreakPointRules.check_three_points_numbers_with_period(line)
        )
        if three_points_number_with_period:
            return three_points_number_with_period, regex
        three_points_number, regex = ClauseBreakPointRules.check_three_points_numbers(
            line
        )
        if three_points_number:
            return three_points_number, regex
        two_points_numbers_with_period, regex = (
            ClauseBreakPointRules.check_two_points_numbers_with_period(line)
        )
        if two_points_numbers_with_period:
            return two_points_numbers_with_period, regex
        two_points_numbers, regex = ClauseBreakPointRules.check_two_points_numbers(line)
        if two_points_numbers:
            return two_points_numbers, regex
        decimal_numbers_with_period, regex = (
            ClauseBreakPointRules.check_decimal_numbers_with_period(line)
        )
        if decimal_numbers_with_period:
            return decimal_numbers_with_period, regex
        decimal_numbers, regex = ClauseBreakPointRules.check_decimal_numbers(line)
        if decimal_numbers:
            return decimal_numbers, regex
        integers_with_period, regex = ClauseBreakPointRules.check_integers_with_period(
            line
        )
        if integers_with_period:
            return integers_with_period, regex
        integers, regex = ClauseBreakPointRules.check_integers(line)
        if integers:
            return integers, regex
        alphabets_with_period, regex = (
            ClauseBreakPointRules.check_alphabets_with_period(line)
        )
        if alphabets_with_period:
            return alphabets_with_period, regex
        uppercase_alphabets_with_period, regex = (
            ClauseBreakPointRules.check_uppercase_alphabets_with_period(line)
        )
        if uppercase_alphabets_with_period:
            return uppercase_alphabets_with_period, regex
        alphabets_in_braces, regex = ClauseBreakPointRules.check_alphabets_in_braces(
            line
        )
        if alphabets_in_braces:
            return alphabets_in_braces, regex
        uppercase_alphabets_in_braces, regex = (
            ClauseBreakPointRules.check_uppercase_alphabets_in_braces(line)
        )
        if uppercase_alphabets_in_braces:
            return uppercase_alphabets_in_braces, regex
        alphabets_with_ending_brace, regex = (
            ClauseBreakPointRules.check_alphabets_with_ending_brace(line)
        )
        if alphabets_with_ending_brace:
            return alphabets_with_ending_brace, regex
        uppercase_alphabets_with_ending_brace, regex = (
            ClauseBreakPointRules.check_uppercase_alphabets_with_ending_brace(line)
        )
        if uppercase_alphabets_with_ending_brace:
            return uppercase_alphabets_with_ending_brace, regex

        return None, None

    @staticmethod
    def remove_extra_puncuations(char: str) -> str:
        output_char = re.sub(r"[()]", "", char.strip())
        output_char = re.sub(r"\.$", "", output_char)
        return output_char

    @staticmethod
    def get_regex_corresponding_int_value(
        regex: re, start_char: str, end_char: str
    ) -> int:
        output_end_char = ClauseBreakPointRules.remove_extra_puncuations(end_char)
        output_start_char = None
        if start_char:
            output_start_char = ClauseBreakPointRules.remove_extra_puncuations(
                start_char
            )
        if regex in [
            ClauseBreakPointRules.roman_numbers_in_braces_regex,
            ClauseBreakPointRules.roman_numbers_regex,
        ]:
            return (
                ClauseBreakPointRules.roman_to_int(output_end_char)
                - ClauseBreakPointRules.roman_to_int(
                    "i" if not output_start_char else output_start_char
                )
                + (1 if not output_start_char else 0)
            )
        if regex in [
            ClauseBreakPointRules.alphabets_in_braces_regex,
            ClauseBreakPointRules.alphabets_with_ending_braces_regex,
            ClauseBreakPointRules.alphabets_with_period_regex,
        ]:
            return (
                1
                if output_end_char == "a"
                else ord(output_end_char)
                - ord("a" if not output_start_char else output_start_char)
            )
        if regex in [
            ClauseBreakPointRules.uppdercase_alphabets_in_braces_regex,
            ClauseBreakPointRules.uppercase_alphabets_with_ending_braces_regex,
            ClauseBreakPointRules.uppercase_alphabets_with_period_regex,
        ]:
            return (
                1
                if output_end_char == "A"
                else ord(output_end_char)
                - ord("A" if not output_start_char else output_start_char)
            )
        if regex in [
            ClauseBreakPointRules.integers_with_braces_regex,
            ClauseBreakPointRules.integers_with_period_regex,
        ]:
            return (
                int(output_end_char)
                if not output_start_char
                else int(output_end_char) - int(output_start_char)
            )
        return 1

    @staticmethod
    def check_period(line: str) -> bool:
        return re.search(ClauseBreakPointRules.period, line) is not None

    @staticmethod
    def check_start_double_quotes(line: str) -> bool:
        return re.search(ClauseBreakPointRules.start_double_quotes, line) is not None

    @staticmethod
    def check_end_double_quotes(line: str) -> bool:
        return re.search(ClauseBreakPointRules.end_double_quotes, line) is not None

    @staticmethod
    def check_semicolon(line: str) -> str:
        value = re.match(ClauseBreakPointRules.semicolon, line)
        if value:
            return value.group(0)
        else:
            return None

    @staticmethod
    def check_colon(line: str) -> str:
        value = re.match(ClauseBreakPointRules.colon, line)
        if value:
            return value.group(0)
        else:
            return None

    @staticmethod
    def check_semicolonand(line: str) -> str:
        value = re.match(ClauseBreakPointRules.semicolonand, line)
        if value:
            return value.group(0)
        else:
            return None

    @staticmethod
    def check_semicolonor(line: str) -> str:
        value = re.match(ClauseBreakPointRules.semicolonor, line)
        if value:
            return value.group(0)
        else:
            return None

    @staticmethod
    def check_integers(line: str) -> tp.Tuple[str, str]:
        value = re.match(ClauseBreakPointRules.integers_regex, line)
        if value:
            return value.group(0), ClauseBreakPointRules.integers_regex
        else:
            return None, None

    @staticmethod
    def check_integers_with_period(line: str) -> tp.Tuple[str, str]:
        value = re.match(ClauseBreakPointRules.integers_with_period_regex, line)
        if value:
            return value.group(0), ClauseBreakPointRules.integers_with_period_regex
        else:
            return None, None

    @staticmethod
    def check_integers_with_braces(line: str) -> tp.Tuple[str, str]:
        value = re.match(ClauseBreakPointRules.integers_with_braces_regex, line)
        if value:
            return value.group(0), ClauseBreakPointRules.integers_with_braces_regex
        else:
            return None, None

    @staticmethod
    def check_decimal_numbers(line: str) -> tp.Tuple[str, str]:
        value = re.match(ClauseBreakPointRules.decimal_numbers_regex, line)
        if value:
            return value.group(0), ClauseBreakPointRules.decimal_numbers_regex
        else:
            return None, None

    @staticmethod
    def check_decimal_numbers_with_period(line: str) -> tp.Tuple[str, str]:
        value = re.match(ClauseBreakPointRules.decimal_numbers_with_period_regex, line)
        if value:
            return (
                value.group(0),
                ClauseBreakPointRules.decimal_numbers_with_period_regex,
            )
        else:
            return None, None

    @staticmethod
    def check_two_points_numbers(line: str) -> tp.Tuple[str, str]:
        value = re.match(ClauseBreakPointRules.two_points_numbers_regex, line)
        if value:
            return value.group(0), ClauseBreakPointRules.two_points_numbers_regex
        else:
            return None, None

    @staticmethod
    def check_three_points_numbers(line: str) -> tp.Tuple[str, str]:
        value = re.match(ClauseBreakPointRules.three_points_numbers_regex, line)
        if value:
            return value.group(0), ClauseBreakPointRules.three_points_numbers_regex
        else:
            return None, None

    @staticmethod
    def check_three_points_numbers_with_period(line: str) -> tp.Tuple[str, str]:
        value = re.match(
            ClauseBreakPointRules.three_points_numbers_with_period_regex, line
        )
        if value:
            return (
                value.group(0),
                ClauseBreakPointRules.three_points_numbers_with_period_regex,
            )
        else:
            return None, None

    @staticmethod
    def check_two_points_numbers_with_period(line: str) -> tp.Tuple[str, str]:
        value = re.match(
            ClauseBreakPointRules.two_points_numbers_with_period_regex, line
        )
        if value:
            return (
                value.group(0),
                ClauseBreakPointRules.two_points_numbers_with_period_regex,
            )
        else:
            return None, None

    @staticmethod
    def check_roman_numbers(line: str) -> tp.Tuple[str, str]:
        value = re.match(
            ClauseBreakPointRules.roman_numbers_regex, line, flags=re.IGNORECASE
        )
        if value:
            return value.group(0), ClauseBreakPointRules.roman_numbers_regex
        else:
            return None, None

    @staticmethod
    def check_roman_numbers_in_braces(line: str) -> tp.Tuple[str, str]:
        value = re.match(
            ClauseBreakPointRules.roman_numbers_in_braces_regex,
            line,
            flags=re.IGNORECASE,
        )
        if value:
            return value.group(0), ClauseBreakPointRules.roman_numbers_in_braces_regex
        else:
            return None, None

    @staticmethod
    def check_all_cases_for_alphabets(line: str) -> tp.Tuple[str, str]:
        alphabets_in_braces_value, alphabets_in_braces_regex = (
            ClauseBreakPointRules.check_alphabets_in_braces(line=line)
        )
        if alphabets_in_braces_value:
            return alphabets_in_braces_value, alphabets_in_braces_regex
        alphabets_with_ending_braces_value, alphabets_with_ending_braces_regex = (
            ClauseBreakPointRules.check_alphabets_with_ending_brace(line=line)
        )
        if alphabets_with_ending_braces_value:
            return (
                alphabets_with_ending_braces_value,
                alphabets_with_ending_braces_regex,
            )
        alphabets_with_period_value, alphabets_with_period_regex = (
            ClauseBreakPointRules.check_alphabets_with_period(line=line)
        )
        if alphabets_with_period_regex:
            return alphabets_with_period_value, alphabets_with_period_regex
        return None, None

    @staticmethod
    def check_alphabets(line: str) -> tp.Tuple[str, str]:
        value = re.match(ClauseBreakPointRules.alphabets_regex, line)
        if value:
            return value.group(0), ClauseBreakPointRules.alphabets_regex
        else:
            return None, None

    @staticmethod
    def check_alphabets_in_braces(line: str) -> tp.Tuple[str, str]:
        value = re.match(ClauseBreakPointRules.alphabets_in_braces_regex, line)
        if value:
            return value.group(0), ClauseBreakPointRules.alphabets_in_braces_regex
        else:
            return None, None

    @staticmethod
    def check_uppercase_alphabets_in_braces(line: str) -> tp.Tuple[str, str]:
        value = re.match(
            ClauseBreakPointRules.uppdercase_alphabets_in_braces_regex, line
        )
        if value:
            return (
                value.group(0),
                ClauseBreakPointRules.uppdercase_alphabets_in_braces_regex,
            )
        else:
            return None, None

    @staticmethod
    def check_alphabets_with_period(line: str) -> tp.Tuple[str, str]:
        value = re.match(ClauseBreakPointRules.alphabets_with_period_regex, line)
        if value:
            return value.group(0), ClauseBreakPointRules.alphabets_with_period_regex
        else:
            return None, None

    @staticmethod
    def check_uppercase_alphabets_with_period(line: str) -> tp.Tuple[str, str]:
        value = re.match(
            ClauseBreakPointRules.uppercase_alphabets_with_period_regex, line
        )
        if value:
            return (
                value.group(0),
                ClauseBreakPointRules.uppercase_alphabets_with_period_regex,
            )
        else:
            return None, None

    @staticmethod
    def check_alphabets_with_ending_brace(line: str) -> tp.Tuple[str, str]:
        value = re.match(ClauseBreakPointRules.alphabets_with_ending_braces_regex, line)
        if value:
            return (
                value.group(0),
                ClauseBreakPointRules.alphabets_with_ending_braces_regex,
            )
        else:
            return None, None

    @staticmethod
    def check_uppercase_alphabets_with_ending_brace(line: str) -> tp.Tuple[str, str]:
        value = re.match(
            ClauseBreakPointRules.uppercase_alphabets_with_ending_braces_regex, line
        )
        if value:
            return (
                value.group(0),
                ClauseBreakPointRules.uppercase_alphabets_with_ending_braces_regex,
            )
        else:
            return None, None

    @staticmethod
    def break_on_period(line: str) -> tp.List[str]:
        return re.split(ClauseBreakPointRules.period, line)

    @staticmethod
    def break_on_semicolon(line: str) -> tp.List[str]:
        return re.split(ClauseBreakPointRules.semicolon, line)

    @staticmethod
    def break_on_semicolonand(line: str) -> tp.List[str]:
        return re.split(ClauseBreakPointRules.semicolonand, line)

    @staticmethod
    def check_condition_for_eol(line: str) -> bool:
        if re.search(r"^(\d+\.|\d+\.\d+\.|[a-zA-Z]\.\s*)", line) is not None:
            return False
        pattern = r"(?:[\u037e;:]|(?:[\u037e;]\s*(?:and|or)))\s*$"
        return re.search(pattern, line) is not None

    @staticmethod
    def roman_to_int(roman: str) -> int:

        total = 0
        prev_value = 0
        for char in reversed(roman.upper()):
            value = ClauseBreakPointRules.roman_values[char]
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value
        return total
