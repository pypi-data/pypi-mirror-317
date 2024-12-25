import re
from typing import Literal

from prettytable import PrettyTable

from premier_league.base import BaseScrapper
from premier_league.utils.xpath import PLAYERS
from premier_league.utils.methods import clean_xml_text, export_to_csv, export_to_json


class TeamNotFoundError(Exception):
    """
    Exception raised when a team is not found in the specified Premier League season.

    Attributes:
        team (str): The name of the team that was not found.
        season (str): The season in which the team was searched for.
    """

    def __init__(self, team: str, season: str):
        self.team = team
        self.season = season

    def __str__(self):
        return f"Team '{self.team}' not found in the {self.season} Premier League season. For all current teams, use the 'get_all_current_teams' method."


class Transfers(BaseScrapper):
    """
    A class for scraping and managing Player transfer data for Premier League teams in a given season.

    This class inherits from BaseScrapper and provides methods to retrieve,
    display, and export transfer data for specified teams and seasons.

    Attributes:
        page: The URL page to be Scrapped.
        _season_top_players (dict): A dictionary containing transfer data for all teams.
    """

    def __init__(self, target_season: str = None):
        """
        Initialize the Transfers object.

        Args:
            target_season (str, optional): The target season for transfer data. Defaults to None.
        """
        super().__init__("https://www.worldfootball.net/transfers/eng-premier-league-{SEASON}/", target_season)
        self.page = self.request_url_page()
        self._season_top_players = self._init_transfers_table()

    def _init_transfers_table(self) -> dict[str, list[list[list[str]]]]:
        """
        Initialize the transfers table by scraping and processing the data.

        Returns:
            dict: A dictionary containing processed transfer data for all teams.
        """
        transfer_list = self.get_list_by_xpath(PLAYERS.TRANSFER_TABLES, False)

        team_transfer_dict = {}
        for transfer in transfer_list:
            try:
                target_team = transfer.xpath(PLAYERS.TRANSFER_HEADER)[0]
                player_transfers = [clean_xml_text(e) for e in
                                    transfer.xpath(PLAYERS.TRANSFER_DATA) if clean_xml_text(e)]
                team_transfer_dict[target_team.split(" » ")[0].strip().lower()] = player_transfers
            except IndexError:
                break

        cleaned_transfer_data = {}
        for team, transfers in team_transfer_dict.items():
            index = 1
            current_type = 'In'
            cleaned_transfer_data[team] = [[["Date", "Name", "Position", "Club"]], [["Date", "Name", "Position", "Club"]]]
            while index <= len(transfers[1:]):
                partition = []
                if bool(re.match(r'^\d{2}/\d{2}$', transfers[index])):
                    partition.append(transfers[index])
                    index += 1
                    try:
                        while not bool(re.match(r'^\d{2}/\d{2}$', transfers[index])):
                            partition.append(transfers[index])
                            index += 1
                    except IndexError:
                        pass

                    if "Out" in partition:
                        current_type = 'Out'
                        partition.remove("Out")
                    if len(partition) == 5:
                        partition[3] = f"{partition[3]}{partition[4]}"
                        partition.pop()
                    if current_type == "In":
                        cleaned_transfer_data[team][0].append(partition)
                    else:
                        cleaned_transfer_data[team][1].append(partition)
        return cleaned_transfer_data

    def print_transfer_table(self, team: str) -> None:
        """
        Print the transfer table for a specified team.

        Args:
            team (str): The name of the team.

        Raises:
            TeamNotFoundError: If the specified team is not found in the current season.
        """
        in_table = PrettyTable()
        out_table = PrettyTable()

        try:
            transfer_in = self._season_top_players[team.lower()][0]
            transfer_out = self._season_top_players[team.lower()][1]
        except KeyError:
            raise TeamNotFoundError(team, self.season)

        in_table.field_names = transfer_in[0]
        out_table.field_names = transfer_out[0]

        list(map(out_table.add_row, transfer_out[1:]))
        list(map(in_table.add_row, transfer_in[1:]))

        print(f"{team} >> Transfers {self.season} In:")
        print(in_table)
        print(f"\n{team} >> Transfers {self.season} Out:")
        print(out_table)

    def transfer_in_table(self, team: str) -> list[list[str]]:
        """
        Get the transfer-in table for a specified team.

        Args:
            team (str): The name of the team.

        Returns:
            list[list[str]]: A list of lists containing transfer-in data.

        Raises:
            TeamNotFoundError: If the specified team is not found in the current season.
        """
        try:
            return self._season_top_players[team.lower()][0]
        except KeyError:
            raise TeamNotFoundError(team, self.season)

    def transfer_out_table(self, team: str) -> list[list[str]]:
        """
        Get the transfer-out table for a specified team.

        Args:
            team (str): The name of the team.

        Returns:
            list[list[str]]: A list of lists containing transfer-out data.

        Raises:
            TeamNotFoundError: If the specified team is not found in the current season.
        """
        try:
            return self._season_top_players[team.lower()][1]
        except KeyError:
            raise TeamNotFoundError(team, self.season)

    def transfer_csv(self, team: str, file_name: str, transfer_type: Literal["in", "out", "both"] = "both"):
        """
        Export transfer data to a CSV file.

        Args:
            team (str): The name of the team.
            file_name (str): The name of the file to export to.
            transfer_type (Literal["in", "out", "both"], optional): The type of transfers to export. Defaults to "both".

        Raises:
            TeamNotFoundError: If the specified team is not found in the current season.
        """
        if transfer_type == "both":
            export_to_csv(file_name,  self.transfer_in_table(team), self.transfer_out_table(team), f"{team} {self.season} Transfers In", f"{team} {self.season} Transfers Out")
        elif transfer_type == "in":
            export_to_csv(file_name,  self.transfer_in_table(team), header=f"{team} {self.season} Transfers In")
        else:
            export_to_csv(file_name,  self.transfer_out_table(team), header=f"{team} {self.season} Transfers Out")

    def transfer_json(self, team: str, file_name: str, transfer_type: Literal["in", "out", "both"] = "both"):
        """
        Export transfer data to a JSON file.

        Args:
            team (str): The name of the team.
            file_name (str): The name of the file to export to.
            transfer_type (Literal["in", "out", "both"], optional): The type of transfers to export. Defaults to "both".

        Raises:
            TeamNotFoundError: If the specified team is not found in the current season.
        """
        if transfer_type == "both":
            export_to_json(file_name,  self.transfer_in_table(team), self.transfer_out_table(team), f"{team} {self.season} Transfers In", f"{team} {self.season} Transfers Out")
        elif transfer_type == "in":
            export_to_json(file_name,  self.transfer_in_table(team))
        else:
            export_to_json(file_name,  self.transfer_out_table(team))

    def get_all_current_teams(self) -> list[str]:
        """
        Get a list of all teams in the given Premier League Season.

        Returns:
            list[str]: A list of team names.
        """
        return list(self._season_top_players.keys())
