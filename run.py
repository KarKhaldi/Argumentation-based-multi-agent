""" This file contains the code for the argumentation model. """

import random

import pandas as pd
from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative

from communication.preferences.Preferences import Preferences
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




class ArgumentEnvironment(Model):
    """ArgumentModel which inherit from Model ."""

    def __init__(self):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)

        self.commits = 0

        # Create agents
        agent1 = ArgumentAgent(1, self, "Karim", Preferences())
        self.schedule.add(agent1)

        agent2 = ArgumentAgent(2, self, "Leila", Preferences())
        self.schedule.add(agent2)

        self.running = True
        self.__messages_service.send_message(
            Message(agent1.name, agent2.name, MessagePerformative.PROPOSE, random.choice(agent1.preferences.n_most_preferred(agent1.items,5)))
        )


    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()
        for agent in self.schedule.agents:
            unread_messages = agent.get_new_messages()
            for message in unread_messages:
                # Parse the message
                sender = message.get_exp()
                receiver = message.get_dest()
                performative = message.get_performative()
                content = message.get_content()

                # Print the message
                print(f"Message from {sender}: {performative}")
                if isinstance(content, list):
                    for element in content:
                        print(element)
                else:
                    print(content)
                print("")

                # If PROPOSE, send ACCEPT or ASK_WHY
                if performative == MessagePerformative.PROPOSE:
                    if agent.preferences.is_item_among_top_10_percent(
                        content, agent.items
                    ):
                        self.__messages_service.send_message(
                            Message(
                                receiver, sender, MessagePerformative.ACCEPT, content
                            )
                        )
                    else:
                        self.__messages_service.send_message(
                            Message(
                                receiver, sender, MessagePerformative.ASK_WHY, content
                            )
                        )

                # If ACCEPT, send COMMIT
                elif performative == MessagePerformative.ACCEPT:
                    # Send COMMIT message
                    self.__messages_service.send_message(
                        Message(receiver, sender, MessagePerformative.COMMIT, content)
                    )
                    self.commits += 1

                # If COMMIT, send COMMIT and stop the simulation
                elif performative == MessagePerformative.COMMIT:
                    if self.commits == 1:
                        self.__messages_service.send_message(
                            Message(
                                receiver, sender, MessagePerformative.COMMIT, content
                            )
                        )
                        self.commits += 1
                    elif self.commits == 2:
                        print(f"Commitment reached for {content} !\n")
                        self.running = False

                # If ASK_WHY, send ARGUE
                elif performative == MessagePerformative.ASK_WHY:
                    self.__messages_service.send_message(
                        Message(
                            receiver,
                            sender,
                            MessagePerformative.ARGUE,
                            agent.support_proposal(content),
                        )
                    )

                # If ARGUE, send ACCEPT or ARGUE
                elif performative == MessagePerformative.ARGUE:
                    [comment, item, couple_value] = content
                    if agent.preferences.is_item_among_top_10_percent(item, agent.items):
                        self.__messages_service.send_message(
                            Message(receiver, sender, MessagePerformative.ACCEPT, item)
                        )
                    else:
                        self.__messages_service.send_message(
                            Message(
                                receiver,
                                sender,
                                MessagePerformative.ARGUE,
                                agent.counter_proposal(item, couple_value),
                            )
                        )


if __name__ == "__main__":
    # Run the simulation
    argument_model = ArgumentEnvironment()

    for i in range(20):
        if not argument_model.running:
            break
        print(f"Step {i}:")
        argument_model.step()
