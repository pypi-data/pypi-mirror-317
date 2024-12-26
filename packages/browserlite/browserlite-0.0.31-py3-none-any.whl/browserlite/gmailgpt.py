from .app import chatgpt,huggingchat
from gmaillite import automail


def gmailgpt():
    def fun(subject,body):
        if ',' in subject:
            s,t = subject.split(',')
            t=int(t)
        else:
            s=subject
            t=80

        subject = s.lower().strip()
        if subject=='chatgpt' and isinstance(t,int):
            return chatgpt(body,sleep=t)

        elif subject=='huggingchat' and isinstance(t,int):
            return huggingchat(body,sleep=t)

        else:
            return 'Invalid subject or sleep time issue ( ex: chatgpt,1 or huggingchat,3 or chatgpt) '
    return automail(fun)