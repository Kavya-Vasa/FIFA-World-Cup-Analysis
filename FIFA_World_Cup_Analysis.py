import pandas as pd
import os

def load_data(file_path):
    """
    Load data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    return pd.read_csv(file_path)

def preprocess_world_cups_data(df):
    """
    Preprocess the World Cups data.
    
    Args:
        df (pd.DataFrame): DataFrame containing the World Cups data.
        
    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    # Convert columns to appropriate data types
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    df['GoalsScored'] = pd.to_numeric(df['GoalsScored'])
    df['QualifiedTeams'] = pd.to_numeric(df['QualifiedTeams'])
    df['MatchesPlayed'] = pd.to_numeric(df['MatchesPlayed'])
    df['Attendance'] = pd.to_numeric(df['Attendance'].str.replace('.', '', regex=False))
    return df

def preprocess_matches_data(df):
    """
    Preprocess the World Cup Matches data.
    
    Args:
        df (pd.DataFrame): DataFrame containing the World Cup Matches data.
        
    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    # Convert columns to appropriate data types
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    
    # Extract date and time from 'Datetime' column
    df['Date'] = df['Datetime'].str.split(' - ').str[0]
    df['Time'] = df['Datetime'].str.split(' - ').str[1].str.strip()
    
    # Convert date and time components to datetime objects
    df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y', errors='coerce')
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M', errors='coerce').dt.time
    
    # Drop rows with invalid datetime values
    df = df.dropna(subset=['Date', 'Time'])
    
    return df

def preprocess_players_data(df):
    """
    Preprocess the World Cup Players data.
    
    Args:
        df (pd.DataFrame): DataFrame containing the World Cup Players data.
        
    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    # No specific preprocessing needed for now
    return df

def analyze_data(world_cups_df, matches_df, players_df):
    """
    Analyze the data to find key metrics and factors influencing the World Cup win.
    
    Args:
        world_cups_df (pd.DataFrame): DataFrame containing the World Cups data.
        matches_df (pd.DataFrame): DataFrame containing the World Cup Matches data.
        players_df (pd.DataFrame): DataFrame containing the World Cup Players data.
        
    Returns:
        dict: Analysis results.
    """
    results = {}
    
    # Example analysis: Total goals scored by winners
    goals_by_winners = world_cups_df.groupby('Winner')['GoalsScored'].sum()
    results['GoalsByWinners'] = goals_by_winners
    
    # Example analysis: Total matches played by winners
    matches_played_by_winners = matches_df[(matches_df['Home Team Name'].isin(world_cups_df['Winner'])) | (matches_df['Away Team Name'].isin(world_cups_df['Winner']))]
    matches_played_by_winners_count = matches_played_by_winners.groupby(['Home Team Name', 'Away Team Name']).size()
    results['MatchesPlayedByWinners'] = matches_played_by_winners_count
    
    # Example analysis: Attendance for matches with winners
    attendance_by_winners = matches_played_by_winners.groupby(['Home Team Name', 'Away Team Name'])['Attendance'].sum()
    results['AttendanceByWinners'] = attendance_by_winners
    
    # Example analysis: Key players from winning teams
    winning_teams = world_cups_df['Winner'].unique()
    key_players = players_df[players_df['Team Initials'].isin(winning_teams)]
    results['KeyPlayers'] = key_players[['Player Name', 'Team Initials', 'Position', 'Event']]
    
    return results

def main():
    world_cups_file = 'C:\\Users\\LENOVO\\Videos\\WorldCups.csv'
    matches_file = 'C:\\Users\\LENOVO\\Videos\\WorldCupMatches.csv'
    players_file = 'C:\\Users\\LENOVO\\Videos\\WorldCupPlayers.csv'
    
    # Load data
    world_cups_df = load_data(world_cups_file)
    matches_df = load_data(matches_file)
    players_df = load_data(players_file)
    
    # Preprocess data
    world_cups_df = preprocess_world_cups_data(world_cups_df)
    matches_df = preprocess_matches_data(matches_df)
    players_df = preprocess_players_data(players_df)
    
    # Analyze data
    analysis_results = analyze_data(world_cups_df, matches_df, players_df)
    
    # Print results
    for key, value in analysis_results.items():
        print(f"{key}:")
        print(value)
        print("\n")

if __name__ == "__main__":
    main()
