# -*- coding: utf-8 -*-

""" a test module """
# -*- coding: utf-8 -*-
' a test module '

__author__ = 'lvxinjin'
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import sys

sys.path.append('..')
from api_test_dealer.config.config import *


class Email:
    def __init__(self, server, sender, password, receiver, title, message=None, path=None):
        """初始化Email
        :param title: 邮件标题，必填。
        :param message: 邮件正文，非必填。
        :param path: 附件路径，可传入list（多附件）或str（单个附件），非必填。
        :param server: smtp服务器，必填。
        :param sender: 发件人，必填。
        :param password: 发件人密码，必填。
        :param receiver: 收件人，多收件人用“；”隔开，必填。
        """
        self.title = title
        self.message = message
        self.files = path

        # self.msg = MIMEMultipart('related')

        self.server = server
        self.sender = sender
        self.receiver = receiver
        self.password = password

    def mail_send(self):
        try:
            f = open(self.files, 'rb')
            mail_body = f.read()
            f.close()
            mail = MIMEMultipart()
            mail.attach(MIMEText(mail_body, _subtype='html', _charset='utf-8'))
            # 构造附件att1，若是要带多个附件，可根据下边的格式构造
            att1 = MIMEText(open(self.files, 'rb').read(), 'base64', 'utf-8')
            att1['Content-Type'] = 'application/octet-stream'
            att1['Content-Disposition'] = 'attachment;filename="Test_report.html"'
            mail.attach(att1)
            mail['From'] = formataddr(['网易邮件', self.sender])
            mail['To'] = formataddr(['吕心劲', self.receiver])
            mail['subject'] = self.title
            try:
                server = smtplib.SMTP_SSL(self.server)  # 发件人邮箱中的SMTP服务器，端口是465
            except smtplib.SMTPAuthenticationError as e:
                logging.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
            else:
                try:
                    server.login(self.sender, self.password)  # 括号中对应的是发件人邮箱账号、邮箱密码
                except smtplib.SMTPAuthenticationError as e:
                    logging.exception('用户名密码验证失败！%s', e)
                else:
                    server.sendmail(self.sender, self.receiver, mail.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件18
                finally:
                    server.quit()  # 这句是关闭连接的意思
                    logging.info('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                                 '同时检查收件人地址是否正确'.format(self.title, self.receiver))
        except Exception as e:
            print(format(e))


if __name__ == '__main__':
    # report = REPORT_PATH + '\\report.html'
    report = report_file
    e = Email(title='接口测试测试报告',
              message='这是今天的测试报告，请查收！',
              receiver='610634528@qq.com',
              server='stmp.163.com',
              sender='l610634528@163.com',
              password='lvxj64518881',
              path=report
              )
    e.mail_send()
