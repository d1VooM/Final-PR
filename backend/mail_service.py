import smtplib
import imaplib
import email
from email.header import decode_header
from email.mime.text import MIMEText

# Данные для авторизации
EMAIL = "sasalozov2004@gmail.com"
PASSWORD = "xndephnanpqcmptv"

def send_smtp(subject, body, recipient):
    """Отправка письма через SMTP SSL (порт 465)"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = recipient
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, recipient, msg.as_string())
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

def get_last_email_imap():
    """Получение последнего письма через IMAP SSL"""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        
        # Поиск всех писем
        status, messages = mail.search(None, "ALL")
        if not messages[0]:
            mail.logout()
            return {"subject": "Ящик пуст", "body": ""}
            
        # Берем ID последнего сообщения
        last_msg_id = messages[0].split()[-1]
        res, msg_data = mail.fetch(last_msg_id, "(RFC822)")
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Декодируем тему письма
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                
                # Извлекаем текст
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            charset = part.get_content_charset() or 'utf-8'
                            body = part.get_payload(decode=True).decode(charset, errors='ignore')
                            break
                else:
                    charset = msg.get_content_charset() or 'utf-8'
                    body = msg.get_payload(decode=True).decode(charset, errors='ignore')
                
                mail.logout()
                return {"subject": subject, "body": body[:200]}
        
        mail.logout()
        return {"subject": "Не удалось прочитать", "body": ""}
    except Exception as e:
        print(f"IMAP Error: {e}")
        return {"subject": "Ошибка IMAP", "body": str(e)}import smtplib
import imaplib
import email
from email.header import decode_header
from email.mime.text import MIMEText

# Данные для авторизации
EMAIL = "sasalozov2004@gmail.com"
PASSWORD = "xndephnanpqcmptv"

def send_smtp(subject, body, recipient):
    """Отправка письма через SMTP SSL (порт 465)"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = recipient
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, recipient, msg.as_string())
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

def get_last_email_imap():
    """Получение последнего письма через IMAP SSL"""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        
        # Поиск всех писем
        status, messages = mail.search(None, "ALL")
        if not messages[0]:
            mail.logout()
            return {"subject": "Ящик пуст", "body": ""}
            
        # Берем ID последнего сообщения
        last_msg_id = messages[0].split()[-1]
        res, msg_data = mail.fetch(last_msg_id, "(RFC822)")
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Декодируем тему письма
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                
                # Извлекаем текст
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            charset = part.get_content_charset() or 'utf-8'
                            body = part.get_payload(decode=True).decode(charset, errors='ignore')
                            break
                else:
                    charset = msg.get_content_charset() or 'utf-8'
                    body = msg.get_payload(decode=True).decode(charset, errors='ignore')
                
                mail.logout()
                return {"subject": subject, "body": body[:200]}
        
        mail.logout()
        return {"subject": "Не удалось прочитать", "body": ""}
    except Exception as e:
        print(f"IMAP Error: {e}")
        return {"subject": "Ошибка IMAP", "body": str(e)}
