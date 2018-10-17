import functools
import ssl
import urllib.request
import gzip
import json
from flask import (
    Blueprint, flash, g, redirect, request, session, url_for
)
from werkzeug.exceptions import abort

from .db import get_db


bp = Blueprint('station', __name__, url_prefix='/station')

@bp.route('/')
def index():
    stationData = getUbikeJson()
    if type(stationData) == dict:
        #TODO: print more clear
        return json.dumps(stationData)
    else:
        return stationData

@bp.route('/<int:stationNo>')
def getBystationNo(stationNo):
    
    if not isStation(stationNo):
        abort(404)
    else:
        stationNoStr = str(stationNo).zfill(4)
        stationData = getUbikeJson()
        if type(stationData) == dict:
            return json.dumps( stationData["retVal"][stationNoStr] )
        else:
            return stationData

@bp.route('/<string:stationName>')
def getByStationName(stationName):
    #TODO: how to contain spaces in url

    stationData = getUbikeJson()
    for cell in stationData["retVal"].values():
        if stationName == cell["sna"] or stationName == cell["snaen"]:
            return json.dumps(cell)
    
    abort(404)


def getUbikeJson():
    context = ssl._create_unverified_context()
    ubikeTaipeiApi = "http://data.taipei/youbike"

    request = urllib.request.Request(
        ubikeTaipeiApi,
        headers = {
            "Accept-Encoding": "gzip"
        }
    )

    response = urllib.request.urlopen(request, context=context)

    if response.status == 200:
        gzipFile = gzip.GzipFile(fileobj=response)
        return json.loads( gzipFile.read() )
    else:
        return "Ubike Server Error"


def isStation(stationNo):

    db = get_db()

    station = db.execute(
        'SELECT *'
        ' FROM stations WHERE stationNo = ?',
        (stationNo, )
    ).fetchone()

    return station is not None
