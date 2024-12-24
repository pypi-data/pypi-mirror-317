import os
import base64
import mimetypes
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from finter.settings import logger


# 환경 변수에서 AWS 자격 증명 가져오기
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION', 'ap-northeast-2')  # 기본값 설정


def send_email(
        sender,  # Must be an email registered with Amazon SES.
        recipient,
        subject,
        body,  # 이메일 본문 내용
        cc_addresses=None,  # CC 수신자 리스트
        attachments=None,  # 첨부 파일 경로 리스트
        addon_subject=None,
):
    """
    이메일을 전송합니다.

    Args:
        sender (str): 발신자 이메일
        recipient (str or list): 수신자 이메일 또는 이메일 리스트
        subject (str): 이메일 제목
        body (str): 이메일 본문
        cc_addresses (list, optional): CC 수신자 이메일 리스트
        attachments (list, optional): 첨부 파일 경로 리스트
        addon_subject (str, optional): 추가 제목
    """
    if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY]):
        logger.error("AWS credentials not found in environment variables")
        raise ValueError("AWS credentials not properly configured")

    ses_client = boto3.client(
        "ses",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )

    # 수신자를 리스트로 변환
    if isinstance(recipient, str):
        recipient = [recipient]

    # CC 주소가 None이면 빈 리스트로 초기화
    cc_addresses = cc_addresses or []

    try:
        # MIME 메시지 생성
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipient)
        if cc_addresses:
            msg['CC'] = ', '.join(cc_addresses)

        # HTML 본문 생성
        addon_subject_str = "" if not addon_subject else f"{addon_subject}"
        body_html = f"""
            <html>
                <body>
                    <h2>{subject}</h2>
                    {addon_subject_str}
                    <div>{body}</div>
                </body>
            </html>
        """

        # HTML 본문 추가
        part_html = MIMEText(body_html, 'html')
        msg.attach(part_html)

        # 첨부 파일 처리
        if attachments:
            for file_path in attachments:
                if not os.path.exists(file_path):
                    logger.warning(f"Attachment not found: {file_path}")
                    continue

                filename = os.path.basename(file_path)
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type is None:
                    mime_type = 'application/octet-stream'

                with open(file_path, 'rb') as file:
                    part = MIMEApplication(file.read())
                    part.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(part)

        # SES로 이메일 전송
        response = ses_client.send_raw_email(
            Source=sender,
            Destinations=recipient + cc_addresses,
            RawMessage={'Data': msg.as_string()}
        )

    except (NoCredentialsError, PartialCredentialsError) as e:
        logger.error(f"Credentials error: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise
    else:
        logger.info(f"Email sent! Message ID: {response['MessageId']}")