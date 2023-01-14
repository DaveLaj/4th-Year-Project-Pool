from django.shortcuts import render
import pandas as pd
import plotly.express as px
import cufflinks as cf
import plotly.graph_objects as go

# Create your views here.





def project2(request):


    





    cf.go_offline()
    cf.set_config_file(offline=False, world_readable=True)
    df = pd.read_csv('ITE112/csv/fastfoodresto.csv')






    df.rename(columns={"latitude": "lat", "longitude": "lon", "categories": "cat"}, inplace=True)
    df.dropna(inplace=True)
    df = df.replace(to_replace={'SUBWAY����':'SUBWAY','Burger King����':'Burger King'}, inplace=False)


    if request.method == 'POST':

        search = request.POST['search']
        df=df[df['name'].str.contains(search, case=False)]

    else:

        df=df 



    

    
    df['text'] = df['name'] + ' : ' + df['cat'].astype(str)

    fig = go.Figure(data=go.Scattergeo(
            lon = df['lon'],
            lat = df['lat'],
            text = df['text'],
            mode = 'markers'
            ))

    fig.update_layout(
            geo_scope='usa',
            paper_bgcolor='rgba(0,0,0,0)',
            width=1000,
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
        )
    chart = fig.to_html()

        
        

    context = {
        "chart": chart,
    }



    return render(request, 'map.html' , context)