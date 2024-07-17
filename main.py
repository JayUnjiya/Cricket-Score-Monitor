import tkinter as tk
from tkinter import ttk, messagebox
import csv
from collections import defaultdict
from operator import itemgetter

class CricketMatch:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.team1_score = 0
        self.team2_score = 0

    def update_score(self, team1_score, team2_score):
        self.team1_score += team1_score
        self.team2_score += team2_score

    def get_winner(self):   
        if self.team1_score > self.team2_score:
            return self.team1
        elif self.team2_score > self.team1_score:
            return self.team2
        else:
            return "Draw"

def save_matches(matches):
    with open("matches.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        for match_key, match in matches.items():
            writer.writerow([match_key, match.team1, match.team2, match.team1_score, match.team2_score])

def add_match_score(matches, ipl_teams, treeview):
    add_window = tk.Toplevel()
    add_window.title("Add Match Score")

    label = ttk.Label(add_window, text="Available teams:")
    label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

    team1_choice = ttk.Combobox(add_window, values=ipl_teams,state="readonly")
    team1_choice.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
    team1_choice.set("Select team 1")

    team2_choice = ttk.Combobox(add_window, values=ipl_teams,state="readonly")
    team2_choice.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
    team2_choice.set("Select team 2")

    team1_score_label = ttk.Label(add_window, text="Enter team 1's score:")
    team1_score_label.grid(row=2, column=0, padx=10, pady=5)

    team1_score_entry = ttk.Entry(add_window)
    team1_score_entry.grid(row=3, column=0, padx=10, pady=5, sticky='ew')

    team2_score_label = ttk.Label(add_window, text="Enter team 2's score:")
    team2_score_label.grid(row=2, column=1, padx=10, pady=5)

    team2_score_entry = ttk.Entry(add_window)
    team2_score_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

    confirm_button = ttk.Button(add_window, text="Add Score", command=lambda: add_match_score_logic(matches, ipl_teams, treeview, add_window, team1_choice.get(), team2_choice.get(), team1_score_entry.get(), team2_score_entry.get()))
    confirm_button.grid(row=4, column=0, columnspan=2, pady=(5, 10), padx=10, sticky='ew')

def add_match_score_logic(matches, ipl_teams, treeview, add_window, team1, team2, team1_score, team2_score):
    try:
        team1_score = int(team1_score)
        team2_score = int(team2_score)

        # Check if both teams selected are different
        if team1 != team2:
            match_key = f"{team1} vs {team2}"
            
            # Check if the match key already exists in the matches dictionary
            if match_key not in matches:
                # Create a new match object and update the scores
                match = CricketMatch(team1, team2)
                match.update_score(team1_score, team2_score)
                matches[match_key] = match

                # Update the treeview with existing matches
                update_treeview(treeview, matches)

                add_window.destroy()
                save_matches(matches)
                messagebox.showinfo("Success", "Score updated!")
            else:
                # Display an error message if the match already exists
                messagebox.showerror("Error", "Match score already exists for the specified teams.")
        else:
            # Display an error message if both teams selected are the same
            messagebox.showerror("Error", "Please select different teams for the match.")

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter numeric values.")

def delete_match_score(matches, ipl_teams, treeview):
    def enable_team_choices(event=None):
        if team1_choice.get() != "Select team 1" and team2_choice.get() != "Select team 2":
            team1_choice.config(state="readonly")
            team2_choice.config(state="readonly")

    delete_window = tk.Toplevel()
    delete_window.title("Delete Match Score")

    label = ttk.Label(delete_window, text="Available teams:")
    label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

    team1_choice = ttk.Combobox(delete_window, values=ipl_teams, state="readonly")
    team1_choice.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
    team1_choice.set("Select team 1")
    team1_choice.bind("<<ComboboxSelected>>", enable_team_choices)

    team2_choice = ttk.Combobox(delete_window, values=ipl_teams, state="readonly")
    team2_choice.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
    team2_choice.set("Select team 2")
    team2_choice.bind("<<ComboboxSelected>>", enable_team_choices)

    confirm_button = ttk.Button(delete_window, text="Delete Score", command=lambda: delete_match_score_logic(matches, ipl_teams, treeview, delete_window, team1_choice.get(), team2_choice.get()))
    confirm_button.grid(row=3, column=0, columnspan=2, pady=(5, 10), padx=10, sticky='ew')

def delete_match_score_logic(matches, ipl_teams, treeview, delete_window, team1, team2):
    try:
        match_key = f"{team1} vs {team2}"

        if match_key in matches:
            del matches[match_key]
            save_matches(matches)

            # Update the treeview with existing matches
            update_treeview(treeview, matches)

            delete_window.destroy()
            messagebox.showinfo("Success", "Match score deleted.")
        else:
            messagebox.showerror("Error", "No match score found for the specified teams.")

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please select teams.")

def display_match_scores(matches):
    display_window = tk.Toplevel()
    display_window.title("Match Scores")

    treeview = ttk.Treeview(display_window, columns=("Team 1", "Score 1", "Team 2", "Score 2", "Winner"), show="headings", height=10)
    treeview.heading("Team 1", text="Team 1")
    treeview.heading("Score 1", text="Score 1")
    treeview.heading("Team 2", text="Team 2")
    treeview.heading("Score 2", text="Score 2")
    treeview.heading("Winner", text="Winner")

    for match_key, match in matches.items():
        winner = match.team1 if match.team1_score > match.team2_score else (match.team2 if match.team2_score > match.team1_score else "Draw")
        treeview.insert("", "end", values=(match.team1, match.team1_score, match.team2, match.team2_score, winner))

    treeview.grid(row=0, column=0, columnspan=2, pady=10)

def search_match_score_gui(matches, ipl_teams):
    search_window = tk.Toplevel()
    search_window.title("Search Match Score")

    label = ttk.Label(search_window, text="Available teams:")
    label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

    team1_label = ttk.Label(search_window, text="Team 1:")
    team1_label.grid(row=1, column=0, padx=10, pady=5)

    team1_choice = ttk.Combobox(search_window, values=ipl_teams , state="readonly")
    team1_choice.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
    team1_choice.set("Select team 1")

    team2_label = ttk.Label(search_window, text="Team 2:")
    team2_label.grid(row=2, column=0, padx=10, pady=5)

    team2_choice = ttk.Combobox(search_window, values=ipl_teams,state="readonly")
    team2_choice.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
    team2_choice.set("Select team 2")

    confirm_button = ttk.Button(search_window, text="Search Match", command=lambda: search_match_score_logic(matches, ipl_teams, search_window, team1_choice.get(), team2_choice.get()))
    confirm_button.grid(row=3, column=0, columnspan=2, pady=(5, 10), padx=10, sticky='ew')


def search_match_score_logic(matches, ipl_teams, search_window, team1, team2):
    try:
        if team1 != team2:
            match_key = f"{team1} vs {team2}"

            match = matches.get(match_key)

            if match:
                messagebox.showinfo("Match Details", f"{match_key}:\n {match.team1} {match.team1_score} - {match.team2} {match.team2_score}\nWinner: {match.get_winner()}")
            else:
                messagebox.showinfo("Match Details", "No match score found for the specified teams.")
        else:
            messagebox.showerror("Error", "Please select different teams for the match.")

        search_window.destroy()

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please select teams.")
def team_statistics_gui(matches, teams):
    stats_window = tk.Toplevel()
    stats_window.title("Team Statistics")

    label = ttk.Label(stats_window, text="Select a team:")
    label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

    team_choice = ttk.Combobox(stats_window, values=teams,state="readonly")
    team_choice.grid(row=1, column=0, columnspan=2, pady=5, padx=10, sticky='ew')
    team_choice.set("Select a team")

    confirm_button = ttk.Button(stats_window, text="Show Statistics", command=lambda: team_statistics_logic(matches, teams, stats_window, team_choice.get()))
    confirm_button.grid(row=2, column=0, columnspan=2, pady=(5, 10), padx=10, sticky='ew')


def team_statistics_logic(matches, teams, stats_window, selected_team):
    try:
        if selected_team in teams:
            total_matches, total_wins, total_draws, total_losses = 0, 0, 0, 0

            for match in matches.values():
                if match.team1 == selected_team or match.team2 == selected_team:
                    total_matches += 1
                    if match.team1_score > match.team2_score:
                        total_wins += 1 if match.team1 == selected_team else 0
                        total_losses += 1 if match.team2 == selected_team else 0
                    elif match.team2_score > match.team1_score:
                        total_wins += 1 if match.team2 == selected_team else 0
                        total_losses += 1 if match.team1 == selected_team else 0
                    else:
                        total_draws += 1

            messagebox.showinfo("Team Statistics", f"Team Statistics for {selected_team}:\nTotal Matches: {total_matches}\nWins: {total_wins}\nDraws: {total_draws}\nLosses: {total_losses}")

        else:
            messagebox.showerror("Error", "Please select a valid team.")

        stats_window.destroy()

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please select a team.")

def leaderboard_gui(matches):
    leaderboard_window = tk.Toplevel()
    leaderboard_window.title("Leaderboard")

    treeview = ttk.Treeview(leaderboard_window, columns=("Team", "Points"), show="headings", height=10)
    treeview.heading("Team", text="Team")
    treeview.heading("Points", text="Points")

    team_points = defaultdict(int)

    for match in matches.values():
        points1 = 2 if match.team1_score > match.team2_score else (1 if match.team1_score == match.team2_score else 0)
        points2 = 2 if match.team2_score > match.team1_score else (1 if match.team1_score == match.team2_score else 0)

        team_points[match.team1] += points1
        team_points[match.team2] += points2

    sorted_teams = sorted(team_points.items(), key=itemgetter(1), reverse=True)

    for team, points in sorted_teams:
        treeview.insert("", "end", values=(team, points))

    treeview.grid(row=0, column=0, columnspan=2, pady=(10, 5), padx=10, sticky='ew')

def update_treeview(treeview, matches):
    for match_key, match in matches.items():
        winner = match.team1 if match.team1_score > match.team2_score else (match.team2 if match.team2_score > match.team1_score else "Draw")
        treeview.insert("", "end", values=(match.team1, match.team1_score, match.team2, match.team2_score, winner))

def load_matches():
    matches = {}
    try:
        with open("matches.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                match_key, team1, team2, team1_score, team2_score = row
                match = CricketMatch(team1, team2)
                match.update_score(int(team1_score), int(team2_score))
                matches[match_key] = match
    except FileNotFoundError:
        print("No existing match data found. Creating a new file.")

    return matches

def main():
    ipl_teams = [
        "Chennai Super Kings", "Gujarat Titans", "Mumbai Indians", "Kolkata Knight Riders",
        "Royal Challengers Bangalore", "Delhi Capitals", "Lucknow Super Giants", "Punjab Kings",
        "Rajasthan Royals", "Sunrisers Hyderabad"
    ]

    matches = load_matches()

    root = tk.Tk()
    root.title("Cricket Score Tracker")

    treeview = ttk.Treeview(root, columns=("Team 1", "Score 1", "Team 2", "Score 2", "Winner"), show="headings", height=10)
    treeview.heading("Team 1", text="Team 1")
    treeview.heading("Score 1", text="Score 1")
    treeview.heading("Team 2", text="Team 2")
    treeview.heading("Score 2", text="Score 2")
    treeview.heading("Winner", text="Winner")

    update_treeview(treeview, matches)

    treeview.grid(row=0, column=0, columnspan=3, pady=10)

    add_button = ttk.Button(root, text="Add Match Score", command=lambda: add_match_score(matches, ipl_teams, treeview))
    add_button.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

    delete_button = ttk.Button(root, text="Delete Match Score", command=lambda: delete_match_score(matches, ipl_teams, treeview))
    delete_button.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

    display_button = ttk.Button(root, text="Display Match Scores", command=lambda: display_match_scores(matches))
    display_button.grid(row=1, column=2, padx=10, pady=5, sticky='ew')

    search_button = ttk.Button(root, text="Search Match Score", command=lambda: search_match_score_gui(matches, ipl_teams))
    search_button.grid(row=2, column=0, padx=10, pady=5, sticky='ew')

    stats_button = ttk.Button(root, text="Team Statistics", command=lambda: team_statistics_gui(matches, ipl_teams))
    stats_button.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

    leaderboard_button = ttk.Button(root, text="Leaderboard", command=lambda: leaderboard_gui(matches))
    leaderboard_button.grid(row=2, column=2, padx=10, pady=5, sticky='ew')

    exit_button = ttk.Button(root, text="Exit", command=root.destroy)
    exit_button.grid(row=3, column=0, columnspan=3, pady=10, sticky='ew')

    root.mainloop()

if __name__ == "__main__":
    main()