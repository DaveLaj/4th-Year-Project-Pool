from django.shortcuts import render
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import BaggingClassifier
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.svm import SVC
# # Create your views here
# 
def index(request):
    return render(request, 'home.html')

def text_uppercase(text):
    return text.upper()


def baglogr_prediction(col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11):           
    filename = 'classification/models/baggingClass_jb.aiml'
    loaded_model_v2 = joblib.load(filename)
    predictrun = [[int(col1),int(col2),int(col3),int(col4),int(col5),int(col6),int(col7),int(col8),int(col9),float(col10),int(col11)]]
    predicted = loaded_model_v2.predict(predictrun)
    return predicted
    


def classification(request):

    form_posted = False
    dictsdia = {0: "Subject has a normal heart.", 1: "Subject has a high probability of having a disease."}
    map_sex={'F': 0, 'M': 1}
    map_cpt={"ASY": 0, "ATA": 1, "NAP": 2, "TA": 3}
    map_recg={"LVH": 0, "NORMAL": 1, "ST": 2}
    map_ea={'N': 0, 'Y': 1}
    map_sts={"DOWN": 0, "FLAT": 1, "UP": 2} 
    
    if request.method == 'POST':

        form_posted = True

        col1 = request.POST['age']
        col2 = text_uppercase(request.POST['sex'])
        col3 = text_uppercase(request.POST['cpt'])
        col4 = request.POST['rbp']
        col5 = request.POST['chol']
        col6 = request.POST['fbs']
        col7 = text_uppercase(request.POST['recg'])
        col8 = request.POST['mhr']
        col9 = text_uppercase(request.POST['ea'])
        col10 = request.POST['op']
        col11 = text_uppercase(request.POST['sts'])

        col2 = map_sex[col2[0]]
        col3 = map_cpt[col3]
        col7 = map_recg[col7]
        
        col9 = map_ea[col9[0]]
        col11 = map_sts[col11]

        

        

    else:
        col1 = None
        col2 = None
        col3 = None
        col4 = None
        col5 = None
        col6 = None
        col7 = None
        col8 = None
        col9 = None
        col10 = None
        col11 = None


    




    if form_posted:
        predicted = baglogr_prediction(col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11)
        predicted = dictsdia[predicted[0]]



    context = {
        "is_posted": form_posted,
        'prediction' : 'None' if form_posted is False else predicted,
        "col1": col1,
        "col2": col2,
        "col3": col3,
        "col4": col4,
        "col5": col5,
        "col6": col6,
        "col7": col7,
        "col8": col8,
        "col9": col9,
        "col10": col10,
        "col11": col11
    }

    
    return render(request, 'dave.html', context)


def bike_input(request):
    
    return render(request, 'bikeinput.html')


def bike_output(request):
    # Get the text

    seasontext = request.GET.get('season')
    mnthtext = request.GET.get('mnth')
    holitext = request.GET.get('holiday')
    weekdtext = request.GET.get('weekday')
    weasittext = request.GET.get('weathersit')
    temptext = request.GET.get('temp')
    atemptext = request.GET.get('atemp')
    humtext =  request.GET.get('hum')
    wndspdtext  = request.GET.get('windspeed')

    sea = int(seasontext)
    mnth = int(mnthtext)
    holiday = int(holitext)
    weekday = int(weekdtext)
    weathersit = int(weasittext)
    temp = float(temptext)
    atemp = float(atemptext)
    hum = float(humtext)
    windspeed = float(wndspdtext)
    filename = 'classification/models/bike_model.aiml'
    loaded_model_v2 = joblib.load(filename)
    sampletest = [[sea, mnth, holiday, weekday, weathersit, temp, atemp, hum, windspeed]]
    predicted = loaded_model_v2.predict(sampletest)
    
    params = {'Category': round(predicted[0])}
    return render(request, 'bike.html', params)