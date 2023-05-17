// SPDX-License-Identifier: GPL-3.0
pragma solidity > 0.8.0 < 0.9.0;

import "./Support.sol";

contract Student is Support {

    constructor (address _dataContract, address _structs_0, address _structs_1) 
            Support(_dataContract, _structs_0, _structs_1) {}

    modifier onlyStudent() {
        MakeStruct0.StatusAddress status = structs_0.getStatusAddress(msg.sender);
        if (status != MakeStruct0.StatusAddress.Student) {
            emit Action(msg.sender, address(0), 0, "ERROR: only student");
            return;
        }
        _;
    }


    // ПРЕ: логин (проверяется в функции _checksForRegistration), пароль (проверяется в функции _checksForRegistration), ФИО (проверяется интерфейсом), номер класса (только с 1 по 11 включительно), 
    // буква класса (один русский символ или два английских), адрес для одноразовой регистрации ученика (адрес должен быть сгенерирован учителем в функции generateAddressForStudent).
    // ПРО: успех - ничего (Пользователь успешно зарегестрирован) / провал - ничего (Неверный адрес / Неверная буква класса / Неверный номер класса).
    function registrationForStudent(
        string memory _login, 
        string memory _pass, 
        string memory _FIO, 
        uint8 _class, 
        string memory _classLetter) public 
    {  
        // string memory _login, 
        // string memory _FIO,
        // string memory _classLetter, 
        // string[] memory _strongSides,
        // address _student,
        // uint8 _class, 
        // bytes32 _pass
        // Функция доступна всем. Если входные данные в порядке, функция создаёт новый аккаунт ученика
        if (_checksForRegistration(_login, _pass, msg.sender)) { // вызывается приватная функция
            if (_class <= 11 && _class >= 1) { // проверка номера класса
                MakeStruct0.StatusAddress status = structs_0.getStatusAddress(msg.sender);
                if (status == MakeStruct0.StatusAddress.ForStudent) { // проверка статуса адреса
                    if (!structs_0.getUsingEmail(_login)) {
                        string[] memory _strongSides = new string[](5);
                        structs_0.setStudentStruct(_login, _FIO, _classLetter,_strongSides, msg.sender, _class, keccak256(abi.encodePacked(_login, _pass)));

                        emit Action(msg.sender, address(0), 0, "Student successfully registered");
                    }
                    else {
                        emit Action(msg.sender, address(0), 0, "ERROR: email occupied");
                    }
                }
                else {
                    emit Action(msg.sender, address(0), 0, "ERROR: wrong address");
                }
            }
            else {
                emit Action(msg.sender, address(0), 0, "ERROR: wrong class");
            }
        }
    }

    function createProjectForStudent(
        string memory _login, 
        string memory _pass, 
        string memory _nameProject, 
        string memory _loginMentor,
        uint16 _numLaboratory) 
        public onlyStudent() userRegistered(_login, _pass, msg.sender)
    {
        address mentor = address(0);
        if (keccak256(abi.encodePacked(_loginMentor)) != keccak256(abi.encodePacked(""))){
            mentor = structs_0.getUsingLogin(_loginMentor);
        }

        if (_findActiveProject(msg.sender) == 0) {
            if (structs_0.getStatusAddress(mentor) == MakeStruct0.StatusAddress.Teacher || mentor == address(0)) {
                if (_checksForProject(_nameProject, _numLaboratory)) {
                    uint16 num = structs_0.getLengthProject();// + 1;
                    address[] memory _members = new address[](5);
                    _members[0] = msg.sender;
        // string memory _name,
        // string memory _goal,
        // string memory _mentor, // addess login
        // string memory _roleMembers,
        // string[] memory _tasksMembers,
        // address[] memory _members,
        // uint16 _num,
        // uint16 _numLaboratory,
        // uint8 _status,
                    structs_0.setProjectStruct(_nameProject,"", _loginMentor, new string[](10),_members,num,_numLaboratory, 3);
                    structs_0.setStatusProject(num, MakeStruct0.StatusProject.Active);

                    if (keccak256(abi.encodePacked(_loginMentor)) != keccak256(abi.encodePacked(""))) {
                       structs_1.setActivesProjects(msg.sender, structs_0.getUsingLogin(_loginMentor), num);
                    }
                    structs_0.setFullDeadLineInProject(num, new uint[](10));
                    structs_0.setFullReadyTaskProject(num, new uint16[](10));
                    structs_0.setLengthProject();

                    emit Action(msg.sender, address(0), 0, "Project create");
                } 
                else {
                    emit Action(msg.sender, address(0), 0, "ERROR: error data");
                }
            } 
            else {
                emit Action(msg.sender, address(0), 0, "ERROR: teacher not exist");
            }
            
        } 
        else {
            emit Action(msg.sender, address(0), 0, "ERROR: you already have active project");
        }
    }

    function send_request_teacher(
        string memory _login, 
        string memory _pass,
        string memory _loginMentor, 
        uint16 _num)
        // 0 - запрос отправлен, 1 - запрос принят, 2 - запрос отклонен
    public onlyStudent() userRegistered(_login, _pass, msg.sender)
    {
        address teacher;
        uint16 status;

        (teacher, status) = structs_1.getRequestStudent(_num);
        if (teacher == address(0)){
            address mentor = structs_0.getUsingLogin(_loginMentor);
            structs_1.setRequestStudent(_num, mentor, 0);
            emit Action(msg.sender, address(0), 0, "Request created");
        } else {
            emit Action(msg.sender, address(0), 0, "Request has already been created");
        }
    }

    // function addStrongSide(string memory _login, string memory _pass, string memory _strongSide) public onlyStudent() userRegistered(_login, _pass, msg.sender) {
    //     string[] memory strongSides = structs_0.getStudentStrongSide(msg.sender);  
    //     if (strongSides.length < 10) {
    //         structs_0.setStudentStrongSide(_strongSide, msg.sender, uint16(strongSides.length) + 1);

    //         emit Action(msg.sender, address(0), 0, "Successfully add strong side");
    //     }
    //     else {
    //         emit Action(msg.sender, address(0), 0, "ERROR: have too much strong sides");
    //     }
    // }

    function changeStrongSide(
        string memory _login, 
        string memory _pass,
        uint16 _numStrongSide, 
        string memory _newStrongSide) 
        public onlyStudent() userRegistered(_login, _pass, msg.sender)
    {
        string[] memory strongSides = structs_0.getStudentStrongSide(msg.sender);   
        if (strongSides.length > _numStrongSide) {
            structs_0.setStudentStrongSide(_newStrongSide, msg.sender, _numStrongSide);

            emit Action(msg.sender, address(0), 0, "Change strong side");
        }
        else {
            emit Action(msg.sender, address(0), 0, "ERROR: wrong number strong side");
        }
    }

    function addTaskInProject(
        string memory _login, 
        string memory _pass,
        string memory _task) 
        public onlyStudent() userRegistered(_login, _pass, msg.sender) haveActiveProject(msg.sender) 
    {
        uint16 numActiveProject = _findActiveProject(msg.sender);
        string[] memory tasksProject = structs_0.getTaskInProject(numActiveProject);
        if (tasksProject.length < 10) {
            structs_0.setTaskInProject(numActiveProject, uint16(tasksProject.length) + 1, _task);

            emit Action(msg.sender, address(0), numActiveProject, "Add task");
        } else {
            emit Action(msg.sender, address(0), numActiveProject, "ERROR: too much tasks");
        }
    }

    function changeTaskInProject(
        string memory _login, 
        string memory _pass, 
        uint8 _numTask, 
        string memory _newTask, 
        uint _date) 
        public onlyStudent() userRegistered(_login, _pass, msg.sender) haveActiveProject(msg.sender)
    {
        uint16 numActiveProject = _findActiveProject(msg.sender);
        string[] memory tasksProject = structs_0.getTaskInProject(numActiveProject);

        if (tasksProject.length > _numTask) {
            if (structs_0.getReadyOneTaskProject(numActiveProject, _numTask) == 0){
                structs_0.setTaskInProject(numActiveProject, _numTask, _newTask);
                structs_0.setDeadLineInProject(numActiveProject, _numTask, _date);
                structs_0.setReadyTaskProject(numActiveProject, _numTask, 0);

                emit Action(msg.sender, address(0), numActiveProject, "Change task");
            } 
            else {
                emit Action(msg.sender, address(0), numActiveProject, "Task is ready");
            }
        }
        else {
            emit Action(msg.sender, address(0), numActiveProject, "ERROR: wrong number task");
        }
    }

    function changeGoalProject(
        string memory _login, 
        string memory _pass, 
        string memory _goal) 
        public onlyStudent() userRegistered(_login, _pass, msg.sender) haveActiveProject(msg.sender)
    {
        uint16 numActiveProject = _findActiveProject(msg.sender);
        structs_0.setGoalInProject(numActiveProject, _goal);

        emit Action(msg.sender, address(0), numActiveProject, "Change goal");
    }


    function checkStudent(address _student) public view 
        returns (
            string memory login,
            string memory FIO,
            string memory classLetter,
            string[] memory strongSides,
            uint8 class,
            bytes32 _pass) 
    {
        // string memory login, 
        // string memory FIO, 
        // string memory classLetter, 
        // string[] memory strongSides, 
        // uint8 class, 
        // bytes32 pass
        
        (login, FIO, classLetter, strongSides, class, _pass) = structs_0.getStudentStruct(_student);

        _pass = bytes32(0); // а вот пароль секретный, его нельзя показывать
    }
    function checkProjectStudent(
        address _student) 
        public view 
        returns (
            string memory name,
            string memory goal,
            string memory mentor,
            string[] memory roleMembers,
            string[] memory tasksMembers,
            address[] memory members,
            uint16 numLaboratory
            // uint16[] memory needKnowledge
            
        )
        // string memory name,
        // string memory goal,
        // string memory loginMentor,
        // string memory roleMembers,
        // string[] memory tasksMembers,
        // address[] memory members,
        // uint16 numLaboratory,
        // uint16[] memory needKnowledge

        {
        uint16 numActiveProject = _findActiveProject(_student);
        (name, goal, mentor, roleMembers,tasksMembers, members, numLaboratory)= structs_0.getProjectStruct(numActiveProject);
    }
}