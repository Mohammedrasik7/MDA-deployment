#!usr/bin/python
import MySQLdb

def connection():
	conn = MySQLdb.connect("192.168.1.249","root","Elait@2017","mda_avance_dev")
	cur = conn.cursor(MySQLdb.cursors.DictCursor)
	return conn, cur