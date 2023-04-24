""" This file is the main to run the project """

from model import ArgumentEnvironment


if __name__ == "__main__":
    # Run the simulation
    argument_model = ArgumentEnvironment()

    for i in range(20):
        if not argument_model.running:
            break
        print(f"Step {i}:")
        argument_model.step()
