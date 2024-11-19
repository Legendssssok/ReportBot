import asyncio
import json
import sys

from pyrogram import Client
from pyrogram.raw.functions.messages import Report
from pyrogram.raw.types import (
    InputReportReasonChildAbuse,
    InputReportReasonCopyright,
    InputReportReasonFake,
    InputReportReasonGeoIrrelevant,
    InputReportReasonIllegalDrugs,
    InputReportReasonOther,
    InputReportReasonPersonalDetails,
    InputReportReasonPornography,
    InputReportReasonSpam,
    InputReportReasonViolence,
)


def get_reason(text, message_ids):
    try:
        # Split message_ids and convert to integers
        message_ids_list = list(map(int, message_ids.split()))
    except ValueError:
        message_ids_list = [int(message_ids)]

    reasons = {
        "Report for child abuse": (InputReportReasonChildAbuse(), message_ids_list),
        "Report for impersonation": (InputReportReasonFake(), message_ids_list),
        "Report for copyrighted content": (
            InputReportReasonCopyright(),
            message_ids_list,
        ),
        "Report an irrelevant geogroup": (
            InputReportReasonGeoIrrelevant(),
            message_ids_list,
        ),
        "Reason for Pornography": (InputReportReasonPornography(), message_ids_list),
        "Report an illegal drug": (InputReportReasonIllegalDrugs(), message_ids_list),
        "Report for offensive person detail": (
            InputReportReasonPersonalDetails(),
            message_ids_list,
        ),
        "Report for spam": (InputReportReasonSpam(), message_ids_list),
        "Report for Violence": (InputReportReasonViolence(), message_ids_list),
        "Report for other": (InputReportReasonOther(), message_ids_list),
    }
    return reasons.get(text, (InputReportReasonOther(), message_ids_list))


async def main(message, message_ids):
    print(message, message_ids)
    config = json.load(open("config.json"))
    getreason, message_ids = get_reason(message, message_ids)  # Corrected here

    # Rest of your code...
    target = config["Target"]
    for account in config["accounts"]:
        session_string = account["Session_String"]
        account_name = account["OwnerName"]
        async with Client(name="Session", session_string=session_string) as app:
            try:
                peer = await app.resolve_peer(target)
            except Exception as e:
                print(f"Failed to resolve peer for {target}: {e}")
                continue

            try:
                report = Report(
                    peer=peer,
                    id=message_ids,
                    reason=getreason,
                    message="This user is sending spam messages",
                )
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
