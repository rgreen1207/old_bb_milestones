from app.models.messages import MessageModelDB
from time import time

system_sms = [
    MessageModelDB( #Anniversary Text
        uuid="95d99f2dbfd5238565543081ecfecff47ec264186608550fcdce1c2f",
        name="anniversary text",
        message_uuid=None,
        client_uuid=None,
        message_9char="mfuyFko9K",
        program_9char=None,
        segment_9char=None,
        message_type=1,
        channel=2,
        status=1,
        body="$fname! Congrats on your $anniv year anniversary! Please enjoy this Blueboard $award reward in appreciation of you and all the magic you bring to our team.",
        time_created=int(time()),
        time_updated=int(time())
    ),
    MessageModelDB( #Birthday Text
        uuid="c9091e439dc2495a8b1f7aa0f6682ba7600089a18e609c2a146b25ae",
        name="birthday text",
        message_uuid=None,
        client_uuid=None,
        message_9char="j6zyFko9x",
        program_9char=None,
        segment_9char=None,
        message_type=2,
        channel=2,
        status=1,
        body="Happy Birthday $fname! $company is sending you a Blueboard $award reward for your birthday!",
        time_created=int(time()),
        time_updated=int(time())
    )
]