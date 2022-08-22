from flask import Flask, request 
from flask import *
app = Flask(__name__)

@app.route('/') # this is the home page route
def hello_world(): # this is the home page function that generates the page code
    return "Hello world!"
    
@app.route('/test') # this is the home page route
def test_hosting(): # this is the home page function that generates the page code
    return "Application Hosted properly!!!"
    
@app.route('/InvYetToPay',methods=['POST'])
def InvYetToPay():
    
    req = request.get_json()
    tag = req["fulfillmentInfo"]["tag"]
    
    import cx_Oracle
    import json
    databasePort = 1556
    databaseHostName = '192.168.1.206'
    DatabaseServiceName = 'EBSVIS'
    DatabaseUsername = 'apex_ebs_extension'
    Databasepassword = 'Apex123'
    dsn = cx_Oracle.makedsn(
    databaseHostName,
    databasePort,
    service_name=DatabaseServiceName
    )
    print('initiated connection to oracle')
    conn = cx_Oracle.connect(
    user=DatabaseUsername,
    password=Databasepassword,
    dsn=dsn
    )
    c = conn.cursor()
    sql_query = 'SELECT count(PAYMENT_STATUS_FLAG) from apps.ap_invoices_all where PAYMENT_STATUS_FLAG=\'N\' and invoice_date>to_date(\'01-JUL-22\',\'dd-mon-yy\')'
    print(sql_query)
    c.execute(sql_query)
    print('sql query executed')
    headerrows = c.fetchall()
    print(headerrows[0][0])
    val=headerrows[0][0]
    if tag == "Number":
        text = "Number of invoices yet to pay are : " + str(val)
    res = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [
                            text
                        ]
                    }
                }
            ]
        }
    }

    # Returns json
    return res
    
@app.route('/SumOfAmountYetToPay',methods=['POST'])
def SumOfAmountYetToPay():

    req = request.get_json()
    tag = req["fulfillmentInfo"]["tag"]
    
    import cx_Oracle
    import json
    databasePort = 1556
    databaseHostName = '192.168.1.206'
    DatabaseServiceName = 'EBSVIS'
    DatabaseUsername = 'apex_ebs_extension'
    Databasepassword = 'Apex123'
    dsn = cx_Oracle.makedsn(
    databaseHostName,
    databasePort,
    service_name=DatabaseServiceName
    )
    print('initiated connection to oracle')
    conn = cx_Oracle.connect(
    user=DatabaseUsername,
    password=Databasepassword,
    dsn=dsn
    )
    c = conn.cursor()
    sql_query = 'select sum(invoice_amount) from apps.ap_invoices_all where PAYMENT_STATUS_FLAG=\'N\' and invoice_date>to_date(\'01-JUL-22\',\'dd-mon-yy\')'
    print(sql_query)
    c.execute(sql_query)
    print('sql query executed')
    headerrows = c.fetchall()
    print(headerrows[0][0])  
    val=headerrows[0][0]   
    if tag == "Amount":
        text = "Total amount to be paid is INR " + str(val)
    res = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [
                            text
                        ]
                    }
                }
            ]
        }
    }

    # Returns json
    return res




@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        
        req = request.get_json()

        tag = req["fulfillmentInfo"]["tag"]
        
        accountinfo= str(req["sessionInfo"]["parameters"]["accountinfo"])
        actionname=  str(req["sessionInfo"]["parameters"]["actionname"])
        periodname=  str(req["sessionInfo"]["parameters"]["periodname"])
          

        #number1= req["number1"]["resolvedValue"]
        if tag == "returnparameters":
            text = "Parameters:" + str(accountinfo)+str(periodname)+str(actionname)
                     
        
        else:
            text = f"There are no fulfillment responses defined for {tag} tag"

        # You can also use the google.cloud.dialogflowcx_v3.types.WebhookRequest protos instead of manually writing the json object
        # Please see https://googleapis.dev/python/dialogflow/latest/dialogflow_v2/types.html?highlight=webhookresponse#google.cloud.dialogflow_v2.types.WebhookResponse for an overview
    except Exception as e:
        text = str(e)
    
    finally:            
            
        res = {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [
                                text
                            ]
                        }
                    }
                ]
            }
        }

    # Returns json
    return res
    
   
if __name__ == '__main__':
  app.run() # This line is required to run Flask on repl.it