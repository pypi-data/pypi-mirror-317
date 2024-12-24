import random
import math

def random(minimum,maximum,rounded=False,number_of_rounding=0):

	final=-1
	final=random.randrange(minimum,maximum)
	if rounded: final=round(final,number_of_rounding)
	return final

def convert_size(size, round_to=2):

	if size<1: return F"{round(0,round_to)} B"
	if size<1024:

		return F"{round(size,round_to)} B"

	size=size/1024
	if size<1024:

		return F"{round(size,round_to)} KB"

	size=size/1024
	if size<1024:

		return F"{round(size,round_to)} MB"

	size=size/1024
	if size<1024:

		return F"{round(size,round_to)} GB"

	size=size/1024
	return F"{round(size,round_to)} TB"

def get5rating(five,four,three,two,one, round_to=1):

	first=five+four+three+two+one
	second=(five*5)+(four*4)+(three*3)+(two*2)+(one*1)
	if first<1: return 0.0
	result=second/first
	result=round(result,round_to)
	return result

def percent(n1, n2):

	return (n1/n2)*100

def ms_to_readable_time(ms, round_year_to=0, round_month_to=0, round_week_to=0, round_day_to=0, round_hour_to=0, round_minute_to=0, round_second_to=0):
	if ms <= 0:
		return "no time at all"
	if ms < 1000:
		return f"{ms} millisecond{"s" if ms > 1 else ""}"
	
	seconds = math.floor(ms / 1000)
	minutes = math.floor(seconds / 60)
	seconds %= math.floor(60)
	hours = math.floor(minutes / 60)
	minutes %= math.floor(60)
	days = math.floor(hours / 24)
	hours %= math.floor(24)
	days = round(days, round_day_to)
	weeks = math.floor(days / 7)
	days %= math.floor(7)
	months = math.floor(weeks / 4.35)
	weeks %= math.floor(4.35)
	years = math.floor(months / 12)
	months %= math.floor(12)
	months = round(months, round_month_to)
	weeks = round(weeks, round_week_to)
	minutes = round(minutes, round_minute_to)
	hours = round(hours, round_hour_to)
	seconds = round(seconds, round_second_to)
	years = round(years, round_year_to)

	result = []
	if years > 0:
		result.append(f"{years} year{"s" if years > 1 else ""}")
	if months > 0:
		result.append(f"{months} month{"s" if months > 1 else ""}")
	if weeks > 0:
		result.append(f"{weeks} week{"s" if weeks > 1 else ""}")
	if days > 0:
		result.append(f"{days} day{"s" if days > 1 else ""}")
	if hours > 0:
		result.append(f"{hours} hour{"s" if hours > 1 else ""}")
	if minutes > 0:
		result.append(f"{minutes} minute{"s" if minutes > 1 else ""}")
	if seconds > 0:
		result.append(f"{seconds} second{"s" if seconds > 1 else ""}")

	return ", ".join(result)

