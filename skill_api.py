def send_sms_twilio(num):
    # Download the helper library from https://www.twilio.com/docs/python/install
    import os
    from twilio.rest import Client

    # Set environment variables for your credentials
    # Read more at http://twil.io/secure
    account_sid = "AC9ea7ea7329ea508b6667396e97a5587c"
    auth_token = "39d712cfaeb93780b090e72f807ce6ba"
    verify_sid = "VA7b48a8fbd67352d9a4027f1c86dd0449"
    # verified_number = "+919644877965"
    verified_number = num
    print(verified_number)
    client = Client(account_sid, auth_token)

    verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=verified_number, channel="sms")
    print(verification.status)






def check_otp_twilio(num,otp_code):
    import os
    from twilio.rest import Client

    # Set environment variables for your credentials
    # Read more at http://twil.io/secure
    account_sid = "AC9ea7ea7329ea508b6667396e97a5587c"
    auth_token = "39d712cfaeb93780b090e72f807ce6ba"
    verify_sid = "VA7b48a8fbd67352d9a4027f1c86dd0449"
    verified_number = num
    client = Client(account_sid, auth_token)
    verification_check = client.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=verified_number, code=otp_code)
    print(verification_check.status)
    return  verification_check.status


# send_sms_twilio(num="8269907262")
# check_otp_twilio(num="8269907262",otp_code="")