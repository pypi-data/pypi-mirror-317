import pytest
from python_plugins.email.smtp import SmtpSSL


@pytest.mark.skip(reason="password is empty")
def test_email(fake):
    host = "smtp.qiye.aliyun.com"
    port = "465"
    user = "test@ojso.com"
    # set password
    password = ""

    # set to's email
    to = "test@ojso.com"
    content = fake.paragraph()
    data = {
        "to": to,
        "subject": "test." + fake.sentence(),
        "content": content,
    }

    s = SmtpSSL(host, port, user, password)
    r = s.send_emsg(data)

    assert not r
