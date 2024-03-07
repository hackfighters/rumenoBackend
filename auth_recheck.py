import os
import math
import random
import smtplib
import bcrypt


def sent_sms():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    otp = OTP + " is your OTP"
    msg = otp

    # Download the helper library from https://www.twilio.com/docs/python/install
    # Download the helper library from https://www.twilio.com/docs/python/install
    import os
    from twilio.rest import Client

    # Set environment variables for your credentials
    # Read more at http://twil.io/secure
    account_sid = "AC9ea7ea7329ea508b6667396e97a5587c"
    auth_token = "39d712cfaeb93780b090e72f807ce6ba"
    verify_sid = "VA7b48a8fbd67352d9a4027f1c86dd0449"
    verified_number = "+918269907262"

    client = Client(account_sid, auth_token)

    verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=verified_number, channel="sms")
    print(verification.status)

    otp_code = otp_code = input("Please enter the OTP:")
    print(otp_code)

    verification_check = client.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=verified_number, code=otp_code)
    print(verification_check.status)

    # s = smtplib.SMTP('smtp.gmail.com', 587)
    # s.starttls()
    # s.login("fusion.with@skillintelligence.tech", "You app password")
    # emailid = input("Enter your email: ")
    # s.sendmail('&&&&&&&&&&&', emailid, msg)
    # a = input("Enter Your OTP >>: ")
    # if a == OTP:
    #     print("Verified")
    # else:
    #     print("Please Check your OTP again")
    return otp_code
def check_user_login(conn,user):
    user = conn.find_one({'username': user["username"]})
    if user and bcrypt.checkpw(user["password"].encode('utf-8'), user['password']):
        return True
    else:
        return False

if __name__ == "__main__":
    res = sent_sms()
    print(res)