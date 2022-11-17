from abc import ABC, abstractmethod
from typing import NamedTuple


class Number(NamedTuple):
    amount: int

    def is_negative(self):
        return str(self.amount).startswith("-")

    def abs_amount_str(self):
        abs_amount = abs(self.amount)
        return str(abs_amount)

    def number_of_periods(self):
        size = len(str(self.amount))
        if size % 3 == 0:
            return size // 3
        return (size // 3) + 1


class BaseWordsConverter(ABC):
    @abstractmethod
    def convert(self, number):
        pass


class EnglishWordsConverter(BaseWordsConverter):
    one_digit = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    two_digits = [
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
    ]
    tens_multiples = [
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
        "hundred",
    ]
    place_value = ["", "thousand", "million", "billion"]

    MAX_SIZE = 12

    def _get_hundreds_words(self, h_digit):
        words = ""

        if h_digit == 0:
            words += ""
        else:
            words += self.one_digit[h_digit]

        if not words == "":
            words += " hundred "
        else:
            words += ""

        return words

    def _get_tens_words(self, t_digit, o_digit):
        words = ""

        if t_digit == 0:
            words += self.one_digit[o_digit]
        elif t_digit == 1:
            words += self.two_digits[o_digit]
        elif t_digit > 1 and o_digit == 0:
            words += self.tens_multiples[t_digit - 2]
        elif t_digit > 1:
            words += self.tens_multiples[t_digit - 2] + " " + self.one_digit[o_digit]

        return words

    def process_period(self, period, index):
        if period == "0":
            return self.one_digit[0]

        number = period.zfill(3)
        h_digit, t_digit, o_digit = map(int, number)

        words = self._get_hundreds_words(h_digit)
        words += self._get_tens_words(t_digit, o_digit)

        words = "" if words == "zero" else words + " "

        if not len(words) == 0:
            words += self.place_value[index]

        return words

    def convert(self, amount):
        number = Number(amount)
        str_number = number.abs_amount_str()

        size = len(str_number)
        if size > self.MAX_SIZE:
            raise ValueError(
                f"Ensure the number has a size less than or equal to {str(self.MAX_SIZE)}."
            )

        count = number.number_of_periods()

        aux = count
        periods_words = []
        for i in range(size - 1, -1, -3):
            i_start = 0 if i - 2 < 0 else i - 2
            i_end = i + 1
            current_period = str_number[i_start:i_end]
            periods_words.insert(0, self.process_period(current_period, aux - count))
            count -= 1

        final_words = " ".join(periods_words).strip()

        if number.is_negative():
            return f"negative {final_words}"
        return final_words


class NumberToWordsConverter:
    """
    This class is responsible return the number in the respective language.
    In order to allow more languages, the converter class must be implemented and
    added to the CONVERTERS variable.
    """

    CONVERTERS = {"en": EnglishWordsConverter}

    def __init__(self, lang):
        self.converter_class = self.CONVERTERS[lang]()

    def to_words(self, number):
        return self.converter_class.convert(amount=number)
