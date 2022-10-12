
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory


import pandas as pd

app = Flask(__name__)

df = pd.read_excel('./res/studs2.xlsx')

print(df)

namelist = df["name"].values.tolist()
mathlist = df["math"].values.tolist()
fizrlist = df["fizra"].values.tolist()
llen = range(1,len(namelist))
mathmean = sum([int(i) for i in mathlist])/len(mathlist)
fizrmean = sum([int(i) for i in fizrlist])/len(fizrlist)

print(namelist)

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/students")
def studs():
    global df
    namelist = df["name"].values.tolist()
    mathlist = df["math"].values.tolist()
    fizrlist = df["fizra"].values.tolist()
    llen = range(1,len(namelist))
    mathmean = sum([int(i) for i in mathlist])/len(mathlist)
    fizrmean = sum([int(i) for i in fizrlist])/len(fizrlist)
    print("================")
    print(df)
    print("================")
    return render_template('students.html', studs=namelist, math=mathlist, mmean=mathmean, l=llen, fizra=fizrlist, fm=fizrmean)


@app.route('/addstudent/<name>', methods = ['POST','GET'])
def user(name):
    if request.method == 'GET':
        global df
        smath = request.args.get('math')
        secon = request.args.get('econ')
        sfizr = False
        if(request.args.get('fizr')==0):
            sfizr = True

        df.loc[-1] = [name,smath,secon,sfizr]
        df.index = df.index + 1  # shifting index
        df = df.sort_index()
        globals()['df']=df
        print(df)
        print("!!!!!GET!!!!!")
        #df.to_excel("./res/new3.xlsx", index=False)
        return ("<p>Added!</p>" + name)

@app.route('/editstudent/<ename>', methods = ['POST','GET'])
def edituser(ename):
    if request.method == 'GET':
        global df
        smath = request.args.get('math')
        secon = request.args.get('econ')
        sfizr = False
        if(request.args.get('fizr')==0):
            sfizr = True

        if(len(df.loc[df['name'] == ename].values.tolist())>0):
            print(df.loc[df['name'] == ename])
            df.loc[df['name'] == ename] = [ename,smath,secon,sfizr]
            globals()['df']=df
            print(df)
            return ("<p>Edited </p>" + ename)
        else:
            return (ename + "<p>not found </p>")


@app.route('/res/<path:path>')
def send_report(path):
    return send_from_directory('res', path)
