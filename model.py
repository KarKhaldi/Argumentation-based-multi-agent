import random

from mesa import Model
from mesa.time import RandomActivation

from communication.message.MessageService import MessageService
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative

from communication.preferences.Preferences import Preferences
from agent import ArgumentAgent



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
