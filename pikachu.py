from flask import Flask, abort, jsonify, render_template,url_for, request,send_from_directory,redirect
import numpy as np 
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

pika = pd.read_csv("Pokemon.csv")
def combination(i):
    return str(i['Type 1'])+ '$' +str(i['Generation'])+'$'+str(i['Legendary'])
pika['Atribute']= pika.apply(combination,axis=1)
pika['Name']= pika['Name'].apply(lambda i: i.lower())

cov = CountVectorizer(tokenizer=lambda pika: pika.split('$'))
pikaulti = cov.fit_transform(pika['Atribute'])
pikavalue = cosine_similarity(pikaulti)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('pokemon.html')

@app.route('/hasil', methods=['GET','POST'])
def Cari():
    body = request.form
    pikapengen = body['pokemon']
    pikapengen = pikapengen.lower()
    if pikapengen not in list(pika['Name']):
        return redirect('/NotFound')
    indexpengen = pika[pika["Name"] == pikapengen].index[0]
    favorit = pika.iloc[indexpengen][["Name",'Type 1','Generation','Legendary']]
    url = 'https://pokeapi.co/api/v2/pokemon/'+ pikapengen
    url = requests.get(url)
    gambarsaran = url.json()["sprites"]["front_default"]
    pikasaran = list(enumerate(pikavalue[indexpengen]))
    pikasortir = sorted(pikasaran, key= lambda x:x[1], reverse= True)
    saran=[]
    for item in pikasortir[:7]:
        x={}
        if item[0] != indexpengen:
            nama = pika.iloc[item[0]]['Name'].capitalize()
            type = pika.iloc[item[0]]['Type 1']
            legend = pika.iloc[item[0]]['Legendary']
            gen = pika.iloc[item[0]]['Generation']
            url = 'https://pokeapi.co/api/v2/pokemon/'+ nama.lower()
            url = requests.get(url)
            pic = url.json()["sprites"]["front_default"] 
            x['Name']= nama
            x['Type']= type
            x['Legend']= legend
            x['Generation']= gen
            x["gambar"] = pic
            saran.append(x)
    return render_template('hasil.html',rekomendasi= saran, favorit= favorit, pic=gambarsaran)


@app.route('/NotFound')
def notFound():
    return render_template('no.html')


if __name__=='__main__':
    app.run(debug=True)