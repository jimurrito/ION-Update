# Updates IP Address(s) of Domain(s) in IONOS's Public Domain Registry

from AutoDNS import *

# gets CLI args
FreqUnt, FreqAmt, Zones, Pub_key, Prv_key, Scrap = getArgs()

# Application Boot Scren
Startup()

# Config Dump
print(f"""\n[CURRENT CONFIGURATION]
[Scope]
{Zones}
[Keys]
Public key: {strMask(Pub_key)}
Private key: {strMask(Prv_key)}
[Idle-Config]
Unit: {FreqUnt}
Amount: {FreqAmt}
""")

# Generate Auth key
Auth_key = Pub_key + "." + Prv_key
# Main Loop
while True:
    VLog("Application Startup")
    # Get Public IP
    PubIP = getPubIP()
    VLog(f"""Current Public IP ({PubIP})""")
    # Get DNS Zones
    rawZones = getZones(Auth_key)
    VLog("DNS Zones grabbed from Provider")
    # Loops PerZone
    for rZone in rawZones:  # The Zones Present in Ionos
        # Validates Domain is Inscope for update
        if valZoneNew(rZone, Zones):
            VLog(f"""Zone '{(rZone["name"])}' is In-Scope for Update""")           
            # Gets Domains (aRecords) in the Zone
            aRecords = getARecords(Auth_key, rZone["id"])
            #print(aRecords)
            if aRecords:
                VLog("(A) Records found")
                for aRec in aRecords:
                    #print(aRec)
                    # Checks if IP on Record is Stale
                    if aRec["content"].find(PubIP) == -1:
                        VLog(f"""Zone '{(rZone["name"])}' is Stale ({aRec["content"]})""")
                        # Updates IP
                        aRec["content"] = PubIP
                        updateRec(Auth_key, rZone["id"], aRec["id"], aRec)
                        VLog(f"""Zone '{(rZone["name"])}' has been Updated""")
                    else:
                        VLog(f"""Zone '{(rZone["name"])}' is already Up-To-Date""")
            else:
                VLog("No (A) Records Found")
        else:
            VLog(f"""Zone '{(rZone["name"])}' is Out-of-Scope""")
            #break
        # Idles until next cycle
    Idle(FreqUnt, int(FreqAmt))