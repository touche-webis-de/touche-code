try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


availableValues = ["Self-direction: thought", "Self-direction: action", "Stimulation", "Hedonism", "Achievement", "Power: dominance", "Power: resources", "Face", "Security: personal", "Security: societal", "Tradition", "Conformity: rules", "Conformity: interpersonal", "Humility", "Benevolence: caring", "Benevolence: dependability", "Universalism: concern", "Universalism: nature", "Universalism: tolerance"]
availableValuesSubtask2 = [value + postfix for value in availableValues for postfix in [' attained', ' constrained']]


def get_available_values_by_subtask(subtask: Literal['1', '2'] = '1'):
    return availableValues if subtask == '1' else availableValuesSubtask2
