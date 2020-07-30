from flask import Flask,jsonify,request,render_template,url_for,Response,send_file
import pymysql
import numpy as np
from .Mod import (groupModel,authModel,TagModel,ticketModel,SendEmailModel,ActivityModel,confirmModel,
showModel,lotteModel,showScoreModel,showUserFeedbackModel,actScoreModel,actScoreModel,QRcodeModel,
imageModel)
from flask_cors import CORS
from threading import Thread
from gevent.pywsgi import WSGIServer
from gevent import monkey
from io import BytesIO
import re
import json
import base64
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config.update(
    SECRET_KEY = 'e7862bb61c376ba4',
    JWT_SECRET_KEY = 'e7862bb61c376ba4',
)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/.well-known/apple-app-site-association' ,methods=['GET'])
def getApple():
    return app.send_static_file('apple-app-site-association')

@app.route('/Fiestadb/Account/select' ,methods=['POST'])
def get_accountData():
    Account = authModel.FiestaDbModel()
    resultDit = Account.getAccountData(request.get_json())
    headResult = {
            'code' : '001',
            'result':[]
    }
    if resultDit == '002':
        headResult['code'] = '002'
    if resultDit == '003':
        headResult['code'] = '003'
    headResult['result'].append(resultDit)
    return jsonify(headResult)   

@app.route('/Fiestadb/Account/upload' ,methods=['POST'])
def upload_accountData():
    Account = authModel.FiestaDbModel() 
    result = Account.postUploadData(request.get_json())
    headResult = {
            'code' : '001'
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult) 

@app.route('/Fiestadb/Account/update' ,methods=['POST'])
@jwt_required
def update_accountData():  
    Account = authModel.FiestaDbModel() 
    result = Account.postUpdateData(request.get_json())
    headResult = {
            'code' : '001'
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult) 

@app.route('/Fiestadb/Account/delete' ,methods=['POST'])
@jwt_required
def delect_accountData():
    Account = authModel.FiestaDbModel() 
    result = Account.postDeleteData(request.get_json())
    headResult = {
            'code' : '001'
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult) 

@app.route('/Fiestadb/Account/SendConfirm' ,methods=['POST']) 
def SendConfirmEmail():
    Account = authModel.FiestaDbModel() 
    inputData = request.get_json()
    Id = Account.Confirm_Id(inputData)
    headResult = {
            'code' : '001'
    }
    if(Id =='002' or Id == '0042' or Id =='004C'):
        headResult['code'] = Id
        return jsonify(headResult) 
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select Mail from ReviewStatus where accountId = \'%s\'' %Id
    cursor.execute(sql)
    Mail = cursor.fetchone()
    rull = '^[a-z0-9]([._\\-]*[a-z0-9])*@([a-z0-9][-a-z0-9]*[a-z0-9].)edu.tw$'
    result = re.match(rull,Mail[0])
    if result == None :
        headResult['code'] = '008'
        db.close()
        return jsonify(headResult) 
    cm = confirmModel.AuthConfirm(Id)
    token = cm.create_confirm_token()
    if inputData['type'] == '1':    
        confirm_url = 'fiesta.nkust.edu.tw:8888/Fiestadb/Account/ValidateEmail?token=' + str(token)[2:-1]
    if inputData['type'] == '2':    
        confirm_url = 'fiesta.nkust.edu.tw:8888/Fiestadb/Account/ForgetPassword?token=' + str(token)[2:-1]
    html = render_template('userMailConfirm.html', confirm_url=confirm_url)
    thr = Thread(target=async_ConfirmSend, args=[app,Mail[0], html])
    thr.start()
    return jsonify(headResult)

@app.route('/Fiestadb/Account/ValidateEmail' ,methods=['GET']) 
def ValidateConfirmEmail_SighUp():
    headResult = {
            'code' : '001'
    }
    token = request.args['token']
    cm = confirmModel.AuthConfirm(0)
    Account = authModel.FiestaDbModel() 
    data = cm.validate_confirm_token(token)
    if(data == False):
        headResult['code'] = '009'
        return jsonify(headResult)
    else:
        result = Account.Reviewstatus_Update(data['user_id'])
        if (result != '001'):
            headResult['code'] = result
            return '驗證過時'
        return render_template('Confirm.html')

@app.route('/Fiestadb/Account/ValidateLogin' ,methods=['POST'])
@jwt_required
def ValidateLogin():
    headResult = {
            'code' : '001',
            'result' : []
    }
    cm = confirmModel.AuthConfirm(0)
    Account = authModel.FiestaDbModel() 
    data = get_jwt_identity()
    if(data == False):
        headResult['code'] = '009'
        return jsonify(headResult)
    else:
        result = Account.getLoginData(data)
        if (result == '002'):
            headResult['code'] = result
            return jsonify(headResult)
        headResult['result'].append(result)
        return jsonify(headResult)    
    
@app.route('/Fiestadb/Account/ForgetPassword' ,methods=['GET']) 
def ValidateConfirmEmail_Forget():
    headResult = {
            'code' : '001'
    }
    token = request.args['token']
    cm = confirmModel.authModelConfirm(0)
    data = cm.validate_confirm_token(token)
    if(data == False):
        headResult['code'] = '009'
        return jsonify(headResult)
    return jsonify(headResult)

@app.route('/Fiestadb/Account/getReviewStatus' ,methods=['POST']) 
@jwt_required
def getReviewStatus():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    headResult = {
            'code' : '001',
            'result':[]
    }
    resultDit = { 'reviewStatus' : reviewStatus }
    headResult['result'].append(resultDit)
    return jsonify(headResult)

@app.route('/Fiestadb/Account/getJoinedGroup' ,methods=['POST']) 
@jwt_required
def getJoinGroupdata():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = Account.getJoinedGroupId(request.get_json())
    headResult = {
            'code' : '001',
            'result' :result
    }
    if result == '0048':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Account/getUnexpiredAct' ,methods=['POST']) 
@jwt_required
def getUnexpiredActData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = Account.getUnexpiredActId(request.get_json())
    headResult = {
            'code' : '001',
            'result' :result
    }
    if result == '0048' or result == '012':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Account/Search' ,methods=['POST']) 
@jwt_required
def Search():
    Account = authModel.FiestaDbModel() 
    result = Account.getSimpleData(request.get_json())
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '013' or result == '004B':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Account/getCreateAct' ,methods=['POST']) 
@jwt_required
def getCreateAct():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'}) 
    result = Account.getCreateAct(request.get_json())
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '013' or result == '0048':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Account/getDataById' ,methods=['POST']) 
@jwt_required
def SearchById():
    Account = authModel.FiestaDbModel() 
    result = Account.getSimpleDataById(request.get_json())
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '013' or result == '004B':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Group/select' ,methods=['POST']) 
@jwt_required
def gotGroupData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = groupModel.getGroupData(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result == '011':
        headResult['code'] = result
    headResult['result'].append(result)
    return jsonify(headResult)

@app.route('/Fiestadb/Group/upload' ,methods=['POST']) 
@jwt_required
def postUploadGroupData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = groupModel.uploadGroupData(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result == '0041' or result == '0045' or result == '0048' or result == '005' or result == '006':
        headResult['code'] = result
    headResult['result'].append(result)
    return jsonify(headResult)

@app.route('/Fiestadb/Group/update' ,methods=['POST']) 
@jwt_required
def postUpdateGroupData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = groupModel.updateGroupData(request.get_json())
    headResult = {
            'code' : '001'
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Group/delete' ,methods=['POST']) 
@jwt_required
def postdeleteGroupData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = groupModel.deleteGroupData(request.get_json())
    headResult = {
            'code' : '001'
    }
    print(result)
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Group/Member/select' ,methods=['POST']) 
@jwt_required
def getGroupMember():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = groupModel.getGroupMember(request.get_json())
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '011':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Group/Member/upload' ,methods=['POST']) 
@jwt_required
def postUploadGroupMember():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = groupModel.uploadGroupMember(request.get_json())
    headResult = {
            'code' : '001'
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Group/Member/update' ,methods=['POST']) 
@jwt_required
def postUpdateGroupMember():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = groupModel.updateGroupMember(request.get_json())
    headResult = {
            'code' : '001'
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Group/Member/delete' ,methods=['POST']) 
@jwt_required
def postdeleteGroupMember():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = groupModel.deleteGroupMember(request.get_json())
    headResult = {
            'code' : '001'
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Group/FIndName' ,methods=['POST']) 
@jwt_required
def FIndName():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = groupModel.findName(request.get_json())
    headResult = {
            'code' : '001'
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Group/getAct' ,methods=['POST'])
@jwt_required
def _selectGroupAct_():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = groupModel.selectGroupAct(request.get_json())
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '0048' or result == '013':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/select' ,methods=['POST']) 
def getActData():
    result = ActivityModel.getActivityData(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result == '010':
        headResult['code'] = result
    headResult['result'].append(result)
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/upload' ,methods=['POST']) 
@jwt_required
def uploadActData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ActivityModel.uploadActivityData(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result == '006' or result == '0047' or result == '0045' or result == '004G':
        headResult['code'] = result
    headResult['result'].append(result)
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/update' ,methods=['POST']) 
@jwt_required
def updateActData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ActivityModel.updateActivityData(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result != '001':
        headResult['code'] = result
    headResult['result'].append(result)
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/delete' ,methods=['POST']) 
@jwt_required
def deleteActData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ActivityModel.deleteActivityData(request.get_json())
    headResult = {
            'code' : '001'
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/updataUnexpired' ,methods=['POST']) 
@jwt_required
def updataUnexpiredActData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ActivityModel.updataUnexpiredActivity(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/getJoinedList' ,methods=['POST']) 
@jwt_required
def getJoinedList():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ActivityModel.getJoinedAuth(request.get_json())
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '004A':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/setJoinedList' ,methods=['POST']) 
@jwt_required
def setJoinedList():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ActivityModel.setJoinedAuth(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/setJoinedListbyGroup' ,methods=['POST']) 
@jwt_required
def setJoinedListbyGroup():
    result = ActivityModel.setJoinedAuthbyGroup(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/deleteJoinedList' ,methods=['POST']) 
@jwt_required
def deleteJoinedAct():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ActivityModel.deleteJoinedAct(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/getRecommend' ,methods=['POST'])
def getRecommendAct():
    current_user = get_jwt_identity()
    result = ActivityModel.getRecommendActTest(request.get_json())
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '0048' or result == '013':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/Search' ,methods=['POST'])
def actSearch():
    result = ActivityModel.getSimpleData(request.get_json())
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '013' or result == '004B':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/getActByTag' ,methods=['POST']) 
def getActByTag():
    result = ActivityModel.getActByTag(request.get_json())
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '013' or result == '004G':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/getCount' ,methods=['POST']) 
#@jwt_required
def getCount():
   # Account = authModel.FiestaDbModel()
#    current_user = get_jwt_identity()
 #   reviewStatus = Account.getReviewStatusForToken(current_user)
  #  if reviewStatus == '020' :
   #     return jsonify({'code':'020'})
    result = ActivityModel.CountPeople(request.get_json())
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '010' or result == '004A':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/getExpire' ,methods=['POST']) 
@jwt_required
def getExpire():
    current_user = get_jwt_identity()
    result = ActivityModel.getExpireAct(current_user)
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '010' or result == '004A':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Activity/getTicketData' ,methods=['POST']) 
@jwt_required
def getTicketData():
    current_user = get_jwt_identity()
    result = ActivityModel.getTicketData(current_user)
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '010' or result == '004A':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Touch/select' ,methods=['POST']) 
@jwt_required
def getTouchPeople():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ActivityModel.getTouchPeople(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result == '010':
        headResult['code'] = result
    headResult['result'].append(result)
    return jsonify(headResult)

@app.route('/Fiestadb/Touch/upload' ,methods=['POST'])
@jwt_required
def setTouchPeople():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ActivityModel.setTouchPeople(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Touch/delete' ,methods=['POST'])
@jwt_required
def deleteTouchPeople():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ActivityModel.deleteTouchPeople(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Tag/upload' ,methods=['POST']) 
@jwt_required
def uploadNewTag():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = TagModel.createTag(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Tag/select' ,methods=['GET']) 
def getTagName():
    result = TagModel.getTagName()
    headResult = {
            'code' : '001',
            'result' : []
    }
    headResult['result'].append(result)
    return jsonify(headResult)

@app.route('/Fiestadb/getSchool' ,methods=['GET'])
def getSchool():
    f = open('./static/Shorthand.json')
    school = json.load(f)
    eng =[]
    for i in school.keys():
        eng.append(i)
    ch =[]
    for i in school.values():
        ch.append(i)
    headResult = {
            'code' : '001',
            'result' : []
    }
    headResult['result'].append(eng)
    headResult['result'].append(ch)
    return jsonify(headResult)

@app.route('/Fiestadb/Show/select' ,methods=['POST'])
@jwt_required
def getShowData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showModel.getShowData(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result == '004A' or result == '013':
        headResult['code'] = result
    headResult['result'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Show/upload' ,methods=['POST']) 
@jwt_required
def uploadShowData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showModel.uploadShowData(request.get_json())
    headResult = {
            'code' : '001',
            'result' : []
    }
    if result == '006' or result == '0045' or result == '004A' or result == '004D' :
        headResult['code'] = result
    headResult['result'].append(result)
    return jsonify(headResult)

@app.route('/Fiestadb/Show/update' ,methods=['POST']) 
@jwt_required
def updateShowData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showModel.updateShowData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Show/delete' ,methods=['POST'])
@jwt_required
def deleteShowData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showModel.deleteShow(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Lotte/select' ,methods=['POST'])
@jwt_required
def getlotteData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = lotteModel.getLotteData(request.get_json())
    headResult = {
            'code' : '001',
            'result' :result
    }
    if result == '004A' or result == '013':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Lotte/upload' ,methods=['POST']) 
@jwt_required
def uploadlotteData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = lotteModel.uploadLotteData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Lotte/update' ,methods=['POST'])
@jwt_required
def updatelotteData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = lotteModel.updateLotteData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Lotte/delete' ,methods=['POST']) 
@jwt_required
def deletelotteData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = lotteModel.deleteLotteData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Lotte/rand' ,methods=['POST'])
@jwt_required
def getRandomAccount():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = lotteModel.getRandomAccount(request.get_json())
    headResult = {
            'code' : '001',
            'result' : []
    }
    if result == '004A' or result == '013' or result == '021':
        headResult['code'] = result
    headResult['result'].append(result)
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Score/Show/SelectByShow' ,methods=['POST'])
@jwt_required
def SelectByShow():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showScoreModel.getDataByShow(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result == '004I' or result == '013':
        headResult['code'] = result
    headResult['result'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Score/Show/SelectByAuth' ,methods=['POST'])
@jwt_required
def SelectByAuth():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showScoreModel.getDataByAuth(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result == '0048' or result == '013':
        headResult['code'] = result
    headResult['result'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Score/Show/upload' ,methods=['POST']) 
@jwt_required
def uploadshowScoreData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showScoreModel.uploadData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Score/Show/update' ,methods=['POST']) 
@jwt_required
def updateshowScoreData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showScoreModel.updateData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Score/Show/delete' ,methods=['POST']) 
@jwt_required
def deleteshowScoreData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showScoreModel.deleteData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Score/Act/SelectByAct' ,methods=['POST'])
@jwt_required
def actSelectByAct():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = actScoreModel.getDataByAct(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result == '004A' or result == '013':
        headResult['code'] = result
    headResult['result'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Score/Act/SelectByAuth' ,methods=['POST'])
@jwt_required
def actSelectByAuth():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = actScoreModel.getDataByAuth(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result == '0048' or result == '013':
        headResult['code'] = result
    headResult['result'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Score/Act/upload' ,methods=['POST']) 
@jwt_required
def uploadactScoreData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = actScoreModel.uploadData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Score/Act/update' ,methods=['POST']) 
@jwt_required
def updateactScoreData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = actScoreModel.updateData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Score/Act/delete' ,methods=['POST']) 
@jwt_required
def deleteactScoreData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = actScoreModel.deleteData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Show/SelectByAct' ,methods=['POST'])
@jwt_required
def SUFMSelectByAct():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showUserFeedbackModel.getDataByAct(request.get_json())
    headResult = {
            'code' : '001',
            'result' :[]
    }
    if result == '004A' or result == '013':
        headResult['code'] = result
    headResult['result'].append(result)
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Show/upload' ,methods=['POST']) 
@jwt_required
def uploadSUFMData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showUserFeedbackModel.uploadData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Show/update' ,methods=['POST']) 
@jwt_required
def updateSUFMData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showUserFeedbackModel.updateData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/FeedBack/Show/delete' ,methods=['POST']) 
@jwt_required
def deleteSUFMData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = showUserFeedbackModel.deleteData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Ticket/SelectByAct' ,methods=['POST'])
def _getTicketDatabyActId_():
    result = ticketModel.getTicketDatabyActId(request.get_json())
    headResult = {
            'code' : '001',
            'result' :result
    }
    if result == '004A' or result == '013':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Ticket/Select' ,methods=['POST'])
@jwt_required
def _getTicketData_():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ticketModel.getTicketData(request.get_json())
    headResult = {
            'code' : '001',
            'result' :result
    }
    if result == '004P' or result == '013':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Ticket/upload' ,methods=['POST']) 
@jwt_required
def uploadTicketData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ticketModel.uploadTicketData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Ticket/update' ,methods=['POST']) 
@jwt_required
def updateTicketData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ticketModel.updateTicketData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Ticket/delete' ,methods=['POST']) 
@jwt_required
def deleteTicketData():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ticketModel.deleteTicketData(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Ticket/updateTicketNotes' ,methods=['POST']) 
@jwt_required
def updateTicketNotes():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ticketModel.updateTicketNotes(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Ticket/updateTicketStatusFalse' ,methods=['POST']) 
@jwt_required
def updateTicketStatusFalse():
    Account = authModel.FiestaDbModel()
    current_user = get_jwt_identity()
    reviewStatus = Account.getReviewStatusForToken(current_user)
    if reviewStatus == '020' :
        return jsonify({'code':'020'})
    result = ticketModel.updateTicketStatusFalse(request.get_json())
    headResult = {
            'code' : '001',
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Ticket/vaildQrcode' ,methods=['POST'])
@jwt_required
def vaildTicketQRcode():
    authId = get_jwt_identity()
    result = ticketModel.vaildTicketbyQRcode(request.get_json(),authId)
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '010' or result == '006':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/Ticket/vaild' ,methods=['POST'])
@jwt_required
def vaildTicket():
    data = get_jwt_identity()
    result = ticketModel.vaildTicket(request.get_json())
    headResult = {
            'code' : '001'
    }
    if result != '001':
        headResult['code'] = result
    return jsonify(headResult)

@app.route('/Fiestadb/QRcode' ,methods=['POST'])
def QRcode():
    result = QRcodeModel.enQRcode(request.get_json())
    # result = QR.enQRcode("1")
    img_io = BytesIO()
    result.save(img_io, 'PNG')
    img_io.seek(0)

    #with open(img_io,"rb") as f:
    #    base64_data = base64.b64encode(f.read())
    #    headResult = {
    #        'code' : '001',
    #        'QRCode': base64_data
    #   }
    #   return jsonify(headResult)
    # response = make_response(send_file(img_io, mimetype='image/png', cache_timeout=0))
    # response.headers.set["Content-Type"] = "application/force-download"
    # response.headers.set["Content-Disposition"] = " attachment; filename='picture.png'"

    #--- B64 PNG顯示 ---
    imageB64 = str(base64.b64encode(img_io.read()))[2:-1]
    # return send_file(img_io,mimetype='image/png', cache_timeout=0)
    return imageB64
    # Content-Disposition: attachment; filename="picture.png"
    #return send_file(img_io, mimetype='image/png', as_attachment = True, cache_timeout=0)
    # return response

@app.route('/Fiestadb/uploadImage' ,methods=['POST'])
@jwt_required
def uploadImage():
    headResult = {
            'code' : '001',
    }
    if 'file' not in request.files:
        headResult['code'] = '016'
        return jsonify(headResult)
    
    _type_ = request.args.get('type')
    Id = request.args.get('Id')
    if _type_ == 'auth':
        file = request.files['file']
        if file and allowed_file(file.filename):
            result = imageModel.uploadAuthImg(file,Id) 
            if result != '001':
                headResult['code'] = result
    elif _type_ == 'act':
        file = request.files['file']
        print(file)
        if file and allowed_file(file.filename):
            result = imageModel.uploadActImg(file,Id) 
            if result != '001':
                headResult['code'] = result
    elif _type_ == 'group':
        file = request.files['file']
        if file and allowed_file(file.filename):
            result = imageModel.uploadGroupImg(file,Id) 
            if result != '001':
                headResult['code'] = result 
            
    return jsonify(headResult)

@app.route('/Fiestadb/test' ,methods=['POST'])
@jwt_required
def test():
    data = get_jwt_identity()
    result = ActivityModel.getRecommendAct(request.get_json(),data)
    headResult = {
            'code' : '001',
            'result' : result
    }
    if result == '004A' or result == '014':
        headResult['code'] = result
    return jsonify(headResult)

def async_ConfirmSend(app, to, template):
    with app.app_context():
        SendEmailModel.ConfirmSend(to,template)

def async_uploadAuthImg(app, file,Id):
    with app.app_context():
        imageModel.uploadAuthImg(file,Id)

def async_uploadActImg(app, file,Id):
    with app.app_context():
        imageModel.uploadActImg(file,Id)

def async_uploadGroupImg(app, file,Id):
    with app.app_context():
        imageModel.uploadGroupImg(file,Id)


        
app.debug = True           
if __name__ == "__main__":
	server  = WSGIServer(("127.0.0.1", 5000), app)
	print("Server started")
	server.serve_forever()
    # app.run()
