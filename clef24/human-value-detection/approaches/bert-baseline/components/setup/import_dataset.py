import traceback

import pandas as pd

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class MissingColumnError(AttributeError):
    """Error indicating that an imported DataFrame lacks necessary columns"""
    pass


def load_arguments_from_tsv(filepath, default_usage='test'):
    """
        Reads arguments from tsv file

        Parameters
        ----------
        filepath : str
            The path to the tsv file
        default_usage : str, optional
            The default value if the column "Usage" is missing

        Returns
        -------
        pd.DataFrame
            the DataFrame with all arguments

        Raises
        ------
        MissingColumnError
            if one of the required columns "Text-ID", "Sentence-ID", or "Text" is missing in the read data
        IOError
            if the file can't be read
        """
    try:
        dataframe = pd.read_csv(filepath, encoding='utf-8', sep='\t', header=0)
        if not {'Text-ID', 'Sentence-ID', 'Text'}.issubset(set(dataframe.columns.values)):
            raise MissingColumnError('The sentence file "%s" does not contain the minimum required columns [Text-ID, Sentence-ID, Text].' % filepath)
        if 'Usage' not in dataframe.columns.values:
            dataframe['Usage'] = [default_usage] * len(dataframe)
        return dataframe
    except IOError:
        traceback.print_exc()
        raise


def load_labels_from_tsv(filepath, label_order, subtask: Literal['1', '2'] = '2'):
    """
        Reads label annotations from tsv file

        Parameters
        ----------
        filepath : str
            The path to the tsv file
        label_order : list[str]
            The listing and order of the labels to use from the read core_data

        Returns
        -------
        pd.DataFrame
            the DataFrame with the annotations

        Raises
        ------
        MissingColumnError
            if one of the required columns "Text-ID" and "Sentence-ID", or names from `label_order` are missing in the read data
        IOError
            if the file can't be read
        """
    try:
        dataframe = pd.read_csv(filepath, encoding='utf-8', sep='\t', header=0)
        if not {'Text-ID', 'Sentence-ID'}.issubset(set(dataframe.columns.values)):
            raise MissingColumnError('The label file "%s" does not contain the minimum required columns [Text-ID, Sentence-ID].' % filepath)
        if subtask == '1':
            format_dataframe = dataframe[['Text-ID', 'Sentence-ID']]
            for label in label_order:
                format_dataframe[label] = dataframe[[f"{label} attained", f"{label} constrained"]].sum(axis=1)
            dataframe = format_dataframe
        else:
            dataframe = dataframe[['Text-ID', 'Sentence-ID'] + label_order]
        return dataframe
    except IOError:
        traceback.print_exc()
        raise
    except KeyError:
        raise MissingColumnError('The label file "%s" does not contain the required columns.' % filepath)
