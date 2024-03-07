from datetime import date
import redis
from PIL import Image
from flask import Flask, session, render_template_string,request,render_template,jsonify
from flask_session import Session
from flask_cors import CORS, cross_origin
from routesRumeno import route_methods as rm
import random, math
import auth_recheck as au
import db_setup
from flask_cors import CORS
import time
import skill_api

# Get the current timestamp
timestamp = time.time()

print("Current timestamp:", timestamp)

# Create the Flask application
app = db_setup.flask_app_creation()

CORS(app, support_credentials=True)
today = date.today()


server_session = Session(app)
app_routes = rm()

def create_connection_sql():
    print("working on creating client")
    import mysql.connector
    connection = mysql.connector.connect(host='localhost',
                                         database='test',
                                         user='root',
                                         password='')


    return connection

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route(app_routes["productCart"],methods = ["POST"])
@cross_origin(supports_credentials=True)
def cart_check():
    try:
        if request.method == 'POST':
            data = request.json
            connection = create_connection_sql()
            cursor = connection.cursor()
            print(data)
            purchase = "NA"
            sql_select_query = "SELECT * FROM usercart WHERE userID ='{}' and pID = '{}'".format(data['uID'],data['id'])
            print(sql_select_query)
            cursor.execute(sql_select_query)
            existing_product = cursor.fetchone()


            if existing_product:
                print(existing_product[6])
                count = str(int(existing_product[6]) + 1)
                update_query = "UPDATE usercart SET quantity = '{}' WHERE userID = '{}' and pID = '{}'".format(count,data["uID"],data["id"])
                print(update_query)
                cursor.execute(update_query)
                connection.commit()
                connection.close()
                return_data = {"msg": "success", "status": 200}
                return return_data
            else:
                sql_insert_Query = "INSERT INTO usercart (userID,pid,totalAmount,quantity,purchaseStatus,img,name,date)VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    data["uID"], data["id"], data["price"],data["amount"],purchase,data["img"],data["name"],today)
                # print(sql_select_Query)
                cursor.execute(sql_insert_Query)
                connection.commit()
                connection.close()
                return_data = {"msg":"success","status":200}
                return return_data
    except Exception as e:
        print("error",e)
        return_data = {"msg": "failed", "status": 0}
        return return_data


@app.route(app_routes["homeRecheck"])
def insert_email():
    return "success"

@app.route(app_routes["loginRumeno"],methods = ["POST"])
@cross_origin(supports_credentials=True)
def get_email():
    if request.method == 'POST':
        data = request.json
        print(data)
        connection = create_connection_sql()
        cursor = connection.cursor()
        if data["username"].isdigit():
            cursor.execute("SELECT * FROM users WHERE mobile='{}'".format(data["username"]))
        else:
            cursor.execute("SELECT * FROM users WHERE userName='{}' and pwd = '{}'".format(data["username"],data["password"]))
        existing_user = cursor.fetchone()
        print(existing_user)

        if existing_user:
            cursor.execute(
                "SELECT * FROM usercart WHERE userID='{}'".format(existing_user[1]))
            pid_data = cursor.fetchone()

            if pid_data:
            # print(pid_data[2])
                pid_list = pid_data[2]
            else:
                pid_list = "NA"
            print("Username exists. please allow login")
            user_data = {"msg": "Success","status":200,"userName":data["username"],"sessionId":"dvshfhdhwsdhgdjggecghdfhd","rId":"fkdgyfdagfduyfgshmfgfusagfjgfg","uID":existing_user[1],"pID":pid_list}
            return user_data
        else:
            user_data = {"msg":"failed"}
            return  user_data


@app.route(app_routes['signupRumeno'], methods=["POST"])
@cross_origin(supports_credentials=True)
def user_register():
    print(request.method)
    if request.method == 'POST':
        data = request.json
        print(data)
        connection = create_connection_sql()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE userName='{}'".format(data["fullName"]))
        existing_user = cursor.fetchone()

        if existing_user:
            print("Username already exists. Please choose a different username.")
            user_data = {"msg":"Failed","status":"0"}
            return user_data
        else:
            sql_query = "SELECT userID FROM users ORDER BY id DESC LIMIT 1"
            cursor.execute(sql_query)
            resid = cursor.fetchone()[0]
            connection.commit()
            usid = str(int(resid) + 1)
            sql_select_Query = "INSERT INTO users (userId,userName,pwd,address,email,mobile)VALUES ('{}','{}','{}','{}','{}','{}')".format(usid,data["fullName"],data["password"],data["address"]+"-"+data["state"]+"-"+data["city"],data["email"],data["mobile"])
            print(sql_select_Query)
            cursor.execute(sql_select_Query)
            connection.commit()
            connection.close()
            user_data = {"msg":"Success","status":200,"userName":data["fullName"],"userId":usid}
            return user_data

@app.route(app_routes['forgotPwd'], methods=["POST"])
@cross_origin(supports_credentials=True)
def forgot_user():
    print(request.method)
    if request.method == 'POST':
        data = request.json
        print(data)
        connection = create_connection_sql()
        cursor = connection.cursor()
        # cursor.execute("SELECT * FROM users WHERE mobile='{}'".format(data["num"]))
        # existing_user = cursor.fetchone()
        existing_user=""

        # if existing_user:
        try:
            print("Username exists sending sms for the otp",data["num"])
            skill_api.send_sms_twilio(num="+91"+data["num"])
            user_data = {"msg" : "success"}
            return user_data
        except Exception as e:
            return "false"

@app.route(app_routes['checkForgotPwd'], methods=["POST"])
@cross_origin(supports_credentials=True)
def forgot_user_check():
    print(request.method)
    if request.method == 'POST':
        data = request.json
        print(data)
        # connection = create_connection_sql()
        # cursor = connection.cursor()
        # cursor.execute("SELECT * FROM users WHERE mobile='{}'".format(data["fullName"]))
        # existing_user = cursor.fetchone()

        # if existing_user:
        print("Username exists sending sms for the otp")
        res = skill_api.check_otp_twilio(num=data["num"],otp_code=data["code"])
        if res == "approved":
            user_data = {"msg":"Success","status":"200"}
            return user_data
        else:
            user_data = {"msg": "failed,wrong otp", "status": "0"}
            return user_data



@app.route(app_routes["productDetails"], methods=["POST"])
@cross_origin(supports_credentials=True)
def view_products():
    if request.method == 'POST':
        product_dict = {"product_name":"rumeno_neneto","p_id":"x123rumenoneneto","total_fav":"51","reviews":"very helpful product","ratings":"4.5","description":"kbfkhdkhgsdhkfgdskgfhkagfhkagfhkafhgahvadhfadjhfvahjfahvchjvfhvcsahvcbavchjsavchjsavhjvvcsvcvchjasvchsvjsavchjsv","b_price":"Rs560"}
        data = request.json
        print(data)
        return product_dict


@app.route(app_routes["transcationDetails"], methods=["POST"])
@cross_origin(supports_credentials=True)
def view_transacations():
    try:
        if request.method == 'POST':
            if request.files:

                # Check if the POST request has a file part
                if 'file' not in request.files:
                    data = {"msg":"No file found","status":"500"}
                    return data

                file = request.files['file']

                # If the user does not select a file, the browser submits an empty file without a filename
                if file.filename == '':
                    data = {"msg": "No selected file", "status": "500"}
                    return data

                # Check if the file has an allowed extension
                if not allowed_file(file.filename):
                    data = {"msg": 'Invalid file extension. Allowed extensions are: ' + ', '.join(ALLOWED_EXTENSIONS), "status": "500"}
                    return data

                # Check if the file size is within the allowed limit
                if len(file.read()) > MAX_FILE_SIZE:
                    data = {"msg":'File size exceeds the allowed limit of {} MB'.format(MAX_FILE_SIZE / (1024 * 1024)),"status":"500"}
                    return data

                # Save the file to a desired location
                file.seek(0)  # Reset the file cursor to the beginning before saving
                file.save('uploads/' + file.filename)
                return_data = {"msg": "success", "status": 200,"data":"text"}
                return return_data
            else:
                data = request.json
                print(data)
                connection = create_connection_sql()
                cursor = connection.cursor()
                sql_query = "INSERT INTO transaction (userId,name,mobile,transactionID,totalAmount,date,time)VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(data["uID"],data["name"],data["mobile"],data["transactionID"],data["amount"],today,timestamp)
    except Exception as e:
        print(e)
        data = {"msg":"error","status":500}
        return data


@app.route(app_routes["dltcart"],methods=['POST','GET'])
def deleteCart():
    try:
        if request.method == "POST":
            data = request.json
            print(data)
            connection = create_connection_sql()
            cursor = connection.cursor()
            sql = "DELETE FROM usercart WHERE userID ='{}' and pID ='{}'".format(data['uID'],data['id'])
            cursor.execute(sql)
            connection.commit()
            connection.close()
            json_data = {"msg": "success", "status": "200"}
            print("success")
            return json_data
        else:
            json_data = {"msg": "failed", "status": "0"}
            return json_data

    except Exception as e:
        print(e)
        json_data = {"msg": "failed", "status": "0"}
        return json_data


@app.route(app_routes["logincart"],methods=['POST','GET'])
def logCart():
    try:
        if request.method == "POST":
            data = request.json
            print(data)
            connection = create_connection_sql()
            cursor = connection.cursor()
            sql = "SELECT * FROM usercart WHERE userID ='{}'".format(data['uID'])
            cursor.execute(sql)
            result = cursor.fetchall()
            print(len(result))
            print(result)
            connection.commit()
            connection.close()
            res_list = []
            for i in range(0,len(result)):
                res_data ={"id":result[i][2],"amount":result[i][6],"price":result[i][4],"img":result[i][7],"name":result[i][8],"uID":result[i][1]}
                res_list.append(res_data)
            json_data = {"msg": "success", "status": "200","data":res_list}
            print("success")
            return json_data
        else:
            json_data = {"msg": "failed", "status": "0"}
            return json_data

    except Exception as e:
        print(e)
        json_data = {"msg": "failed", "status": "0"}
        return json_data

# connection_string = "mongodb+srv://fusionwith:<skill7234>@clustersiw.ho3d55q.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)







