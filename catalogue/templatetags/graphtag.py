"""
SANSA-EO Catalogue - Graphtag template tag

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '16/08/2012'
__copyright__ = 'South African National Space Agency'

from django import template

#Pie3D chart
from pygooglechart import PieChart3D

register = template.Library()


@register.simple_tag
def gPieChart(data, labels, exclude_first):
    """
    Template tag that returns google chart URL

    data - actual data list
    labels - used for labeling data
    exclude_first - if 1 first record will be excluded, 0 first record is not
        excluded from graph
    """
    #parseData
    mydata, mykeys = parseData(data, labels)
    if exclude_first:
        mydata = mydata[1:]
        mykeys = mykeys[1:]

    chart = PieChart3D(600, 300)
    # Add some data
    chart.add_data(mydata)
    # Assign the labels to the pie data
    chart.set_pie_labels(mykeys)

    #set google chart set of colours
    chart.set_colours_within_series((
        '3366CC', 'DC3912', 'FF9900', '109618', '990099', '0099C6', 'DD4477',
        '66AA00', 'B82E2E', '316395', '994499', '22AA99', 'AAAA11', '6633CC',
        'E47100', '8B0707', '651067', '329262'))

    #return chart URL
    return chart.get_url()


def parseData(data, labels):
    keys = [key for key in labels]
    mydata = []
    mylabels = []
    for row in data:
        mydata.append(row['count'])
        mylabels.append(row[labels[keys[0]]])

    return mydata, mylabels
