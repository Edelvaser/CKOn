// SPDX-License-Identifier: GPL-3.0
pragma solidity > 0.8.0 < 0.9.0;

import "./GlobalStorage.sol";
import "./MakeStruct0.sol";
import "./MakeStruct1.sol";

contract Support {

    GlobalStorage data;
    MakeStruct0 structs_0;
    MakeStruct1 structs_1;

    event Action (address hero, address target, uint16 numProject, string text);

    modifier userRegistered(string memory _login, string memory _pass, address _sender) {
        MakeStruct0.StatusAddress status = structs_0.getStatusAddress(_sender);
        require(status == MakeStruct0.StatusAddress.Student || status == MakeStruct0.StatusAddress.Teacher ||
            status == MakeStruct0.StatusAddress.Admin);
        require(structs_0.getPassword(_sender) == keccak256(abi.encodePacked(_login, _pass)));
        _;
    }

    modifier normalText(string memory _text) 
    {
        if (bytes(_text).length < 20) { // 10 русских символов
            emit Action(msg.sender, address(0), 0, "ERROR: short text");
            return;
        } 
        if (bytes(_text).length > 340) { // или 170 русских символов
            emit Action(msg.sender, address(0), 0, "ERROR: long text");
            return;
        }
        _;
    }

    modifier haveActiveProject(address _user) 
    {
        uint16 numActiveProject = _findActiveProject(_user);
        if (numActiveProject == 0) {
            emit Action(msg.sender, address(0), 0, "ERROR: you don't have an active project");
            return;
        }
        _;
    }


    constructor (address _data, address _struct_0, address _struct_1) {
        data = GlobalStorage(_data);
        structs_0 = MakeStruct0(_struct_0);
        structs_1 = MakeStruct1(_struct_1);
    }


    function checkRegister(string memory _login, string memory _pass, address _sender) 
    external view returns (bool) 
    {
        MakeStruct0.StatusAddress status = structs_0.getStatusAddress(_sender);
        if (status != MakeStruct0.StatusAddress.Student &&
        status != MakeStruct0.StatusAddress.Teacher &&
        status != MakeStruct0.StatusAddress.Admin) {
            return false;
        }
        bytes32 passSender = structs_0.getPassword(_sender);
        if (!(passSender == keccak256(abi.encodePacked(_login, _pass)))) {
            return false;
        }
        return true;
    }

    function _findActiveProject(address _user) 
    public view returns (uint16 activeProject) 
    {
        uint16[] memory myProjects = structs_0.getOwnerProjects(_user);
        for (uint16 i = 0; i < myProjects.length; i++) {
            if (structs_0.getStatusProject(myProjects[i]) == MakeStruct0.StatusProject.Active || 
                structs_0.getStatusProject(myProjects[i]) == MakeStruct0.StatusProject.Sleep) {
                return myProjects[i];
            }
        }
        return 0;
    }

    function _checksForProject(string memory _nameProject, uint16 _numLaboratory) 
    internal returns (bool) 
    {
        if (bytes(_nameProject).length >= 14) {
            if (bytes(_nameProject).length <= 100) {
                uint16[] memory laboratories = structs_0.getLaboratories();
                for (uint16 i = 0; i < laboratories.length; i++){
                    if (_numLaboratory == laboratories[i]) {
                       return true;
                    }
                }
                emit Action(msg.sender, address(0), 0, "ERROR: wrong number laboratory");
            }
            else {
                emit Action(msg.sender, address(0), 0, "ERROR: too long name project");
            }
        }
        else {
            emit Action(msg.sender, address(0), 0, "ERROR: short name project");
        }
        return false;
    }

    function _checksForRegistration(
        string memory _login, 
        string memory _pass, 
        address _sender)
        internal returns (bool) {
        if (bytes(_pass).length != 0 && bytes(_login).length != 0) {
            if (structs_0.getUsingLogin(_login) == address(0)) {
                MakeStruct0.StatusAddress status = structs_0.getStatusAddress(_sender);
                if (status != MakeStruct0.StatusAddress.Teacher && 
                    status != MakeStruct0.StatusAddress.Student &&
                    status != MakeStruct0.StatusAddress.Admin) {
                    return true;
                }
                else {
                    emit Action(msg.sender, address(0), 0, "ERROR: address occupied");
                }
            }
            else {
                emit Action(msg.sender, address(0), 0, "ERROR: login occupied");
            }
        }
        else {
            emit Action(msg.sender, address(0), 0, "ERROR: empty password or login");
        }
        return false;
    }
    
    function auth (
        string memory _login, 
        string memory _pass, 
        address _sender) 
        external view userRegistered(_login, _pass, _sender)
        returns (bool a) 
    {
        return true;
    }

    function myTransfer(address _recipient) external payable 
    {
        if (msg.sender.balance >= msg.value) {
            payable(_recipient).transfer(msg.value);
        }
    }

    function checkLab(uint16[] memory _lab) internal view returns (bool flag){
        uint16[] memory laboratories = structs_0.getLaboratories();
        uint8 c = 0;
        for (uint16 i=0; i<_lab.length; i++){
            for (uint16 j=0; j<laboratories.length; j++){
                if (_lab[i] == laboratories[j]) {
                    c += 1; break;
                }
            }
        }
        flag = (c == _lab.length);
    }

    function checkSubjects(uint16[] memory _subject) internal view returns (bool flag){
        uint16[] memory subjects = structs_0.getSchSubjects();
        uint8 c = 0;
        for (uint16 i = 0; i < _subject.length; i++){
            for (uint16 j = 0; j < subjects.length; j++){
                if (_subject[i] == subjects[j]) {
                    c += 1;
                    break;
                }
            }
        }
        flag = (c == _subject.length);
    }

    function checkProject(uint16 _numProject) public view 
        returns (
            string memory name,
            string memory goal,
            string memory loginMentor,
            string[] memory roleMembers,
            string[] memory tasks,
            address[] memory members,
            uint16 numLaboratory
            // uint16[] memory numSchoolSubjects
        )
    {
        // string memory name,
        // string memory goal,
        // string memory loginMentor,
        // string memory roleMembers,
        // string[] memory tasksMembers,
        // address[] memory members,
        // uint16 numLaboratory,
        // uint16 status,
        (name, goal, loginMentor, roleMembers, tasks, members, numLaboratory) = structs_0.getProjectStruct(_numProject);
    }

    function checkTaskDeadline(
        uint16 _num) 
        public view 
        returns (
            string[] memory tasksMembers,
            uint[] memory deadLine,
            uint16[] memory ready
        ) 
        {
        tasksMembers = structs_0.getTaskInProject(_num);
        deadLine = structs_0.getDeadLineInProject(_num);
        ready = structs_0.getReadyTaskProject(_num);
    }

    function checkNumArhiveProject() 
        public view 
        returns (
            uint16[] memory archiveProject
        )
        {
        uint lengthProject = structs_0.getLengthProject();
        archiveProject = new uint16[](lengthProject);
        uint16 j = 0;
        for (uint16 i=0; i<lengthProject; i++){
            if (structs_0.getStatusProject(i) != MakeStruct0.StatusProject.Active && 
                structs_0.getStatusProject(i)!= MakeStruct0.StatusProject.Not){
                archiveProject[j] = i;
                j++;
            }
        }
    }


    function constructData(
        // uncomment on product
        // uint16[] memory _schSubjects, 
        // uint16[] memory _laboratories,
        // uint16[] memory _departments)
        )
        external {
        //comment on product
        uint16[] memory _schSubjects = new uint16[](7);
        uint16[] memory _laboratories = new uint16[](7);
        uint16[] memory _departments = new uint16[](7);
        for (uint16 i=0;i<7;i++){
            _schSubjects[i] = i;
            _laboratories[i] = 100+i;
            _departments[i] = 200+i;
        }
        structs_0.setLengthProject();
        structs_1.setLaboratories(_laboratories);
        structs_1.setSchSubjects(_schSubjects);
        structs_1.setDepartments(_departments);
        structs_0.setStatusAddress(0xA8368d91ce67D60b9e1288eB2ba2555C0e09EE94, MakeStruct0.StatusAddress.ForTeacher);
        structs_0.setStatusAddress(0x486516Ce05a158cBD488F219Ca64Fea674b4b8f7, MakeStruct0.StatusAddress.ForTeacher);
        structs_0.setStatusAddress(0x16496CAA734bA101cA1D931c648F9FA12856B69e, MakeStruct0.StatusAddress.ForTeacher);
        structs_0.setStatusAddress(0x52a0024cB03CCB7B787eba15A6f7FF7EF2fCE3f9, MakeStruct0.StatusAddress.ForTeacher);
        structs_0.setStatusAddress(0xF18919Fa57FBa4c75c4bE86762B485f1b4A5D954, MakeStruct0.StatusAddress.ForTeacher);
        structs_0.setStatusAddress(0xE2449a03bFa5A89dA6295EB6547e91A15c63Ac8B, MakeStruct0.StatusAddress.ForTeacher);
        structs_0.setStatusAddress(0xa796B7739989cDcA7c861BEd94F4aE01d23B18CE, MakeStruct0.StatusAddress.ForTeacher);
        structs_0.setStatusAddress(0xa3e508192eeD1CB8151D6F2dB5Bd0ba45dC49535, MakeStruct0.StatusAddress.ForTeacher);
        structs_0.setStatusAddress(0x19acaE5Ab26022D4e0249899cD6d780BD1a31DD0, MakeStruct0.StatusAddress.ForTeacher);


        structs_0.setStatusAddress(0x6D7Bd28346ceDB712Fa6811C4e16332A8fD38f26, MakeStruct0.StatusAddress.ForStudent);
        structs_0.setStatusAddress(0xD08270D7cFd9b50A6E94b40c95175acD9A62c234, MakeStruct0.StatusAddress.ForStudent);
        structs_0.setStatusAddress(0x234D8945797EE0995A9748DAd31E3629bB0dD888, MakeStruct0.StatusAddress.ForStudent);
        structs_0.setStatusAddress(0x2180768fE112ff886b74436bF0E46954E87B7882, MakeStruct0.StatusAddress.ForStudent);
        structs_0.setStatusAddress(0xF375A7eEDe5f1d2420e17e5eAaBa5FEf17098bdd, MakeStruct0.StatusAddress.ForStudent);
        structs_0.setStatusAddress(0x1b4e31DE080A09083f92b64626cE1487B1f6bC00, MakeStruct0.StatusAddress.ForStudent);
        structs_0.setStatusAddress(0xAE05dd8c2a3A791ac26dD8124CBE8dB4aA96C2ca, MakeStruct0.StatusAddress.ForStudent);

    }
}