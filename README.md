# Cricket Score Tracker

## Overview

Cricket Score Tracker is a GUI application built using Python's Tkinter library that allows users to manage and track cricket match scores. Users can add, delete, and search match scores, display match details, view team statistics, and see the leaderboard of teams based on their performance.

## Features

- **Add Match Score**: Add the scores of two teams for a particular match.
- **Delete Match Score**: Remove the scores of a specified match.
- **Display Match Scores**: View all recorded match scores.
- **Search Match Score**: Search for a match score by selecting two teams.
- **Team Statistics**: View the statistics (total matches, wins, draws, losses) for a selected team.
- **Leaderboard**: Display the leaderboard showing teams sorted by their points.

## Prerequisites

- Python 3.x
- Tkinter (usually included with Python)
- `collections` and `operator` modules (standard Python libraries)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/JayUnjiya/Cricket-Score-Monitor
    cd cricket-score-tracker
    ```

2. Run the application:

    ```sh
    python cricket_score_tracker.py
    ```

## Usage

1. **Add Match Score**:
   - Click on "Add Match Score" button.
   - Select the two teams and enter their scores.
   - Click "Add Score" to save the match score.

2. **Delete Match Score**:
   - Click on "Delete Match Score" button.
   - Select the two teams whose score you want to delete.
   - Click "Delete Score" to remove the match score.

3. **Display Match Scores**:
   - Click on "Display Match Scores" button to view all match scores.

4. **Search Match Score**:
   - Click on "Search Match Score" button.
   - Select the two teams and click "Search Match" to view the score.

5. **Team Statistics**:
   - Click on "Team Statistics" button.
   - Select a team to view its statistics.

6. **Leaderboard**:
   - Click on "Leaderboard" button to view the sorted list of teams based on their points.

7. **Exit**:
   - Click on "Exit" button to close the application.

## Code Structure

- `CricketMatch`: A class representing a cricket match with methods to update scores and get the winner.
- `save_matches`: Function to save match data to a CSV file.
- `add_match_score`, `delete_match_score`, `display_match_scores`, `search_match_score_gui`, `team_statistics_gui`, `leaderboard_gui`: Functions to handle the respective GUI operations.
- `main`: Main function to set up the GUI and start the application.

## Example Usage

Here's a basic example of how to add a match score:

```python
# Initialize the CricketMatch class
match = CricketMatch("Team A", "Team B")

# Update the score
match.update_score(150, 145)

# Save the match details
matches = {"Team A vs Team B": match}
save_matches(matches)
