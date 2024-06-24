import flask
from flask import request, jsonify
from test_queries import *
from netapp_test2 import *
from flask import Flask, send_file, render_template
	
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    #    return '''<h1>NetApp</h1>
#<p>Retrieval of legal docs.</p>'''
    return render_template('search.html')
    # return '''<h1><center>turingTonks</center></h1>'''

@app.route('/askquery', methods=['GET'])
def api_query():
    text1=""
    text2=""
    text3=""
    text4=""
    text5=""
    text6=""
    text7=""
    text8=""
    text9=""
    text10=""
    text11=""
    text12=""
    if 'query' in request.args:
        ret=test_query(request.args['query'])
        fin=[]
        flag=0
        if 'date' in request.args:
            for i in ret:
                if (retrieve_firstdate(i)==request.args['date']):
                    fin.append(i)
            if(request.args['date']):
                flag=1
        if 'appeal_no' in request.args:
            for i in ret:
                appellate_jurisdiction, appeal_num=retrieve_AppellateJurisdiction(i)
                if (appeal_num==request.args['appeal_no']):
                    fin.append(i)
            if(request.args['appeal_no']):
                flag=1
        if 'appellate' in request.args:
            ret1=request.args['appellate']
            ret1=ret1.lower()
            for i in ret:
                appellate_jurisdiction, appeal_num=retrieve_AppellateJurisdiction(i)
                if(appellate_jurisdiction):
                    if (appellate_jurisdiction.lower()==ret1):
                        fin.append(i)
            if(request.args['appellate']):
                flag=1
        if flag!=1:
            fin=ret
        if len(fin)==0:
            text1= "No relevant document found."
    else:
        text2= "Error: No query provided. Please specify query."
    ct=0
    cleanlist=[]
    [cleanlist.append(x) for x in fin if x not in cleanlist]   
    fin=cleanlist 

    if(ct<len(fin)):
        text3=fin[0]
    ct=ct+1
    if(ct<len(fin)):
        text4=fin[1]
    ct=ct+1
    if(ct<len(fin)):
        text5=fin[2]
    ct=ct+1
    if(ct<len(fin)):
        text6=fin[3]
    ct=ct+1
    if(ct<len(fin)):
        text7=fin[4]
    ct=ct+1
    if(ct<len(fin)):
        text8=fin[5]
    ct=ct+1
    if(ct<len(fin)):
        text9=fin[6]
    ct=ct+1
    if(ct<len(fin)):
        text10=fin[7]
    ct=ct+1
    if(ct<len(fin)):
        text11=fin[8]
    ct=ct+1
    if(ct<len(fin)):
        text12=fin[9]
    ct=ct+1

    return render_template("new_index.html",text1=text1,text2=text2,text3=text3,text4=text4,text5=text5,text6=text6,text7=text7,text8=text8,text9=text9,text10=text10,text11=text11,text12=text12)

@app.route('/docwise', methods=['GET'])
def api_docwise():
	if 'doc' in request.args:
		if 'judgement' in request.args:
			ret=retrieve_finalJudgement(request.args['doc'])
		elif 'penalCode' in request.args:
			ret=retrieve_penalCodes(request.args['doc'])
		elif 'date' in request.args:
			ret=retrieve_firstdate(request.args['doc']+'.txt')
		elif 'appellate' in request.args:
			appellate_jurisdiction, appeal_no=retrieve_AppellateJurisdiction(request.args['doc']+'.txt')
			ret=appellate_jurisdiction+" Appeal No. "+appeal_no
		else: 
			return "Please specify what feature you want to see."
	else:
		return "Error: No document number provided. Please specify."
	return jsonify(ret)

@app.route('/alldocs', methods=['GET'])
def api_all():
    ret=all_docs();
    return jsonify(ret)

@app.route('/download')
def download_file():
	if 'doc' in request.args:
		path = "Prior_Cases/"+request.args['doc']+'.txt'
	else:
		return "Enter document name."
	#path = "sample.txt"
	return send_file(path, as_attachment=True)

app.run()









