import email
import imaplib
import os
import tempfile
from datetime import datetime
from email import utils

IMAP_SERVER = "imap.mail.me.com"
IMAP_PORT = 993
EMAIL_ACCOUNT = os.environ.get("EMAIL_ACCOUNT")
APP_PASSWORD = os.environ.get("APP_PASSWORD")


def connect_to_imap() -> imaplib.IMAP4_SSL:
    """Connect to iCloud IMAP."""
    assert EMAIL_ACCOUNT, "EMAIL_ACCOUNT environment variable not set"
    assert APP_PASSWORD, "APP_PASSWORD environment variable not set"
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
    mail.select("INBOX")
    return mail


def search_emails(
    mail: imaplib.IMAP4_SSL, sender: str, since_date: str | None = None
) -> list[str]:
    """Search for emails from the given sender since a date."""
    if since_date:
        since_date = (
            datetime.strptime(since_date, "%Y-%m-%d %H:%M:%S")
            .date()
            .strftime("%d-%b-%Y")
        )
        search_criteria = f'(FROM "{sender}" SINCE "{since_date}")'
    else:
        search_criteria = f'(FROM "{sender}")'

    _, data = mail.search(None, search_criteria)
    if not data or not data[0]:
        return []
    return data[0].split()


def download_pdf_attachment(
    mail: imaplib.IMAP4_SSL, email_id: str
) -> tuple[str | None, str | None]:
    """Retrun date and filepath of the PDF attachment from a given email."""
    _, data = mail.fetch(email_id, "(BODY.PEEK[])")
    response_part = data[0]
    if not response_part:
        return None, None
    if isinstance(response_part, tuple):
        raw_msg = response_part[1]
    else:
        raw_msg = response_part
    msg = email.message_from_bytes(raw_msg)
    date = utils.parsedate_to_datetime(msg["Date"]).date().strftime("%Y-%m-%d")
    for part in msg.walk():
        if part.get_content_type() != "application/pdf":
            continue
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            payload = part.get_payload(decode=True)
            assert isinstance(payload, bytes)
            tmp.write(payload)
            tmp.flush()
            return date, tmp.name
    return None, None
