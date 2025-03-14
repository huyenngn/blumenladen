import email
import imaplib
import os
import tempfile

IMAP_SERVER = "imap.mail.me.com"
IMAP_PORT = 993
EMAIL_ACCOUNT = os.environ.get("EMAIL_ACCOUNT")
APP_PASSWORD = os.environ.get("APP_PASSWORD")
EMAIL_FOLDER = os.environ.get("EMAIL_FOLDER")


def connect_to_imap() -> imaplib.IMAP4_SSL:
    """Connect to iCloud IMAP."""
    assert EMAIL_ACCOUNT
    assert APP_PASSWORD
    assert EMAIL_FOLDER
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
    mail.select(EMAIL_FOLDER)
    return mail


def search_emails(
    mail: imaplib.IMAP4_SSL, sender: str, since_date: str | None = None
) -> list[str]:
    """Search for emails from the given sender since a date."""
    if since_date:
        search_criteria = f'(FROM "{sender}" SINCE "{sender}")'
    else:
        search_criteria = f'(FROM "{sender}")'

    _, data = mail.search(None, search_criteria)
    return data[0].split()


def download_pdf_attachment(
    mail: imaplib.IMAP4_SSL, email_id: str
) -> tuple[str | None, tempfile._TemporaryFileWrapper | None]:
    """Retrun date and filepath of the PDF attachment from a given email."""
    _, data = mail.fetch(email_id, "(RFC822)")
    for response_part in data:
        if not isinstance(response_part, tuple):
            continue
        msg = email.message_from_bytes(response_part[1])
        date = msg["Date"]
        for part in msg.walk():
            if part.get_content_type() != "application/pdf":
                continue
            with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
                payload = part.get_payload(decode=True)
                tmp.write(payload)  # type: ignore
                return date, tmp
    return None, None
