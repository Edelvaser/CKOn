// SPDX-License-Identifier: GPL-3.0
pragma solidity > 0.8.0 < 0.9.0;

import "./Support.sol";

contract Teacher_0 is Support {

   constructor (address _dataContract, address _structs_0, address _structs_1) Support(_dataContract, _structs_0, _structs_1) {}

    modifier onlyTeacher() {
        MakeStruct0.StatusAddress status = structs_0.getStatusAddress(msg.sender);
        if (status != MakeStruct0.StatusAddress.Teacher) {
            emit Action(msg.sender, address(0), 0, "ERROR: only teacher");
            return;
        }
        _;
    }

    modifier teachersProject(uint16 _num) {
        bool flag = false;
        uint16[] memory numActiveProject = structs_1.getActivesProjects(msg.sender);

        for (uint16 i = 0; i < numActiveProject.length;i++){
            flag = (flag || (_num == numActiveProject[i]));
        }

        if (!flag){
            emit Action(msg.sender, address(0), _num, "ERROR: Not your project");
        }
        require(flag);
        _;
    }

    function checkTeacher(address _teacher) 
        public view 
        returns (
        string memory login, 
        string memory FIO, 
        uint16 numDepartment, // выбирается из глобального массива departments (все главы кафедр будут по умолчанию занесены в систему
        uint16[] memory numSchoolSubjects, // те предметы, которы е ведёт учитель (выбираются из глобального массива schoolSubjects)
        uint16[] memory numLaboratories,// выбираются из глобального массива laboratories
        bytes32 _pass,
        bool headTeacher,
        bool scientistManager)
    {
        (login, FIO, numDepartment, numSchoolSubjects, numLaboratories, _pass, headTeacher, scientistManager) = structs_0.getTeacherStruct(_teacher);
        _pass = bytes32(0);
    }


    function registrationForTeacher(
        string memory _login, 
        string memory _pass, 
        string memory _FIO, 
        uint16[] memory _leadsSchoolSubjects, 
        uint16[] memory _laboratories) 
        public 
    {

        // string memory _login, 
        // string memory _FIO,
        // address _teacher, 
        // uint16 _numDepartment,
        // uint16[] memory _numSchoolSubjects, 
        // uint16[] memory _numLaboratories,
        // bytes32 _pass,
        // bool _headTeacher,
        // bool _scientistManager
        if (_checksForRegistration(_login, _pass, msg.sender)) {
            MakeStruct0.StatusAddress status = structs_0.getStatusAddress(msg.sender);
            if (status == MakeStruct0.StatusAddress.ForTeacher) { // проверка статус
                if ((_laboratories.length != 0) && (checkLab(_laboratories)) && checkSubjects(_leadsSchoolSubjects) && (_leadsSchoolSubjects.length != 0) && keccak256(abi.encodePacked(_FIO)) != keccak256(abi.encodePacked(""))) {
                    structs_0.setTeacherStruct(_login, _FIO, msg.sender, 0, _leadsSchoolSubjects, _laboratories, keccak256(abi.encodePacked(_login, _pass)), false, false);
                    structs_1.setFullAddedUsers(msg.sender, new address[](0));
                    structs_1.setFullAddedPasswords(msg.sender, new string[](0));
                    emit Action(msg.sender, address(0), 0, "Teacher successfully registered");
                }
                else {
                    emit Action(msg.sender, address(0), 0, "ERROR: error data");
                }
            }
            else {
                emit Action(msg.sender, address(0), 0, "ERROR: wrong address");
            }
        }
    }

    function generateAddressForStudent(
        string memory _login,
        string memory _pass,
        address _newStudent,
        string memory _pass_user)
        public userRegistered(_login, _pass, msg.sender) onlyTeacher()
    {
        MakeStruct0.StatusAddress status = structs_0.getStatusAddress(_newStudent);
        if (status == MakeStruct0.StatusAddress.Not) {
            structs_0.setStatusAddress(_newStudent, MakeStruct0.StatusAddress.ForStudent);
            structs_1.setAddedUsers(msg.sender, _newStudent);
            structs_1.setAddedPasswords(msg.sender, _pass_user);

            emit Action(msg.sender, address(0), 0, "Address generated");
        }
        else {
            emit Action(msg.sender, address(0), 0, "ERROR: address already using");
        }
    }

    function createProjectForTeacher(
        string memory _login, 
        string memory _pass, 
        string memory _nameProject, 
        uint16 _numLaboratory) 
        public onlyTeacher() userRegistered(_login, _pass, msg.sender)
    {
        if (_checksForProject(_nameProject, _numLaboratory)) {
            uint16 num = structs_0.getLengthProject();// + 1;
            address[] memory _members = new address[](5);
            structs_0.setProjectStruct(_nameProject,"", _login, new string[](10), _members, num,  _numLaboratory, 3);
            structs_0.setStatusProject(num, MakeStruct0.StatusProject.Active);
            structs_0.setLengthProject();
            structs_1.setActivesProjects(address(0), msg.sender, num);
            structs_0.setFullDeadLineInProject(num, new uint[](10));
            structs_0.setFullReadyTaskProject(num, new uint16[](10));

            emit Action(msg.sender, address(0), 0, "Create project");
        } else {
            emit Action(msg.sender, address(0), 0, "ERROR: error create project");
        }
    }

    function addStudentInProject(
        string memory _login, 
        string memory _pass, 
        uint16 _numProject,
        address addressStudent)
        public userRegistered(_login, _pass, msg.sender) onlyTeacher() teachersProject(_numProject)
    {
        if (structs_0.getStatusAddress(addressStudent) == MakeStruct0.StatusAddress.Student) {
            address[] memory membersProjects = structs_0.getMembersProject(_numProject);
            uint16 i = 0;
            for (i = 0; i < membersProjects.length; i++) {
                if (membersProjects[i] == addressStudent){
                    emit Action(msg.sender, addressStudent, _numProject, "Already in the project");
                    return;
                } 
                else if (membersProjects[i] == address(0)){
                    break;
                }
            }

            if (i == 5){
                emit Action(msg.sender, addressStudent, _numProject, "Project is full");
                return;
            }
            structs_0.setMembersProject(_numProject, i, addressStudent);
            structs_0.setOwnerProjects(addressStudent, _numProject);

            emit Action(msg.sender, addressStudent, _numProject, "Add in project");
        }
        else {
            emit Action(msg.sender, address(0), _numProject, "ERROR: this address not belong student");
        }
    }     

    function changeTaskInProjectTeacher(
        string memory _login, 
        string memory _pass, 
        uint16 _num_proj,
        string memory _newTask, 
        uint _date, 
        uint16 _num_task, 
        uint16 _ready)
        public onlyTeacher() userRegistered(_login, _pass, msg.sender) teachersProject(_num_proj)
    {
        if (structs_0.getReadyOneTaskProject(_num_proj, _num_task) == 0){
            structs_0.setTaskInProject(_num_proj, _num_task, _newTask);
            structs_0.setDeadLineInProject(_num_proj, _num_task, _date);
            structs_0.setReadyTaskProject(_num_proj, _num_task, _ready);

            emit Action(msg.sender, address(0), _num_proj, "Task change");
        } 
        else {
            emit Action(msg.sender, address(0), _num_proj, "Task is ready");
        }
    }

    function deleteStudentOutProject(
        string memory _login, 
        string memory _pass, 
        uint16 _numProject,
        address addressStudent)
        public userRegistered(_login, _pass, msg.sender) onlyTeacher() teachersProject(_numProject)
    {
        if (structs_0.getStatusAddress(addressStudent) == MakeStruct0.StatusAddress.Student) {
            address[] memory membersProjects = structs_0.getMembersProject(_numProject);
            uint16 i=0;

            for (i = 0; i < membersProjects.length; i++) {
                if (membersProjects[i] == addressStudent){
                    structs_0.setMembersProject(_numProject, i, address(0));
                    
                    emit Action(msg.sender, addressStudent, _numProject, "Delete out project");
                    return;
                }
            }
            
            if (i == 5){
                emit Action(msg.sender, addressStudent, _numProject, "Not in project");
                return;
            }
        }
        else {
            emit Action(msg.sender, address(0), _numProject, "ERROR: this address not belong student");
        }
    }

    function checkMyActiveProject() 
        public view 
        returns (
        uint16[] memory activeProject) 
    {
        activeProject = structs_1.getActivesProjects(msg.sender);
    }

    function checkNumAllActiveProject()
        public view 
        returns (
        uint16[] memory activeProject)
    {
        uint lengthProject = structs_0.getLengthProject();
        activeProject = new uint16[](lengthProject);
        uint16 j = 0;

        for (uint16 i = 0; i < lengthProject; i++){
            if (structs_0.getStatusProject(i) == MakeStruct0.StatusProject.Active || structs_0.getStatusProject(i) == MakeStruct0.StatusProject.Sleep){
                activeProject[j] = i;
                j++;
            }
        }
    }

    function changeGoalProjectTeacher(
        string memory _login, 
        string memory _pass, 
        string memory _goal,
        uint16 _num) 
        public onlyTeacher() userRegistered(_login, _pass, msg.sender)
    {
        uint16[] memory numActiveProjects = checkNumAllActiveProject();
        for (uint16 i = 0; i<numActiveProjects.length; i++){
            if (_num == numActiveProjects[i]){
                structs_0.setGoalInProject(_num, _goal);
                emit Action(msg.sender, address(0), _num, "Change goal");
                return;
            }
        }
        emit Action(msg.sender, address(0), _num, "ERROR: Not your project");
    }
}