import re
import sys
from typing import List, Optional

import pandas as pd


class WhatsappChatToDF:
    """
    A class to process WhatsApp chat logs and convert them into a structured Pandas DataFrame.

    Attributes:
        input_file (str): Path to the input text file containing WhatsApp chat logs.
        data (List[str]): List of chat lines after reading from the file.
        pd_data (pd.DataFrame): Pandas DataFrame containing structured chat data.
        users (List[str]): List of unique users in the chat.
    """

    def __init__(self, input_file: str):
        """
        Initialize the class with the input file path.

        Args:
            input_file (str): Path to the input text file.
        """
        self.file: str = input_file
        self.data: Optional[List[str]] = None
        self.pd_data: Optional[pd.DataFrame] = None
        self.users: Optional[List[str]] = None

    def read_file(self) -> None:
        """
        Reads the input file and loads chat data into a list of lines.
        """
        with open(self.file, "r", encoding="utf8") as f:
            self.data = f.read().splitlines()

    def add_missing_info(self, current_line: str, previous_line: str) -> str:
        """
        Adds timestamp and username from the previous line to the current line.

        Args:
            current_line (str): Current chat line missing information.
            previous_line (str): Previous chat line with timestamp and username.

        Returns:
            str: Updated chat line with missing information added.
        """
        previous_ts, previous_user = previous_line.split("-", 1)
        current_line = f"{previous_ts.strip()} - {previous_user.split(':')[0].strip()}: {current_line}"
        return current_line

    @staticmethod
    def is_valid_format(input_string: str) -> bool:
        """
        Validates if the input string is in a valid time format (HH:MM).

        Args:
            input_string (str): Input string to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        return bool(re.match(r"^\d{2}:\d{2}$", input_string))

    def clean_data(self) -> None:
        """
        Cleans chat data by ensuring all lines have timestamp and username information.
        """
        if self.data is None:
            raise ValueError("Data is not loaded. Call read_file() first.")

        for idx, line in enumerate(self.data):
            if "-" not in line:
                self.data[idx] = self.add_missing_info(
                    self.data[idx], self.data[idx - 1]
                )
            else:
                parts = line.split("-")[0].strip().split(",")
                if len(parts) < 2 or (
                    len(parts) > 1
                    and not self.is_valid_format(parts[1].strip().split(" ")[0])
                ):
                    self.data[idx] = self.add_missing_info(
                        self.data[idx], self.data[idx - 1]
                    )

    def drop_message(
        self,
        contains: str = "Messages to this chat and calls are now secured with end-to-end encryption",
    ) -> "WhatsappChatToDF":
        """
        Removes lines containing a specific message.

        Args:
            contains (str): Message substring to filter out.

        Returns:
            self: For method chaining.
        """
        if self.data is None:
            raise ValueError("Data is not loaded. Call read_file() first.")

        self.data = [line for line in self.data if contains not in line]
        return self

    def prepare_df(self) -> None:
        """
        Converts cleaned chat data into a Pandas DataFrame.
        """
        if self.data is None:
            raise ValueError(
                "Data is not loaded. Call read_file() and clean_data() first."
            )

        timestamps: List[str] = []
        users: List[str] = []
        messages: List[str] = []

        for line in self.data:
            ts, rest = line.split("-", 1)
            user, message = rest.split(":", 1)
            timestamps.append(ts.strip())
            users.append(user.strip())
            messages.append(message.strip())

        self.pd_data = pd.DataFrame(
            {"Timestamp": timestamps, "User": users, "Message": messages}
        )
        self.pd_data["Timestamp"] = pd.to_datetime(
            self.pd_data["Timestamp"], format="%d/%m/%y, %H:%M"
        )
        self.pd_data["Date"] = self.pd_data["Timestamp"].dt.strftime("%d-%b-%Y")
        self.pd_data["Weekday"] = self.pd_data["Timestamp"].dt.strftime("%a")
        self.pd_data = self.pd_data.fillna("")
        self.pd_data = self.pd_data[self.pd_data["Message"] != ""].reset_index(
            drop=True
        )
        self.pd_data = self.pd_data[
            ~self.pd_data["Message"].str.contains("deleted")
        ].reset_index(drop=True)
        self.pd_data = self.pd_data[
            self.pd_data["Message"] != "<Media omitted>"
        ].reset_index(drop=True)
        self.users = self.pd_data["User"].unique().tolist()

    def check_n_users(self) -> None:
        """
        Ensures there are exactly two users in the chat.
        If not, the program exits with an error message.
        """
        if self.users is None:
            raise ValueError("Users are not initialized. Call prepare_df() first.")

        n_users: int = len(self.users)
        if n_users != 2:
            print(f"Error: {n_users} users found. Chat must have exactly 2 users.")
            print(f"Users: {', '.join(self.users)}")
            sys.exit()

    def remove_forward_messages(self, min_length: int = 15) -> "WhatsappChatToDF":
        """
        Removes messages classified as forwards based on message count threshold.

        Args:
            min_length (int): Threshold for message count to classify as forwards.

        Returns:
            self: For method chaining.
        """
        if self.pd_data is None:
            raise ValueError("DataFrame is not initialized. Call prepare_df() first.")

        message_count = (
            self.pd_data.groupby(["User", "Timestamp"])
            .size()
            .reset_index(name="MessageCount")
        )
        forwards = message_count[message_count["MessageCount"] > min_length]
        forwards["IsForward"] = True

        self.pd_data = self.pd_data.merge(
            forwards, on=["User", "Timestamp"], how="left"
        )
        self.pd_data = self.pd_data[self.pd_data["IsForward"].isna()].drop(
            columns=["IsForward", "MessageCount"], errors="ignore"
        )
        self.pd_data.reset_index(drop=True, inplace=True)
        return self

    def run(self) -> pd.DataFrame:
        """
        Executes the entire process of reading, cleaning, and processing the chat data.

        Returns:
            pd.DataFrame: Processed Pandas DataFrame containing the chat data.
        """
        self.read_file()
        self.drop_message().drop_message(contains="security code changed").drop_message(
            contains="Messages and calls are end"
        ).drop_message(contains="Your security code with").drop_message(
            contains="Missed group voice call"
        ).drop_message(
            contains="Missed voice call"
        ).drop_message(
            contains="Missed video call"
        ).drop_message(
            contains="Missed group video call"
        ).drop_message(
            contains="live location shared"
        ).drop_message(
            contains=".vcf (file attached)"
        )
        self.clean_data()
        self.prepare_df()
        self.check_n_users()
        self.remove_forward_messages(min_length=15)
        return self.pd_data


if __name__ == "__main__":
    input_file: str = "data/text/wc_amma.txt"
    wctd = WhatsappChatToDF(input_file)
    df = wctd.run()
    print(df)
