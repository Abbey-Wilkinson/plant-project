"""Transform script for the plants pipeline."""
import pandas as pd


def make_botanist_df(df):

    botanist = df[["botanist_name", "botanist_email", "botanist_phone"]]

    return botanist


def create_dataframe_for_each():
    pass


if __name__ == "__main__":

    df2 = pd.read_csv("test_output.csv")

    botanists = make_botanist_df(df2)
    print(botanists)
