import requests
from bs4 import BeautifulSoup

class Search:
    #Function to find the Player ID for the searched player
    @staticmethod
    def __findPlayerID(response):
        playerID = None
        playerURL = None
        letter = None
        #Make sure response was succesful
        if response.status_code == 200:
            parsedData = BeautifulSoup(response.content, 'html.parser')
            #If taken to search results, then select first result
            if(parsedData.find("title").contents[0] == "Search Results | Baseball-Reference.com"):
                try:
                    playerURL = parsedData.find("div", {"class": "search-item-url"}).contents[0].text 
                except:
                    print("Player does not exist")
                    return None
            #Otherwise, find data from player page
            else:
                playerURL = str(parsedData.find("link", {"rel": "canonical"}))
            letterIndex = playerURL.find("/players/") + 9
            letter = playerURL[letterIndex]
            startIndex = letterIndex + 2
            endIndex = int(playerURL.find(".shtml"))
            playerID = playerURL[startIndex:endIndex]
        return (letter, playerID)

    #Function to find the Position for the searched player
    @staticmethod
    def __findPlayerPosition(response):
        position = None
        #Make sure response was succesful
        if response.status_code == 200:
            parsedData = BeautifulSoup(response.content, 'html.parser')
            try: 
                position = parsedData.find("p").contents[2].text
            except:
                print("Position not found")
        else:
            print("Error making request")
        return position
    
    #Function that parses for the stats for hitters
    @staticmethod
    def __parseHitterStats(response, playerName, searchYear):
        player_stats = None
        # Parse the response data using BeautifulSoup
        parsedData = BeautifulSoup(response.content, 'html.parser')
                
        # Find the table containing the player's standard batting stats
        table = parsedData.find("table", {"id": "batting_standard"})
        if(not table):
            print(f"Unable to find batting stats for {playerName}\n")
            return None
        
        # Find the row containing the player's stats from that year
        rows = table.find_all("tr")
        player_row = None
        for row in rows:
            year = row.find("th", {"data-stat": "year_ID"})
            if year and year.text == searchYear:
                player_row = row
                break
        if(player_row):
            # Extract Player's stats from the row
            cols = player_row.find_all("td")
            player_stats = {
                "age": cols[0].text,
                "team": cols[1].text,
                "games": cols[3].text,
                "pa": cols[4].text,
                "ab": cols[5].text,
                "r": cols[6].text,
                "h": cols[7].text,
                "hr": cols[10].text,
                "rbi": cols[11].text,
                "sb": cols[12].text,
                "cs": cols[13].text,
                "bb": cols[14].text,
                "so": cols[15].text,
                "batting_avg": cols[16].text,
                "onbase_pct": cols[17].text,
                "slugging_pct": cols[18].text,
                "ops": cols[19].text,
                "ops_plus": cols[20].text,
                "total_bases": cols[21].text,
                }
        else:
            print(f"No hitting stats found for {playerName} in {searchYear} \n")
        return player_stats
    
    #Function that parses for the stats of pitchers
    @staticmethod
    def __parsePitcherStats(response, playerName, searchYear):
        player_stats = None
        # Parse the response data using BeautifulSoup
        parsedData = BeautifulSoup(response.content, 'html.parser')
                
        # Find the table containing the player's standard batting stats
        table = parsedData.find("table", {"id": "pitching_standard"})
        if(not table):
            print(f"Unable to find pitching stats for {playerName}\n")
            return None
    
        # Find the row containing the player's stats from that year
        rows = table.find_all("tr")
        player_row = None
        for row in rows:
            year = row.find("th", {"data-stat": "year_ID"})
            if year and year.text == searchYear:
                player_row = row
                break
        if(player_row):
            # Extract Player's stats from the row
            cols = player_row.find_all("td")
            player_stats = {
                "age": cols[0].text,
                "team": cols[1].text,
                "wins": cols[3].text,
                "losses": cols[4].text,
                "w-l%": cols[5].text,
                "era": cols[6].text,
                "games": cols[7].text,
                "starts": cols[8].text,
                "saves": cols[12].text,
                "innings pitches": cols[13].text,
                "hits": cols[14].text,
                "runs": cols[15].text,
                "earned runs": cols[16].text,
                "hr": cols[17].text,
                "BB": cols[18].text,
                "strikeouts": cols[20].text
                }
        else:
            print(f"No pitching stats found for {playerName} in {searchYear} \n")
        return player_stats

    #High Level function for finding the player's stats
    @staticmethod
    def statSearch():
        pitching_stats = None
        hitting_stats = None

        #Prompt user to search for a player
        playerName = input("Enter a player: \n")

        #Prompt user to enter a year
        searchYear = str(input("What year?\n"))


        search_url = f"https://www.baseball-reference.com/search/search.fcgi?search={playerName}"
        response = requests.get(search_url)

        (letter, playerID) = Search.__findPlayerID(response)
        
        if(playerID != None):
            # Set up the URL for the player's stats page on Baseball Reference
            url = f"https://www.baseball-reference.com/players/{letter}/{playerID}.shtml"
            
            # Make the request to the website
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                #Get position
                position = Search.__findPlayerPosition(response)
                position = position.lower()

                if(position.__contains__("pitcher")):
                    pitching_stats = Search.__parsePitcherStats(response, playerName, searchYear)    
                hitting_stats = Search.__parseHitterStats(response, playerName, searchYear)

                if pitching_stats:
                    # Print pitching stats
                    print(f"{playerName}'s pitching stats from {searchYear}:")
                    print(pitching_stats)
                if hitting_stats:
                    # Print hitting stats
                    print(f"{playerName}'s batting stats from {searchYear}:")
                    print(hitting_stats)
            else:
                print("Failed to get data from website. Status code:", response.status_code)
