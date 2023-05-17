// SPDX-License-Identifier: GPL-3.0
pragma solidity > 0.8.0 < 0.9.0;

import "./GlobalStorage.sol";

contract MakeStruct1 {

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
            "37", "38", "39", "40", "41", "42", "43", "44", "45",
            "46", "47", "48", "49", "50"]; // change
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

//Dop function

    function setLaboratories(
       uint16[] memory laboratories
    ) external onlyContract()
    {
        data.setFullUint16ArrayDataUser(keccak256(abi.encodePacked(keys[22])), laboratories);
        data.setUint16DataUser(keccak256(abi.encodePacked(keys[31])), uint16(laboratories.length));
    }

    function setSchSubjects(
       uint16[] memory schSubjects
    ) external onlyContract()
    {
        data.setFullUint16ArrayDataUser(keccak256(abi.encodePacked(keys[21])), schSubjects);
        data.setUint16DataUser(keccak256(abi.encodePacked(keys[30])), uint16(schSubjects.length));
    }

    function setDepartments(
       uint16[] memory departments
    ) external onlyContract()
    {
        data.setFullUint16ArrayDataUser(keccak256(abi.encodePacked(keys[29])), departments);
        data.setUint16DataUser(keccak256(abi.encodePacked(keys[32])), uint16(departments.length));
    }


    function getActivesProjectsStudent(address _addr) external view returns(uint16 own_proj)
    {
        own_proj = data.getUint16DataUser(keccak256(abi.encodePacked(_addr, keys[34])));
    }

    function getActivesProjects(address _addr) external view returns(uint16[] memory own_proj)
    {
        own_proj = data.getUint16ArrayDataUser(keccak256(abi.encodePacked(_addr, keys[35])));
    }

    function setActivesProjects(address _addr_student, address _addr_teacher, uint16 _num_project) external
    {
        data.pushUint16ArrayDataUser(keccak256(abi.encodePacked(_addr_teacher, keys[35])), _num_project);
        data.setUint16DataUser(keccak256(abi.encodePacked(_addr_student, keys[34])), _num_project);
    }

    function getAddedUsers(address _sender) 
    view external returns (address[] memory addedUsers)
    {
        addedUsers = data.getAddressArrayDataUsers(keccak256(abi.encodePacked(_sender, keys[38])));
    }

    function setAddedUsers(address _sender, address _user) external  onlyContract()
    {
        data.addAddressArrayDataUsers(keccak256(abi.encodePacked(_sender, keys[38])), _user);
    }

    function setFullAddedUsers(address _sender, address[] memory _addedUsers) external  onlyContract()
    {
        data.setFullAddressArrayDataUsers(keccak256(abi.encodePacked(_sender, keys[38])), _addedUsers);
    }

    function getAddedPasswords(address _sender) 
    view external returns (string[] memory passUsers)
    {
        require(msg.sender == owner_contract);
        passUsers = data.getStringArrayDataUser(keccak256(abi.encodePacked(_sender, keys[39])));
    }

    function setAddedPasswords(address _sender, string memory _userPass) external  onlyContract()
    {
        data.addStringArrayDataUser(keccak256(abi.encodePacked(_sender, keys[39])), _userPass);
    }

    function setFullAddedPasswords(address _sender, string[] memory _addedPass) external  onlyContract()
    {
        data.setFullStringArrayDataUser(keccak256(abi.encodePacked(_sender, keys[39])), _addedPass);
    }

// Laboratory's functions
// Functions for me
    function setLaboratoryStruct(uint _numLaboratory, address[] memory _teachers, address _HeadlTeacher) external {
        data.setAddressDataUser(keccak256(abi.encodePacked(_numLaboratory, keys[44])), _HeadlTeacher);
        data.setFullAddressArrayDataProject(keccak256(abi.encodePacked(_numLaboratory, keys[45])), _teachers);
    }

    function getLaboratoryStruct(uint _numLaboratory) view external returns(
        address[] memory _teachers, address _HeadlTeacher) {
        _teachers = data.getAddressArrayDataProject(keccak256(abi.encodePacked(_numLaboratory, keys[45])));
        _HeadlTeacher = data.getAddressDataUser(keccak256(abi.encodePacked(_numLaboratory, keys[44])));
    }

    function addLaboratoryTeacher(uint _numLaboratory, address _teacher) external {
        data.addAddressArrayDataProject(keccak256(abi.encodePacked(_numLaboratory, keys[45])), _teacher);
    }

    function setFullLaboratoryTeachers(uint _numLaboratory, address[] memory _teachers) external {
        data.setFullAddressArrayDataProject(keccak256(abi.encodePacked(_numLaboratory, keys[45])), _teachers);
    }

    function getLaboratoryTeachers(uint _numLaboratory) external view returns(address[] memory _teachers) {
        _teachers = data.getAddressArrayDataProject(keccak256(abi.encodePacked(_numLaboratory, keys[45])));
    }

    function setLaboratoryHeadlTeacher(uint _numLaboratory, address _headlteacher) external {
        data.setAddressDataUser(keccak256(abi.encodePacked(_numLaboratory, keys[44])), _headlteacher);
    }

    function getLaboratoryHeadlTeacher(uint _numLaboratory) external view returns(address _headlteacher) {
        _headlteacher = data.getAddressDataUser(keccak256(abi.encodePacked(_numLaboratory, keys[44])));
    }

   function setTeacherNumDepartment(address _addr, uint16 _numDepartment) external {
        data.setUint16DataUser(keccak256(abi.encodePacked(_addr, keys[0])), _numDepartment);
    }

    function getTeacherNumDepartment(address _addr) external view returns(uint16 _num) {
        _num = data.getUint16DataUser(keccak256(abi.encodePacked(_addr, keys[6])));
    }

    function setTeacherNumSchoolSubjects(address _addr, uint16 _sub) external {
        data.addUint16ArrayDataUser(keccak256(abi.encodePacked(_addr, keys[7])), _sub);
    }

    function getTeacherNumSchoolSubjects(address _addr) external view returns(uint16[] memory _sub) {
        _sub = data.getUint16ArrayDataUser(keccak256(abi.encodePacked(_addr, keys[7])));
    }

    function addTeacherNumLaboratories(address _addr, uint16 _lab) external {
        data.addUint16ArrayDataUser(keccak256(abi.encodePacked(_addr, keys[8])), _lab);
    }

    function setFullTeacherNumLaboratories(address _address, uint16[] memory _labs) external {
        data.setFullUint16ArrayDataProject(keccak256(abi.encodePacked(_address, keys[45])), _labs);
    }

    function getTeacherNumLaboratories(address _addr) external view returns(uint16[] memory _labs) {
        _labs = data.getUint16ArrayDataUser(keccak256(abi.encodePacked(_addr, keys[8])));
    }

    function setTeacherHeadTeacher(address _addr, bool _head) external {
        data.setBoolDataUser(keccak256(abi.encodePacked(_addr, keys[11])), _head);
    }

    function getTeacherHeadTeacher(address _addr) external view returns(bool _head) {
        _head = data.getBoolDataUser(keccak256(abi.encodePacked(_addr, keys[11])));
    }

    function setTeacherScientistManager(address _addr, bool _manager) external {
        data.setBoolDataUser(keccak256(abi.encodePacked(_addr, keys[12])), _manager);
    }

    function getTeacherScientistManager(address _addr) external view returns(bool _manager) {
        _manager = data.getBoolDataUser(keccak256(abi.encodePacked(_addr, keys[12])));
    }

    function getProjectScientistManager(uint _num) external view returns(address _scientistManager) {
        _scientistManager = data.getAddressDataProject(keccak256(abi.encodePacked(_num, keys[46])));
    }

    function setProjectScientistManager(uint _num, address _scientistManager) external {
        data.setAddressDataProject(keccak256(abi.encodePacked(_num, keys[46])), _scientistManager);
    }

    function getProjectTeachers(uint _num) external view returns(address[] memory _otherTeachers) {
        _otherTeachers = data.getAddressArrayDataProject(keccak256(abi.encodePacked(_num, keys[47])));
    }

    function setProjectTeachers(uint _num, address[] memory _otherTeachers) external {
        data.setFullAddressArrayDataProject(keccak256(abi.encodePacked(_num, keys[47])), _otherTeachers);
    }
    
    function setUserLogin(address _teacher, string memory _login) external {
        data.setStringDataUser(keccak256(abi.encodePacked(_teacher, keys[0])), _login);
        data.setAddressDataUser(keccak256(abi.encodePacked(_login, keys[28])), _teacher); 
    }

    function getRequestStudent(uint16 _num) 
        external view returns(address teacher, uint16 status) {
        teacher = data.getAddressDataProject(keccak256(abi.encodePacked(_num, keys[48])));
        status = data.getUint16DataProject(keccak256(abi.encodePacked(_num, keys[49])));
    }

    function setRequestStudent(uint16 _num, address _teacher, uint16 _status) external {
        if (_status == 0){
            data.setAddressDataProject(keccak256(abi.encodePacked(_num, keys[48])), _teacher);
            data.setUint16DataProject(keccak256(abi.encodePacked(_num, keys[49])), _status);
        }
        if (_status == 1){
            string memory usingLogin = data.getStringDataUser(keccak256(abi.encodePacked(_teacher, keys[0])));
            data.setStringDataProject(keccak256(abi.encodePacked(_num, keys[23])), usingLogin);
            data.setUint16DataProject(keccak256(abi.encodePacked(_num, keys[49])), _status);
        }
        if (_status == 2){
            data.setAddressDataProject(keccak256(abi.encodePacked(_num, keys[48])), address(0));
            data.setUint16DataProject(keccak256(abi.encodePacked(_num, keys[49])), _status);
        }
    }

}