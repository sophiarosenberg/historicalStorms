# !/usr/bin/env python
# Script to download .nc files from a THREDDS catalog directory

from xml.dom import minidom
from urllib.request import urlopen
from urllib.request import urlretrieve
import numpy as np
import os

# Divide the url you get from the data portal into two parts
# Everything before "catalog/"
# WIS DATA NEEDS TO BE CONVERTED TO GMT
server_url = 'https://chldata.erdc.dren.mil/thredds/'
buoys = ['ST63226']

def get_elements(url, tag_name, attribute_name):
    """Get elements from an XML file"""
    # usock = urllib2.urlopen(url)
    usock = urlopen(url)
    xmldoc = minidom.parse(usock)
    usock.close()
    tags = xmldoc.getElementsByTagName(tag_name)
    attributes = []
    for tag in tags:
        attribute = tag.getAttribute(attribute_name)
        attributes.append(attribute)
    return attributes


def main():
    request_url = 'catalog/wis/Atlantic/'
    #request_url = 'catalog/frf/geomorphology/DEMs/duneLidarDEM/'

    # Everything after "catalog/"
    for ff in range(len(buoys)):
        years = np.arange(1980,2021)

        for qq in years:

            url = os.path.join(server_url, request_url, buoys[ff], str(qq), 'catalog.xml').replace("\\", "/")
            #url = os.path.join(server_url,request_url,str(qq),'catalog.xml')

            print(url)
            catalog = get_elements(url, 'dataset', 'urlPath')
            files = []
            for citem in catalog:
                if (citem[-3:] == '.nc'):
                    files.append(citem)
            count = 0

            file_subset = files[0:12]

            for f in file_subset:
                count += 1
                file_url = server_url + 'fileServer/' + f
                file_prefix = file_url.split('/')[-1][:-3]
                file_name = file_prefix + '.nc'
                #file_name = file_prefix + '_' + str(count) + '.nc'

                print('Downloading file %d of %d' % (count, len(file_subset)))
                print(file_url)
                print(file_name)
                a = urlretrieve(file_url, file_name)
                print(a)

    return catalog, files, file_subset

main()
# Run main function when in comand line mode
if __name__ == '__main__':
    catalog, files, file_subset = main() 