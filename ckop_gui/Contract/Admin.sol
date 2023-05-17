// SPDX-License-Identifier: GPL-3.0
pragma solidity > 0.8.16; //0.8.17


import "./GlobalStorage.sol";
import "./MakeStruct.sol";


contract Admin {

    GlobalStorage data;
    MakeStruct structs;

    event Action (address hero, address target, uint numProject, string text);

    mapping(bytes32 => address[]) addressDataUser;


    modifier onlyAdmin() {
        if (structs.getStatusAddress(msg.sender) != MakeStruct.StatusAddress.Admin) {
            emit Action(msg.sender, address(0), 0, "ERROR: only admin");
            return;
        }
        _;
    }

    modifier dealOnlyWithTeacher(address _addr) {
        if (structs.getStatusAddress(_addr) != MakeStruct.StatusAddress.Teacher) {
            emit Action(msg.sender, _addr, 0, "ERROR: the person you want to deal with is not a teacher");
            return;
        }
        _;
    }

    modifier userRegistered(string memory _login, string memory _pass, address _sender) {
        MakeStruct.StatusAddress status = structs.getStatusAddress(_sender);
        if (status != MakeStruct.StatusAddress.Student &&
        status != MakeStruct.StatusAddress.Teacher &&
        status != MakeStruct.StatusAddress.Admin) {
            emit Action(msg.sender, address(0), 0, "ERROR: you not registered");
            return;
        }
        bytes32 pass_b =  structs.getPassword(_sender);
        if (!(pass_b == keccak256(abi.encodePacked(_login, _pass)))) {
            emit Action(msg.sender, address(0), 0, "ERROR: wrong data");
            return;
        }
        _;
    }

// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   del addr2 
    // function changeHeadTeacher(string memory _ulogin, string memory _pass, address _addr1, address _addr2) public userRegistered(_ulogin, _pass, msg.sender) onlyAdmin dealOnlyWithTeacher(_addr1) dealOnlyWithTeacher(_addr2) {
    //     (string memory _login, string memory _fio, uint16 _numDepartment, uint16[] memory _numSchoolSubjects, uint16[] memory _numLaboratories, bytes32 _pass, bool _headTeacher, bool _scientistManager) = structs.getTeacherStruct(_addr1);
    //     (string memory _login2, string memory _fio2, uint16 _numDepartment2, uint16[] memory _numSchoolSubjects2, uint16[] memory _numLaboratories2, bytes32 _pass2, bool _headTeacher2, bool _scientistManager2) = structs.getTeacherStruct(_addr2);
    //     if (_numDepartment != _numDepartment2) {
    //         emit Action(msg.sender, address(0), 0, "ERROR: addresses are from different departments");
    //         return;
    //     }
    //     structs.setTeacherStruct(_addr1, _login, _fio, _numDepartment, _numSchoolSubjects, _numLaboratories, _pass, !_headTeacher, _scientistManager);
    //     structs.setTeacherStruct(_addr2, _login2, _fio2, _numDepartment2, _numSchoolSubjects2, _numLaboratories2, _pass2, !_headTeacher2, _scientistManager2);
    //     emit Action(msg.sender, address(0), 0, "HeadTeacher in Department was successfully changed");
    // }

    function addTeacherToLaboratory(string memory _ulogin, string memory _pass, uint16 _numLaboratory, address _addr1) public userRegistered(_ulogin, _pass, msg.sender) onlyAdmin dealOnlyWithTeacher(_addr1) {
        (string memory _login, string memory _fio, uint16 _numDepartment, uint16[] memory _numSchoolSubjects, uint16[] memory _numLaboratories, bytes32 _pass, bool _headTeacher, bool _scientistManager) = structs.getTeacherStruct(_addr1);        
        for (uint i; i < _numLaboratories.length; i++) {
            if (_numLaboratory == _numLaboratories[i]) {
                emit Action(msg.sender, _addr1, 0, "ERROR: this teacher is already in this laboratory");
                return;
            }
        }
        uint16[] memory _list = new uint16[](50);
        for (uint i; i < _numLaboratories.length; i++) {
            _list[i] = _numLaboratories[i];
            _list[i+1] = _numLaboratory;
        }
        structs.setTeacherStruct(_addr1, _login, _fio, _numDepartment, _numSchoolSubjects, _list, _pass, _headTeacher, _scientistManager);
        (address[] memory _teachers, address _HeadlTeacher) = structs.getLaboratoryStruct(_numLaboratory);
        address[] memory _list2 = new address[](20);
        for (uint i; i < _teachers.length; i++) {
            _list2[i] = _teachers[i];
            _list2[i++] = _addr1;
        }
        structs.setLaboratoryStruct(_numLaboratory, _list2, _HeadlTeacher);
        emit Action(msg.sender, _addr1, 0, "The teacher was successfully added to the laboratory");
    }

    function changeHeadlTeacherInLaboratory(string memory _ulogin, string memory _pass, uint16 _numLaboratory, address _newHeadlTeacher) public userRegistered(_ulogin, _pass, msg.sender) onlyAdmin dealOnlyWithTeacher(_newHeadlTeacher) {
        (string memory _login, string memory _fio, uint16 _numDepartment, uint16[] memory _numSchoolSubjects, uint16[] memory _numLaboratories, bytes32 _pass, bool _headTeacher, bool _scientistManager) = structs.getTeacherStruct(_newHeadlTeacher);        
        bool f = false;
        for (uint i; i < _numLaboratories.length; i++) {
            if (_numLaboratories[i] == _numLaboratory) f = !f;
        }
        if (!f) {
            emit Action(msg.sender, _newHeadlTeacher, 0, "ERROR: this teacher is not in this laboratory");
            return;
        }
        (address[] memory _teachers, address _HeadlTeacher) = structs.getLaboratoryStruct(_numLaboratory);
        if (_HeadlTeacher == _newHeadlTeacher) {
            emit Action(msg.sender, _newHeadlTeacher, 0, "ERROR: this teacher is already a head teacher in this laboratory");
            return;
        }
        address[] memory _list = new address[](20);
        for (uint i; i < _teachers.length; i++) {
            if (_list[i] != _newHeadlTeacher) {
                _list[i] = _teachers[i];
            } else {
                _list[i] = _HeadlTeacher;
            }
        }
        structs.setLaboratoryStruct(_numLaboratory, _list, _newHeadlTeacher);
        emit Action (msg.sender, _newHeadlTeacher, 0, "A head teacher in laboratory was successfully changed");
    } 

    function deleteTeacherInLaboratory(string memory _ulogin, string memory _pass, uint16 _numLaboratory, address _teacher) public userRegistered(_ulogin, _pass, msg.sender) onlyAdmin dealOnlyWithTeacher(_teacher) {
        (string memory _login, string memory _fio, uint16 _numDepartment, uint16[] memory _numSchoolSubjects, uint16[] memory _numLaboratories, bytes32 _pass, bool _headTeacher, bool _scientistManager) = structs.getTeacherStruct(_teacher);        
        bool f = false;
        for (uint i; i < _numLaboratories.length; i++) {
            if (_numLaboratories[i] == _numLaboratory) f = !f;
        }
        if (!f) {
            emit Action(msg.sender, _teacher, 0, "ERROR: this teacher is not in this laboratory");
            return;
        }
        uint16[] memory _list = new uint16[](50);
        uint t;
        for (uint i; i < _numLaboratories.length; i++) {
            if (_numLaboratories[t] != _numLaboratory) _list[i] = _numLaboratories[t];
            else i--;
        }
        structs.setTeacherStruct(_teacher, _login, _fio, _numDepartment, _numSchoolSubjects, _list, _pass, _headTeacher, _scientistManager);
        (address[] memory _teachers, address _HeadlTeacher) = structs.getLaboratoryStruct(_numLaboratory);
        address[] memory _list2 = new address[](20);
        t = 0;
        for (uint i; i < _teachers.length; i++) {
            if (_teachers[t] != _teacher) _list2[i] = _teachers[t];
            else i--;
            t++;
        }
        structs.setLaboratoryStruct(_numLaboratory, _list2, _HeadlTeacher);
        emit Action (msg.sender, _teacher, 0, "The teacher in laboratory was successfully deleted");
    }

    function deleteTeacher(string memory _ulogin, string memory _pass, address _deadMan) public onlyAdmin userRegistered(_ulogin, _pass, msg.sender) {
        (string memory _login, string memory _fio, uint16 _numDepartment, uint16[] memory _numSchoolSubjects, uint16[] memory _numLaboratories, bytes32 _pass, bool _headTeacher, bool _scientistManager) = structs.getTeacherStruct(_deadMan);        
        structs.setTeacherStruct(_deadMan, "", "", 0, new uint16[](50), new uint16[](50), bytes32(0), false, false);
        uint16[] memory _prs = structs.getOwnerProjects(_deadMan);
        if (_scientistManager) {
            for(uint i; i < _prs.length; i++) {
                (string memory _n, string memory _g, address[] memory _members, uint16 _numlab, uint16 _status, string[] memory _tasks, string memory _role, address _proscientistManager, address[] memory _otherTeachers) = structs.getProjectStruct(_prs[i]);
                if (_proscientistManager == _deadMan) structs.setProjectStruct(_prs[i], _n, _g, _members, _numlab, _tasks, _role, address(0), _otherTeachers);
            }
        }
        for(uint i; i < _prs.length; i++) {
            (string memory _n, string memory _g, address[] memory _members, uint16 _numlab, uint16 _status, string[] memory _tasks, string memory _role, address _proscientistManager, address[] memory _otherTeachers) = structs.getProjectStruct(_prs[i]);
            address[] memory _teachers = new address[](10);
            uint t;
            for (uint j; j < _otherTeachers.length; j++) {
                if (_otherTeachers[t] != _deadMan) _teachers[j] = _otherTeachers[t];
                else j--;
            }
            structs.setProjectStruct(_prs[i], _n, _g, _members, _numlab, _tasks, _role, _proscientistManager, _teachers);
        }
    }


}