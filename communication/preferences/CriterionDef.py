""" Orders and creates the criterias """

PERSONNAL_INTEREST = 0
ORIGINALITY = 1
CONTROVERSE = 2
SUBJECT_KNOWLEDGE = 3
AMOUNT_OF_WORK = 4


# Create a dict
criterion_name_dict = {
    "PERSONNAL_INTEREST": PERSONNAL_INTEREST,
    "ORIGINALITY": ORIGINALITY,
    "CONTROVERSE": CONTROVERSE,
    "SUBJECT_KNOWLEDGE": SUBJECT_KNOWLEDGE,
    "AMOUNT_OF_WORK": AMOUNT_OF_WORK,
}

reverse_criterion_name_dict = {
    PERSONNAL_INTEREST: "PERSONNAL_INTEREST",
    ORIGINALITY: "ORIGINALITY",
    CONTROVERSE: "CONTROVERSE",
    SUBJECT_KNOWLEDGE: "SUBJECT_KNOWLEDGE",
    AMOUNT_OF_WORK: "AMOUNT_OF_WORK",
}


def criterion_find(criteria: str):
    """CriterionName enum class.
    Enumeration containing the possible CriterionName.
    """

    return criterion_name_dict[criteria]


def criterion_name(criteria_value: int):
    """CriterionName enum class.
    Enumeration containing the possible CriterionName.
    """

    return reverse_criterion_name_dict[criteria_value]




#!/usr/bin/env python3


class CriterionValue:
    """CriterionValue class.
    This class implements the CriterionValue object which associates an item with a CriterionName and a Value.
    """
    def __init__(self, item, criterion_name, value):
        """Creates a new CriterionValue.
        """
        self.__item = item
        self.__criterion_name = criterion_name
        self.__value = value

    def get_item(self):
        """Returns the item.
        """
        return self.__item

    def get_criterion_name(self):
        """Returns the criterion name.
        """
        return self.__criterion_name

    def get_value(self):
        """Returns the value.
        """
        return self.__value