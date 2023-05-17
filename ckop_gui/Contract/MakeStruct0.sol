// SPDX-License-Identifier: GPL-3.0
pragma solidity > 0.8.0 < 0.9.0;

import "./GlobalStorage.sol";

// contract Bred {
//     GlobalStorage data;
//     constructor (address _data) {
//         data = GlobalStorage(_data);
//     }
// }

contract MakeStruct0{

    GlobalStorage data;

    enum StatusProject {Not, Completed, Sleep, Active}
    enum StatusAddress {Not, Block, ForTeacher, ForStudent, ForAdmin, Teacher, Student, Admin}

    string[] public keys;

    address owner_contract;
    address[] logic_contract;

    // uint public start_block;
    // uint public start_date;

    constructor (address _dataContract) {
        // date  ====>   1672779600
        data = GlobalStorage(_dataContract);
        keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
            "10", "11", "12", "13", "14", "15", "16", "17", "18", 
            "19", "20", "21", "22", "23", "24", "25", "26", "27", 
            "28", "29", "30", "31", "32", "33", "34", "35", "36",
            "37", "38", "39", "40", "41", "42", "43"]; // change
        owner_contract = msg.sender;
        logic_contract.push(msg.sender);
        // start_block = block.number;
        // start_date = _date;
    }

    modifier onlyContract() {
        bool flag = false;
        for (uint16 i = 0; i < logic_contract.length; i++){
            flag = (flag || (msg.sender == logic_contract[i]));
        }
        require(flag);
        // require(true);
        _;
    }

//Secure function

    function getAddressContract() public view returns (address[] memory) {
        return logic_contract;
    }

    function setAddressContract(address _new_addr_contract) public {
        require(msg.sender == owner_contract);
        logic_contract.push(_new_addr_contract);
    }

    function getOwnerContract() public view returns (address) {
        return owner_contract;
    }

    function setOwnerContract(address _new_addr_owner) public {
        require(msg.sender == owner_contract);
        owner_contract = _new_addr_owner;
    }

//Student function

    function getStudentStruct(address _student) external view returns (
        string memory login, 
        string memory FIO, 
        string memory classLetter, 
        string[] memory strongSides, 
        uint8 class, 
        bytes32 pass)
    {
        login = data.getStringDataUser(keccak256(abi.encodePacked(_student, keys[2])));
        FIO = data.getStringDataUser(keccak256(abi.encodePacked(_student, keys[1])));
        classLetter = data.getStringDataUser(keccak256(abi.encodePacked(_student, keys[3])));
        strongSides = data.getStringArrayDataUser(keccak256(abi.encodePacked(_student, keys[4])));
        class = data.getUint8DataUser(keccak256(abi.encodePacked(_student, keys[5])));
        pass = data.getBytes32DataUser(keccak256(abi.encodePacked(_student, keys[10])));
    }

    function setStudentStruct(
        string memory _login, 
        string memory _FIO,
        string memory _classLetter, 
        string[] memory _strongSides,
        address _student,
        uint8 _class, 
        bytes32 _pass)
    external onlyContract()
    {
        data.setStringDataUser(keccak256(abi.encodePacked(_student, keys[2])), _login); // логин
        data.setStringDataUser(keccak256(abi.encodePacked(_student, keys[1])), _FIO); // ФИО
        data.setStringDataUser(keccak256(abi.encodePacked(_student, keys[3])), _classLetter); // буква класса
        data.setFullStringArrayDataUser(keccak256(abi.encodePacked(_student, keys[4])), _strongSides); // сильные стороны
        data.setUint8DataUser(keccak256(abi.encodePacked(_student, keys[5])), _class); // номер класса
        data.setBytes32DataUser(keccak256(abi.encodePacked(_student, keys[10])), _pass); // пароль
        
        data.setAddressDataUser(keccak256(abi.encodePacked(_login, keys[28])), _student); // адрес теперь используется
        data.setUint8DataUser(keccak256(abi.encodePacked(_student, keys[15])), uint8(StatusAddress.Student)); // изменение статуса адреса
        data.setBoolDataUser(keccak256(abi.encodePacked(_login, keys[14])), true); // логин используется

        data.setFullUint16ArrayDataUser(keccak256(abi.encodePacked(_student, keys[9])), new uint16[](0)); // другие проекты
    }

    function getStudentStrongSide(address _student) view external returns (string[] memory strongSides) {
        strongSides = data.getStringArrayDataUser(keccak256(abi.encodePacked(_student, keys[4])));
    }

    function setStudentStrongSide(string memory _strongSide, address _student, uint16 _num) external onlyContract() {   
        data.setStringArrayDataUser(keccak256(abi.encodePacked(_student, keys[4])), _num, _strongSide);
    }


//Teacher function
    function getTeacherStruct(address _teacher) external view returns (
        string memory FIO, 
        string memory login, 
        uint16 numDepartment,
        uint16[] memory numSchoolSubjects,
        uint16[] memory numLaboratories,
        bytes32 pass,
        bool headTeacher,
        bool scientistManager
    )
    {
        FIO = data.getStringDataUser(keccak256(abi.encodePacked(_teacher, keys[1])));
        login = data.getStringDataUser(keccak256(abi.encodePacked(_teacher, keys[0])));
        numDepartment = data.getUint16DataUser(keccak256(abi.encodePacked(_teacher, keys[6])));
        numSchoolSubjects = data.getUint16ArrayDataUser(keccak256(abi.encodePacked(_teacher, keys[7])));
        numLaboratories = data.getUint16ArrayDataUser(keccak256(abi.encodePacked(_teacher, keys[8])));
        pass = data.getBytes32DataUser(keccak256(abi.encodePacked(_teacher, keys[4])));
        headTeacher = data.getBoolDataUser(keccak256(abi.encodePacked(_teacher, keys[11])));
        scientistManager = data.getBoolDataUser(keccak256(abi.encodePacked(_teacher, keys[12])));
    }

    function setTeacherStruct(
        string memory _login, 
        string memory _FIO,
        address _teacher, 
        uint16 _numDepartment,
        uint16[] memory _numSchoolSubjects, 
        uint16[] memory _numLaboratories,
        bytes32 _pass,
        bool _headTeacher,
        bool _scientistManager
    ) external onlyContract()
    {
        data.setStringDataUser(keccak256(abi.encodePacked(_teacher, keys[0])), _login);
        data.setStringDataUser(keccak256(abi.encodePacked(_teacher, keys[1])), _FIO);
        data.setUint16DataUser(keccak256(abi.encodePacked(_teacher, keys[6])),_numDepartment);
        data.setFullUint16ArrayDataUser(keccak256(abi.encodePacked(_teacher, keys[7])),_numSchoolSubjects);
        data.setFullUint16ArrayDataUser(keccak256(abi.encodePacked(_teacher, keys[8])), _numLaboratories);
        data.setBytes32DataUser(keccak256(abi.encodePacked(_teacher, keys[10])), _pass);
        data.setBoolDataUser(keccak256(abi.encodePacked(_teacher, keys[11])), _headTeacher);
        data.setBoolDataUser(keccak256(abi.encodePacked(_teacher, keys[12])), _scientistManager);

        data.setAddressDataUser(keccak256(abi.encodePacked(_login, keys[28])), _teacher); 
        data.setUint8DataUser(keccak256(abi.encodePacked(_teacher, keys[15])), uint8(StatusAddress.Teacher)); // статус адреса
        data.setBoolDataUser(keccak256(abi.encodePacked(_login, keys[14])), true);

        data.setFullUint16ArrayDataUser(keccak256(abi.encodePacked(_teacher, keys[9])), new uint16[](0));
    }

//Project function

    function getProjectStruct(uint16 _num) external view returns(
        string memory name,
        string memory goal,
        string memory loginMentor,
        string[] memory roleMembers,
        string[] memory tasksMembers,
        address[] memory members,
        uint16 numLaboratory
        // uint16 status,
        // uint16[] memory needKnowledge
    )
    {
        name = data.getStringDataProject(keccak256(abi.encodePacked(_num, keys[17])));
        goal = data.getStringDataProject(keccak256(abi.encodePacked(_num, keys[18])));
        loginMentor = data.getStringDataProject(keccak256(abi.encodePacked(_num, keys[23])));
        members = data.getAddressArrayDataProject(keccak256(abi.encodePacked(_num, keys[24])));
        numLaboratory = data.getUint16DataProject(keccak256(abi.encodePacked(_num, keys[25])));
        // needKnowledge = data.getUint16ArrayDataProject(keccak256(abi.encodePacked(_num, keys[26])));
        // status = data.getUint16DataProject(keccak256(abi.encodePacked(_num, keys[27])));
        tasksMembers = data.getStringArrayDataProject(keccak256(abi.encodePacked(_num, keys[20])));
        // roleMembers = data.getStringDataUser(keccak256(abi.encodePacked(_num, keys[19])));
        roleMembers = data.getStringArrayDataProject(keccak256(abi.encodePacked(_num, keys[19])));

    }

    function setProjectStruct(
        string memory _name,
        string memory _goal,
        string memory _mentor, // addess login
        // string[] memory _roleMembers,
        string[] memory _tasksMembers,
        address[] memory _members,
        uint16 _num,
        uint16 _numLaboratory,
        uint8 _status
        // uint16[] memory _needKnowledge
    ) external onlyContract()
    {
        data.setStringDataProject(keccak256(abi.encodePacked(_num, keys[17])), _name);
        data.setStringDataProject(keccak256(abi.encodePacked(_num, keys[18])), _goal);
        data.setStringDataProject(keccak256(abi.encodePacked(_num, keys[23])), _mentor);
        data.setFullAddressArrayDataProject(keccak256(abi.encodePacked(_num, keys[24])), _members);//
        data.setUint16DataProject(keccak256(abi.encodePacked(_num, keys[25])), _numLaboratory);
        // data.setFullUint16ArrayDataProject(keccak256(abi.encodePacked(_num, keys[26])), _needKnowledge);
        data.setUint16DataProject(keccak256(abi.encodePacked(_num, keys[27])), _status);
        data.setFullStringArrayDataProject(keccak256(abi.encodePacked(_num, keys[20])), _tasksMembers);
        // data.setStringDataUser(keccak256(abi.encodePacked(_num, keys[19])),_roleMembers);
        data.setFullStringArrayDataProject(keccak256(abi.encodePacked(_num, keys[19])), new string[](5));

        data.pushUint16ArrayDataUser(keccak256(abi.encodePacked(_members[0], keys[9])), _num);
        data.setUint16DataProject(keccak256(abi.encodePacked(keys[16])), _num);
    }

    function getOwnerProjects(address _addr) external view returns(uint16[] memory own_proj)
    {
        own_proj = data.getUint16ArrayDataUser(keccak256(abi.encodePacked(_addr, keys[9])));
    }

    function setOwnerProjects(address _addr, uint16 _num) external
    {
        data.pushUint16ArrayDataUser(keccak256(abi.encodePacked(_addr, keys[9])), _num);
    }

    function getStatusProject(uint16 _num) external view returns(StatusProject status)
    {
        status = StatusProject(data.getUint16DataProject(keccak256(abi.encodePacked(_num, keys[27]))));
    }
    
    function setStatusProject(uint16 _num, StatusProject _status) external onlyContract()
    {
        data.setUint16DataProject(keccak256(abi.encodePacked(_num, keys[27])), uint16(_status));
    }

    // function setRoleMembers(uint16 _num, string memory _roleMembers) external onlyContract()
    // {
    //     data.setStringDataUser(keccak256(abi.encodePacked(_num, keys[19])), _roleMembers);
    // }

    function setRoleMembers(uint16  _num_project, uint16 _num, string memory _roleMembers) external  onlyContract()
    {
        data.setStringArrayDataProject(keccak256(abi.encodePacked(_num_project, keys[19])), _num, _roleMembers);
    }

    function getTaskInProject(uint16 _num_project) view external returns (string[] memory tasksProject)
    {
        tasksProject = data.getStringArrayDataProject(keccak256(abi.encodePacked(_num_project, keys[20])));
    }

    function setTaskInProject(uint16  _num_project, uint16 _num, string memory _tasks) external  onlyContract()
    {
        data.setStringArrayDataProject(keccak256(abi.encodePacked(_num_project, keys[20])), _num, _tasks);
    }

    function setGoalInProject(uint16 _num, string memory _goal) external  onlyContract()
    {
        data.setStringDataProject(keccak256(abi.encodePacked(_num, keys[18])), _goal);
    }

    function getLengthProject() view external returns (uint16 LengthProject)
    {
        LengthProject = data.getUint16DataProject(keccak256(abi.encodePacked(keys[16])));
    }

    function setLengthProject() external  onlyContract()
    {
        data.setUint16DataProject(keccak256(abi.encodePacked(keys[16])), this.getLengthProject() + 1);
    }

    function getMembersProject(uint16 _num)
    view external 
    returns (address[] memory membersProjects)
    {
        membersProjects = data.getAddressArrayDataProject(keccak256(abi.encodePacked(_num, keys[24])));
    }

    function setMembersProject(uint16 _num, uint16 _num_memb, address _newStudent) 
    external  onlyContract()
    {
        data.setAddressArrayDataProject(keccak256(abi.encodePacked(_num, keys[24])), 
            _num_memb, _newStudent);
    }

    function getDeadLineInProject(uint16 _num_project) view external returns (uint[] memory deadLineProject)
    {
        deadLineProject = data.getUintArrayDataProject(keccak256(abi.encodePacked(_num_project, keys[36])));
    }

    function setDeadLineInProject(uint16  _num_project, uint16 _num, uint _deadLineTask) external  onlyContract()
    {
        data.setUintArrayDataProject(keccak256(abi.encodePacked(_num_project, keys[36])), _num, _deadLineTask);
    }

    function setFullDeadLineInProject(uint16  _num_project, uint[] memory _deadLineTask) external  onlyContract()
    {
        data.setFullUintArrayDataProject(keccak256(abi.encodePacked(_num_project, keys[36])), _deadLineTask);
    }

    function getReadyTaskProject(uint16 _num_project) view external returns (uint16[] memory readyTasksProject)
    {
        readyTasksProject = data.getUint16ArrayDataProject(keccak256(abi.encodePacked(_num_project, keys[37])));
    }

    function getReadyOneTaskProject(uint16 _num_project, uint16 _num_task) 
    view external returns (uint16 readyTaskProject)
    {
        readyTaskProject = data.getUint16ArrayDataProject(keccak256(abi.encodePacked(_num_project, keys[37])))[_num_task];
    }

    function setReadyTaskProject(uint16  _num_project, uint16 _num, uint16 _readyTask) external  onlyContract()
    {
        data.setUint16ArrayDataProject(keccak256(abi.encodePacked(_num_project, keys[37])), _num, _readyTask);
    }

    function setFullReadyTaskProject(uint16  _num_project, uint16[] memory _readyTask) external  onlyContract()
    {
        data.setFullUint16ArrayDataProject(keccak256(abi.encodePacked(_num_project, keys[37])), _readyTask);
    }


//Dop function
    function getStatusAddress(address _addr) external view returns(StatusAddress status)
    {
        status = StatusAddress(data.getUint8DataUser(keccak256(abi.encodePacked(_addr, keys[15]))));
    }

    function setStatusAddress(
       address _addr,
       StatusAddress _status
    ) external onlyContract()
    {
        data.setUint8DataUser(keccak256(abi.encodePacked(_addr, keys[15])), uint8(_status));
    }

    function getPassword(address _addr) external view onlyContract() returns(bytes32 pass)
    {
        pass = data.getBytes32DataUser(keccak256(abi.encodePacked(_addr, keys[10])));
    }

    function getUsingLogin(string memory _login) external view returns(address usingLogin)
    {
        usingLogin = data.getAddressDataUser(keccak256(abi.encodePacked(_login, keys[28])));
    }

    function getUsingAddress(address _addr) external view returns(string memory login)
    {
        login = data.getStringDataUser(keccak256(abi.encodePacked(_addr, keys[0])));
    }

    function getUsingEmail(string memory _email) external view returns(bool usingEmail)
    {
        usingEmail = data.getBoolDataUser(keccak256(abi.encodePacked(_email, keys[14])));
    }

    function getSchSubjects() external view returns(uint16[] memory schSubjects)
    {
        schSubjects = data.getUint16ArrayDataUser(keccak256(abi.encodePacked(keys[21])));
    }

    function getLaboratories() external view returns(uint16[] memory labor)
    {
        labor = data.getUint16ArrayDataUser(keccak256(abi.encodePacked(keys[22])));
    }

    // function setLaboratories(
    //    uint16[] memory laboratories
    // ) external onlyContract()
    // {
    //     data.setFullUint16ArrayDataUser(keccak256(abi.encodePacked(keys[22])), laboratories);
    //     data.setUint16DataUser(keccak256(abi.encodePacked(keys[31])), uint16(laboratories.length));
    // }

    // function setSchSubjects(
    //    uint16[] memory schSubjects
    // ) external onlyContract()
    // {
    //     data.setFullUint16ArrayDataUser(keccak256(abi.encodePacked(keys[21])), schSubjects);
    //     data.setUint16DataUser(keccak256(abi.encodePacked(keys[30])), uint16(schSubjects.length));
    // }

    // function setDepartments(
    //    uint16[] memory departments
    // ) external onlyContract()
    // {
    //     data.setFullUint16ArrayDataUser(keccak256(abi.encodePacked(keys[29])), departments);
    //     data.setUint16DataUser(keccak256(abi.encodePacked(keys[32])), uint16(departments.length));
    // }


    // function getActivesProjectsStudent(address _addr) external view returns(uint16 own_proj)
    // {
    //     own_proj = data.getUint16DataUser(keccak256(abi.encodePacked(_addr, keys[34])));
    // }

    // function getActivesProjects(address _addr) external view returns(uint16[] memory own_proj)
    // {
    //     own_proj = data.getUint16ArrayDataUser(keccak256(abi.encodePacked(_addr, keys[35])));
    // }

    // function setActivesProjects(address _addr_student, address _addr_teacher, uint16 _num_project) external
    // {
    //     data.pushUint16ArrayDataUser(keccak256(abi.encodePacked(_addr_teacher, keys[35])), _num_project);
    //     data.setUint16DataUser(keccak256(abi.encodePacked(_addr_student, keys[34])), _num_project);
    // }


    // function getAddedUsers(address _sender) 
    // view external returns (address[] memory addedUsers)
    // {
    //     addedUsers = data.getAddressArrayDataUsers(keccak256(abi.encodePacked(_sender, keys[38])));
    // }

    // function setAddedUsers(address _sender, address _user) external  onlyContract()
    // {
    //     data.addAddressArrayDataUsers(keccak256(abi.encodePacked(_sender, keys[38])), _user);
    // }

    // function setFullAddedUsers(address _sender, address[] memory _addedUsers) external  onlyContract()
    // {
    //     data.setFullAddressArrayDataUsers(keccak256(abi.encodePacked(_sender, keys[38])), _addedUsers);
    // }

    // function getAddedPasswords(address _sender) 
    // view external returns (string[] memory passUsers)
    // {
    //     require(msg.sender == owner_contract);
    //     passUsers = data.getStringArrayDataUser(keccak256(abi.encodePacked(_sender, keys[39])));
    // }

    // function setAddedPasswords(address _sender, string memory _userPass) external  onlyContract()
    // {
    //     data.addStringArrayDataUser(keccak256(abi.encodePacked(_sender, keys[39])), _userPass);
    // }

    // function setFullAddedPasswords(address _sender, string[] memory _addedPass) external  onlyContract()
    // {
    //     data.setFullStringArrayDataUser(keccak256(abi.encodePacked(_sender, keys[39])), _addedPass);
    // }

}