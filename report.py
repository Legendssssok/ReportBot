import sys
from pyrogram import Client, filters
import asyncio
import json
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import *


def get_reason(text):
    if text == "Report for child abuse":
        return InputReportReasonChildAbuse()
    elif text == "Report for impersonation":
        return InputReportReasonFake()
    elif text == "Report for copyrighted content":
        return InputReportReasonCopyright()
    elif text == "Report an irrelevant geogroup":
        return InputReportReasonGeoIrrelevant()
    elif text == "Reason for Pornography":
        return InputReportReasonPornography()
    elif text == "Report an illegal durg":
        return InputReportReasonIllegalDrugs()
    elif text == "Report for offensive person detail":
        return InputReportReasonSpam()
    elif text == "Report for spam":
        return InputReportReasonPersonalDetails()
    elif text == "Report for Violence":
        return InputReportReasonViolence()

#report = app.send(report_peer)

async def main(message):
     try:
         config = json.load(open("config.json"))
     except Exception as e:
         print(f"Error loading config file: {e}")
         sys.exit(1)
     resportreaso = message
     resportreason = InputReportReasonPersonalDetails()
    # resportreason = input("whats ur pepoet reason: ")
     
     pee = "limitlesssmp"
     for account in config["accounts"]:
        string = "BADWZRoAnt4idW25Y-buW9YMT9HfpeHymo7Rg54qTvGr3jDfjgIPxPGDhHvROPb_-FfKymqqAbGUM9_49NSnISVT5J991pqRHDxByyHomB6c8WdbQeBJYI_-jG1PRHpMw6GxHq8JXe7BqCS9H1RdgVzF-KaWtckcLZD8a1goG-NI89LhHlhWCRnQzCeyzUGsYSdulQaTyZbwJ_G7CgRLw75omoyuUEaRBjIZrIW2AcOZw6Tm4buhvRcT-xjQZcNFT8--yo--hSEHoMYpJNgTl7YPo5Whrimqf2TZTFCmFSAWEeCQoXnAX-RbmiGgjWIZSmfypGvSnRaH5xJsjH1z0yq-KZHhBwAAAAAGfH9sAA"
        Name = "SASSY"
        async with Client(name="Session", session_string=string) as app:
            try:
                #await app.get_chat(-1001433138571)
                peer = await app.resolve_peer(pee)
                peer_id = peer.channel_id
                access_hash = peer.access_hash
                channel = InputPeerChannel(channel_id=peer_id, access_hash=access_hash)
            except Exception as e:
                print(f"Error 1: {e}")
            # elif dat.lower() == "user":
            #     peer = await app.resolve_peer(pee)
                
            #     user_id = int(peer.user_id)
            #     access_hash = str(peer.access_hash)
            #     channel = InputPeerUser(user_id=user_id, access_hash=access_hash)
            
            report_peer = ReportPeer(
                                        peer=channel, 
                                        reason=resportreason, 
                                        message=resportreaso
                                    )

            try:
                result = await app.invoke(report_peer)
                print(result, 'Reported by Account', Name)
                 
            except BaseException as e:
                print(f"Error2 : {e}")
                print("failed to report from :", Name)
            
                
if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <reason> <message>")
        sys.exit(1)

    # Get command-line arguments
    input_string = sys.argv[1]

    asyncio.run(main(message=input_string))
