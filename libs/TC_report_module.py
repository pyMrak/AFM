# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 13:32:59 2017

@author: andmra2
"""
#from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.chart import LineChart, Reference, ScatterChart, Series
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.chart.axis import ChartLines
from PIL import Image as PILImage


#wb = load_workbook('KopijaTC_template.xlsx')

def write_TC_header(gdat, wb, i):
    img = Image('Graphic\Pic\Hidria.jpg')
    img.width = 142
    img.height = 53
    wb['Poročilo'].add_image(img, 'B1')
    wb['Poročilo']['A2']='Date: '+ gdat.TC_header.date
    wb['Poročilo']['G2']='Order No./Customer: '+ gdat.TC_header.order_nr
    wb['Poročilo']['D9']= gdat.TC_header.production_date
    wb['Poročilo']['D11']= i
    wb['Poročilo']['I7']= gdat.TC_header.gp_nr
    wb['Poročilo']['I9']= gdat.TC_header.nominal_v
    if gdat.TC_header.nominal_v == '5V':   
        wb['Poročilo']['A19']= '11V-2s'
        wb['Poročilo']['A21']= '5V-58s'
    elif gdat.TC_header.nominal_v == '4,4V':   
        wb['Poročilo']['A19']= '11V-1,9s'
        wb['Poročilo']['A21']= '4,4V-58,1s'
    elif gdat.TC_header.nominal_v == '11V':   
        wb['Poročilo']['A19']= '11V-60s'
        wb['Poročilo']['A21']= ' '
    elif gdat.TC_header.nominal_v == '13,5V':
        wb['Poročilo']['A19']= '13,5V-2s'
        wb['Poročilo']['A21']= '8V-18s'
    elif  gdat.TC_header.nominal_v == '23V':
        wb['Poročilo']['A19']= '23V-60s'
        wb['Poročilo']['A21']= ' '
    else:
        raise RuntimeError('unknown nominal voltage')
    wb['Poročilo']['G45']='Prepared by/signature: ' + gdat.TC_header.creator
    
    wb['Poročilo'].add_image(Image('Graphic\Pic\Legend.png'), 'D49')
    #wb['Poročilo'].add_image(Image('TCRTG\\a.jpg', size=(170, 305)), 'D75')
    wb['Poročilo'].column_dimensions['I'].width = 9.10
    wb['Poročilo'].column_dimensions['J'].width = 9.10
    wb['Poročilo'].column_dimensions['K'].width = 9.10
    wb['Poročilo'].column_dimensions['L'].width = 9.10
    #wb['Poročilo'].column_dimensions['L'].width = 4.1
    
    return wb


#write TC graph
def write_TC_diff_graph(wb):
    tempImg = 'Graphic/Pic/temp.png'
    graph = LineChart()
    
    graph.style = 7
    
    data = Reference(wb['Meritve 800-1100'], min_col=22, min_row=2, max_col=23, max_row=6)
    x_ax = Reference(wb['Meritve 800-1100'], min_col=21, min_row=3, max_row=6)
    graph.add_data(data, titles_from_data=True)
    graph.set_categories(x_ax)
    
    ser1 = graph.series[0]
    ser2 = graph.series[1]
    
    ser2.marker.symbol = "square"
    ser2.marker.graphicalProperties.solidFill = "01A021"
    ser2.graphicalProperties.line.solidFill = "FF0000"
    
    ser1.marker.symbol = "square"
    ser1.marker.graphicalProperties.solidFill = "035C9B"
    ser1.marker.graphicalProperties.line.solidFill = "035C9B"
    ser1.graphicalProperties.line.solidFill = "006CBA"
    ser1.hiLowLines = ChartLines()
    
    graph.y_axis.scaling.min = 750
    graph.y_axis.scaling.max = 1200
    graph.x_axis.majorGridlines=ser1.hiLowLines
    graph.x_axis.minorGridlines=ser1.hiLowLines
    
    graph.height = 7.9
    graph.width = 19.3
    
    #wb['Poročilo'].add_image(Image('Graphic\Pic\Xaxis_units.png'), 'G40')#,size=(70, 20)
    fp = 'Graphic\Pic\Xaxis_units.png'
#    im = PILImage.open(fp)
#    im = im.resize((74, 15), PILImage.ANTIALIAS)
#    im.save(fp=tempImg, format='png')
    wb['Poročilo'].add_image(Image(fp), 'G40')
    
    #wb['Poročilo'].add_image(Image('Graphic\Pic\yaxis_units.png'), 'C31')#.add_image(Image('Graphic\Pic\yaxis_units.png'), 'C31')
    fp = 'Graphic\Pic\yaxis_units.png'
#    im = PILImage.open(fp)
#    im = im.resize((15, 196), PILImage.ANTIALIAS)
#    im.save(fp=tempImg, format='png')
    wb['Poročilo'].add_image(Image(fp), 'C31')
    
    
    graph.layout=Layout(
        manualLayout=ManualLayout(
            x=0.01, y=0,
            h=0.9, w=0.8,
        )
    )
    wb['Poročilo'].add_chart(graph, "B26")
    
    return wb


def write_TC_func_graph(wb, MS):
#write functional graph
    tempImg = 'Graphic/Pic/temp.png'
    chart = ScatterChart()
    chart1 = ScatterChart()
    
    xvalues = Reference(wb['Meritev 11V-2s 5V-58s'], min_col=1, min_row=2, max_row=6502)
    values = Reference(wb['Meritev 11V-2s 5V-58s'], min_col=4, min_row=2, max_row=6502)
    values1 = Reference(wb['Meritev 11V-2s 5V-58s'], min_col=2, min_row=2, max_row=6502)
    values2 = Reference(wb['Meritev 11V-2s 5V-58s'], min_col=3, min_row=2, max_row=6502)
    values3 = Reference(wb['Meritev 11V-2s 5V-58s'], min_col=5, min_row=2, max_row=6502)
    
    series = Series(values, xvalues,title='T surface')
    series1 = Series(values1, xvalues, title='U')
    series2 = Series(values2, xvalues, title='I')
    series3 = Series(values3, xvalues, title='T inside')
    
    series.graphicalProperties.line.solidFill="018606"
    series1.graphicalProperties.line.solidFill="000000"
    series2.graphicalProperties.line.solidFill="D30000"
    series3.graphicalProperties.line.solidFill="0027BF"
    
    chart.series.append(series)
    chart1.series.append(series1)
    chart1.series.append(series2)
    chart.series.append(series3)
    
    chart1.x_axis.scaling.min = 0
    chart.y_axis.scaling.min = 700
    chart1.x_axis.scaling.max = 60+round((MS-1)/100)
    chart.y_axis.scaling.max = 1300
    chart1.y_axis.scaling.min = 0
    chart1.y_axis.scaling.max = 30
    
    chart1.y_axis.axId = 100
    chart.x_axis.title = None #'t [s]'
    chart.y_axis.title = None #'T [°C]'
    chart1.y_axis.title = None #'U [V], I [A]'
    chart.y_axis.majorGridlines=None
    chart.y_axis.crosses = "max"
    
    chart1 += chart
    
    chart1.height = 9.5
    chart1.width = 19.3
    
    chart1.legend=None
    chart1.layout=Layout(
        manualLayout=ManualLayout(
            x=0, y=0,
            h=0.9, w=0.95,
        )
    )
       
    #wb['Poročilo'].add_image(Image('Graphic\Pic\Graph_legend.png'), 'L49')#,size=(100, 130)
    fp = 'Graphic\Pic\Graph_legend.png'
    im = PILImage.open(fp)
    im = im.resize((118, 63), PILImage.ANTIALIAS)
    im.save(fp=tempImg, format='png')
    wb['Poročilo'].add_image(Image(fp), 'L49')
    
    #wb['Poročilo'].add_image(Image('Graphic\Pic\Xxaxis_units.png'), 'H71')#,size=(50, 13)
    fp = 'Graphic\Pic\Xxaxis_units.png'
#    im = PILImage.open(fp)
#    im = im.resize((30, 15), PILImage.ANTIALIAS)
#    im.save(fp=tempImg, format='png')
    wb['Poročilo'].add_image(Image(fp), 'H71')
    
    #wb['Poročilo'].add_image(Image('Graphic\Pic\Y1axis_units.png'), 'C60')#,size=(13, 75)
    fp = 'Graphic\Pic\Y1axis_units.png'
#    im = PILImage.open(fp)
#    im = im.resize((15, 71), PILImage.ANTIALIAS)
#    im.save(fp=tempImg, format='png')
    wb['Poročilo'].add_image(Image(fp), 'C60')
    
    #wb['Poročilo'].add_image(Image('Graphic\Pic\Y2axis_units.png'), 'N61')#,size=(13, 50)
    fp = 'Graphic\Pic\Y2axis_units.png'
#    im = PILImage.open(fp)
#    im = im.resize((15, 118), PILImage.ANTIALIAS)
#    im.save(fp=tempImg, format='png')
    wb['Poročilo'].add_image(Image(fp), 'N61')
    
    wb['Poročilo'].add_chart(chart1, "B53")

    return wb

def write_800_1100_graph(wb, file_n, TC_dat_name):
#write functional graph

    chart = ScatterChart()
    
    xvalues = Reference(wb['Meritve 800-1100'], min_col=1, min_row=2, max_row=27502)
    values = Reference(wb['Meritve 800-1100'], min_col=4, min_row=2, max_row=27502)
    
    series = Series(values, xvalues,title='T surface')
    
    chart.series.append(series)
    
    chart.title = 'fun:'+file_n+' TC:'+TC_dat_name
    
    chart.x_axis.scaling.min = 0
    chart.x_axis.scaling.max = 275
    chart.y_axis.scaling.min = 600
    chart.y_axis.scaling.max = 1200
    
    wb['Meritve 800-1100'].add_chart(chart, "G3")
    
    #wb['Poročilo'].print_options.color = True

    return wb

#wb.save('document_template.xlsx')