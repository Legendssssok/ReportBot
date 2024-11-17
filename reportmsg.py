import sys
from pyrogram import Client, enums, filters
import asyncio
import json
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import (
    InputReportReasonChildAbuse,
    InputReportReasonFake,
    InputReportReasonCopyright,
    InputReportReasonGeoIrrelevant,
    InputReportReasonPornography,
    InputReportReasonIllegalDrugs,
    InputReportReasonSpam,
    InputReportReasonPersonalDetails,
    InputReportReasonViolence,
    InputReportReasonOther,
    InputPeerChannel
)

from pyrogram.raw.functions.messages import Report

def get_reason(text, message_ids):
    ok = []
    try:
        ok = message_ids.split()
    except:
        ok = [message_ids]
    reasons = {
        "Report for child abuse": (InputReportReasonChildAbuse(), ok),
        "Report for impersonation": (InputReportReasonFake(), ok),
        "Report for copyrighted content": (InputReportReasonCopyright(), ok),
        "Report an irrelevant geogroup": (InputReportReasonGeoIrrelevant(), ok),
        "Reason for Pornography": (InputReportReasonPornography(), ok),
        "Report an illegal drug": (InputReportReasonIllegalDrugs(), ok),
        "Report for offensive person detail": (InputReportReasonPersonalDetails(), ok),
        "Report for spam": (InputReportReasonSpam(), ok),
        "Report for Violence": (InputReportReasonViolence(), ok),
        "Report for other": (InputReportReasonOther(), ok)
    }
    return reasons.get(text, (InputReportReasonOther(), ok))


async def main(message, message_ids):
    print(message, message_ids)
    config = json.load(open("config.json"))
    getreason, message_ids = get_reason(int(message), message_ids)

    target = config['Target']
    for account in config["accounts"]:
        session_string = account["Session_String"]
        account_name = account['OwnerName']
        async with Client(name="Session", session_string=session_string) as app:
            try:
                peer = await app.resolve_peer(target)
            except Exception as e:
                print(f"Failed to resolve peer for {target}: {e}")
                continue

            try:
                report = Report(peer=peer, id=message_ids, reason=getreason, message="This user is sending spam messages")
                result = await app.invoke(report)
                print(f"Successfully reported by account {account_name}: {result}")
            except Exception as e:
                print(f"Failed to report from account {account_name}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python your_script.py <reason>")
        sys.exit(1)

    reason = sys.argv[1]
    message_ids = sys.argv[2]
    asyncio.run(main(message=reason, message_ids=message_ids))
