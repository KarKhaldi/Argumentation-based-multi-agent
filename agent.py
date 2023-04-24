import random

import pandas as pd

from communication.agent.CommunicatingAgent import CommunicatingAgent

from communication.preferences.CriterionDef import CriterionValue, criterion_find
from communication.preferences.Item import Item
from arguments.argument import CoupleValue, Argument

DATASET_PATH_LEILA = "Leila.csv"
DATASET_PATH_KARIM = "Karim.csv"


class ArgumentAgent(CommunicatingAgent):
    """ArgumentAgent which inherit from CommunicatingAgent ."""

    def __init__(self, unique_id, model, name, preferences):
        super().__init__(unique_id, model, name)
        self.preferences = preferences
        self.name = name
        # Add values
        self.items = []
        if self.name == 'Leila': 
            dataset = pd.read_csv(DATASET_PATH_LEILA)
        else : 
            dataset = pd.read_csv(DATASET_PATH_KARIM)

        self.preferences.set_criterion_name_list([0, 1, 2, 3, 4])
        for _, row in dataset.iterrows():
            new_item = Item(row["SUBJECTS"], "")
            self.items.append(new_item)
            for column in dataset.columns:
                if column != "SUBJECTS":
                    self.preferences.add_criterion_value(
                        CriterionValue(
                            new_item,
                            criterion_find(column),
                            row[column],
                        )
                    )



    
    def support_proposal(self, item):
        """
        Used when the agent receives " ASK_WHY " after having proposed an item
        : param item : str - name of the item which was proposed
        : return : string - the strongest supportive argument
        """
        argument = Argument(True, item)
        premisses = argument.list_supporting_proposal(item, self.preferences)
        return ["Because", item, random.choice(premisses)]
    

    def counter_proposal(self, proposed_item: Item, couple_value: CoupleValue):
        """
        Find a counter proposal to the given item
        - Try to find an item with a better value for the given criterion
        - If not, consider a better criterion
        - If not, propose a random item
        """

        # Find the value of the proposed item for the given criterion
        criterion = couple_value.criterion_name
        value = self.preferences.get_value(proposed_item, criterion)

        for item in self.items:
            item_value = self.preferences.get_value(item, criterion)
            if item_value > value:
                return [
                    "Found better item for this criterion",
                    item,
                    CoupleValue(criterion, item_value),
                ]

        # Consider a better criterion
        best_criterion = None
        for criterion in self.preferences.get_criterion_name_list():
            if criterion != couple_value.criterion_name:
                best_criterion = criterion
            else:
                break
        # Find an item with a better value for the best criterion
        if best_criterion is not None:
            best_criterion_value = self.preferences.get_value(proposed_item, best_criterion)
            for item in self.items:
                item_value = self.preferences.get_value(item, best_criterion)
                if item_value > best_criterion_value:
                    return [
                        "The criterion is not the most important one",
                        item,
                        CoupleValue(best_criterion, item_value),
                    ]

        # Else random item
        item = random.choice(self.items)
        return [
            "The item is not satisfying, how about...",
            item,
            self.support_proposal(item)[2],
        ]


