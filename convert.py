import json
import time
from calendar import timegm
from datetime import datetime
from dateutil.parser import parse as parseTimeString

def parseTime(iso_string):
	dt = parseTimeString(iso_string)
	dt = dt - dt.utcoffset()
	print(iso_string, timegm(dt.timetuple()))
	return timegm(dt.timetuple())

def parseInfo(schedule):
	schedule = schedule["schedule"]
	return schedule["version"], schedule["base_url"], schedule["conference"]

def parseConference(conference):
	return conference["acronym"], conference["title"], conference["start"], conference["end"], conference["daysCount"], conference["timeslot_duration"], conference["days"]

def saveConference(version, base_url, acronym, title, start, end, daysCount, timeslot_duration):
	info = {"version": version, "base_url":base_url, "acronym":acronym, "title":title, "start":start, "end":end, "daysCount":daysCount, "timeslot_duration":timeslot_duration}
	with open("output/conference.json", "w") as conferenceFile:
		conferenceFile.write(json.dumps(info))

def parseDay(day):
	return day["index"], day["date"], parseTime(day["day_start"]), parseTime(day["day_end"]), day["rooms"]

def saveDay(id, index, date, day_start, day_end, roomList):
	info = {"index":index, "date":date, "day_start":day_start, "day_end":day_end, "rooms":roomList}
	with open("output/day{}.json".format(id), "w") as dayFile:
		dayFile.write(json.dumps(info))

def parseRoom(room):
	events = []
	for event in room:
		events.append({"id":event["id"], "start":event["start"], "duration":event["duration"], "title":event["title"]})
	return events

def saveEvents(dayId, roomId, events):
	with open("output/day{}_room{}.json".format(dayId, roomId), "w") as eventsFile:
		eventsFile.write(json.dumps(events))

def saveEventDetails(event):
	event['date'] = parseTime(event['date'])
	with open("output/event{}.json".format(event["id"]), "w") as eventFile:
		eventFile.write(json.dumps(event))

with open("schedule.json") as scheduleFile:
	schedule = json.loads(scheduleFile.read())
version, base_url, conference = parseInfo(schedule)
acronym, title, start, end, daysCount, timeslot_duration, days = parseConference(conference)
saveConference(version, base_url, acronym, title, start, end, daysCount, timeslot_duration)

#Now we're left with parsing the days
for i in range(len(days)):
	index, date, day_start, day_end, rooms = parseDay(days[i])
	roomList = []
	for room in rooms:
		roomList.append(room)
	saveDay(i, index, date, day_start, day_end, roomList)
	for j in range(len(roomList)):
		events = parseRoom(rooms[roomList[j]])
		saveEvents(i, j, events)
		for event in rooms[roomList[j]]:
			saveEventDetails(event)