#!/usr/bin/env python
import argparse
import git
import sys
from datetime import datetime, date, timedelta
import time

#Suppress stack traces, but print exceptions.
def err(text, die=False, status=1):
	print >> sys.stderr, text
	if die:
		quit(status)
def hook(x,y,z):
    if not str(y)=="":
        print >> sys.stderr, "\n"+x.__name__+": "+ str(y)
    else:
        print >> sys.stderr, "\n"+x.__name__
#sys.excepthook = hook

def strdelta(delta, seconds=False):
	hours, remainder = divmod(int(delta.total_seconds()), 3600)
	minutes, seconds = divmod(remainder, 60)
	if seconds:
		return '%s hours, %s minutes, and %s seconds' % (hours, minutes, seconds)
	else:
		if seconds>=30:
			minutes=minutes+1
		return '%s hours and  %s minutes' % (hours, minutes)

parser = argparse.ArgumentParser(description='A git timeclock')
parser.add_argument('dir', default='.', help='The directory of the git repo', nargs='?')
doTime=parser.add_mutually_exclusive_group()
doTime.add_argument('-s', '--start', action='store_const', dest='doTime',const='start',
	help='Record a new start tag on top of the current HEAD.')
doTime.add_argument('-e', '--end', action='store_const', dest='doTime', const='end',
	help='Record a new end tag.')
parser.add_argument('-d', '--debug', action='count', help='various debug stuffs')
parser.add_argument('-t', '--time', help='''Start counting tags from this date
	Formatted like: [YYYY-][MM-]DD.
	The year and the month are optional, but you need to use dashes if you do specify them''')

args=parser.parse_args()
debug = args.debug

if debug >= 1:
	print args

sdate=None
if not args.time==None:
	time_splt=args.time.split("-")
	if len(time_splt)==3:
		try:
			sdate=date(int(time_splt[0]), int(time_splt[1]), int(time_splt[2]))
		except ValueError, e:
			err("Date must match YYYY-MM-DD. Ignored.")
	elif len(time_splt)==2:
		try:
			sdate=date(date.today().year, int(time_splt[0]), int(time_splt[1]))
		except ValueError, e:
			err("Date must match YYYY-MM-DD. Ignored.")
	elif len(time_splt)==1:
		try:
			sdate=date(date.today().year, date.today().month, int(time_splt[0]))
		except ValueError, e:
			err("Date must match YYYY-MM-DD. Ignored.")
	else:
		err("Date must match YYYY-MM-DD. Ignored.")
if debug>=1:
	print sdate
	quit()

repo = git.Repo(args.dir)

try:
	current_commit = repo.commit()
except ValueError, e:
	print >> sys.stderr, "Will not work on an empty repo."
	quit(1)

if not args.doTime == None:
	message = "#tc-"+str(args.doTime)+" "+str(datetime.today()).split(".")[0]
	if not debug >= 2:
		#The actual tag path doesn't matter
		repo.create_tag("timeclock/"+str(time.time()),m=" \""+message+"\"")
	else:
		print "timeclock/"+str(time.time())
		print message
	quit()

start=None
end=None
deltalist=[]
for i in repo.tags:
	if i.tag == None:
		continue
	x=i.tag
	if not sdate==None:
		if datetime.fromtimestamp(x.tagged_date).date()>sdate:
			continue
	#print datetime.fromtimestamp(x.tagged_date)
	if "#tc-start " in x.message:
		if (not start==None) and (not end==None):
			delta=end-start
			deltalist.append(delta)
			print "Work session: "+strdelta(delta)
			start=None
			end=None
		start=datetime.fromtimestamp(x.tagged_date)
		print "Start: "+str(start)
	elif "#tc-end " in x.message:
		end=datetime.fromtimestamp(x.tagged_date)
		print "End: "+str(end)
if (not start==None) and (not end==None):
	delta=end-start
	deltalist.append(delta)
	print "Work session: "+strdelta(delta)

print "---------"
deltatotal=timedelta(0)
for i in deltalist:
	deltatotal+=i
print "Totals: "+strdelta(deltatotal)