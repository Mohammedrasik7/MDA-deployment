from flask import Flask, jsonify, json, render_template, request, redirect, url_for, flash, session
from db import connection

app = Flask(__name__)

@app.route('/')
@app.route('/<string:pc>')
@app.route('/<string:pc>/<string:sc>')
@app.route('/<string:pc>/<string:sc>/<string:tc>')
@app.route('/<string:pc>/<string:sc>/<string:tc>/<string:qc>')
@app.route('/<string:pc>/<string:sc>/<string:tc>/<string:qc>/<string:ac>')
def iep_creation(pc=None, sc=None, tc=None, qc=None, ac=None):
	conn, cur = connection()

	activity_cat =''
	methods=''

	
	cur.execute("SELECT DISTINCT Primary_area FROM IEP_Ref_Categories ;") 
	primary_cat = cur.fetchall()

	cur.execute("SELECT DISTINCT Secondary_area FROM IEP_Ref_Categories WHERE Primary_area = %s;", [pc]) 
	secondary_cat = cur.fetchall()

	cur.execute("SELECT DISTINCT Tertiary_area FROM IEP_Ref_Categories WHERE Primary_area = %s and Secondary_area=%s ;", [pc, sc]) 
	tertiary_cat = cur.fetchall()

	cur.execute("SELECT DISTINCT Quarternary_area FROM IEP_Ref_Categories WHERE Primary_area = %s and Secondary_area=%s and Tertiary_area=%s ;", [pc, sc, tc]) 
	quarternary_cat = cur.fetchall()

	 
	if pc and sc and not tc and not qc and not ac:
		cur.execute("SELECT DISTINCT Activities FROM IEP_Ref_Categories WHERE  Primary_area = %s and Secondary_area=%s and Tertiary_area='' and Quarternary_area='';", [pc,sc])
		activity_cat = cur.fetchall()
	 
	if pc and sc and tc and not qc and not ac:
		
		cur.execute("SELECT count(*) FROM IEP_Ref_Categories WHERE Tertiary_area=%s;", [tc])
		tertiary_exist = cur.fetchall()

		cur.execute("SELECT count(*) FROM IEP_Ref_Categories WHERE Activities=%s;", [tc])
		activity_exist = cur.fetchall()
		print tertiary_exist, activity_exist

		if activity_exist != 0:
			cur.execute("SELECT DISTINCT Methods, Materials FROM IEP_Ref_Categories WHERE  Primary_area = %s and Secondary_area = %s and Activities = %s;", [pc,sc,tc]) 
			methods = cur.fetchall()

			cur.execute("SELECT DISTINCT Activities FROM IEP_Ref_Categories WHERE  Primary_area = %s and Secondary_area = %s and Tertiary_area=%s and Quarternary_area='';", [pc,sc,tc])
			activity_cat = cur.fetchall()

		elif tertiary_exist != 0:

			cur.execute("SELECT DISTINCT Methods, Materials FROM IEP_Ref_Categories WHERE  Primary_area = %s and Secondary_area = %s and Activities = %s;", [pc,sc,tc]) 
			methods = cur.fetchall()

			cur.execute("SELECT DISTINCT Activities FROM IEP_Ref_Categories WHERE  Primary_area = %s and Secondary_area = %s and Tertiary_area=%s and Quarternary_area='';", [pc,sc,tc])
			activity_cat = cur.fetchall()
		
	if pc and sc and tc and qc and not ac:

		cur.execute("SELECT count(*) FROM IEP_Ref_Categories WHERE Quarternary_area=%s;", [qc])
		quartanary_exist = cur.fetchall()

		cur.execute("SELECT count(*) FROM IEP_Ref_Categories WHERE Activities=%s;", [qc])
		activity_exist = cur.fetchall()

		if activity_exist!=0:
			cur.execute("SELECT DISTINCT Methods, Materials FROM IEP_Ref_Categories WHERE  Primary_area = %s and Secondary_area = %s and Tertiary_area=%s and Activities = %s;", [pc,sc,tc,qc])
			methods= cur.fetchall()	

			cur.execute("SELECT DISTINCT Activities FROM IEP_Ref_Categories WHERE  Primary_area = %s and Secondary_area = %s and Tertiary_area=%s and Quarternary_area=%s;", [pc,sc,tc,qc])
	  		activity_cat = cur.fetchall()		
		elif quartanary_exist!=0:
			cur.execute("SELECT DISTINCT Activities FROM IEP_Ref_Categories WHERE  Primary_area = %s and Secondary_area = %s and Tertiary_area=%s and Quarternary_area=%s;", [pc,sc,tc,qc])
	  		activity_cat = cur.fetchall()

	  		cur.execute("SELECT DISTINCT Methods, Materials FROM IEP_Ref_Categories WHERE  Primary_area = %s and Secondary_area = %s and Tertiary_area=%s and Activities = %s;", [pc,sc,tc,qc])
			methods= cur.fetchall()	
	  
	
	if pc and sc and tc and qc and ac:
	   cur.execute("SELECT DISTINCT Methods, Materials FROM IEP_Ref_Categories WHERE  Primary_area = %s and Secondary_area = %s and Tertiary_area=%s and Quarternary_area=%s and Activities = %s;", [pc,sc,tc,qc,ac])
	   methods= cur.fetchall()

	print('activity_cat',activity_cat)
		   
	
	return render_template('hello.html', pc=pc, sc=sc, tc=tc, qc=qc, ac=ac,
		primary_cat=primary_cat, secondary_cat=secondary_cat, tertiary_cat=tertiary_cat, quarternary_cat=quarternary_cat, activity_cat= activity_cat, methods=methods)

if __name__ == "__main__":
	app.debug = True
	app.run()



