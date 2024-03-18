import os

from dotenv import load_dotenv

from app.resource.util.lang import get_current_language
from app.resource.util.mailer.templetes.base_template import BaseTempleteInterface

load_dotenv()


class PasswordReset(BaseTempleteInterface):
    def get_html_ja(self, verify_token: str, suppout_url: str) -> str:
        return f"""
        <!DOCTYPE html>
        <html lang="ja">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>パスワードリセットのURL</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #ffffff;
                        color: #4a4a4a;
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: auto;
                        padding: 20px;
                        background-color: #f8f8f8;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    h1 {{
                        color: #007bff;
                        font-size: 24px;
                    }}
                    p {{
                        font-size: 16px;
                        line-height: 1.5;
                    }}
                    .highlight {{
                        color: #007bff;
                        font-weight: bold;
                    }}
                    .verify-button a {{
                        display: inline-block;
                        color: #fff;
                        background-color: #007bff;
                        padding: 15px 30px;
                        text-decoration: none;
                        border-radius: 5px;
                        font-weight: bold;
                        box-shadow: 0 4px 8px rgba(0,123,255,.3);
                        transition: transform 0.3s ease, background-color 0.3s ease;
                    }}
                    .verify-button a:hover {{
                        background-color: #0056b3;
                        transform: translateY(-2px);
                        box-shadow: 0 6px 12px rgba(0,123,255,.4);
                    }}
                    .footer {{
                        margin-top: 20px;
                        font-size: 14px;
                        color: #aaa;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>パスワードリセットのご案内</h1>
                    <p>パスワードリセットのリクエストを受け付けました。以下のボタンをクリックして、パスワードのリセット手続きを完了してください。</p>
                    <div class="verify-button">
                        <a href="{self.get_verify_url(verify_token)}">パスワードをリセット</a>
                    </div>
                    <div class="footer">
                        <p>もしパスワードリセットをリクエストしていない場合、またはその他の質問がある場合は、いつでもお気軽に<a href="{suppout_url}">お問い合わせ</a>ください。</p>
                    </div>
                </div>
            </body>
        </html>
        """

    def get_html_en(self, verify_token: str, support_url: str) -> str:
        return f"""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Password Reset Notification</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #ffffff;
                        color: #4a4a4a;
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: auto;
                        padding: 20px;
                        background-color: #f8f8f8;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    h1 {{
                        color: #007bff;
                        font-size: 24px;
                    }}
                    p {{
                        font-size: 16px;
                        line-height: 1.5;
                    }}
                    .highlight {{
                        color: #007bff;
                        font-weight: bold;
                    }}
                    .verify-button a {{
                        display: inline-block;
                        color: #fff;
                        background-color: #007bff;
                        padding: 15px 30px;
                        text-decoration: none;
                        border-radius: 5px;
                        font-weight: bold;
                        box-shadow: 0 4px 8px rgba(0,123,255,.3);
                        transition: transform 0.3s ease, background-color 0.3s ease;
                    }}
                    .verify-button a:hover {{
                        background-color: #0056b3;
                        transform: translateY(-2px);
                        box-shadow: 0 6px 12px rgba(0,123,255,.4);
                    }}
                    .footer {{
                        margin-top: 20px;
                        font-size: 14px;
                        color: #aaa;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Password Reset Instructions</h1>
                    <p>We have received a request to reset your password. Please click the button below to proceed with the password reset process.</p>
                    <div class="verify-button">
                        <a href="{self.get_verify_url(verify_token)}">Reset Password</a>
                    </div>
                    <div class="footer">
                        <p>If you did not request a password reset, or if you have any other questions, please feel free to <a href="{support_url}">contact us</a> at any time.</p>
                    </div>
                </div>
            </body>
        </html>
        """

    def get_verify_url(self, verify_token: str) -> str:
        lang = get_current_language()
        return f"{os.getenv('BASE_URL')}/password-reset/{verify_token}/{lang}"
