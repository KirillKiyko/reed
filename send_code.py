import smtplib

from code_generator import id_generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_code(email):
    code = id_generator()

    fromaddr = 'support@reedit.io'
    toaddrs = '{}'.format(email)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Reed"
    msg['From'] = fromaddr
    msg['To'] = toaddrs

    username = 'reedautoreply@gmail.com'
    password = 'Reed@dM!n@2017'

    text = "Verification code:\n{code}".format(code=code)
    html = """\
            <html xmlns="http://www.w3.org/1999/xhtml">
              <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <title>Verification</title>
              </head>
              <body>
                <table width="95%" border="0" cellspacing="0" cellpadding="0" >
                  <tr>
                    <td align="center" valign="top" bgcolor="#f6f3e4"><br>
                    <br>
                    <table width="600" border="0" cellspacing="0" cellpadding="0" >
                      <tr>
                        <td align="center" valign="top" style="padding-left:13px; padding-right:13px;">
                        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #fff;">
                
                          <tr>
                            <td align="left" valign="top" style="font-family: 'Libre Franklin', sans-serif; font-size:48px; background-color:#19446a;">

                              <img src="https://github.com/KirillKiyko/reed_logo/blob/master/reed_logo.png?raw=true" alt="" width="30%" style="padding-top:10px;">
                            </td>
                          </tr>

                          <tr align="center" valign="bottom" style="font-size: 24px;font-family: 'Libre Franklin', sans-serif;">
                          
                            <td>
                             <br>
                              <b style="color: #19446a;">Don't share this code with anyone.</b><br>
                                <b style="color: #19446a;">Verification code:</b><br>
                                <br>
                              <b style="font-size: 50px; color: #19446a;">{code}</b>
                            </td>
                          </tr>

                          <tr>
                            <td>
                              <br>
                              <br>
                            </td>
                          </tr>
                          
                        </table>
                        </td>
                      </tr>
                    </table>
                    <br>
                    <br>
                </td>
                  </tr>
                </table>
              </body>
            </html>
            """.format(code=code)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
      server = smtplib.SMTP('smtp.gmail.com:587')
      server.ehlo_or_helo_if_needed()
      server.starttls()
      server.login(username, password)
      server.sendmail(fromaddr, toaddrs, msg.as_string())
      server.quit()

      return code
    except Exception:
      return 'Incorrect email'