#!/usr/bin/python
# -*- coding: utf-8 -*-
# glenn@sensepost.com_
# snoopy_ng // 2013
# By using this code you agree to abide by the supplied LICENSE.txt

import sys
import os
from MaltegoTransform import *
import logging
from datetime import datetime
from sqlalchemy import create_engine, MetaData, select, and_
from transformCommon import *
from base64 import b64decode
from xml.sax.saxutils import escape
import re
from wigle_api import Wigle

logging.basicConfig(level=logging.DEBUG,filename='/tmp/maltego_logs.txt',format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
illegal_xml_re = re.compile(u'[\x00-\x08\x0b-\x1f\x7f-\x84\x86-\x9f\ud800-\udfff\ufdd0-\ufddf\ufffe-\uffff]')

def main():
#    print "Content-type: xml\n\n";
#    MaltegoXML_in = sys.stdin.read()
#    logging.debug(MaltegoXML_in)
#    if MaltegoXML_in <> '':
#     m = MaltegoMsg(MaltegoXML_in)

    TRX = MaltegoTransform()
    TRX.parseArguments(sys.argv)
    lat = TRX.getVar("latitude")
    lng = TRX.getVar("longitude")
    address = TRX.getVar("streetaddress")

    logging.debug(lat)
    logging.debug(address)

    wig=Wigle("sourkiss","sourkiss","glenn@sensepost.com")
    wig.login()
    ssids = wig.fetchNearbySSIDs(lat=lat,lng=lng,address=address)


    for s,coords in ssids.iteritems():
        ssid=escape(s)
        ssid = illegal_xml_re.sub('', ssid)
        lat,lng,dist = coords

        NewEnt=TRX.addEntity("snoopy.SSID", ssid)
        NewEnt.addAdditionalFields("ssid","ssid", "strict",ssid)
        NewEnt.addAdditionalFields("lat","latitude", "strict",str(lat))
        NewEnt.addAdditionalFields("long","longitude", "strict",str(lng))
        NewEnt.setWeight(int((1.0/dist)*500))
        NewEnt.addAdditionalFields("dist","distance", "strict",str(dist))

    TRX.returnOutput()

main()
#me = MaltegoTransform()
#me.addEntity("maltego.Phrase","hello bob")
#me.returnOutput()                
