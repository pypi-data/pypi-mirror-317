import datetime

def get_time_in_format(format="<dd>/<mm>/<y>, <hh>:<nn>:<ss> <TT>", a=datetime.datetime.now().year, b=datetime.datetime.now().month, c=datetime.datetime.now().day, d=datetime.datetime.now().hour, e=datetime.datetime.now().minute, f=datetime.datetime.now().second):
	result = format
	date = str(c)
	if c < 10:
		date = "0" + date
	month = str(b)
	if b < 10:
		month = "0" + month
	year = str(a)
	year = year[-2:]
	hour24 = str(d)
	if d < 10:
		hour24 = "0" + hour24
	if d > 12:
		hour12 = str(d - 12)
		hour12x0 = str(d - 12)
		daytime = "PM"
		daytime_lc = "pm"
	elif d == 0:
		hour12 = "12"
		hour12x0 = "12"
		daytime = "AM"
		daytime_lc = "am"
	elif d <= 12:
		if d > 0:
			hour12 = str(d)
			hour12x0 = str(d)
			daytime = "AM"
			daytime_lc = "am"
	if d < 10:
		if d > 0:
			hour12 = "0" + hour12
	if d < 22:
		if d > 12:
			hour12 = "0" + hour12
	minute = str(e)
	if e < 10:
		minute = "0" + minute
	second = str(f)
	if f < 10:
		second = "0" + second
	
	result = result.replace("<d>", str(c))
	result = result.replace("<D>", str(c))
	result = result.replace("<dd>", date)
	result = result.replace("<DD>", date)
	result = result.replace("<w>", str(datetime.datetime(a, b, c).weekday()))
	result = result.replace("<W>", datetime.datetime(a, b, c).strftime("%A"))
	result = result.replace("<m>", str(b))
	result = result.replace("<M>", datetime.datetime(a, b, 1).strftime("%B"))
	result = result.replace("<mm>", month)
	result = result.replace("<y>", str(a))
	result = result.replace("<Y>", year)
	result = result.replace("<h>", hour12x0)
	result = result.replace("<hh>", hour12)
	result = result.replace("<H>", str(d))
	result = result.replace("<HH>", hour24)
	result = result.replace("<n>", str(e))
	result = result.replace("<N>", str(e))
	result = result.replace("<nn>", minute)
	result = result.replace("<NN>", minute)
	result = result.replace("<s>", str(f))
	result = result.replace("<S>", str(f))
	result = result.replace("<ss>", second)
	result = result.replace("<SS>", second)
	result = result.replace("<tt>", daytime_lc)
	result = result.replace("<TT>", daytime)
	
	return result
