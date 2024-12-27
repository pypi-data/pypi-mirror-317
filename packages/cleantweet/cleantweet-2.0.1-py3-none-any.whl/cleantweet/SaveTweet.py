import pandas as pd


def save_tweet(text: str, file_name: str, column_name: str = 'text', index: bool = False):
    """
    a wrapper method for the pandas to_csv() method, so you use it like you were using the pandas method
    :param text: text/string to be saved
    :param file_name: how you want to name the file
    :param column_name: what name do you want to give the text column, default is 'text'
    :param index: do you want to have an index column or not
    :return: a print statement when the text has been saved to the current working directory
    """
    if text:
        data_frame = pd.DataFrame({
            column_name: [text]
        })

        data_frame.to_csv(file_name, sep='\t', index=index)

        print(f'{file_name} has been saved.')













