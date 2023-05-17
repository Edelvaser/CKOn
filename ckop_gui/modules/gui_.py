# from web3 import Web3, middleware, parity, exceptions
from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
# from web3.middleware import geth_poa_middleware
from modules.work_to_email import send_email
from modules.secret_key import key
import random
import string
from modules.work_to_date import *
from modules.dop_function import *
from modules.const import *
import datetime

#***************************************ОСНОВНЫЕ ПАРАМЕТРЫ***********************************************

# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# contract_makestruct0 = w3.eth.contract(address=conn_adr_makestruct0, abi=abi_make_struct0)
# contract_makestruct1 = w3.eth.contract(address=conn_adr_makestruct1, abi=abi_make_struct1)
# contract_student = w3.eth.contract(address=conn_adr_student, abi=abi_student)
# contract_teacher_0 = w3.eth.contract(address=conn_adr_teacher, abi=abi_teacher)
w3, contract_makestruct0, contract_makestruct1, contract_teacher_0, \
    contract_teacher_1, contract_student  = construct_contracts()
gui_ckop = Blueprint("gui_ckop", __name__)
gui_ckop.secret_key = key

letters_and_numbers = string.ascii_uppercase + string.ascii_lowercase + '1234567890'

isMiner = False
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
    print(project, '************************', task_deadline,sep='\n')
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
    print("Address project mentor", addrr)
    h = contract_teacher_0.functions.checkTeacher(addrr).call()
    print("Info project mentor", h)
    if h[0]: mentor = h[1] + "(" + h[0]+ ")"
    else: mentor = ""
    teacher, status = contract_makestruct1.functions.getRequestStudent(indexxx).call()
    print("Request teacher",teacher, status)

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
    print(data, '************************', data2, '*************', data3, sep='\n')
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
    print("Teacher info:", h)
    projects_name= {}

    
    #     if k[2]==session['login'] or (teacher == session['addr'] and status == 0):
    #         projects_name.update({i : k[0]})    
    for i in p:
        k = contract_teacher_0.functions.checkProject(i).call({'from': addr})
        teacher, status = contract_makestruct1.functions.getRequestStudent(i).call()
        if k[2]==session['login'] or (teacher == session['addr'] and status == 0):
            projects_name[i] = k[0]
            # projects_name.append(k[0])
    return projects_name, fio, login, laboratories[h[4][0]], schoolSubjects[h[3][0]]

def get_members(data, addr):
    res = []
    print(data)
    for u in data:
        data_user = contract_makestruct0.functions.getStudentStruct(u).call({'from': addr})
        fio = data_user[1]
        login_user = data_user[0]
        if fio != "":
            res.append(fio + "(" + login_user +")")
    return ", ".join(res)


@gui_ckop.route('/')
@gui_ckop.route('/<message>')
def index(message=''):
    # if 'addr' in session.keys() and 'password_addr' in session.keys():
    session['corectly_login'] = ""
    session['corectly_pass'] = ""
    session['message'] = ""
    session['mes_type'] = ""
    # try:
    #     w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
    #     return redirect(url_for('gui_ckop.go_to_auth'))
    # except: pass
    if message: mes_type = "status_class_wrong"
    else: mes_type = ""
    return render_template('first_walet.html', message=message, mes_type=mes_type)

@gui_ckop.post('/back')
def back(message=''):
    pass

# #************************************Авторизация кошелька*********************************
@gui_ckop.post('/walet')
def walet(message=''):
    address = request.form['walet']
    password = request.form['password']
    if address == "" or password == "":
        return redirect(url_for('gui_ckop.index', message='Кошелек не найден'))
    try:
    # print(address, password)
        # w3.parity.personal.unlock_account(address, password)
        session.update({'addr': address, 'password_addr': password})
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        # print(w3.geth.personal.)
        res = miner_geth(w3, True)
        print(res)
        return redirect(url_for('gui_ckop.auth'))
    except Exception as e:
        print('ОШИИИИИИБКААААААААА:', e)
        return redirect(url_for('gui_ckop.index', message='Кошелек не найден'))



@gui_ckop.post('/exit')
def exit_lc():
    session.clear()
    res = miner_geth(w3, False)
    print(res)
    return redirect(url_for("gui_ckop.index"))

#************************************Авторизация аккаунта*********************************

@gui_ckop.get('/go_to_auth')
def go_to_auth(message=''):
    print(message)
    session.update({'url': request.url})
    try:
        # if session['corectly_login'] and session['corectly_pass']:
            number = contract_makestruct0.functions.getStatusAddress(session['addr']).call({'from': session['addr']})
            if int(number) == 5:
                return redirect(url_for('gui_ckop.go_to_teacher_cabinet'))
            elif int(number) == 6:
                return redirect(url_for('gui_ckop.go_to_student_cabinet'))
            elif int(number) in (2, 3, 4):
                 return redirect(url_for('gui_ckop.auth'))
            else: 
                return 'НЕИЗВЕСТНЫЙ ПОЛЬЗОВАТЕЛЬ'
        # else:
        #     return redirect(url_for('gui_ckop.index'))
    except BaseException as e:
        if message: mes_type = "status_class_wrong"
        else: mes_type = ""
        if e == 'corectly_login':
            return render_template('auth.html', addr=session.get('addr', ""), message=message, mes_type=mes_type)
        print('ОШИИИИИИБКААААААААА:', e)
        return render_template('auth.html', addr=session.get('addr', ""), message=message, mes_type=mes_type)


@gui_ckop.get('/auth')
def auth_rend():
    return render_template('auth.html', addr=session.get('addr', ""))

@gui_ckop.post('/auth')
def auth(message=''):
    session.update({'addr': request.form['addr']})
    password = request.form['password']
    login = request.form['login']
    if login == "" or password == "":
        return render_template('auth.html', addr=session.get('addr', ""), 
                    message="Заполните поля!", mes_type="status_class_wrong",
                    login_old=login)
    try:
        block = w3.eth.block_number
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'], 1000000)
        print(login, password)
        res = contract_student.functions.auth(login, password, session['addr']).call({'from': session['addr']})
        if not res:
            return render_template('auth.html', addr=session.get('addr', ""), 
                    message="Неверные данные", mes_type="status_class_wrong",
                    login_old=login)
        # ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
        # if ev.get_all_entries():
        #     print(ev.get_all_entries()[0]['args']['text'])
        #     return render_template('auth.html', addr=session.get('addr', ""), 
        #             message=ev.get_all_entries()[0]['args']['text'], mes_type="status_class_wrong",
        #             login_old=login)
        session.update({'password_acc': password, 'login': login, 'corectly_login': login, 'corectly_pass':password})
        number = contract_makestruct0.functions.getStatusAddress(session['addr']).call({'from': session['addr']})
        print(number)
        session["message"] = ""
        session["mes_type"] = ""
        if int(number) == 5:
            return redirect(url_for('gui_ckop.go_to_teacher_cabinet'))
        elif int(number) == 6:
            return redirect(url_for('gui_ckop.go_to_student_cabinet'))
        else: 
            return 'mjsdijgndsfgsdg'
    except BaseException as e:
        print('ОШИИИИИИБКААААААААА:', e)
        return render_template('auth.html', addr=session.get('addr', ""), message="Неверные данные", mes_type="status_class_wrong")
        # return redirect(url_for('gui_ckop.auth', message=e, mes_type="status_class_wrong"))
    
# #************************************Регистрация аккаунта Пользавателя*********************************
@gui_ckop.post('/reg')
def reg(message=''):
    session.update({'url': request.url})
    number = contract_makestruct0.functions.getStatusAddress(session['addr']).call({'from': session['addr']})
    print(number)
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
     
# #************************************Регистрация аккаунта ученика*********************************
@gui_ckop.get('/go_to_student_cabinet')
def go_to_student_cabinet():
    session.update({'url': 'http://127.0.0.1:5000/go_to_auth'})
    # checkStudent:::::::::: string memory login, string memory FIO, string memory classLetter, string memory email, string[] memory strongSides, uint8 class, bytes32 _pass
    # checkProject:::::::::: string memory name, string memory goal, address mentor, uint16 numLaboratory, uint16 status, string[] memory tasksMembers, string memory roleMembers
    print(session["addr"])
    data, num, data2, data3, slovar = check_project_student(session['addr'])
    if len(data2[4]) > 2: ch = 5
    else: ch = 10

    st_side = []
    for st in data[3]:
        if st != "":
            st_side.append(st)
    check_strong_side = len(st_side) > 0
    strong_side=", ".join(st_side)
    return render_template('student_cabinet.html', message=session["message"], mes_type= session["mes_type"], 
        login=data[0], 
        name=data[1], classnum=data[-2], classletter=data[2], Project_name=data2[0], 
        check_strong_side=check_strong_side, strong_side=strong_side, 
        Laboratorie=laboratories[data2[6]], new_proj_avalible=data2[0]=='')
    
    # return render_template('student_cabinet.html', message=message, login=data[0], 
    #     name=data[1], classnum=data[-2], classletter=data[2], Project_name=data2[0], 
    #     check_strong_side=len(data[3])<6 and len(data[3])>0, strong_side=slovar, 
    #     Laboratorie=laboratories[data2[6]], )


@gui_ckop.post('/go_to_reg_student')
def go_to_reg_student(message=''):
    session.update({'url': request.url})
    return render_template('reg_student.html', message=message)

@gui_ckop.post('/reg_student')
def reg_student():
    try:
        rep_password = request.form['rep_password']
        login = request.form['login']
        password = request.form['password']
        fio = request.form['FIO']
        clas = request.form['class']
        classletter = request.form['classletter']
        useLogin = contract_makestruct0.functions.getUsingLogin(login).call()
        print(useLogin)
        if useLogin != ("0x" + "0"*40):
            message = "Email уже есть в системе"
        elif check_email(login) and password != '' and fio != '' and clas != '' \
                and classletter != '' and password == rep_password\
                and 0<int(clas)<12 and len(classletter)==1 and classletter.upper() in alf:
            rand_string = ''.join(random.choice(letters_and_numbers) for i in range(3))+''.join(random.choice(letters_and_numbers) for i in range(3))+''.join(random.choice(letters_and_numbers) for i in range(3))
            print(rand_string)
            session['rand-string'] = rand_string
            send_email(login, text=rand_string)
            session.update({'login': login, 'password_acc':password, 'FIO':fio, 'clas':int(clas), 'classletter':classletter})
            print(session['login'], session['password_acc'], session['FIO'], session['clas'], session['classletter'])
            return render_template('check_email.html')
        elif not check_email(login):
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
        print('###########################', e, '#######################', sep='\n')
        return render_template('reg_student.html', message='Неверные данные')


# #************************************Функция ученика********************************
@gui_ckop.post('/go_to_create_projects')
def go_to_create_projects(message=''):
    return render_template('create_project_for_student.html', listt=laboratories2, message=message)

@gui_ckop.post('/go_to_create_strong_side')
def go_to_create_strong_side(message=""):
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


#НАДО ДУМАТЬ НАД checkTaskDeadlinecheckTaskDeadlinecheckTaskDeadlinecheckTaskDeadlinecheckTaskDeadlinecheckTaskDeadlinecheckTaskDeadlinecheckTaskDeadline
@gui_ckop.get('/go_to_change_projects')
@gui_ckop.post('/go_to_change_projects')
def go_to_change_projects():
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
    # if num != 0:
    return render_template('proj_student.html', message=session["message"], role=data2[3][ind_user], 
                slovar=slovar, tasks=data2[4], Goal=data2[1], login=data[0], tutor=tutor, 
                members = get_members(data2[5], session['addr']),
                mes_type = session["mes_type"],
                project_name=data2[0], laboratorie=laboratories[data2[6]], ch=ch,
                new_proj_avalible=data2[0]=='')


@gui_ckop.post('/create_project')
def create_project():
    name_project = request.form['name_project']
    login = request.form['walet']
    if name_project != "":
        # try:
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
            if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Project create':
                print(ev.get_all_entries()[0]['args']['text'])
                session["message"]= ev.get_all_entries()[0]['args']['text']
            else:
                session["message"]= 'Проект успешно создан'
                session["mes_type"] = "status_class_good"
            num = contract_student.functions._findActiveProject(session['addr']).call()
            print(num)
            if login != "" and num != 0:
                tx_hash = contract_student.functions.send_request_teacher(session['login'], 
                    session['password_acc'], login, num).transact({'from': session['addr']})
                tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
                ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
                if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Request created':
                    print(ev.get_all_entries()[0]['args']['text'])
                    session["message"]= ev.get_all_entries()[0]['args']['text']
                    session["mes_type"] = "status_class_good"

            return redirect(url_for('gui_ckop.go_to_student_cabinet'))
        # except BaseException as e:
        #     print('ОШИИИИИИБКААААААААА:', e)
        #     return render_template('create_project_for_student.html', listt=laboratories2, 
        #         message="Ошибка создания проекта", mes_type = "status_class_wrong")
    else:
        return render_template('create_project_for_student.html', listt=laboratories2, 
                message="Заполните все поля", mes_type = "status_class_wrong")

@gui_ckop.post('/create_strong_side')
def create_strong_side(message=''):
    # try:
        strong_side = request.form['strong_side']
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        tx_hash = contract_student.functions.addStrongSide(session['login'], session['password_acc'], strong_side).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        block = w3.eth.block_number
        ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Change strong side':
            session["message"] = ev.get_all_entries()[0]
            session["mes_type"] = "status_class_wrong"
        else:
            session["message"] = 'Сторона успешна изменена'
            session["mes_type"] = "status_class_wrong"
        return redirect(url_for('gui_ckop.go_to_student_cabinet'))

@gui_ckop.post('/change_strong_side')
def change_strong_side(message=''):
    try:
        new_side = request.form['side']
        indexx = request.form['indexx']
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        tx_hash = contract_student.functions.changeStrongSide(session['login'], 
                        session['password_acc'], int(indexx), new_side).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        block = w3.eth.block_number
        ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Change strong side':
            session["message"] = ev.get_all_entries()[0]
            session["mes_type"] = "status_class_wrong"
        else:
            session["message"] = 'Сторона успешна изменена'
            session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.go_to_student_cabinet'))
    except BaseException as e:
        print('ОШИИИИИИБКААААААААА:', e)
        return e

@gui_ckop.post('/change_goal_project')
def change_goal_project(message=''):
    try:
        goal = request.form['goal']
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        tx_hash = contract_student.functions.changeGoalProject(session['login'], session['password_acc'], goal).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        block = w3.eth.block_number
        ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Change goal':
            print(ev.get_all_entries()[0]['args']['text'])
            session["message"] = ev.get_all_entries()[0]
            session["mes_type"] = "status_class_wrong"
        else:
            session["message"] = 'Цель успешна изменена'
            session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.go_to_change_projects'))
    except BaseException as e:
        print('ОШИИИИИИБКААААААААА:', e)
        session["message"] = 'Ошибка при изменении цели'
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for('gui_ckop.go_to_change_projects'))


@gui_ckop.post('/create_task')
def create_task(message=''):
    try:
        num = contract_student.functions._findActiveProject(session['addr']).call({'from': session['addr']})
        tasks = contract_student.functions.checkProject(num).call({'from': session['addr']})[4]
        task = request.form['task']
        data = request.form['date'].replace('.', '-')
        if task == "" or data == "":
            session["message"] = 'Заполните все поля'
            session["mes_type"] = "status_class_wrong"
        elif '' not in tasks:
            session["message"] = 'У Вас много задач в проекте'
            session["mes_type"] = "status_class_wrong"
        elif date_to_unix(data) < int(datetime.datetime.now().timestamp()):
            session["message"] = 'Некорректная дата'
            session["mes_type"] = "status_class_wrong"
        else:
            w3.geth.personal.unlock_account(session['addr'], session['password_addr'], 1000000)
            tx_hash = contract_student.functions.changeTaskInProject(session['login'], session['password_acc'], 
                tasks.index(''), task, date_to_unix(data)).transact({'from': session['addr']})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            block = w3.eth.block_number
            ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
            if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Change task':
                print(ev.get_all_entries()[0]['args']['text'])
                session["message"] = ev.get_all_entries()[0]['args']['text']
                session["mes_type"] = "status_class_wrong"
            else: 
                session["message"]='Задача добавлена'
                session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.go_to_change_projects'))
    except BaseException as e:
        print('ОШИИИИИИБКААААААААА:', e)
        session["message"] = "Ошибка при создании задачи!"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for('gui_ckop.go_to_change_projects'))



@gui_ckop.post('/changeTaskInProject')
def changeTaskInProject(message=''):
    try:
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
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Change task':
            print(ev.get_all_entries()[0]['args']['text'])
            session["message"] = ev.get_all_entries()[0]['args']['text']
            session["mes_type"] = "status_class_wrong"
        else: 
            session["message"]='Задача успешно изменена'
            session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.go_to_change_projects'))
    except BaseException as e:
        print('ОШИИИИИИБКААААААААА:', e)
        session["message"] = "Ошибка при изменении задачи!"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for('gui_ckop.go_to_change_projects'))

# #************************************Регистрация аккаунта учителя*********************************

@gui_ckop.get('/go_to_teacher_cabinet')
def go_to_teacher_cabinet():
    projects_name, login, fio, labs, sub, = teacher_cabinet_info(session['addr'])
    session.update({'lab_name': labs, "FIO":fio, "login":login})
    return render_template('teacher_cabinet.html', message=session["message"], 
            projects=projects_name, login=login, fio=fio, 
            lab=session['lab_name'], sub=sub,  mes_type = session["mes_type"])


@gui_ckop.post('/reg_teacher_check')
def reg_teacher_check():
    email = request.form['email']
    password = request.form['password']
    rep_pass = request.form['rep_password']
    FIO = request.form['FIO']
    try:
        schSub = request.form['SchoolSubjects']
        lab_s = request.form['laboratories']
    except:
        schSub = "";lab_s = ""
    try:
        if '@' in email and password != '' and FIO != '' and schSub != '' and lab_s != '' and password == rep_pass:
            rand_string = ''.join(random.choice(letters_and_numbers) for i in range(3))+''.join(random.choice(letters_and_numbers) for i in range(3))+''.join(random.choice(letters_and_numbers) for i in range(3))
            SchoolSubject = schoolSubjects[int(schSub)]
            laboratorie = laboratories[int(lab_s)]
            print(rand_string)
            session['rand-string'] = rand_string
            send_email(email, text=rand_string)
            session.update({'login': email, 'password_acc':password, 
                'FIO':FIO, 'SchoolSubject': SchoolSubject, 'laboratorie': laboratorie})
            print(session['login'], session['password_acc'], session['FIO'], [schoolSubjects2.index(session['SchoolSubject'])],  [99+laboratories2.index(session["laboratorie"])])
            return render_template('check_email_teacher.html')
        else:
            if not '@' in email: mess = "Некорректный email"
            elif password == '' or FIO == '' or schSub == '' or lab_s != '': mess = "Заполнены не все поля"
            elif password != rep_pass: mess = "Пароли не совпадают"
            else: mess = 'Неверно ведены данные'
            return render_template("reg_teacher.html", listt=laboratories, subject=schoolSubjects, 
                message=mess, mes_type="status_class_wrong")
    except BaseException as e:
        print(e)
        return render_template("reg_teacher.html", listt=laboratories, subject=schoolSubjects, 
                message="Неверно ведены данные", mes_type="status_class_wrong")


@gui_ckop.post('/check_email_teacher')
def check_email_teacher():
    check = request.form['check']
    print(session['login'], session['password_acc'], session['SchoolSubject'],  session["laboratorie"], session['addr'])
    if check == session['rand-string']:
        block = w3.eth.block_number
        tx_hash = contract_teacher_0.functions.registrationForTeacher(
            session['login'], session['password_acc'], session['FIO'], 
            [schoolSubjects2.index(session['SchoolSubject'])],
            [99+laboratories2.index(session["laboratorie"])]).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        ev = contract_teacher_0.events.Action.createFilter(fromBlock=block, toBlock="latest")
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Teacher successfully registered':
            print(ev.get_all_entries())
            print(ev.get_all_entries()[0]['args']['text'])
            return render_template("reg_teacher.html", 
                    listt=laboratories, subject=schoolSubjects, 
                    message=ev.get_all_entries()[0]['args']['text'])
        return redirect(url_for('gui_ckop.go_to_teacher_cabinet'))
    else:
        return render_template('check_email.html', message='Неверный код',mes_type="status_class_wrong")

@gui_ckop.post('/check_email')
def check_email():
    check = request.form['check']
    print(session['login'], session['password_acc'], session['FIO'], session['clas'], session['classletter'])
    if check == session['rand-string']:
        block = w3.eth.block_number
        # w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        tx_hash = contract_student.functions.registrationForStudent(session['login'], 
                session['password_acc'], session['FIO'], session['clas'], session['classletter']).transact(
                        {'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        ev = contract_student.events.Action.createFilter(fromBlock=block,toBlock="latest")
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Student successfully registered':
            print(ev.get_all_entries()[0]['args']['text'])
            message = ev.get_all_entries()[0]['args']['text']
            return render_template('reg_student.html', message=message, mes_type="status_class_wrong",
                login=session['login'], fio = session['FIO'], 
                clas = session['clas'], classletter = session['classletter'])
        return redirect(url_for('gui_ckop.go_to_student_cabinet'))
        #     return render_template("reg_student.html", listt=laboratories, subject=schoolSubjects, message=ev.get_all_entries()[0]['args']['text'])
        # return redirect(url_for('gui_ckop.go_to_student_cabinet'))
    else:
        return render_template('check_email.html', message='Неверный код',mes_type="status_class_wrong")


#**************************************************ФУНКЦИИ УЧИТЕЛЯ********************************
@gui_ckop.post('/go_to_create_projects_teacher')
def go_to_create_projects_teacher(message=''):
    return render_template('create_project_for_teacher.html', message=message)


@gui_ckop.post('/create_project_teacher')
def create_project_teacher(message=''):
    try:
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
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Create project':
            print(ev.get_all_entries()[0]['args']['text'])
            # session["message"] = ev.get_all_entries()[0]['args']['text']
            # session["mes_type"] = "status_class_wrong"
            return render_template('create_project_for_teacher.html',
                message=ev.get_all_entries()[0]['args']['text'], mes_type="status_class_wrong")
        else: 
            session["message"]='Проект создан'
            session["mes_type"] = "status_class_good"
        return redirect(url_for("gui_ckop.go_to_teacher_cabinet"))
        # return redirect(url_for('gui_ckop.go_to_change_projects'))
    except BaseException as e:
        print('ОШИИИИИИБКААААААААА:', e)
        session["message"]='Ошибка при создании проекта'
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for(gui_ckop.go_to_teacher_cabinet))

@gui_ckop.get('/go_to_create_acc_for_student')
@gui_ckop.post('/go_to_create_acc_for_student')
def go_to_create_acc_for_student():
    if request.method == "POST":
        session["message"] = ""
        session["mes_type"] = ""
    return render_template('create_acc_for_student.html', message = session["message"],
        mes_type=session["mes_type"])
    

@gui_ckop.post('/create_acc_for_student')
def create_acc_for_student():
    try:
        session["mes_type"] = "status_class_wrong"
        pass_walet = request.form['pass_walet']
        if pass_walet == "":
            session["message"] = "Введите пароль"
        else:
            new_acc = w3.geth.personal.new_account(pass_walet)
        print(new_acc)
        block = w3.eth.block_number
        tx_hash = contract_teacher_0.functions.generateAddressForStudent(
            session['login'], session['password_acc'], new_acc, pass_walet).transact(
                {'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        ev = contract_teacher_0.events.Action.createFilter(fromBlock=block, toBlock="latest")
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Address generated':
            print(ev.get_all_entries()[0]['args']['text'])
            session["message"]='Не удалось сгенерировать адрес'     
        else:
            session["message"]= new_acc
            session["mes_type"] = "status_class_good"
            contract_teacher_0.functions.myTransfer(new_acc).transact(
                {'from': '0xff42Fc7fdB5928b63da0bF2340880369fE335bf0', 
                'value': '1000000000000000'})
        return redirect(url_for('gui_ckop.go_to_create_acc_for_student'))
    except BaseException as e:
        print('ОШИИИИИИБКААААААААА:', e)
        session["message"]='Не удалось сгенерировать адрес'
        return redirect(url_for('gui_ckop.go_to_create_acc_for_student'))

@gui_ckop.post('/addStudentInProject')
def addStudentInProject(message=''):
    # try:
        session["mes_type"] = "status_class_wrong"
        login = request.form['login_student']
        if login == "" or "@" not in login:
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
                if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Add in project':
                    print(ev.get_all_entries()[0]['args']['text'])
                    session["message"] = ev.get_all_entries()[0]['args']['text']
                else:
                    session["message"] = "Ученик добавлен в проект"
                    session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.proj_tutor'))
    # except BaseException as e:
        print('Ошибка:', e)
        session["message"] = "Ошибка добавления в проект"
        return redirect(url_for('gui_ckop.proj_tutor'))

@gui_ckop.post('/go_to_look_teacher_project')
def go_to_look_teacher_project(message=''):
    proj_num = contract_teacher_0.functions.checkNumAllActiveProject().call({'from': session['addr']})
    # j=len(p)//2
    # projects_number = p[:j]
    projects_name= {}
    for i in proj_num:
        k=contract_teacher_0.functions.checkProject(i).call({'from': session['addr']})
        teacher, status = contract_makestruct1.functions.getRequestStudent(i).call()
        if k[2]==session['login'] or (teacher == session['addr'] and status == 0):
            projects_name.update({i : k[0]})    

    return render_template('proj_all_tutor.html', project_list=projects_name)


@gui_ckop.post('/go_to_change_teacher_project')
def go_to_change_teacher_project():
    if request.method == "POST":
        session["message"] = ""
        session["mes_type"] = ""
    indexxx = int(request.form['indexxx'])
    session['index_project'] = indexxx
    return(redirect(url_for("gui_ckop.proj_tutor")))
    # student_name, project_name = get_teacher_project_info(session['index_project'], session['addr'])
    # return render_template('proj_tutor.html', students = student_name, project_name=project_name, 
    #     tutor=session['FIO'], laboratorie=session['lab_name'], len_tasks = 5)

@gui_ckop.get('/proj_tutor')
def proj_tutor():
    # student_name, project_name, tasks, roles, goal, labs
    student_name, project_name, tasks, goal, labs, mentor  = get_teacher_project_info(session['index_project'], session['addr'])

    return render_template('proj_tutor.html', students = student_name, 
        project_name=project_name, 
        tutor=mentor, laboratorie=labs, len_tasks = 5, goal_project=goal,
        message=session["message"], mes_type = session["mes_type"], tasks=tasks)

@gui_ckop.post("/response_yes")
def response_yes():
    # try:
        session["mes_type"] = "status_class_wrong"
        block = w3.eth.block_number
        tx_hash = contract_teacher_1.functions.send_response_teacher(
            session['login'], session['password_acc'], session['index_project'], 
            1).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        ev = contract_teacher_1.events.Action.createFilter(fromBlock=block, toBlock="latest")
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Response created':
            print(ev.get_all_entries()[0]['args']['text'])
            session["message"] = ev.get_all_entries()[0]['args']['text']
        else:
            session["message"] = "Предложение принято"
            session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.proj_tutor'))
    # except BaseException as e:
        # print('Ошибка:', e)
        # session["message"] = "Ошибка при работе с проектом"
        # return redirect(url_for('gui_ckop.proj_tutor'))

@gui_ckop.post("/response_no")
def response_no():
    # try:
        session["mes_type"] = "status_class_wrong"
        block = w3.eth.block_number
        tx_hash = contract_teacher_1.functions.send_response_teacher(
            session['login'], session['password_acc'], session['index_project'], 2).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        ev = contract_teacher_1.events.Action.createFilter(fromBlock=block, toBlock="latest")
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Response created':
            print(ev.get_all_entries()[0]['args']['text'])
            session["message"] = ev.get_all_entries()[0]['args']['text']
        else:
            session["message"] = "Предложение отклонено"
            session["mes_type"] = "status_class_good"
        return redirect(url_for("gui_ckop.go_to_teacher_cabinet"))
    # except BaseException as e:
    #     print('Ошибка:', e)
    #     session["message"] = "Ошибка при работе с проектом"
    #     return redirect(url_for("gui_ckop.go_to_teacher_cabinet"))


# string memory _login, 
# string memory _pass,
# string memory _roleInProject,
# uint16 _numProject,
# uint16 _numUser) 
@gui_ckop.post('/create_role')
def create_role():
        role = request.form['role']
        login_user = request.form['login_student']
    # try:
        session["mes_type"] = "status_class_wrong"
        if login_user == "" or role == "":
            session["message"] = "Заполните поля"
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
                if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Successfully change role':
                    print(ev.get_all_entries()[0]['args']['text'])
                    session["message"] = ev.get_all_entries()[0]['args']['text']
                else: 
                    session["message"]='Роль успешно задана'
                    session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.proj_tutor'))
    # except BaseException as e:
    #     print('ОШИИИИИИБКААААААААА:', e)
    #     session["message"] = "Ошибка при создании роли!"
    #     return redirect(url_for('gui_ckop.proj_tutor'))

@gui_ckop.post('/create_task_teacher')
def create_task_teacher(message=''):
    try:
        # num = contract_student.functions._findActiveProject(session['addr']).call({'from': session['addr']})
        tasks = contract_student.functions.checkProject(session['index_project']).call({'from': session['addr']})[4]
        task = request.form['task']
        data = request.form['date'].replace('.', '-')
        if task == "" or data == "":
            session["message"] = 'Заполните все поля'
            session["mes_type"] = "status_class_wrong"
        elif '' not in tasks:
            session["message"] = 'У Вас много задач в проекте'
            session["mes_type"] = "status_class_wrong"
        elif date_to_unix(data) < int(datetime.datetime.now().timestamp()):
            session["message"] = 'Некорректная дата'
            session["mes_type"] = "status_class_wrong"
        else:
            w3.geth.personal.unlock_account(session['addr'], session['password_addr'], 1000000)
            tx_hash = contract_teacher_0.functions.changeTaskInProjectTeacher(session['login'], session['password_acc'], 
                session['index_project'], task, date_to_unix(data), tasks.index(''), 0).transact({'from': session['addr']})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            block = w3.eth.block_number
            ev = contract_teacher_0.events.Action.createFilter(fromBlock=block,toBlock="latest")
            if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Task change':
                print(ev.get_all_entries()[0]['args']['text'])
                session["message"] = ev.get_all_entries()[0]['args']['text']
                session["mes_type"] = "status_class_wrong"
            else: 
                session["message"]='Задача добавлена'
                session["mes_type"] = "status_class_good"
        return redirect(url_for('gui_ckop.proj_tutor'))
    except BaseException as e:
        print('ОШИИИИИИБКААААААААА:', e)
        session["message"] = "Ошибка при создании задачи!"
        session["mes_type"] = "status_class_wrong"
        return redirect(url_for('gui_ckop.proj_tutor'))

@gui_ckop.post('/changeTaskInProjectTeacher')
def changeTaskInProjectTeacher():
    try:
        # tasks = contract_student.functions.checkProject(session['index_project']).call({'from': session['addr']})[4]
        task = request.form['task']
        date = request.form['date'].replace('.', '-')
        if request.form.get("check_ready"): check = True
        else: check = False
        indexx = int(request.form['indexxx'])
        print(indexx, task, date, check)
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'], 1000000)
        # string memory _login, 
        # string memory _pass, 
        # uint16 _num_proj,
        # string memory _newTask, 
        # uint _date, 
        # uint16 _num_task, 
        # uint16 _ready
        tx_hash = contract_teacher_0.functions.changeTaskInProjectTeacher(session['login'], 
                session['password_acc'], session['index_project'], 
                task, date_to_unix(date), indexx, int(check)).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        block = w3.eth.block_number
        ev = contract_teacher_0.events.Action.createFilter(fromBlock=block,toBlock="latest")
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Task change':
            print(ev.get_all_entries()[0]['args']['text'])
            session["message"] = ev.get_all_entries()[0]['args']['text']
            session["mes_type"] = "status_class_wrong"
        else: 
            session["message"]='Задача изменена'
            session["mes_type"] = "status_class_good"
        return(redirect(url_for("gui_ckop.proj_tutor")))
        # if len(tasks) > 2: ch = 5
        # else: ch = 10
        # student_name, project_name = get_teacher_project_info(session['index_project'], session['addr'])
        # return render_template('proj_tutor.html', students = student_name, project_name=project_name, 
        #     tutor=session['FIO'], laboratorie=session['lab_name'], len_tasks = 5)
    except:
        session["message"] = "Ошибка при изменении задачи"
        session["mes_type"] = "status_class_wrong"
        return(redirect(url_for("gui_ckop.proj_tutor")))

@gui_ckop.post('/change_goal_project_tutor')
def change_goal_project_tutor(message=''):
    try:
        goal = request.form['goal']
        w3.geth.personal.unlock_account(session['addr'], session['password_addr'])
        tx_hash = contract_teacher_0.functions.changeGoalProjectTeacher(
            session['login'], session['password_acc'], goal, session["index_project"]).transact({'from': session['addr']})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        block = w3.eth.block_number
        ev = contract_teacher_0.events.Action.createFilter(fromBlock=block,toBlock="latest")
        if ev.get_all_entries() and ev.get_all_entries()[0]['args']['text'] != 'Change goal':
            print(ev.get_all_entries()[0]['args']['text'])
            session["message"] = "Ошибка при изменении цели"
            session["mes_type"] = "status_class_wrong"
        else:
            session["message"]='Цель изменена'
            session["mes_type"] = "status_class_good"
        return(redirect(url_for("gui_ckop.proj_tutor")))
    except BaseException as e:
        print('ОШИИИИИИБКААААААААА:', e)
        session["message"]='Ошибка при изменении цели!'
        session["mes_type"] = "status_class_wrong"
        return(redirect(url_for("gui_ckop.proj_tutor")))
#****************************************Запуск********************************************

if __name__ == '__main__':
    session.clear()

    # from watchminer import WatchMiner
    # WatchMiner().start() 
    gui_ckop.run(debug = True, host="0.0.0.0", port="5000")















