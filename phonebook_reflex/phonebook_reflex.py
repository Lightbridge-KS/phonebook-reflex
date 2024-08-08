"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from typing import List
import pandas
import reflex as rx
from rxconfig import config

phonebook_raw = pandas.read_csv("data/TelephoneDepartment.csv")
phonebook = phonebook_raw[["CodeName", "Description", "Telephone"]].fillna("")

# Query Function

def query_any_column_df(df, query_text: str, case=False):
    """
    Filters the rows of a DataFrame based on whether any column contains the query text.
    """
    # Create a mask for each column and combine them using 'any' along the columns
    mask = df.apply(lambda column: column.str.contains(
        query_text, case=case)).any(axis=1)
    # Filter the DataFrame using the combined mask
    filtered_df = df[mask]
    return filtered_df



class TextfieldQuery(rx.State):
    text: str = ""

    @rx.var
    def filter_df(self) -> pandas.core.frame.DataFrame:
        phonebook_filtered = query_any_column_df(phonebook, self.text)
        return phonebook_filtered


def index():
    return rx.vstack(
        rx.heading("PhoneBook for RadRAMA", padding="2em"),
        # rx.text(f"Query: {TextfieldQuery.text}"), 
        rx.input(
            placeholder="Search here...",
            value=None,
            on_change=TextfieldQuery.set_text,
            width="30%", size="3"
        ),
        rx.box(
            rx.data_table(
                data=TextfieldQuery.filter_df,
                pagination=True,
                search=False,
                sort=True,
            ),
            padding="1em",
            width="80%"
        ),
        width="100%",
        align="center",
    )


app = rx.App()
app.add_page(index)
