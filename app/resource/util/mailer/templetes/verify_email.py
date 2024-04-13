import os

from dotenv import load_dotenv

from app.resource.util.lang import get_current_language
from app.resource.util.mailer.templetes.base_template import BaseTempleteInterface

load_dotenv()


class VerifyEmail(BaseTempleteInterface):
    def get_html_ja(self, verify_token: str, account_name: str, suppout_url) -> str:
        return f"""
        <!DOCTYPE html>
        <html lang="ja">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>NowGoへの招待</title>
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
                    <h1>NowGoへようこそ！</h1>
                    <p>{account_name}さん</p>
                    <p>あなたをNowGoの世界に招待します。NowGoは、同じ興味や趣味を持つ人々が集まり、情報を共有し合えるプラットフォームです。ここでは、新しい友達を見つけたり、様々なトピックについて話し合ったりすることができます。</p>
                    <p>ご参加いただくには、<span class="highlight">下記のボタンをクリックしてメール認証を完了</span>させる必要があります。認証プロセスを通じて、安全なコミュニティ環境を保ち、あなたの体験を最大限に引き出すことができます。</p>
                    <div class="verify-button">
                        <a href="{self.get_verify_url(verify_token)}">認証する</a>
                    </div>
                    <div class="footer">
                        <p>
                            もし質問があれば、いつでもお気軽に
                            <a href="{suppout_url}">お問い合わせ</a>
                            ください。
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """

    def get_html_en(self, verify_token: str, account_name: str, support_url) -> str:
        return f"""
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to NowGo</title>
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
                    <h1>Welcome to NowGo!</h1>
                    <p>Dear {account_name},</p>
                    <p>You are invited to join the world of NowGo. NowGo is a platform where people with similar interests and hobbies come together to share information. Here, you can find new friends and discuss various topics.</p>
                    <p>To join us, you need to <span class="highlight">click the button below to complete your email verification</span>. Through the verification process, we maintain a safe community environment and maximize your experience.</p>
                    <div class="verify-button">
                        <a href="{self.get_verify_url(verify_token)}">Verify</a>
                    </div>
                    <div class="footer">
                        <p>
                            If you have any questions, please feel free to
                            <a href="{support_url}">contact us</a>
                            anytime.
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """

    def get_verify_url(self, verify_token: str) -> str:
        lang = get_current_language()
        return f"{os.getenv('BASE_URL')}/verify-email/{verify_token}/{lang}"
