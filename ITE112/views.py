from django.shortcuts import render
import pandas as pd
import plotly.express as px
import cufflinks as cf
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import io


def project1(request):

    location= None

    df = pd.read_csv('ITE112/csv/doh-epi-dengue-data.csv')
    df.rename({'loc': 'location', 'Region': 'region'}, axis=1, inplace=True)
    df.dropna(inplace=True)
    df['year'] = df['date'].str.split('/', expand=True)[2]
    df['year'] = df['year'].astype(int)

    if request.method == 'POST' and 'location' in request.POST:

        location = request.POST['location']


    locationlist = pd.unique(df['location'])

 
    def show_region():
            

            table = pd.DataFrame(columns=['year', 'cases', 'deaths'])
            for year in pd.unique(df['year']):
                if location:
                    rows = (df['year'] == year) & (df['location'] == location)
                else:
                    rows = (df['year'] == year)
                cases = df[rows]['cases'].sum()
                deaths = df[rows]['deaths'].sum()
                table = table.append(
                    {'year': year, 'cases': cases, 'deaths' : deaths},
                    ignore_index=True
                )

            sum_of_cases = table['cases'].sum()
            sum_of_deaths = table['deaths'].sum()

            # First, create a function that will generate the hover text for a given x, y value and data type
            def generate_text(y, data_type):
                if data_type in ('cases', 'deaths'):
                    return f'{y}'

            def annotate(year, column, label):
                for x, y in zip(year, column):
                    plt.annotate(
                        generate_text(y, label),
                        (x, y), textcoords="offset points",
                        xytext=(0,5), ha='center', fontsize=7
                    )

            fig = plt.figure()
            # Then, iterate over the x and y values in your plots and use the `annotate` function to add the hover text
            annotate(table['year'], table['cases'], 'cases')
            annotate(table['year'], table['deaths'], 'deaths')

            plt.plot(table['year'], table['cases'], label='Cases')
            plt.plot(table['year'], table['deaths'], label='Deaths')
            plt.xlabel('Year')
            plt.title(f'Dengue Records Year - 2016 - 2021')
            plt.ylabel('Cases/Deaths')
            plt.legend()

            imgdata = io.StringIO()
            fig.savefig(imgdata, format='svg')
            imgdata.seek(0)

            
            context = {
                'data': imgdata.getvalue(),
                'cases': int(sum_of_cases),
                'deaths': int(sum_of_deaths),
                'location': 'Overall' if location is None else location, 
            }

            return context

    context = show_region()
    context['locationlist'] =  locationlist
    

    return render(request, 'dengue.html', {'context': context})







def project2(request):


    cf.go_offline()
    cf.set_config_file(offline=False, world_readable=True)
    df = pd.read_csv('ITE112/csv/fastfoodrestofull.csv')

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



