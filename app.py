
import requests


"""
Get team ranking data from rankings API
"""
def get_ranking_data():
	data = {}
	try:
		url = “https://delivery.chalk247.com/team_rankings/NFL.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0”
		response = requests.get(url)
		if response.status_code != 200:
			raise Exception("Rankings Result not found")
		data = response.json()["results"]["data"]
	except Exception as e:
		raise Exception(e)
	finally:
		return data

	
"""
Generate a dict containing event data along with team ranking information
"""
def get_event_data(event, ranking_data):
	data = {}
	try:
		data["event_id"] = event["event_id"]
		event_date_value = event["event_date"].split(" ")
		event_date = event_date_value[0].split("-")
		data["event_date"] = event_date[2]+"-" + event_date[1] + "-" + event_date[0]
		data["event_time"] = event_date_value[1]
		away_team_id = event["away_team_id"]
		data["away_team_id"] = away_team_id
		data["away_nick_name"] = event["away_nick_name"]
		data["away_city"] = event["away_city"]
		away_rank, away_rank_points = generate_team_rank_data(away_team_id, ranking_data)
		data["away_rank"] = away_rank
		data["away_rank_points"] = away_rank_points
		home_team_id = event["home_team_id"]
		data["home_team_id"] = home_team_id
		data["home_nick_name"] = event["home_nick_name"]
		data["home_city"] = event["home_city"]
		home_rank, home_rank_points = generate_team_rank_data(home_team_id, ranking_data)
		data["home_rank"] = home_rank
		data["home_rank_points"] = home_rank_points
	except Exception as e:
		raise Exception (e)
	finally:
		return data


"""
Get team rank from the rankings api response based on team_id
"""
def generate_team_rank_data(team_id, team_data):
	rank = ""
	points = ""
	try:
		team_data = [team for team in team_data if team["team_id"] == team_id]
		if team_data:
		    team = team_data[0]
		    rank = team["rank"]
		    points = str(round(float(team["adjusted_points"]), 2))
	except exception as e:
		raise Exception(e)
	finally:
		return rank, points

"""
Get event scoreboard for a particular date range
"""
def get_scoreboard_response(start_date, end_date):
    try:
    	url = "https://delivery.chalk247.com/scoreboard/NFL/{start_date}/{end_date}.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0".format(start_date=start_date, end_date= end_date)
    	response = requests.get(url)
    	if response.status_code != 200:
    		raise Exception("Scoreboard API Result not found")
    	else:
    		data = response.json()
    		return data["results"]
    except Exception as e:
        raise Exception(e)

"""
Generate the list of event data having both event info and ranking information
"""
def get_complete_event_response(start_date, end_date):
	try:
		data = []
		scoreboard_data = get_scoreboard_response(start_date, end_date)
		ranking_data = get_ranking_data()
		for date, events in scoreboard_data.items():
		    if events:
    			event_data = events.get("data", {})
    			for event_id, event_values in event_data.items():
    				data.append(get_event_data(event_values, ranking_data))
		return data
	except Exception as e:
		print(e.message)
		raise Exception(e)


if __name__ == "__main__":
	start_date = input("Enter Start Date: ")
	end_date = input("Enter End Date: ")
	result = get_complete_event_response(start_date, end_date)
	print(result)
			
		
	
	
