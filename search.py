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
                "Age": cols[0].text,
                "Team": cols[1].text,
                "Games": cols[3].text,
                "PA": cols[4].text,
                "AB": cols[5].text,
                "R": cols[6].text,
                "H": cols[7].text,
                "HR": cols[10].text,
                "RBI": cols[11].text,
                "SB": cols[12].text,
                "CS": cols[13].text,
                "BB": cols[14].text,
                "SO": cols[15].text,
                "BA": cols[16].text,
                "OBP": cols[17].text,
                "SLG": cols[18].text,
                "OPS": cols[19].text,
                "OPS+": cols[20].text,
                "Total Bases": cols[21].text,
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
                "Age": cols[0].text,
                "Team": cols[1].text,
                "Wins": cols[3].text,
                "Losses": cols[4].text,
                "W-L%": cols[5].text,
                "ERA": cols[6].text,
                "Games": cols[7].text,
                "Starts": cols[8].text,
                "Saves": cols[12].text,
                "Innings Pitched": cols[13].text,
                "Hits": cols[14].text,
                "Runs": cols[15].text,
                "Earned Runs": cols[16].text,
                "HR": cols[17].text,
                "BB": cols[18].text,
                "Strikeouts": cols[20].text
                }
        else:
            print(f"No pitching stats found for {playerName} in {searchYear} \n")
        return player_stats

    #Get the player's image file
    @staticmethod
    def __getImage(response):
        # Parse the response data using BeautifulSoup
        parsedData = BeautifulSoup(response.content, 'html.parser')
        
        image_url = parsedData.find("img")["src"]
        print(image_url)
        image_data = requests.get(image_url).content

        with open('image.jpg', 'wb') as f:
            f.write(image_data)
            f.close

    #High Level function for finding the player's stats
    @staticmethod
    def statSearch(playerName, searchYear):
        pitching_stats = None
        hitting_stats = None

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
                #Get image
                Search.__getImage(response)

                #Get position
                position = Search.__findPlayerPosition(response)
                position = position.lower()

                if(position.__contains__("pitcher")):
                    pitching_stats = Search.__parsePitcherStats(response, playerName, searchYear)    
                hitting_stats = Search.__parseHitterStats(response, playerName, searchYear)

                if pitching_stats:
                    # Print pitching stats
                   # print(f"{playerName}'s pitching stats from {searchYear}:")
                    #print(pitching_stats)
                    pitching_stats["Position"] = position.title()
                    return pitching_stats
                if hitting_stats:
                    # Print hitting stats
                    #print(f"{playerName}'s batting stats from {searchYear}:")
                    #print(hitting_stats)
                    hitting_stats["Position"] = position.title()
                    return hitting_stats
            else:
                print("Failed to get data from website. Status code:", response.status_code)
            return None
