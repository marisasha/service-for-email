from datetime import datetime
import json
import imaplib
import email
import chardet
import asyncio
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import F
from django.db.models.functions import Cast
from django.db.models import CharField

from django_app import models


class EmailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.fetch_emails()

    async def disconnect(self, close_code):
        pass

    async def fetch_emails(self):
        user = self.scope["user"]
        profile = await sync_to_async(models.Profile.objects.get)(user=user)
        mail_login = profile.mail_login
        mail_password = profile.mail_password

        email_data = await asyncio.to_thread(
            self.fetch_emails_sync, mail_login, mail_password, user
        )

        await self.send(json.dumps({"emails": email_data}))

    def fetch_emails_sync(self, mail_login, mail_password, user):

        mail = imaplib.IMAP4_SSL("imap.mail.ru")
        mail.login(mail_login, mail_password)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()
        email_data = []

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    text = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                text = part.get_payload(decode=True).decode(
                                    part.get_content_charset(), errors="replace"
                                )
                    else:
                        text = msg.get_payload(decode=True).decode(
                            msg.get_content_charset(), errors="replace"
                        )

                    subject, encoding = email.header.decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        if encoding == "unknown-8bit":
                            subject = subject.decode("latin-1", errors="replace")
                        elif encoding:
                            subject = subject.decode(encoding, errors="replace")
                        else:
                            detected = chardet.detect(subject)
                            subject = subject.decode(
                                detected["encoding"], errors="replace"
                            )

                    sender, encoding = email.header.decode_header(msg.get("From"))[0]
                    if isinstance(sender, bytes):
                        if encoding == "unknown-8bit":
                            sender = sender.decode("latin-1", errors="replace")
                        elif encoding:
                            sender = sender.decode(encoding, errors="replace")
                        else:
                            detected = chardet.detect(sender)
                            sender = sender.decode(
                                detected["encoding"], errors="replace"
                            )

                    raw_date = msg["Date"]
                parsed_date = email.utils.parsedate_tz(raw_date)

                if parsed_date:
                    d = datetime.fromtimestamp(email.utils.mktime_tz(parsed_date))

                    date_str = d.strftime("%Y-%m-%d %H:%M:%S")

                email_data.append({"s": subject, "f": sender, "d": date_str, "t": text})

                models.Message.objects.create(
                    author=sender,
                    topic=subject,
                    date_send=date_str,
                    text=text,
                    user=user,
                )

            mail.store(email_id, "+FLAGS", "\\Seen")

        messages = list(
            models.Message.objects.filter(user=user)
            .annotate(
                date_send_str=Cast(F("date_send"), output_field=CharField()),
                date_added_str=Cast(F("date_added"), output_field=CharField()),
            )
            .values("author", "topic", "date_send_str", "date_added_str", "text")
            .order_by("-date_send_str")
        )
        return messages
