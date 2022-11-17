from rest_framework import serializers

from converter_app.converters import NumberToWordsConverter

MAX_INTEGER_VALUE = 999999999999


class NumberToEnglishConverterSerializer(serializers.Serializer):
    number = serializers.IntegerField(
        write_only=True, max_value=MAX_INTEGER_VALUE, min_value=-MAX_INTEGER_VALUE
    )
    number_in_english = serializers.SerializerMethodField()

    def get_number_in_english(self, obj):
        number = NumberToWordsConverter(lang="en")
        return number.to_words(obj.get("number"))
