import content
import datetime
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
import msal
class DailyDigestEmail:

    def __init__(self):
        self.content = {'quote': {'include': True, 'content': content.get_random_quote()},
                        'weather': {'include': True, 'content': content.get_weather_forecast()},
                        'twitter': {'include': True, 'content': content.get_twitter_trends()},
                        'wikipedia': {'include': True, 'content': content.get_wikipedia_article()}}

        self.recipients_list = ['sa522408@gmail.com',
                                'sa766959@gmail.com',
                                'saddam.groot@gmail.com',
                                'saddam.ahmad.cs.2016@mitmeerut.ac.in']

        self.sender_credentials = {'email': 'sa522408@gmail.com', # your sender email address
                                   'password': 'ievl wgnt bfaa iltu'} # your sender password

    """
    Send digest email to all recipients on the recipient list.
    """
    def send_email(self):
        # build email message
        msg = EmailMessage()
        msg['Subject'] = f'Daily Digest - {datetime.date.today().strftime("%d %b %Y")}'
        msg['From'] = self.sender_credentials['email']
        msg['To'] = ', '.join(self.recipients_list)

        # add Plaintext and HTML content
        msg_body = self.format_message()
        msg.set_content(msg_body['text'])
        msg.add_alternative(msg_body['html'], subtype='html')

        # secure connection with STMP server and send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.sender_credentials['email'],
                        self.sender_credentials['password'])
            server.send_message(msg)

    """
    Generate email message body as Plaintext and HTML.
    """
    def format_message(self):
        ##############################
        ##### Generate Plaintext #####
        ##############################
        text = f'*~*~*~*~* Daily Digest - {datetime.date.today().strftime("%d %b %Y")} *~*~*~*~*\n\n'

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            text += '*~*~* Quote of the Day *~*~*\n\n'
            text += f'"{self.content["quote"]["content"]["quote"]}" - {self.content["quote"]["content"]["author"]}\n\n'

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            text += f'*~*~* Forecast for {self.content["weather"]["content"]["city"]}, {self.content["weather"]["content"]["country"]} *~*~*\n\n'
            for forecast in self.content['weather']['content']['periods']:
                temp = str(float(forecast['temp'])-273)
                #print(temp)
                text += f'{forecast["timestamp"].strftime("%d %b %H%M")} - {temp}\u00B0C | {forecast["description"]}\n'
            text += '\n'

        # format Twitter trends
        if self.content['twitter']['include'] and self.content['twitter']['content']:
            text += '*~*~* Top Ten Twitter Trends *~*~*\n\n'
            for trend in self.content['twitter']['content'][0:10]: # top ten
                text += f'{trend["name"]}\n'
            text += '\n'

        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            text += '*~*~* Daily Random Learning *~*~*\n\n'
            text += f'{self.content["wikipedia"]["content"]["title"]}\n{self.content["wikipedia"]["content"]["extract"]}'
        
        #########################
        ##### Generate HTML #####
        #########################
        html = f"""<html>
    <body>
    <center>
        <h1>Daily Digest - {datetime.date.today().strftime('%d %b %Y')}</h1>
        """

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            html += f"""
        <h2>Quote of the Day</h2>
        <i>"{self.content['quote']['content']['quote']}"</i> - {self.content['quote']['content']['author']}
        """

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            html += f"""
        <h2>Forecast for {self.content['weather']['content']['city']}, {self.content['weather']['content']['country']}</h2> 
        <table>
                    """

            for forecast in self.content['weather']['content']['periods']:
                temp = str(float(forecast['temp'])-273)
                html += f"""
            <tr>
                <td>
                    {forecast['timestamp'].strftime('%d %b %H%M')}
                </td>
                <td>
                    <img src="{forecast['icon']}">
                </td>
                <td>
                    {temp}\u00B0C | {forecast['description']}
                </td>
            </tr>
                        """               

            html += """
            </table>
                    """

        # format Twitter trends
        if self.content['twitter']['include'] and self.content['twitter']['content']:
            html += """
        <h2>Top Ten Twitter Trends</h2>
                    """

            for trend in self.content['twitter']['content'][0:10]: # top ten
                html += f"""
        <b><a href="{trend['url']}">{trend['name']}</a></b><p>
                        """

        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            html += f"""
        <h2>Daily Random Learning</h2>
        <h3><a href="{self.content['wikipedia']['content']['url']}">{self.content['wikipedia']['content']['title']}</a></h3>
        <table width="800">
            <tr>
                <td>{self.content['wikipedia']['content']['extract']}</td>
            </tr>
        </table>
                    """

        # footer
        html += """
    </center>
    </body>
</html>
                """

        return {'text': text, 'html': html}

if __name__ == '__main__':
    email = DailyDigestEmail()

    ##### test format_message() #####
    print('\nTesting email body generation...')
    message = email.format_message()

    # print Plaintext and HTML messages
    print('\nPlaintext email body is...')
    print(message['text'])
    print('\n------------------------------------------------------------')
    print('\nHTML email body is...')
    print(message['html'])

    # save Plaintext and HTML messages to file
    with open('message_text.txt', 'w', encoding='utf-8') as f:
        f.write(message['text'])
    with open('message_html.html', 'w', encoding='utf-8') as f:
        f.write(message['html'])

    ##### test send_email() #####
    print('\nSending test email...')
    email.send_email()