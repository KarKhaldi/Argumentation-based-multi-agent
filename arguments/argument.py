""" Module for generating Arguments """

from communication.preferences.Preferences import Preferences
from communication.preferences.Item import Item
from communication.preferences.CriterionDef import criterion_name


class Argument:
    """Argument class .
    This class implements an argument used during the interaction .

    attr :
    decision :
    item :
    comparison_list :
    couple_values_list :
    """

    def __init__(self, boolean_decision, item):
        """Creates a new Argument ."""
        self.decision = boolean_decision
        self.item = item
        self.comparison_list = []
        self.couple_values_list = []

    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """Adds a premiss comparison in the comparison list ."""
        self.comparison_list.append(Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values(self, criterion_name, value):
        """Add a premiss couple values in the couple values list ."""
        self.couple_values_list.append(CoupleValue(criterion_name, value))

    def list_supporting_proposal(self, item: Item, preferences: Preferences):
        """Generate a list of premisses which can be used to support an item
        : param item : Item - name of the item
        : return : list of all premisses PRO (value over 5) an item ( sorted by order of importance
        based on agent ’s preferences )
        """
        premisses = []
        for criterion in preferences.get_criterion_name_list():
            if preferences.get_value(item, criterion) > 4:
                premisses.append(
                    CoupleValue(criterion, preferences.get_value(item, criterion))
                )
        # if len premisses === 0 then return all premisses -> should not happen during any step, except if initialization is badly done
        if len(premisses) == 0:
            for criterion in preferences.get_criterion_name_list():
                premisses.append(
                    CoupleValue(criterion, preferences.get_value(item, criterion))
                )
        return premisses

    def list_attacking_proposal(self, item: Item, preferences: Preferences):
        """Generate a list of premisses which can be used to attack an item
        : param item : Item - name of the item
        : return : list of all premisses CON (value under 5) an item ( sorted by order of importance
        based on preferences )
        """
        premisses = []
        for criterion in preferences.criterion_name_list:
            if preferences.get_criterion_value(item, criterion).value < 5:
                premisses.append(
                    CoupleValue(criterion, preferences.get_value(item, criterion))
                )
        return premisses



""" Implements an argument: criteria and value"""



class CoupleValue:
    """CoupleValue class .
    This class implements a couple value used in argument object .

    attr :
    criterion_name :
    value :
    """

    def __init__(self, criterion_name, value):
        """Creates a new couple value ."""
        self.criterion_name = criterion_name
        self.value = value

    # print function
    def __str__(self):
        return (
            "Argument : "
            + str(criterion_name(self.criterion_name))
            + " = "
            + str(self.value)
        )


class Comparison:
    """Comparison class .
    This class implements a comparison object used in argument object .

    attr :
    best_criterion_name :
    worst_criterion_name :
    """

    def __init__(self, best_criterion_name, worst_criterion_name):
        """Creates a new comparison ."""
        self.best_criterion_name = best_criterion_name
        self.worst_criterion_name = worst_criterion_name
