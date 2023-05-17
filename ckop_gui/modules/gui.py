# from web3 import Web3, middleware, parity, exceptions
from flask import g, Flask, render_template, \
    request, redirect, url_for, session, Blueprint, current_app,\
    send_file
# from web3.middleware import geth_poa_middleware
from modules.work_to_email import send_email
from modules.secret_key import key
import random
from modules.work_to_date import *
from modules.dop_function import *
from modules.const import *
import datetime
import logging
import os
from hashlib import sha256


# formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

logging.basicConfig(filename = './logs/log.log', level=logging.INFO, 
        format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
        encoding="utf-8"
)
# handler = logging.handlers.RotatingFileHandler(
        # 'log.txt',
        # maxBytes=1024 * 1024)
logging.getLogger('werkzeug').setLevel(logging.WARNING)
# logging.getLogger('werkzeug').addHandler(handler)

#***************************************ОСНОВНЫЕ ПАРАМЕТРЫ***********************************************

w3, contract_makestruct0, contract_makestruct1, contract_teacher_0, \
    contract_teacher_1, contract_student  = construct_contracts()
gui_ckop = Blueprint("gui_ckop", __name__)
gui_ckop.secret_key = key



# isMiner = False
# session["isMiner"] = False
    # string memory name,
    # string memory goal,
    # string memory loginMentor,
    # string memory roleMembers,
    # string[] memory tasks,
    # address[] memory members,
    # uint16 numLaboratory
def get_teacher_project_info(indexxx, addr):
    project = contract_teacher_0.functions.checkProject(indexxx).call({'from': addr})
    task_deadline = contract_student.functions.checkTaskDeadline(indexxx).call({'from':addr})
    current_app.logger.info("Project info: " + json.dumps(project))
    current_app.logger.info("Task and deadlone info: " + json.dumps(task_deadline))
    tasks = {}
    k=0
    if task_deadline[0]:
        for i in range(10):
            if task_deadline[0][i] != "":
                if task_deadline[2][i] == 1: tasks.update({k: [task_deadline[0][i], unix_to_date(task_deadline[1][i]), 'checked']})
                else: tasks.update({k: [task_deadline[0][i], unix_to_date(task_deadline[1][i]), 'nonchecked']})
            k+=1
    strudent_addr = project[5]
    student_name = []
    project_name=project[0]
    addrr = contract_makestruct0.functions.getUsingLogin(project[2]).call()
    current_app.logger.info("Address project mentor: %s", addrr)
    h = contract_teacher_0.functions.checkTeacher(addrr).call()
    current_app.logger.info("Info project mentor: %s", h)
    if h[0]: mentor = h[1] + "(" + h[0]+ ")"
    else: mentor = ""
    teacher, status = contract_makestruct1.functions.getRequestStudent(indexxx).call()
    current_app.logger.info("Request teacher: %s, status^ %s",teacher, status)

    # roles=project[3]
    goal = project[1]
    labs = laboratories[project[6]]
    for i in range(len(strudent_addr)):
        data = contract_student.functions.checkStudent(strudent_addr[i]).call({'from': addr})
        if data[0] != '': student_name.append(data[1] + "(" + data[0] +") : " + project[3][i])
    return student_name, project_name, tasks, goal, labs, mentor
    # return data, num, data2, data3, 

def check_project_student(addr):
    data = contract_student.functions.checkStudent(addr).call({'from': addr})
    num = contract_student.functions._findActiveProject(addr).call({'from': addr})
    data2 = contract_student.functions.checkProject(num).call({'from': addr})
    data3 = contract_student.functions.checkTaskDeadline(num).call({'from':addr})
    current_app.logger.info("Student info: address: %s, login: %s, FIO: %s, class: %s%s,", addr, data[0],data[1],str(data[4]),data[2])
    current_app.logger.info("ACtive Project address: %s, number: %s",addr, str(num))
    current_app.logger.info("Project info: address: %s, Name %s, LoginMentor %s", addr, data2[0], data2[2])
    slovar = {}
    k=0
    if data3[0]:
        for i in range(10):
            if data3[0][i] != "":
                if data3[2][i] == 1: slovar.update({k: [data3[0][i], unix_to_date(data3[1][i]), 'checked']})
                else: slovar.update({k: [data3[0][i], unix_to_date(data3[1][i]), 'nonchecked']})
            k+=1
    return data, num, data2, data3, slovar

def teacher_cabinet_info(addr):
    h = contract_teacher_0.functions.checkTeacher(addr).call({'from': addr})
    login = h[0]
    fio = h[1]
    p = contract_teacher_0.functions.checkNumAllActiveProject().call({'from': addr})
    current_app.logger.info("Teacher info: %s, %s", h[0], h[1])
    projects_name= {}
    for i in p:
        k = contract_teacher_0.functions.checkProject(i).call({'from': addr})
        teacher, status = contract_makestruct1.functions.getRequestStudent(i).call()
        if k[2]==session['login'] or (teacher == session['addr'] and status == 0):
            projects_name[i] = k[0]
            # projects_name.append(k[0])
    return projects_name, fio, login, laboratories[h[4][0]], schoolSubjects[h[3][0]]

def get_members(data, addr):
    res = []
    for u in data:
        data_user = contract_makestruct0.functions.getStudentStruct(u).call({'from': addr})
        fio = data_user[1]
        login_user = data_user[0]
        if fio != "":
            res.append(fio + "(" + login_user +")")
    ans = ", ".join(res)
    current_app.logger.info("Members info: %s", ans)
    return ans

def make_token(addr, login):
    # rand_str = "".join(random.choices(letters_and_numbers, k=10))
    st = addr + login + tokens_str
    token = sha256(st.encode()).hexdigest()
    return token

def check_token(addr, login, token):
    st = addr + login + tokens_str
    return token == sha256(st.encode()).hexdigest()

@gui_ckop.route('/')
def index():
    current_app.logger.info('First page')
    message = ""
    mes_type = ""
    if "message" in session and "mes_type" in session: 
        message = session["message"]
        mes_type = session["mes_type"]
    session.clear()
    # if message: mes_type = "status_class_wrong"
    # else: mes_type = ""
    return render_template('first_walet.html', message=message, mes_type=mes_type)

@gui_ckop.post('/back')
def back(message=''):
    pass

# #************************************Авторизация кошелька*********************************
@gui_ckop.post('/walet')
def walet():
    try:
        address = request.form['walet']
        password = request.form['password']
        if address == "" or password == "":
            session["message"] = "Заполните поля"
            session["mes_type"] = "status_class_wrong"
            return redirect(url_for('gui_ckop.index'))
        current_app.logger.info('Start unlock account: %s', address)
        session.update({'addr': address, 'password_addr': password})
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        # res = miner_geth(w3, True)
        return redirect(url_for('gui_ckop.auth'))
    except BaseException as e:
        # print(e)
        # print(type(e))
        current_app.logger.info('Error exception : %s', e)
        session["message"] = "Неверные данные"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for('gui_ckop.index'))



@gui_ckop.post('/exit')
def exit_lc():
    session.pop('addr', None)
    session.pop('login', None)
    session.clear()
    # res = miner_geth(w3, False)
    return redirect(url_for("gui_ckop.index"))

#************************************Авторизация аккаунта*********************************

@gui_ckop.get('/auth')
def auth_rend():
    return render_template('auth.html', addr=session.get('addr', ""))

@gui_ckop.post('/auth')
def auth(message=''):
    try:
        current_app.logger.info('Start auth, address: %s', session["addr"])
        session.update({'addr': request.form['addr']})
        password = request.form['password']
        login = request.form['login']
        if login == "" or password == "":
            return render_template('auth.html', addr=session.get('addr', ""), 
                    message="Заполните поля!", mes_type="status_class_wrong",
                    login_old=login)
        block = w3.eth.block_number
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'], 1000000)
        current_app.logger.info("User login: %s, password passed", session['addr'])
        res = contract_student.functions.auth(login, password, session['addr']).call({'from': session['addr']})
        if not res:
            return render_template('auth.html', addr=session.get('addr', ""), 
                    message="Неверные данные", mes_type="status_class_wrong",
                    login_old=login)
        # ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
        # if ev.get_all_entries():
        #     current_app.logger.info(ev.get_all_entries()[0]['args']['text'])
        #     return render_template('auth.html', addr=session.get('addr', ""), 
        #             message=ev.get_all_entries()[0]['args']['text'], mes_type="status_class_wrong",
        #             login_old=login)
        session.update({'password_acc': password, 'login': login, 'corectly_login': login, 'corectly_pass':password})
        number = contract_makestruct0.functions.getStatusAddress(session['addr']).call({'from': session['addr']})
        current_app.logger.info("Status user %s is %s", login, str(number))
        session["message"] = ""
        session["mes_type"] = ""
        session["token"] = make_token(session["addr"], session["login"])
        if int(number) == 5:
            return redirect(url_for('gui_ckop.go_to_teacher_cabinet'))
        elif int(number) == 6:
            return redirect(url_for('gui_ckop.go_to_student_cabinet'))
        else: 
            return 'mjsdijgndsfgsdg'
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        return render_template('auth.html', addr=session.get('addr', ""), message="Неверные данные", mes_type="status_class_wrong")
        # return redirect(url_for('gui_ckop.auth', message=e, mes_type="status_class_wrong"))
    
# #************************************Регистрация аккаунта Пользавателя*********************************
@gui_ckop.post('/reg')
def reg():
    # if 'addr' not in session:
    #     session["message"] = "Авторизуйтесь, пожалуйста"
    #     session["mes_type"] = "status_class_wrong"
    #     return redirect(url_for("gui_ckop.index"))
    try:
        message = ""
        number = contract_makestruct0.functions.getStatusAddress(session['addr']).call({'from': session['addr']})
        current_app.logger.info("Status user %s is %s", session['addr'], str(number))
        if int(number) == 2:
            return render_template("reg_teacher.html", listt=laboratories, subject=schoolSubjects)
        elif int(number) == 3:
            return render_template('reg_student.html', message=message)
        elif int(number) in  (5, 6):
            message = "Вы уже зарегистрированы. Авторизуйтесь"
            mes_type = "status_class_good"
            return render_template('auth.html', addr=session.get('addr', ""), message=message, mes_type=mes_type)
        else:
            message = "Ошибка регистрации!"
            mes_type = "status_class_wrong"
            return render_template('auth.html', addr=session.get('addr', ""), message=message, mes_type=mes_type)
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"] = "Ошибка"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
     
# #************************************Регистрация аккаунта ученика*********************************
@gui_ckop.get('/go_to_student_cabinet')
def go_to_student_cabinet():
    if 'addr' not in session or "login" not in session :
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        data, num, data2, data3, slovar = check_project_student(session['addr'])
        if len(data2[4]) > 2: ch = 5
        else: ch = 10

        st_side = []
        for st in data[3]:
            if st != "":
                st_side.append(st)
        check_strong_side = len(st_side) > 0
        strong_side=", ".join(st_side)
        status_project = contract_makestruct0.functions.getStatusProject(num).call()
        return render_template('student_cabinet.html', message=session["message"], mes_type= session["mes_type"], 
            login=data[0], 
            name=data[1], classnum=data[-2], classletter=data[2], Project_name=data2[0], 
            check_strong_side=check_strong_side, strong_side=strong_side, 
            Laboratorie=laboratories[data2[6]], new_proj_avalible=data2[0]=='',
            status_project = (status_project in (2, 3)))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"] = "Ошибка"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))


@gui_ckop.post('/go_to_reg_student')
def go_to_reg_student(message=''):
    current_app.logger.info('Reg student start, addres: %s', session["addr"])
    if 'addr' not in session:
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    return render_template('reg_student.html', message=message)

@gui_ckop.post('/reg_student')
def reg_student():
    current_app.logger.info('Reg student start, addres: %s', session["addr"])
    if 'addr' not in session:
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        rep_password = request.form['rep_password']
        login = request.form['login']
        password = request.form['password']
        fio = request.form['FIO']
        clas = request.form['class']
        classletter = request.form['classletter']
        useLogin = contract_makestruct0.functions.getUsingLogin(login).call()
        current_app.logger.info("Login in use: %s", str(useLogin == ("0x" + "0"*40)))
        if useLogin != ("0x" + "0"*40):
            message = "Email уже есть в системе"
        elif check_email_re(login) and password != '' and fio != '' and clas != '' \
                and classletter != '' and password == rep_password\
                and 0<int(clas)<12 and len(classletter)==1 and classletter.upper() in alf:
            rand_string = ''.join(random.choice(letters_and_numbers) for i in range(3))+''.join(random.choice(letters_and_numbers) for i in range(3))+''.join(random.choice(letters_and_numbers) for i in range(3))
            current_app.logger.info("Email message: %s", rand_string)
            session['rand-string'] = rand_string
            send_email(login, text=rand_string)
            session.update({'login': login, 'password_acc':password, 'FIO':fio, 'clas':int(clas), 'classletter':classletter})
            # current_app.logger.info(session['login'], session['password_acc'], session['FIO'], session['clas'], session['classletter'])
            return render_template('check_email.html')
        elif not check_email_re(login):
            message = "Некорректный e-mail"
        elif password == '' or fio == "" or clas == '' or classletter == '':
            message = "Заполните все поля"
        elif password != rep_password:
            message = "Пароли не совпадают"
        elif int(clas)<=0 or int(clas)>11:
            message = "Неверный класс"
        elif len(classletter)!=1 or classletter.upper() not in alf:
            message = "Неверная буква класса"
        else:
            message = "Ошибка!"
        return render_template('reg_student.html', message=message, mes_type="status_class_wrong",
                login=login, fio = fio, clas = clas, classletter = classletter)
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        return render_template('reg_student.html', message='Неверные данные')


# ************************************Функция ученика********************************
@gui_ckop.post('/go_to_create_projects')
def go_to_create_projects(message=''):
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    return render_template('create_project_for_student.html', listt=laboratories2, message=message)

@gui_ckop.post('/go_to_create_strong_side')
def go_to_create_strong_side(message=""):
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        data = contract_student.functions.checkStudent(session['addr']).call({'from': session['addr']})
        strong_side = data[3]
        if len(strong_side)<=7: len_tasks = 0
        else: len_tasks = 10
        slovar = {}
        k=0
        for i in data[3]:
            slovar.update({k: i})
            k+=1
        return render_template('change_strong_side.html',  strong_side=", ".join(data[3]), str_sd_len=(len(strong_side)<5), len_tasks=len_tasks, message=message, slovar=slovar)
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"] = "Ошибка."
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for('gui_ckop.go_to_student_cabinet'))

@gui_ckop.get('/go_to_change_projects')
@gui_ckop.post('/go_to_change_projects')
def go_to_change_projects():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        if request.method == "POST":
            session["message"] = ""
            session["mes_type"] = ""
        data, num, data2, data3, slovar = check_project_student(session['addr'])
        if len(data2[4]) > 2: ch = 5
        else: ch = 10
        addr = contract_makestruct0.functions.getUsingLogin(data2[2]).call()
        fio_tutor = contract_teacher_0.functions.checkTeacher(addr).call()[0]
        tutor = fio_tutor + "(" + (data2[2]) + ")"
        ind_user = data2[5].index(session['addr'])
        status_project = contract_makestruct0.functions.getStatusProject(num).call()
        # if num != 0:
        return render_template('proj_student.html', message=session["message"], role=data2[3][ind_user], 
                    slovar=slovar, tasks=data2[4], Goal=data2[1], login=data[0], tutor=tutor, 
                    members = get_members(data2[5], session['addr']),
                    mes_type = session["mes_type"],
                    project_name=data2[0], laboratorie=laboratories[data2[6]], ch=ch,
                    new_proj_avalible=data2[0]=='', status_project=status_project)
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"] = "Ошибка."
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for('gui_ckop.go_to_student_cabinet'))


@gui_ckop.post('/create_project')
def create_project():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))   
    try:
        name_project = request.form['name_project']
        login = request.form['walet']
        if name_project != "":
            session["mes_type"] = "status_class_wrong"
            lab_ind = request.form['laboratories']
            laboratorie = laboratories2.index(lab_ind)
            w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
            block = w3.eth.block_number
            tx_hash = contract_student.functions.createProjectForStudent(session['login'], 
                session['password_acc'], name_project, "",
                int(laboratorie)+99).transact({'from': session['addr']})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
            ev_text = ev.get_all_entries()[0]['args']['text']
            if ev.get_all_entries() and ev_text != 'Project create':
                current_app.logger.info("Event contracts %s", ev_text)
                if ev_text in event_message: session["message"] = event_message[ev_text]
                else: session["message"]="Ошибка: " + ev_text
            else:
                session["message"]= 'Проект успешно создан'
                session["mes_type"] = "status_class_good"
            num = contract_student.functions._findActiveProject(session['addr']).call()
            current_app.logger.info(num)
            if login != "" and num != 0:
                tx_hash = contract_student.functions.send_request_teacher(session['login'], 
                    session['password_acc'], login, num).transact({'from': session['addr']})
                tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
                ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
                ev_text = ev.get_all_entries()[0]['args']['text']
                if ev.get_all_entries() and ev_text != 'Request created':
                    current_app.logger.info("Event contracts %s", ev_text)
                    if ev_text in event_message: session["message"] = event_message[ev_text]
                    else: session["message"]="Ошибка: " + ev_text
                else: 
                    session["mes_type"] = "status_class_good"
                    session["message"] = event_message[ev_text]

            return redirect(url_for('gui_ckop.go_to_student_cabinet'))
        else:
            return render_template('gui_ckop.create_project_for_student', listt=laboratories2, 
                message="Заполните все поля", mes_type = "status_class_wrong")
    except BaseException as e:
            current_app.logger.info('Error exception: %s', e)
            session["message"] = "Ошибка создания проекта"
            return redirect(url_for('create_project_for_student'))
# @gui_ckop.post('/create_strong_side')
# def create_strong_side(message=''):
#     try:
#         session["mes_type"] = "status_class_wrong"
#         strong_side = request.form['strong_side']
#         w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
#         tx_hash = contract_student.functions.addStrongSide(session['login'], session['password_acc'], strong_side).transact({'from': session['addr']})
#         tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
#         block = w3.eth.block_number
#         ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
#         ev_text = ev.get_all_entries()[0]['args']['text']
#         if ev.get_all_entries() and ev_text != 'Change strong side':
#             if ev_text in event_message: session["message"] = event_message[ev_text]
#             else: session["message"]="Ошибка"
#         else:
#             session["message"] = 'Сторона успешна изменена'
#             session["mes_type"] = "status_class_good"
#         return redirect(url_for('gui_ckop.go_to_student_cabinet'))
#     except:

@gui_ckop.post('/change_strong_side')
def change_strong_side(message=''):
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))  
    try:
        session["mes_type"] = "status_class_wrong"
        new_side = request.form['side']
        indexx = request.form['indexx']
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        tx_hash = contract_student.functions.changeStrongSide(session['login'], 
                        session['password_acc'], int(indexx), new_side).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        block = w3.eth.block_number
        ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
        ev_text = ev.get_all_entries()[0]['args']['text']
        if ev.get_all_entries() and ev_text != 'Change strong side':
            current_app.logger.info("Event contract: %s", ev_text)
            if ev_text in event_message: session["message"] = event_message[ev_text]
            else: session["message"]="Ошибка: " + ev_text
        else:
            session["message"] = 'Сторона успешна изменена'
            session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.go_to_student_cabinet'))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        return redirect(url_for('gui_ckop.go_to_student_cabinet'))

@gui_ckop.post('/change_goal_project')
def change_goal_project(message=''):
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))  
    try:
        session["mes_type"] = "status_class_wrong"
        goal = request.form['goal']
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        tx_hash = contract_student.functions.changeGoalProject(session['login'], session['password_acc'], goal).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        block = w3.eth.block_number
        ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
        ev_text = ev.get_all_entries()[0]['args']['text']
        if ev.get_all_entries() and ev_text != 'Change goal':
            current_app.logger.info("Event contract: %s", ev_text)
            if ev_text in event_message: session["message"] = event_message[ev_text]
            else: session["message"]="Ошибка: " + ev_text
        else:
            session["message"] = 'Цель успешна изменена'
            session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.go_to_change_projects'))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"] = 'Ошибка при изменении цели'
        return redirect(url_for('gui_ckop.go_to_change_projects'))


@gui_ckop.post('/create_task')
def create_task(message=''):
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))  
    try:
        session["mes_type"] = "status_class_wrong"
        num = contract_student.functions._findActiveProject(session['addr']).call({'from': session['addr']})
        tasks = contract_student.functions.checkProject(num).call({'from': session['addr']})[4]
        task = request.form['task']
        data = request.form['date'].replace('.', '-')
        if task == "" or data == "":
            session["message"] = 'Заполните все поля'
        elif '' not in tasks:
            session["message"] = 'У Вас много задач в проекте'
        elif date_to_unix(data) < int(datetime.datetime.now().timestamp()):
            session["message"] = 'Некорректная дата'
        else:
            w3.geth.personal.unlock_account(session['addr'], session['password_addr'], 1000000)
            tx_hash = contract_student.functions.changeTaskInProject(session['login'], session['password_acc'], 
                tasks.index(''), task, date_to_unix(data)).transact({'from': session['addr']})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            block = w3.eth.block_number
            ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
            ev_text = ev.get_all_entries()[0]['args']['text']
            if ev.get_all_entries() and ev_text != 'Change task':
                current_app.logger.info("Event contract: %s", ev_text)
                if ev_text in event_message: session["message"] = event_message[ev_text]
                else: session["message"]="Ошибка: " + ev_text
            else: 
                session["message"]='Задача добавлена'
                session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.go_to_change_projects'))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"] = "Ошибка при создании задачи!"
        return redirect(url_for('gui_ckop.go_to_change_projects'))



@gui_ckop.post('/changeTaskInProject')
def changeTaskInProject(message=''):
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))  
    try:
        session["mes_type"] = "status_class_wrong"
        num = contract_student.functions._findActiveProject(session['addr']).call({'from': session['addr']})
        tasks = contract_student.functions.checkProject(num).call({'from': session['addr']})[4]
        # tasks = contract_student.functions.checkProject(session['addr']).call({'from': session['addr']})[5]
        indexxx = request.form['indexxx']
        task = request.form['task']
        block = w3.eth.block_number
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        tx_hash = contract_student.functions.changeTaskInProject(session['login'], session['password_acc'], int(indexxx), task, date_to_unix('2023-12-31')).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
        ev_text = ev.get_all_entries()[0]['args']['text']
        if ev.get_all_entries() and ev_text != 'Change task':
            current_app.logger.info("Event contract: %s", ev_text)
            if ev_text in event_message: session["message"] = event_message[ev_text]
            else: session["message"]="Ошибка: " + ev_text
        else: 
            session["message"]='Задача успешно изменена'
            session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.go_to_change_projects'))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"] = "Ошибка при изменении задачи!"
        return redirect(url_for('gui_ckop.go_to_change_projects'))

# #************************************Регистрация аккаунта учителя*********************************

@gui_ckop.get('/go_to_teacher_cabinet')
def go_to_teacher_cabinet():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))  
    try:
        if 'message' not in session:
            session['message'] = ""
        projects_name, login, fio, labs, sub, = teacher_cabinet_info(session['addr'])

        session.update({'lab_name': labs, "FIO":fio, "login":login})
        return render_template('teacher_cabinet.html', message=session["message"], 
                projects=projects_name, login=login, fio=fio, 
                lab=session['lab_name'], sub=sub,  mes_type = session["mes_type"],
                )
    except BaseException as e:
        current_app.logger.info('Error auth teacher, address: %s, error: %s', session["addr"], e)
        return render_template('first_walet.html', message="Что-то пошло не так", mes_type="status_class_wrong")

@gui_ckop.post('/reg_teacher_check')
def reg_teacher_check():
    # or "login" not in session or "token" not in session or\
        # not check_token(session['addr'], session["login"], session["token"]):
    current_app.logger.info('Start reg teacher, address: %s', session["addr"])
    if 'addr' not in session:
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        current_app.logger.warning('You not auth, address: %s', session["addr"])
        return redirect(url_for("gui_ckop.index"))  
    try:
        email = request.form['email']
        password = request.form['password']
        rep_pass = request.form['rep_password']
        FIO = request.form['FIO']
        schSub = request.form['SchoolSubjects']
        lab_s = request.form['laboratories']
    except:
        schSub = "";lab_s = ""
    try:
        if check_email_re(email) and password != '' and FIO != '' and schSub != '' and lab_s != '' and password == rep_pass:
            
            rand_string = ''.join(random.choice(letters_and_numbers) for i in range(3))+''.join(random.choice(letters_and_numbers) for i in range(3))+''.join(random.choice(letters_and_numbers) for i in range(3))
            SchoolSubject = schoolSubjects[int(schSub)]
            laboratorie = laboratories[int(lab_s)]
            current_app.logger.info("Email: %s random staring: %s", email, rand_string)
            session['rand-string'] = rand_string
            send_email(email, text=rand_string)
            session.update({'login': email, 'password_acc':password, 
                'FIO':FIO, 'SchoolSubject': SchoolSubject, 'laboratorie': laboratorie})
            # current_app.logger.info(session['login'], session['password_acc'], session['FIO'], [schoolSubjects2.index(session['SchoolSubject'])],  [99+laboratories2.index(session["laboratorie"])])
            return render_template('check_email_teacher.html')
        else:
            current_app.logger.warning('Неверные данные, address: %s', session["addr"])
            if not check_email_re(email): mess = "Некорректный email"
            elif password == '' or FIO == '' or schSub == '' or lab_s != '': mess = "Заполнены не все поля"
            elif password != rep_pass: mess = "Пароли не совпадают"
            else: mess = 'Неверно ведены данные'
            current_app.logger.warning('%s, address: %s', mess, session["addr"])
            return render_template("reg_teacher.html", listt=laboratories, subject=schoolSubjects, 
                message=mess, mes_type="status_class_wrong")
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        return render_template("reg_teacher.html", listt=laboratories, subject=schoolSubjects, 
                message="Неверно ведены данные", mes_type="status_class_wrong")


@gui_ckop.post('/check_email_teacher')
def check_email_teacher():
    if 'addr' not in session:
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        current_app.logger.warning('You not auth, address: %s', session["addr"])
        return redirect(url_for("gui_ckop.index"))  
    current_app.logger.info('Check email teacher, address: %s', session["addr"])
    try:
        check = request.form['check']
        if check == session['rand-string']:
            block = w3.eth.block_number
            tx_hash = contract_teacher_0.functions.registrationForTeacher(
                session['login'], session['password_acc'], session['FIO'], 
                [schoolSubjects2.index(session['SchoolSubject'])],
                [99+laboratories2.index(session["laboratorie"])]).transact({'from': session['addr']})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            ev = contract_teacher_0.events.Action.createFilter(fromBlock=block, toBlock="latest")
            ev_text = ev.get_all_entries()[0]['args']['text']
            if ev.get_all_entries() and ev_text != 'Teacher successfully registered':
                current_app.logger.info("Event contract: %s", ev_text)
                if ev_text in event_message: session["message"] = event_message[ev_text]
                else: session["message"]="Ошибка: " + ev_text
                return render_template("reg_teacher.html", 
                            listt=laboratories, subject=schoolSubjects, 
                            message=session["message"])
            session["token"] = make_token(session["addr"], session["login"])
            session["mes_type"] = ""
            return redirect(url_for('gui_ckop.go_to_teacher_cabinet'))
        else:
            return render_template('check_email.html', message='Неверный код',mes_type="status_class_wrong")
    except BaseException as e:
            current_app.logger.info('Error exception: %s', e)
            return render_template('check_email.html', message='Ошибка',mes_type="status_class_wrong")

@gui_ckop.post('/check_email')
def check_email():
    try:
        session["message"] = ""
        session["mes_type"] = ""
        check = request.form['check']
        # current_app.logger.info(session['login'], session['password_acc'], session['FIO'], session['clas'], session['classletter'])
        if check == session['rand-string']:
            block = w3.eth.block_number
            # w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
            tx_hash = contract_student.functions.registrationForStudent(session['login'], 
                    session['password_acc'], session['FIO'], session['clas'], session['classletter']).transact(
                            {'from': session['addr']})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
            ev_text = ev.get_all_entries()[0]['args']['text']
            if ev.get_all_entries() and ev_text != 'Student successfully registered':
                current_app.logger.info("Event contract: %s", ev_text)
                if ev_text in event_message: session["message"] = event_message[ev_text]
                else: session["message"]="Ошибка: " + ev_text
                return render_template('reg_student.html', message=session["message"], 
                    mes_type="status_class_wrong",
                    login=session['login'], fio = session['FIO'], 
                    clas = session['clas'], classletter = session['classletter'])
            session["token"] = make_token(session["addr"], session["login"])
            session["mes_type"] = ""
            return redirect(url_for('gui_ckop.go_to_student_cabinet'))
        else:
            return render_template('check_email.html', message='Неверный код',mes_type="status_class_wrong")
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        return render_template('check_email.html', message='Ошибка',mes_type="status_class_wrong")

#**************************************************ФУНКЦИИ УЧИТЕЛЯ********************************
@gui_ckop.post('/go_to_create_projects_teacher')
def go_to_create_projects_teacher(message=''):
    return render_template('create_project_for_teacher.html', message=message)


@gui_ckop.post('/create_project_teacher')
def create_project_teacher(message=''):
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index")) 
    try:
        session["mes_type"] = "status_class_wrong"
        name_prject = request.form['name_project']
        if name_prject == "":
            return render_template('create_project_for_teacher.html',
                message="Введите имя проекта", mes_type="status_class_wrong")
        block = w3.eth.block_number
        laboratorie = contract_teacher_0.functions.checkTeacher(session['addr']).call({'from': session['addr']})[4][0]
        tx_hash = contract_teacher_0.functions.createProjectForTeacher(
            session['login'], session['password_acc'], name_prject, 
            laboratorie).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        ev = contract_teacher_0.events.Action.createFilter(fromBlock=block, toBlock="latest")
        ev_text = ev.get_all_entries()[0]['args']['text']
        if ev.get_all_entries() and ev_text != 'Create project':
            current_app.logger.info("Event contract: %s", ev_text)
            if ev_text in event_message: session["message"] = event_message[ev_text]
            else: session["message"]="Ошибка: " + ev_text
            return render_template('create_project_for_teacher.html',
                message=ev.get_all_entries()[0]['args']['text'], mes_type="status_class_wrong")
        else: 
            session["message"]='Проект создан'
            session["mes_type"] = "status_class_good"
        return redirect(url_for("gui_ckop.go_to_teacher_cabinet"))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"]='Ошибка при создании проекта'
        return redirect(url_for("gui_ckop.go_to_teacher_cabinet"))

@gui_ckop.get('/go_to_create_acc_for_student')
@gui_ckop.post('/go_to_create_acc_for_student')
def go_to_create_acc_for_student():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index")) 
    if request.method == "POST":
        session["message"] = ""
        session["mes_type"] = ""
    return render_template('create_acc_for_student.html', message = session["message"],
        mes_type=session["mes_type"])
    

@gui_ckop.post('/create_acc_for_student')
def create_acc_for_student():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index")) 
    try:
        session["mes_type"] = "status_class_wrong"
        pass_walet = request.form['pass_walet']
        if pass_walet == "":
            session["message"] = "Введите пароль"
        else:
            new_acc = w3.geth.personal.new_account(pass_walet)
        current_app.logger.info("New acc: %s", new_acc)
        block = w3.eth.block_number
        tx_hash = contract_teacher_0.functions.generateAddressForStudent(
            session['login'], session['password_acc'], new_acc, pass_walet).transact(
                {'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        ev = contract_teacher_0.events.Action.createFilter(fromBlock=block, toBlock="latest")
        ev_text = ev.get_all_entries()[0]['args']['text']
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Address generated':
            current_app.logger.info("Event contract: %s", ev_text)
            if ev_text in event_message: session["message"] = event_message[ev_text]
            else: session["message"]="Ошибка: " + ev_text     
        else:
            session["message"]= new_acc
            session["mes_type"] = "status_class_good"
            contract_teacher_0.functions.myTransfer(new_acc).transact(
                {'from': '0xff42Fc7fdB5928b63da0bF2340880369fE335bf0', 
                'value': '1000000000000000'})
        return redirect(url_for('gui_ckop.go_to_create_acc_for_student'))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"]='Не удалось сгенерировать адрес'
        return redirect(url_for('gui_ckop.go_to_create_acc_for_student'))

@gui_ckop.post('/addStudentInProject')
def addStudentInProject(message=''):
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index")) 
    try:
        session["mes_type"] = "status_class_wrong"
        login = request.form['login_student']
        if login == "" or not check_email_re(login):
            session["message"] = "Введите корректный логин ученика"
        else:
            addr_stud = contract_makestruct0.functions.getUsingLogin(login).call()
            number = contract_makestruct0.functions.getStatusAddress(addr_stud).call()
            members=contract_teacher_0.functions.checkProject(session['index_project']).call()[5]
            if addr_stud == "0x"+"0"*40:
                session["message"] = "Логин не зарегестрирован"
            elif number != 6:
                session["message"] = "Это не ученик"
            elif addr_stud in members:
                session["message"] = "Ученик уже в проекте"
                session["mes_type"] = "status_class_good"
            elif contract_student.functions._findActiveProject(addr_stud).call() :
                session["message"] = "Ученик занят в другом проекте"
            else:
                block = w3.eth.block_number
                tx_hash = contract_teacher_0.functions.addStudentInProject(
                    session['login'], session['password_acc'], session['index_project'], 
                    addr_stud).transact({'from': session['addr']})
                tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
                ev = contract_teacher_0.events.Action.createFilter(fromBlock=block, toBlock="latest")
                ev_text = ev.get_all_entries()[0]['args']['text']
                if ev.get_all_entries() and ev_text != 'Add in project':
                    current_app.logger.info("Event contract: %s", ev_text)
                    if ev_text in event_message: session["message"] = event_message[ev_text]
                    else: session["message"]="Ошибка: " + ev_text
                else:
                    session["message"] = "Ученик добавлен в проект"
                    session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.proj_tutor'))
    except BaseException as e:
        current_app.logger.info('Ошибка:', e)
        session["message"] = "Ошибка добавления в проект"
        return redirect(url_for('gui_ckop.proj_tutor'))

@gui_ckop.post('/go_to_look_teacher_project')
def go_to_look_teacher_project(message=''):
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        proj_num = contract_teacher_0.functions.checkNumAllActiveProject().call({'from': session['addr']})
        projects_name= {}
        for i in proj_num:
            k=contract_teacher_0.functions.checkProject(i).call({'from': session['addr']})
            teacher, status = contract_makestruct1.functions.getRequestStudent(i).call()
            if k[2]==session['login'] or (teacher == session['addr'] and status == 0):
                projects_name.update({i : k[0]})    

        return render_template('proj_all_tutor.html', project_list=projects_name)
    except BaseException as e:
        current_app.logger.info('Ошибка:', e)
        session["message"] = "Ошибка добавления в проект"
        return redirect(url_for('gui_ckop.go_to_teacher_cabinet'))


@gui_ckop.post('/go_to_change_teacher_project')
def go_to_change_teacher_project():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    if request.method == "POST":
        session["message"] = ""
        session["mes_type"] = ""
    indexxx = int(request.form['indexxx'])
    session['index_project'] = indexxx
    return(redirect(url_for("gui_ckop.proj_tutor")))

@gui_ckop.get('/proj_tutor')
def proj_tutor():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        student_name, project_name, tasks, goal, labs, mentor  = get_teacher_project_info(
            session['index_project'], session['addr'])
        status_project = contract_makestruct0.functions.getStatusProject(session["index_project"]).call()
        current_app.logger.info("Status project %s: %s", session["index_project"], status_project)
        return render_template('proj_tutor.html', students = student_name, 
            project_name=project_name, 
            tutor=mentor, laboratorie=labs, len_tasks = 5, goal_project=goal,
            message=session["message"], mes_type = session["mes_type"], tasks=tasks,
            status_project=status_project)
    except BaseException as e:
        current_app.logger.info('Ошибка: %s', e)
        return redirect(url_for('gui_ckop.go_to_teacher_cabinet'))

@gui_ckop.post("/response_yes")
def response_yes():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        session["mes_type"] = "status_class_wrong"
        block = w3.eth.block_number
        tx_hash = contract_teacher_1.functions.send_response_teacher(
            session['login'], session['password_acc'], session['index_project'], 
            1).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        ev = contract_teacher_1.events.Action.createFilter(fromBlock=block, toBlock="latest")
        ev_text = ev.get_all_entries()[0]['args']['text']
        if ev.get_all_entries() and ev_text != 'Response created':
            current_app.logger.info("Event contract: %s", ev_text)
            if ev_text in event_message: session["message"] = event_message[ev_text]
            else: session["message"]="Ошибка: " + ev_text
        else:
            session["message"] = "Предложение принято"
            session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.proj_tutor'))
    except BaseException as e:
        current_app.logger.info('Ошибка:', e)
        session["message"] = "Ошибка при работе с проектом"
        return redirect(url_for('gui_ckop.proj_tutor'))

@gui_ckop.post("/response_no")
def response_no():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        session["mes_type"] = "status_class_wrong"
        block = w3.eth.block_number
        tx_hash = contract_teacher_1.functions.send_response_teacher(
            session['login'], session['password_acc'], session['index_project'], 2).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        ev = contract_teacher_1.events.Action.createFilter(fromBlock=block, toBlock="latest")
        ev_text = ev.get_all_entries()[0]['args']['text']
        if ev.get_all_entries() and ev_text != 'Response created':
            current_app.logger.info("Event contract: %s", ev_text)
            if ev_text in event_message: session["message"] = event_message[ev_text]
            else: session["message"]="Ошибка: " + ev_text
        else:
            session["message"] = "Предложение отклонено"
            session["mes_type"] = "status_class_good"
        return redirect(url_for("gui_ckop.go_to_teacher_cabinet"))
    except BaseException as e:
        current_app.logger.info('Ошибка:', e)
        session["message"] = "Ошибка при работе с проектом"
        return redirect(url_for("gui_ckop.go_to_teacher_cabinet"))


# string memory _login, 
# string memory _pass,
# string memory _roleInProject,
# uint16 _numProject,
# uint16 _numUser) 
@gui_ckop.post('/create_role')
def create_role():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        role = request.form['role']
        login_user = request.form['login_student']
        session["mes_type"] = "status_class_wrong"
        if login_user == "" or role == "" or (not check_email_re(login_user)):
            session["message"] = "Заполните корректно поля"
        else:
            addr_stud = contract_makestruct0.functions.getUsingLogin(login_user).call()
            number = contract_makestruct0.functions.getStatusAddress(addr_stud).call()
            members=contract_teacher_0.functions.checkProject(session['index_project']).call()[5]
            if addr_stud == "0x"+"0"*40:
                session["message"] = "Логин не зарегестрирован"
            elif number != 6:
                session["message"] = "Это не ученик"
            elif addr_stud not in members:
                session["message"] = "Ученик не в проекте"
            else:
                ind_user = members.index(addr_stud)
                w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
                tx_hash = contract_teacher_1.functions.changeRole(session['login'], session['password_acc'], 
                        role, session['index_project'], ind_user).transact({'from': session['addr']})
                tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
                block = w3.eth.block_number
                ev = contract_teacher_1.events.Action.createFilter(fromBlock=block,toBlock="latest")
                ev_text = ev.get_all_entries()[0]['args']['text']
                if ev.get_all_entries() and ev_text != 'Successfully change role':
                    current_app.logger.info("Event contract: %s", ev_text)
                    if ev_text in event_message: session["message"] = event_message[ev_text]
                    else: session["message"]="Ошибка: " + ev_text
                else: 
                    session["message"]='Роль успешно задана'
                    session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.proj_tutor'))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"] = "Ошибка при создании роли!"
        return redirect(url_for('gui_ckop.proj_tutor'))

@gui_ckop.post('/create_task_teacher')
def create_task_teacher(message=''):
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        session["mes_type"] = "status_class_wrong"
        # num = contract_student.functions._findActiveProject(session['addr']).call({'from': session['addr']})
        tasks = contract_student.functions.checkProject(session['index_project']).call({'from': session['addr']})[4]
        task = request.form['task']
        data = request.form['date'].replace('.', '-')
        if task == "" or data == "":
            session["message"] = 'Заполните все поля'
        elif '' not in tasks:
            session["message"] = 'У Вас много задач в проекте'
        elif date_to_unix(data) < int(datetime.datetime.now().timestamp()):
            session["message"] = 'Некорректная дата'
        else:
            w3.geth.personal.unlock_account(session['addr'], session['password_addr'], 1000000)
            tx_hash = contract_teacher_0.functions.changeTaskInProjectTeacher(
                session['login'], session['password_acc'], 
                session['index_project'], task, date_to_unix(data), 
                tasks.index(''), 0).\
                    transact({'from': session['addr']})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            block = w3.eth.block_number
            ev = contract_teacher_0.events.Action.createFilter(fromBlock=block,toBlock="latest")
            ev_text = ev.get_all_entries()[0]['args']['text']
            if ev.get_all_entries() and ev_text != 'Task change':
                current_app.logger.info("Event contract: %s", ev_text)
                if ev_text in event_message: session["message"] = event_message[ev_text]
                else: session["message"]="Ошибка: " + ev_text
            else: 
                session["message"]='Задача добавлена'
                session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.proj_tutor'))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"] = "Ошибка при создании задачи!"
        return redirect(url_for('gui_ckop.proj_tutor'))

@gui_ckop.post('/changeTaskInProjectTeacher')
def changeTaskInProjectTeacher():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        session["mes_type"] = "status_class_wrong"
        # tasks = contract_student.functions.checkProject(session['index_project']).call({'from': session['addr']})[4]
        task = request.form['task']
        date = request.form['date'].replace('.', '-')
        if request.form.get("check_ready"): check = True
        else: check = False
        indexx = int(request.form['indexxx'])
        # current_app.logger.info(indexx, task, date, check)
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'], 1000000)
        tx_hash = contract_teacher_0.functions.changeTaskInProjectTeacher(session['login'], 
                session['password_acc'], session['index_project'], 
                task, date_to_unix(date), indexx, int(check)).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        block = w3.eth.block_number
        ev = contract_teacher_0.events.Action.createFilter(fromBlock=block,toBlock="latest")
        ev_text = ev.get_all_entries()[0]['args']['text']
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Task change':
            current_app.logger.info("Event contract: %s", ev_text)
            if ev_text in event_message: session["message"] = event_message[ev_text]
            else: session["message"]="Ошибка: " + ev_text
        else: 
            session["message"]='Задача изменена'
            session["mes_type"] = "status_class_good"
        return(redirect(url_for("gui_ckop.proj_tutor")))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"] = "Ошибка при изменении задачи"
        return(redirect(url_for("gui_ckop.proj_tutor")))

@gui_ckop.post('/change_goal_project_tutor')
def change_goal_project_tutor():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        session["mes_type"] = "status_class_wrong"
        goal = request.form['goal']
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        tx_hash = contract_teacher_0.functions.changeGoalProjectTeacher(
            session['login'], session['password_acc'], goal, session["index_project"]).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        block = w3.eth.block_number
        ev = contract_teacher_0.events.Action.createFilter(fromBlock=block,toBlock="latest")
        ev_text = ev.get_all_entries()[0]['args']['text']
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Change goal':
            current_app.logger.info("Event contract: %s", ev_text)
            if ev_text in event_message: session["message"] = event_message[ev_text]
            else: session["message"]="Ошибка: " + ev_text
        else:
            session["message"]='Цель изменена'
            session["mes_type"] = "status_class_good"
        return(redirect(url_for("gui_ckop.proj_tutor")))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"]='Ошибка при изменении цели!'
        return(redirect(url_for("gui_ckop.proj_tutor")))

@gui_ckop.post("/freeze_project")
def freeze_project():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        session["mes_type"] = "status_class_wrong"
    # enum StatusProject {Not, Completed, Sleep, Active}
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        old_status = contract_makestruct0.functions.getStatusProject(session["index_project"]).call()
        current_app.logger.info("Status project %s: %s", session["index_project"], old_status)
        if old_status != 3:
            session["message"]='Проект неактивен'
        else:
            tx_hash = contract_teacher_1.functions.changeStatus(
                session['login'], session['password_acc'], session["index_project"], 2).transact({'from': session['addr']})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            block = w3.eth.block_number
            ev = contract_teacher_1.events.Action.createFilter(fromBlock=block,toBlock="latest")
            ev_text = ev.get_all_entries()[0]['args']['text']
            if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != "Status change":
                current_app.logger.info("Event contract: %s", ev_text)
                if ev_text in event_message: session["message"] = event_message[ev_text]
                else: session["message"]="Ошибка: " + ev_text
            else:
                session["message"]='Проект заморожен'
                session["mes_type"] = "status_class_good"
        return(redirect(url_for("gui_ckop.proj_tutor")))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"]='Ошибка при заморозке проекта!'
        return(redirect(url_for("gui_ckop.proj_tutor")))

@gui_ckop.post("/end_project")
def end_project():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        session["mes_type"] = "status_class_wrong"
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        old_status = contract_makestruct0.functions.getStatusProject(session["index_project"]).call()
        current_app.logger.info("Status project %s: %s", session["index_project"], old_status)
        if old_status != 3:
            session["message"]='Проект неактивен'
        else:
            tx_hash = contract_teacher_1.functions.changeStatus(
                session['login'], session['password_acc'], session["index_project"], 1).transact({'from': session['addr']})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            block = w3.eth.block_number
            ev = contract_teacher_1.events.Action.createFilter(fromBlock=block,toBlock="latest")
            ev_text = ev.get_all_entries()[0]['args']['text']
            if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != "Status change":
                current_app.logger.info("Event contract: %s", ev_text)
                if ev_text in event_message: session["message"] = event_message[ev_text]
                else: session["message"]="Ошибка: " + ev_text
            else:
                session["message"]='Проект закончен'
                session["mes_type"] = "status_class_good"
        return(redirect(url_for("gui_ckop.proj_tutor")))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"]='Ошибка при окончании проекта!'
        return(redirect(url_for("gui_ckop.proj_tutor")))


@gui_ckop.post("/resurect_project")
def resurect_project():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    try:
        session["mes_type"] = "status_class_wrong"
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        old_status = contract_makestruct0.functions.getStatusProject(session["index_project"]).call()
        current_app.logger.info("Status project %s: %s", session["index_project"], old_status)
        if old_status == 3:
            session["message"]='Проект активен'
        else:
            tx_hash = contract_teacher_1.functions.changeStatus(
                session['login'], session['password_acc'], session["index_project"], 3).transact({'from': session['addr']})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            block = w3.eth.block_number
            ev = contract_teacher_1.events.Action.createFilter(fromBlock=block,toBlock="latest")
            ev_text = ev.get_all_entries()[0]['args']['text']
            if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != "Status change":
                current_app.logger.info("Event contract: %s", ev_text)
                if ev_text in event_message: session["message"] = event_message[ev_text]
                else: session["message"]="Ошибка: " + ev_text
            else:
                session["message"]='Проект активен'
                session["mes_type"] = "status_class_good"
        return(redirect(url_for("gui_ckop.proj_tutor")))
    except BaseException as e:
        current_app.logger.info('Error exception: %s', e)
        session["message"]='Ошибка при восстановлении проекта!'
        return(redirect(url_for("gui_ckop.proj_tutor")))

#****************************************Запуск********************************************

@gui_ckop.get("/logs/")
def get_full_logs():
    if 'addr' not in session or "login" not in session or "token" not in session or\
        not check_token(session['addr'], session["login"], session["token"]):
        session["message"] = "Авторизуйтесь, пожалуйста"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for("gui_ckop.index"))
    if os.name == "nt":
        path_or_file =os.getcwd() + '\\ckop_gui\\logs\\log.log'
    else:
        path_or_file = './ckop_gui/logs/log.log'
    return send_file(path_or_file)
    # return redirect(url_for("gui_ckop.index"))

# @gui_ckop.get("/log/")
# def get_log():
#     if os.name == "nt":
#         path_or_file =os.getcwd() + '\\ckop_gui\\logs\\log.log'
#     else:
#         path_or_file = './ckop_gui/logs/log.log'
#     return send_file(path_or_file)
#     # return redirect(url_for("gui_ckop.index"))
@gui_ckop.app_errorhandler(404)
@gui_ckop.app_errorhandler(405)
def handle_404(err):
    return render_template('404.html'), 404

@gui_ckop.app_errorhandler(500)
def handle_500(err):
    return render_template('500.html'), 500


if __name__ == '__main__':
    session.clear()

    # from watchminer import WatchMiner
    # WatchMiner().start() 
    current_app.logger.info('Server started')
    gui_ckop.run(debug = True, host="0.0.0.0", port="5000")















