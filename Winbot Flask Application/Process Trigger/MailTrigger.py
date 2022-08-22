from imap_tools import MailBox, AND
import requests
import json
import pandas as pd
import cx_Oracle
import keyring

def getAuthentication(granttype, clientid, clientsecret, clientscope, OrchestratorURL):
    print("inside get auth")
    url = "" + OrchestratorURL + "/identity/connect/token"
    data = "grant_type="+granttype+"&client_id="+clientid+"&client_secret="+clientsecret+"&scope="+clientscope
    # url = "https://winfo101.winfosolutions.com/api/Account/Authenticate"

    # data = {"tenancyName": "" + tenantName + "", "usernameOrEmailAddress": "" + username + "","password": "" + password + ""}

    header = {"content-type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=header, verify=False)
    print(str(response.status_code))

    r_json = response.json()

    key = r_json["access_token"]
    print("key is " + str(key))
    return key


def getRobotId(key, inputRobotEnv, folderid, OrchestratorUrl):
    print("in get robotid orche url-->" + OrchestratorUrl)

    url = "" + OrchestratorUrl + "/odata/Robots"
    print(url)
    print(key)

    header = {"content-type": "application/json",
              "Authorization": "Bearer " + str(key),
              "X-UIPATH-OrganizationUnitId": ""+folderid+""}    #folder id is 2 for test env
    response = requests.get(url, headers=header, verify=False)
    print(str(response.status_code))

    r_json = response.json()
    print(str(r_json))
    val = json.dumps(r_json['value'])
    print("here")
    print(val)
    resp_dict = json.loads(val)
    for i in resp_dict:
        print("in for-->" + inputRobotEnv)
        if inputRobotEnv in i['RobotEnvironments']:

            print("in if")

            robotId = i['Id']
            robotName = str(i['Name'])
            print(
                "now let us check whether status is available or not for this following robot-->" + robotName + " " + str(
                    robotId))
            robot_status = getRobotStatus(key, robotId, folderid, OrchestratorUrl)
            print("stats-->" + robot_status)
            if robot_status == 'Available':
                print("this robot is available-->" + robotName)
                return robotId, robot_status
            else:
                print("this robot is busy -->" + robotName)
            print("Robot id-->" + str(robotId))
            print(robotName)
    return "noid", "nothing"


def getRobotStatus(key, RobotID, folderid, OrchestratorUrl):
    global Statee
    print("in get robot status function")
    url = "" + OrchestratorUrl + "/odata/Sessions?$filter=Robot/Id eq " + str(RobotID) + "&$ Select =State"

    header = {"content-type": "application/json", "Authorization": "Bearer " + str(key),
              "X-UIPATH-OrganizationUnitId": ""+folderid+""}
    response = requests.get(url, headers=header, verify=False)

    print(str(response.status_code))

    r_json = response.json()
    print(str(r_json))
    val = json.dumps(r_json['value'])
    print("here")
    print(val)
    resp_dict = json.loads(val)
    for i in resp_dict:
        Statee = i['State']
        # print(Status)
    return Statee


def getReleaseKey(key, inputProcessKey, folderid, OrchestratorUrl):
    global releaseKey
    url = "" + OrchestratorUrl + "/odata/Releases"

    header = {"content-type": "application/json",
              "Authorization": "Bearer " + str(key),
              "X-UIPATH-OrganizationUnitId": ""+folderid+""}

    response = requests.get(url, headers=header, verify=False)
    print(str(response.status_code))

    r_json = response.json()
    val = json.dumps(r_json['value'])
    resp_dict = json.loads(val)
    print(resp_dict)
    for i in resp_dict:
        if i['ProcessKey'] == inputProcessKey:
            releaseKey = str(i['Key'])
            processKey = str(i['ProcessKey'])
            print("processKey is " + str(processKey))
            print("releaseKey is " + str(releaseKey))
    return releaseKey

    # startJob(key, robotId, releaseKey)


def startJob(key, robotId, releaseKey, OrchestratorUrl, folderid,Trigger_Point,Process_Name):
    print("key is " + str(key))
    print("robot id is " + str(robotId))
    print("release key is " + str(releaseKey))

    url = "" + OrchestratorUrl + "/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"

    data = {
        "startInfo": {
            "ReleaseKey": str(releaseKey),
            "Strategy": "Specific",
            "RobotIds": [robotId],
            "InputArguments": "{\"Trigger_Point\":\""+Trigger_Point+"\",\"Process_Name\":\""+Process_Name+"\"}"
            "InputArguments": credentials
        }
    }

    header = {"content-type": "application/json",
              "Authorization": "Bearer " + str(key),
              "X-UIPATH-OrganizationUnitId": ""+folderid+""}

    response = requests.post(url, data=json.dumps(data), headers=header, verify=False)
    print(str(response.status_code))

    r_json = response.json()
    jobId = r_json['value'][0]['Id']
    print(str(jobId))


def PWDKEYRING(NetworkAddress, user_name):
    return keyring.get_password(NetworkAddress, user_name)


def MailCheck():
    with open('C:\\WINBOT Flask Application\\Process Trigger\\Config.txt') as config:
        json_data = json.load(config)
        # ------------------------------Only database details will be in the Config file
        databasePort = json_data["Port"]
        databaseHostName = json_data["HostName"]
        DatabaseServiceName = json_data["ServiceName"]
        DatabaseUsername = json_data["User"]
        DBNetworkAddress = json_data["DBNetworkAddress"]
        Databasepassword = PWDKEYRING(DBNetworkAddress, DatabaseUsername)
        try:
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
            #-------------------insert new tables queries here
            sql_query = 'SELECT * FROM winbot_configuration'
            print(sql_query)
            c.execute(sql_query)
            print('sql query executed')
            #fetch header column names
            headercolumns = [x[0] for x in c.description]  # for getting column names
            print(headercolumns)
            #fetch all rows
            headerrows = c.fetchall()
            if not headerrows:
                print('no rows')
            else:
                headerdata = pd.DataFrame(headerrows, columns=headercolumns)  # it will give output as same as table
                print(headerdata)

                granttype = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'Grant Type'].values[0]
                clientid = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'Client Id'].values[0]
                clientsecret = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'Client Secret'].values[0]
                clientscope = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'Scope'].values[0]
                OrchestratorURL = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'Orchestrator URL'].values[0]
                folderid = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'Folder Id'].values[0]
                mail = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'Mail ID'].values[0]
                emailaddress = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'Email Network Address'].values[0]
                servername = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'Server Name'].values[0]
                imapport = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'Imap Port'].values[0]
                pwd = PWDKEYRING(emailaddress, mail)
                sharepointclientsecret = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'SharePoint Client Secret'].values[0]
                sharepointclientid = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'SharePoint Client ID'].values[0]
                sharepointusername = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'SharePoint UserName'].values[0]
                sharepointpassword = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'SharePoint Password'].values[0]
                sharepointscope = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'SharePoint Scope'].values[0]
                sharepointtenantname = headerdata['CONFIGURATION_VALUE'][headerdata['CONFIGURATION_NAME'] == 'SharePoint Tenant'].values[0]
                sql_query = 'SELECT * FROM winbot_python_lines_config where enabled = \'Yes\''
                print(sql_query)
                c.execute(sql_query)
                # fetch header column names
                linecolumns = [x[0] for x in c.description]  # for getting column names
                # fetch all rows
                linerows = c.fetchall()
                if not linerows:
                    print('no rows')
                else:
                    linedata = pd.DataFrame(linerows,
                                            columns=linecolumns)
                #---------------------------------------------------
                for i in linedata.itertuples():
                    if i.SOURCE == 'Share Point':
                        url_token = "https://login.microsoftonline.com/"+sharepointtenantname+"/oauth2/v2.0/token"
                        data_token = "grant_type=password&username="+sharepointusername+"&password="+sharepointpassword+"&client_id="+sharepointclientid+"&client_secret="+sharepointclientsecret+"&scope="+sharepointscope

                        header_token = {"content-type": "application/x-www-form-urlencoded",
                                        "SdkVersion": "postman-graph/v1.0"}

                        response_token = requests.post(url_token, data=data_token, headers=header_token, verify=False)
                        print(str(response_token.status_code))
                        AccessToken_json = response_token.json()
                        Sharepoint_AccessToken = AccessToken_json["access_token"]
                        print("Sharepoint access token is " + str(Sharepoint_AccessToken))

                        folder_value = "WinBot Inbox/"+i.INPUT_FOLDER
                        folder_value_arr = folder_value.split("/")
                        move_folder_value ="WinBot Input/" + i.INPUT_FOLDER
                        inputProcessKey = i.ORCHESTRATOR_PROCESS_NAMES
                        inputRobotEnv = i.ENVIRONMENT
                        print("move folder value "+str(move_folder_value))
                        move_folder_value_arr = move_folder_value.split("/")
                        count = 0
                        parent_folder_id = ""
                        move_parent_folder_id = ""
                        files_present = False
                        for folder_name in folder_value_arr:
                            if count == 0:
                                url = "https://graph.microsoft.com/v1.0/me/drive/root/children?filter=name eq '" + folder_name + "'"

                            else:
                                url = "https://graph.microsoft.com/v1.0/me/drive/items/" + parent_folder_id + "/children?filter=name eq '" + folder_name + "'"
                            print("URl in parent folder " + str(url))

                            header = {"Authorization": "Bearer " + str(Sharepoint_AccessToken)}
                            response = requests.get(url, headers=header, verify=False)
                            r_json = response.json()
                            print(r_json)
                            val = json.dumps(r_json['value'])
                            print(val)
                            resp_dict = json.loads(val)
                            print(str(resp_dict[0]['id']))
                            parent_folder_id = resp_dict[0]['id']
                            count = count + 1
                        print("parent folder id is " + str(parent_folder_id))
                        count_m = 0
                        for folder_name in move_folder_value_arr:
                            if count_m == 0:
                                url = "https://graph.microsoft.com/v1.0/me/drive/root/children?filter=name eq '" + folder_name + "'"

                            else:
                                url = "https://graph.microsoft.com/v1.0/me/drive/items/" + move_parent_folder_id + "/children?filter=name eq '" + folder_name + "'"

                            header = {"Authorization": "Bearer " + str(Sharepoint_AccessToken)}
                            response = requests.get(url, headers=header, verify=False)
                            r_json = response.json()
                            print(r_json)
                            val = json.dumps(r_json['value'])
                            print(val)
                            resp_dict = json.loads(val)
                            print(str(resp_dict[0]['id']))
                            move_parent_folder_id = resp_dict[0]['id']
                            count_m = count_m + 1
                        print("move parent folder id is " + str(move_parent_folder_id))

                        url2 = "https://graph.microsoft.com/v1.0/me/drive/items/" + parent_folder_id + "/children"
                        header2 = {"Authorization": "Bearer " + str(Sharepoint_AccessToken)}
                        response2 = requests.get(url2, headers=header2, verify=False)
                        r_json2 = response2.json()
                        print(r_json2)
                        val2 = json.dumps(r_json2['value'])
                        resp_dict1 = json.loads(val2)
                        file_val = "file"
                        count_files = 0
                        for x in resp_dict1:
                            if file_val in x:
                                count_files = count_files + 1
                        if count_files > 0:
                            token = getAuthentication(granttype, clientid, clientsecret, clientscope,
                                                      OrchestratorURL)
                            RobotStateAndID = getRobotId(token, inputRobotEnv, folderid,
                                                         OrchestratorURL)
                            # RobotState = getRobotStatus(token, robotID, OrchestratorURL)
                            print(
                                "RobotState after getting the return statement from authentication to main code -->" + str(
                                    RobotStateAndID[1]))
                            if RobotStateAndID[1] == 'Available':
                                files_present = True
                                for x in resp_dict1:
                                    if file_val in x:
                                        file_id = x['id']
                                        file_name = x['name']
                                        url3 = "https://graph.microsoft.com/v1.0/me/drive/items/" + file_id
                                        print(url3)
                                        data3 = {
                                            """parentReference""": {
                                                """id""": ""+str(move_parent_folder_id)+""},
                                            """name""": "" + str(file_name) + ""

                                        }

                                        # data3 = """{"parentReference": {"id":"01Q6PN2TTAFLKIAXYTZVELGPUW7ZJ7NBQZ"}, "name":"""""+file_name+"""""}"""
                                        print(json.dumps(data3))
                                        header3 = {"content-type": "application/json",
                                                   "Authorization": "Bearer " + str(Sharepoint_AccessToken)}
                                        response3 = requests.patch(url3, headers=header3, data=json.dumps(data3),
                                                                   verify=False)
                                        print(response3.status_code)
                                        print(response3.reason)
                                        print(file_id)
                            else:
                                print("Robot is not available")

                            if files_present == True:
                                token = getAuthentication(granttype, clientid, clientsecret, clientscope,
                                                          OrchestratorURL)
                                robotID = getRobotId(token, inputRobotEnv, folderid, OrchestratorURL)
                                releaseKey = getReleaseKey(token, inputProcessKey, folderid, OrchestratorURL)
                                startJob(token, robotID[0], releaseKey, OrchestratorURL, folderid,i.SOURCE,i.WINBOT_PROCESS_NAME)




                    else:
                        print("mail->" + str(mail))
                        print("pwd ->" + str(pwd))
                        with MailBox(servername, imapport).login(mail, pwd, initial_folder='INBOX') as mailbox:
                            print("in mail box")
                            breakFor = False

                            for msg in mailbox.fetch(AND(seen=False), reverse=False, mark_seen=False):
                                print("fetching the mails")
                                mailExists = False

                                print("all->" + msg.subject)

                                if not linerows:
                                    print('no rows')
                                else:
                                    linedata = pd.DataFrame(linerows,
                                                            columns=linecolumns)  # it will give output as same as table
                                    for i in linedata.itertuples():
                                        if i.SOURCE == 'Mail':
                                            mailExists = False
                                            print("subj--->" + i.SUBJECT)
                                            subj = i.SUBJECT
                                            if subj in msg.subject:
                                                # inputRobotName = i.ROBOT_NAME
                                                inputProcessKey = i.ORCHESTRATOR_PROCESS_NAMES
                                                inputRobotEnv = i.ENVIRONMENT
                                                mailFolder = i.INPUT_FOLDER
                                                token = getAuthentication(granttype, clientid, clientsecret,
                                                                          clientscope,
                                                                          OrchestratorURL)
                                                RobotStateAndID = getRobotId(token, inputRobotEnv, folderid,
                                                                             OrchestratorURL)
                                                # RobotState = getRobotStatus(token, robotID, OrchestratorURL)
                                                print(
                                                    "RobotState after getting the return statement from authentication to main code -->" + str(
                                                        RobotStateAndID[1]))
                                                if RobotStateAndID[1] == 'Available':
                                                    mailExists = True
                                                    mailfolder1 = mailFolder
                                                    # mailbox.move(msg.uid, mailfolder1)
                                                    mailbox.move(
                                                        [msg.uid for msg in
                                                         mailbox.fetch(AND(seen=False, subject=subj), mark_seen=False)],
                                                        mailfolder1)
                                                else:
                                                    print("Robot is busy for this subject-->" + str(subj))
                                                    # breakFor=True
                                                break
                                    if breakFor == True:
                                        break
                                    if mailExists == True:
                                        token = getAuthentication(granttype, clientid, clientsecret, clientscope,
                                                                  OrchestratorURL)
                                        robotID = getRobotId(token, inputRobotEnv, folderid, OrchestratorURL)
                                        releaseKey = getReleaseKey(token, inputProcessKey, folderid, OrchestratorURL)
                                        startJob(token, robotID[0], releaseKey, OrchestratorURL, folderid,i.SOURCE,"")
                                        print("mails read")
                                        print("next turn")
                                        break



        except cx_Oracle.Error as error:
            print(error)
        finally:
            # release the connection
            if conn:
                conn.close()


if __name__ == '__main__':
    MailCheck()
