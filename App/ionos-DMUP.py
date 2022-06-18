# Updates IP Address(s) of Domain(s) in IONOS's Public Domain Registry
# Docker Fork

from AutoDNS import *

# Captures CLI Arguments
FreqUnt, FreqAmt, Zones, Pub_key, Prv_key = getArgs()

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

        # Convert Zones to array
        Zones = [Zones]

        # Loops Per Zone (Domains)
        for dZone in Zones:  # Zones set to be Updated
            #print(Zones, dZone); exit()
            # Validates Domain is Inscope for update
            if valZone(rZone, dZone):
                VLog(f"""Zone '{(rZone["name"])}' is In-Scope for Update""")
                # Gets Domains in the Zone
                aRec = getARecords(Auth_key, rZone["id"])
                # Checks if IP on Record is Stale
                if str(aRec["content"]) != PubIP:
                    VLog(f"""Zone '{(rZone["name"])}' is Stale ({aRec["content"]})""")
                    # Updates IP
                    aRec["content"] = PubIP
                    updateRec(Auth_key, rZone["id"], aRec["id"], aRec)
                    VLog(f"""Zone '{(rZone["name"])}' has been Updated""")
                else:
                    VLog(f"""Zone '{(rZone["name"])}' is already Up-To-Date""")
            else:
                VLog(f"""Zone '{(rZone["name"])}' is Out-of-Scope""")
            # Breaks loop when done with Domain/Record updating
            break
        # Ensures Parent Loop isnt broken
        continue
    # Idles until next cycle
    Idle(FreqUnt, int(FreqAmt))