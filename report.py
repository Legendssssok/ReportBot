import sys
from pyrogram import Client, filters
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


def get_reason(text):
    reasons = {
        "Report for child abuse": (InputReportReasonChildAbuse(), "This group involves child abuse content."),
        "Report for impersonation": (InputReportReasonFake(), "This group impersonates another person or entity."),
        "Report for copyrighted content": (InputReportReasonCopyright(), "This group shares copyrighted content."),
        "Report an irrelevant geogroup": (InputReportReasonGeoIrrelevant(), "This group targets irrelevant geographical areas."),
        "Reason for Pornography": (InputReportReasonPornography(), "This group contains pornographic material."),
        "Report an illegal drug": (InputReportReasonIllegalDrugs(), "This group promotes illegal drug activities."),
        "Report for offensive person detail": (InputReportReasonPersonalDetails(), "This group shares offensive personal details."),
        "Report for spam": (InputReportReasonSpam(), "This group sends spam messages."),
        "Report for Violence": (InputReportReasonViolence(), "This group promotes or glorifies violence."),
        "Report for other": (InputReportReasonOther(), "This group violates Telegram policies in other ways.")
    }
    return reasons.get(text, (InputReportReasonOther(), "Unknown reason provided."))


async def main(message):
    config = json.load(open("config.json"))
    reason_type, reason_message = get_reason(message)

    target = config['Target']
    for account in config["accounts"]:
        session_string = account["Session_String"]
        account_name = account['OwnerName']
        async with Client(name="Session", session_string=session_string) as app:
            try:
                peer = await app.resolve_peer(target)
                peer_id = peer.channel_id
                access_hash = peer.access_hash
                channel = InputPeerChannel(channel_id=peer_id, access_hash=access_hash)
            except Exception as e:
                print(f"Failed to resolve peer for {target}: {e}")
                continue

            report_peer = ReportPeer(
                peer=channel,
                reason=reason_type,
                message=reason_message
            )

            try:
                result = await app.invoke(report_peer)
                print(f"Successfully reported by account {account_name}: {result}")
            except Exception as e:
                print(f"Failed to report from account {account_name}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <reason>")
        sys.exit(1)

    reason = sys.argv[1]
    asyncio.run(main(message=reason))
