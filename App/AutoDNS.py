# Functions for updating IONOS domain records(A)
import requests
import json
import re
from datetime import datetime
from time import sleep
import getopt
import sys

# Get Public IP


def getPubIP():
    return (
        str(requests.get("https://ifconfig.me").content)
        .replace("b'", "")
        .replace("'", "")
    )


# Get DNS Zones
def getZones(Key: str) -> json:
    __headers = {"X-Api-Key": f"{Key}"}
    return json.loads(
        requests.get(
            "https://api.hosting.ionos.com/dns/v1/zones/", headers=__headers
        ).content
    )

# input (PerZoneJson, inscopeZones)
# Output bool
def valZoneNew(Input: json, Targets: list) -> bool:
    # Input["name"] == name of found Zone
    for Tar in Targets:
        try:
            re.search(Input["name"], Tar).group(0)
            __inScope__ = True
        except:
            __inScope__ = False
        if __inScope__:
            break
    return __inScope__


# Valaidate Zone is Inscope
def valZone(Input: json, Target: str) -> bool:
    iName = str(Input["name"])
    try:
        re.search(iName, Target).group(0)
        __inScope__ = True
    except:
        __inScope__ = False
    return __inScope__


def getARecords(Key: str, ZoneID: str) -> json:
    __headers__ = {"X-Api-Key": f"{Key}"}
    #allRecs = []
    for aRec in json.loads(
        requests.get(
            f"https://api.hosting.ionos.com/dns/v1/zones/{ZoneID}", headers=__headers__
        ).content
    )["records"]:
        if str(aRec["type"]) == "A":
            try:
                if allRecs:
                    allRecs.update(aRec)
            except:
                allRecs = [aRec]
    if not allRecs:
        allRecs = 0
    return allRecs


def updateRec(Key: str, ZoneID: str, RecID: str, Input: json):
    __headers__ = {"X-Api-Key": f"{Key}", "Content-Type": "application/json"}
    return json.loads(
        requests.put(
            f"https://api.hosting.ionos.com/dns/v1/zones/{ZoneID}/records/{RecID}",
            json=Input,
            headers=__headers__,
        ).content
    )


def VLog(MSG: str = "Message"):
    Time = (datetime.now()).isoformat(timespec="seconds")
    print(f"[{Time}]-[{MSG}]")


def Idle(Unit: str, Amount: int):
    if Unit == "hours":
        __unit__ = "Hour"
        wTime = 3600 * Amount
    elif Unit == "days":
        __unit__ = "Day"
        wTime = 86400 * Amount
    else:
        Exception(
            f"""Invaid Unit Provided ["{Unit}"], the accepted options are h = Hours and d = Days"""
        )
    VLog(f"Entering Idle-Mode for {Amount} {__unit__}(s)")
    sleep(int(wTime))


def Startup():
    print(open("logo").read())


def getArgs():
    argList = sys.argv[1:]
    optS = "u:a:s:b:v:"
    optL = ["unit=", "amount=", "scope=", "pubkey=", "prvkey="]
    try:
        args, scrapValues = getopt.getopt(argList, optS, optL)
        Scope = []
        for cArg, cVal in args:
            if cArg in ("-u", "--unit"):
                Unit = cVal
            elif cArg in ("-a", "--amount"):
                Amount = cVal
            elif cArg in ("-s", "--scope"):
                Scope.append(cVal)
            elif cArg in ("-b", "--pubkey"):
                pbKey = cVal
            elif cArg in ("-v", "--prvkey"):
                pvKey = cVal
            else:
                Exception(f"Invalid Argument provided '{argList}'")
    except:
        Exception(
            f"Error proccesing arguments. Please create bug report if this continues.")
    return Unit, Amount, Scope, pbKey, pvKey, scrapValues


def strMask(Input: str) -> str:
    chrList = list(Input)
    count = len(chrList) - round(((len(chrList)) / 4) + 1)
    while count >= 0:
        chrList[count] = "*"
        count += -1
    return "".join(chrList)
