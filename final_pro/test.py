import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':   

    '''send_mail(
        '来自www.xxxxx.com的测试邮件',
        '欢迎访问www.xxxxx.com，这里是xx站点，本站专注于xx内容的分享！',
        'zt23571113@163.com',
        ['1481378837@qq.com'],)'''
    web_name = 'xxx'
    web_url = '2019'
    subject, from_email, to = 'xxx注册验证','zt23571113@163.com','zt23571113@163.com'
    text_content = '欢迎注册访问www.{}.com。您由于（可能是别人冒用您的邮箱）在{}使用了您的这个邮箱注册'.format(web_name,web_name)
    html_content = '''
                    <style type="text/css">
                    a:hover{{ color:red;}}
                    p:hover{{ color:blue }}
                    </style>
                    <p>欢迎注册访问www.{}.com。您（可能是别人冒用您的邮箱）在{}使用了这个邮箱注册</p>
                    <p><a href = "http://{}/confirm/?code={}">确认链接</a></p>
                    <p>请点击以上链接完成注册确认（如果这不是您的操作请忽略，若您持续受到此骚乱，请联系管理员）</p>
                    <p>有效期为三天</p>
                    '''.format(web_name,web_name,web_name,web_url,'test')
    msg = EmailMultiAlternatives(subject,text_content,from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    

