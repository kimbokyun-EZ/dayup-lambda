import json
from urllib.parse import parse_qs

def lambda_handler(event, context):

    url = None

    print(parse_qs(event.get('body')).get('code')[0])

    # 인증코드
    code = parse_qs(event.get('body')).get('code')[0]

    url = "location.href = \'dayup://dayup.co.kr/auth/apple?code="+code +"\'"

    # HTML 요소를 완성하여 반환
    html_start = """
                <!DOCTYPE html>
                <html lang="ko">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Redirect Page</title>
                </head>
                """
    html_end = """
                </html>
                """
    html_result = html_start
    html_result += "<body>"
    html_result += "<script>"
    html_result += str(url)
    html_result += "</script>"
    html_result += "</body>"
    html_result += html_end

    return html_result

