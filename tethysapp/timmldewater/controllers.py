import sys
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import numpy as np
import math

from tethys_sdk.gizmos import *


@login_required()

def home(request):
    """
    Controller for the construction dewatering simulator
    """
    # Define view options
    view_options = MVView(
        projection='EPSG:4326',
        center=[-111.64925, 40.24721],
        zoom=16.5,
        maxZoom=22,
        minZoom=2
    )

    # Define drawing options
    drawing_options = MVDraw(
        controls=['Delete', 'Move', 'Point', 'Box', 'Polygon'],
        initial='Box',
        output_format='WKT'
    )

    # Define map view options
    map_view_options = MapView(
            height='600px',
            width='100%',
            controls=['ZoomSlider', 'Rotate', 'FullScreen',
                      {'MousePosition': {'projection': 'EPSG:4326'}},
                      {'ZoomToExtent': {'projection': 'EPSG:4326', 'extent': [-130, 22, -65, 54]}}],
            layers=[],
            view=view_options,
            basemap='OpenStreetMap',
            draw=drawing_options,
            legend=True
    )

    # Define text input boxes for UI
    k = TextInput(display_text='Average Hydraulic Conductivity',
                  name='k',
                  initial='0.000231',
                  placeholder='e.g. 0.000231',
                  prepend='k =',
                  append='[ft/s]',
                  )
    bedrock = TextInput(display_text='Bedrock Elevation',
                  name='bedrock',
                  initial='0',
                  placeholder='e.g. 0',
                  prepend='Elev. =',
                  append='[ft]',
                  )
    iwte = TextInput(display_text='Initial Water Table Elevation',
                  name='iwte',
                  initial='100',
                  placeholder='e.g. 100',
                  prepend='Elev. =',
                  append='[ft]',
                  )
    q = TextInput(display_text='Total Combined Flow',
                  name='q',
                  initial='2',
                  placeholder='e.g. 2',
                  prepend='Q =',
                  append='[cfs]',
                  )
    dwte = TextInput(display_text='Desired Water Table Elevation',
                  name='dwte',
                  initial='70',
                  placeholder='e.g. 70',
                  prepend='Elev. =',
                  append='[ft]',
                  )

    execute = Button(display_text='Calculate Water Table Elevations',
                     attributes='onclick=app.dewater();',
                     submit=True,
                     classes='btn-success')

    instructions = Button(display_text='Instructions',
                     attributes='onclick=generate_water_table',
                     submit=True)

    context = { 'page_id' : '1', 'map_view_options': map_view_options,
                'k':k,
                'bedrock':bedrock,
                'iwte':iwte,
                'q':q,
                'dwte':dwte,
                'execute':execute,
                'instructions':instructions}

    return render(request, 'timmldewater/home.html', context)


def generate_water_table(request):

    #set module paths for timml repository
    sys.path.append("/home/jacobbf1/tethysdev/tethysapp-timmldewater/tethysapp/timmldewater/timml")
    sys.path.append("/usr/local/lib/python2.7/dist-packages")
    sys.path.append("/usr/lib/python2.7/dist-packages")

    # print os.getcwd()
    # print sys.path

    from timml import *
    # import matplotlib.pyplot
    # matplotlib.use('PS')
    # import matplotlib.pyplot
    # matplotlib.pyplot.ioff()
    # matplotlib.pyplot.close("all")

    import Tkinter as tk
    root = tk.Tk()


    get_data = request.GET

    xIndex = json.loads(get_data['xIndex'])
    yIndex = json.loads(get_data['yIndex'])
    wXCoords = json.loads(get_data['wXCoords'])
    wYCoords = json.loads(get_data['wYCoords'])
    cellSide = json.loads(get_data['cellSide'])
    initial = float(json.loads(get_data['initial']))
    bedrock = float(json.loads(get_data['bedrock']))
    q = float(json.loads(get_data['q']))
    k = float(json.loads(get_data['k']))

    waterTable = []

    #This is the analytic element model test, retrieving heads for now
    ml = Model(k = [2,6,4], zb = [140,80,0], zt = [165,120,60], c = [2000,20000], n = [0.3,0.25,0.3], nll = [0.2,0.25])
    rf = Constant(ml,20000,20000,175,[0])
    p=CircAreaSink(ml,10000,10000,15000,0.0002,[0])
    w1=Well(ml,10000,8000,3000,.3,[1],'well 1')
    w2=Well(ml,12000,8000,5000,.3,[2],'well 2')
    w3=Well(ml,10000,4600,5000,.3,[1,2],'maq well')
    #
    HeadLineSink(ml, 9510,  19466, 12620, 17376, 170,[0])
    HeadLineSink(ml, 12620, 17376, 12753, 14976, 168,[0])
    HeadLineSink(ml, 12753, 14976, 13020, 12176, 166,[0])
    HeadLineSink(ml, 13020, 12176, 15066, 9466,  164,[0])
    HeadLineSink(ml, 15066, 9466,  16443, 7910,  162,[0])
    HeadLineSink(ml, 16443, 7910,  17510, 5286,  160,[0])
    HeadLineSink(ml, 17510, 5286,  17600, 976,   158,[0])
    #
    HeadLineSink(ml, 356,   6976,  4043,  7153, 174,[0])
    HeadLineSink(ml, 4043,  7153,  6176,  8400, 171,[0])
    HeadLineSink(ml, 6176,  8400,  9286,  9820, 168,[0])
    HeadLineSink(ml, 9286,  9820,  12266, 9686, 166,[0])
    HeadLineSink(ml, 12266, 9686,  15066, 9466, 164,[0])
    #
    HeadLineSink(ml, 1376,  1910,  4176,  2043, 170,[0])
    HeadLineSink(ml, 4176,  2043,  6800,  1553, 166,[0])
    HeadLineSink(ml, 6800,  1553,  9953,  2086, 162,[0])
    HeadLineSink(ml, 9953,  2086,  14043, 2043, 160,[0])
    HeadLineSink(ml, 14043, 2043,  17600, 976 , 158,[0])
    #
    ml.solve(doIterations=True)

    contourList = timcontour(ml, 0, 20000, 50, 0, 20000, 50, 3, 20, newfig = True, returncontours = True)
    # matplotlib.pyplot.clf()
    # matplotlib.pyplot.cla()
    # matplotlib.pyplot.close("all")

    root.destroy()

    # try:
    #     # equivalent to %matplotlib in IPython
    #     get_ipython().magic('matplotlib')
    # except:
    #     pass

    # try:
    #     count = 0
    #     while (count<100):
    #         print contourList.collections[count].get_paths()
    #         print count
    #         count = count + 1
    # except:
    #     pass

    # This section constructs the featurecollection polygons defining the water table elevations
    # Cells are defined at the corners, water table elevation is defined at the center of the cell

    for long in np.arange(xIndex[0]-cellSide, xIndex[1]+cellSide, cellSide):
        for lat in np.arange(yIndex[0]-cellSide, yIndex[1]+cellSide, cellSide):
            waterTable.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [
                                    [   [long,lat],
                                        [long + cellSide, lat],
                                        [long + cellSide, lat + cellSide],
                                        [long, lat + cellSide],
                                        [long,lat]
                                    ]
                                   ]
                    },
                    'properties': {
                        'elevation' : elevationCalc(long,lat,wXCoords,wYCoords,cellSide,initial,bedrock,q,k),
                    }
            })

    return JsonResponse({
        "sucess": "Data analysis complete!",
        "local_Water_Table": json.dumps(waterTable)
    })


# Assign elevations to raster grid
def elevationCalc (long, lat, wXCoords,wYCoords,cellSide, initial, bedrock, q, k):
    H = initial - bedrock

    i = 0
    sum = 0.0

    while (i < len(wXCoords)):

        wellx = wXCoords[i]
        welly = wYCoords[i]
        Q = q/len(wXCoords)

        deltax = abs(long+cellSide/2-wellx)
        deltay = abs(lat+cellSide/2-welly)

        wellr = pow((pow(deltax,2) + pow(deltay,2)),0.5)

        #Make sure that we don't create a complex value for the water table elevation
        if (wellr < math.exp(math.log(500)-math.pi*k*pow(H,2)/Q)):
            wellr = math.exp(math.log(500)-math.pi*k*pow(H,2)/Q)
            sum = sum + Q*math.log(500/wellr)

        elif (math.log(500/wellr)<0):
            sum = sum

        else:
            sum = sum + Q*math.log(500/wellr)
        i = i+1

    wtElevation = math.pow(abs(math.pow(H,2) - sum/(math.pi*k)),0.5) + bedrock
    # print wtElevation # for debugging purposes
    return (round(wtElevation, 2))



