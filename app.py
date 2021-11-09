from flask import Flask,request,abort,jsonify
import requests
from bs4 import BeautifulSoup
import time 

app = Flask('app')

def check(token):
  if token == "FREE":
    return True
  else:
    return False

@app.before_request
def authWall():
  if not request.is_json: 
    abort(jsonify({"message":f"{request.method} method not allowed.","ip":request.environ['HTTP_X_FORWARDED_FOR']}))
  token = request.json.get('token')
  if token is None:
    abort(jsonify({"message":"authentication required!","ip":request.environ['HTTP_X_FORWARDED_FOR']}))
  if token is not None :
    if check(token):
      pass
    else:
      abort(jsonify({"message":"authentication error!","ip":request.environ['HTTP_X_FORWARDED_FOR']}))

@app.route('/gauTry',methods = ['POST'])
def gramAltin():
  ts = time.time()
  r = requests.get("https://altin.in")
  soup = BeautifulSoup(r.content,"html.parser")
  s = soup.find("li", class_="midrow satis")
  a = soup.find("li", class_="midrow alis")
  satis = str(s).replace('<li class="midrow satis" title="Gram Altın - Satış">',"").replace("</li>","")
  alis = str(a).replace('<li class="midrow alis" title="Gram Altın - Alış">',"").replace("</li>","")
  data = {"tur":"gau-try","alis":alis,"satis":satis,"zaman-damgasi":ts}
  return jsonify(data)

@app.route("/usdTry",methods=["POST"])
def usdtry():
  ts = time.time()
  r = requests.get("https://altin.in")
  soup = BeautifulSoup(r.content,"html.parser")
  dolartl = str(soup.find("h2", id="dfiy")).replace('<h2 id="dfiy">',"").replace("</h2>","")
  data = {"tur":"usd-try","kur":dolartl,"zaman-damgasi":ts}
  return jsonify(data)

@app.route("/eurTry",methods=["POST"])
def eurtry():
  ts = time.time()
  r = requests.get("https://altin.in")
  soup = BeautifulSoup(r.content,"html.parser")
  eurotl = str(soup.find("h2", id="efiy")).replace('<h2 id="efiy">',"").replace("</h2>","")
  data = {"tur":"eur-try","kur":eurotl,"zaman-damgasi":ts}
  return jsonify(data)

@app.route("/gbpTry",methods=["POST"])
def gbptry():
  ts = time.time()
  r = requests.get("https://altin.in")
  soup = BeautifulSoup(r.content,"html.parser")
  sterlintl= str(soup.find("h2", id="sfiy")).replace('<h2 id="sfiy">',"").replace("</h2>","")
  data = {"tur":"gbp-try","kur":sterlintl,"zaman-damgasi":ts}
  return jsonify(data)

app.run(host='0.0.0.0', port=8080, debug=False)
