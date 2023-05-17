// SPDX-License-Identifier: GPL-3.0
pragma solidity > 0.8.0 < 0.9.0;

contract GlobalStorage {

    // Безопасность:

    address ownerContract;
    address[] logicContracts;

    // Данные пользователей:

    mapping (bytes32 => string) internal stringDataUser;
    mapping (bytes32 => string[]) internal stringArrayDataUser;
    mapping (bytes32 => address) internal addressDataUser;
    mapping (bytes32 => address[]) internal addressArrayDataUsers;
    mapping (bytes32 => uint8) internal uint8DataUser;
    mapping (bytes32 => uint16) internal uint16DataUser;
    mapping (bytes32 => uint16[]) internal uint16ArrayDataUser;
    mapping (bytes32 => uint16[]) internal uintArrayDataUser;
    mapping (bytes32 => bytes32) internal bytes32DataUser;
    mapping (bytes32 => bytes32[]) internal bytes32ArrayDataUser;
    mapping (bytes32 => bool) internal boolDataUser;

    // Данные проекта:

    mapping (bytes32 => string) internal stringDataProject;
    mapping (bytes32 => string[]) internal stringArrayDataProject;
    mapping (bytes32 => address) internal addressDataProject;
    mapping (bytes32 => address[]) internal addressArrayDataProject;
    mapping (bytes32 => uint16) internal uint16DataProject;
    mapping (bytes32 => uint16[]) internal uint16ArrayDataProject;
    mapping (bytes32 => uint[]) internal uintArrayDataProject;

    constructor() {
        ownerContract = msg.sender;
        logicContracts.push(msg.sender);
    }


    // Модификаторы доступа:

    modifier onlyContract() {
        bool flag = false;
        for (uint16 i = 0; i < logicContracts.length; i++) {
            flag = msg.sender == logicContracts[i];
        }
        require(flag);
        _;
    }

    function getAddressContract() public view returns (address[] memory) {
        return logicContracts;
    }

    function setAddressContract(address _newAddressContract) public {
        require(msg.sender == ownerContract);
        logicContracts.push(_newAddressContract);
    }

    function getOwnerContract() public view returns(address) {
        return ownerContract;
    }

    function setOwnerContract(address _newAddressContract) public {
        require(msg.sender == ownerContract);
        ownerContract = _newAddressContract;
    }

    function delAddressContract(address _oldAddress) public {
        require(msg.sender == ownerContract);
        for (uint16 i = 0; i < logicContracts.length; i++){
            if (logicContracts[i] == _oldAddress){
                logicContracts[i] = address(0);
                break;
            }
        }
    }

    // Просмотр данных пользователей:

    function getStringDataUser(bytes32 _key) external view returns (string memory) {
        return stringDataUser[_key];
    }

    function getStringArrayDataUser(bytes32 _key) external view returns (string[] memory) {
        return stringArrayDataUser[_key];
    }

    function getUint8DataUser(bytes32 _key) external view returns (uint8) {
        return uint8DataUser[_key];
    }

    function getUint16DataUser(bytes32 _key) external view returns (uint16) {
        return uint16DataUser[_key];
    }

    function getUint16ArrayDataUser(bytes32 _key) external view returns (uint16[] memory) {
        return uint16ArrayDataUser[_key];
    }

    function getBytes32DataUser(bytes32 _key) external view returns (bytes32) {
        return bytes32DataUser[_key];
    }

    function getBytes32ArrayDataUser(bytes32 _key) external view returns (bytes32[] memory) {
        return bytes32ArrayDataUser[_key];
    }

    function getBoolDataUser(bytes32 _key) external view returns (bool) {
        return boolDataUser[_key];
    }

    function getAddressDataUser(bytes32 _key) external view returns (address) {
        return addressDataUser[_key];
    }

    // Изменение данных пользователей:

    function setStringDataUser(bytes32 _key, string memory _newString) external {
        stringDataUser[_key] = _newString;
    }

    function addStringArrayDataUser(bytes32 _key, string memory _newString) external {
        stringArrayDataUser[_key].push(_newString);
    }

    function setStringArrayDataUser(bytes32 _key, uint16 _num, string memory _newString) external {
        stringArrayDataUser[_key][_num] = _newString;
    }

    function setFullStringArrayDataUser(bytes32 _key, string[] memory _newString) external {
        stringArrayDataUser[_key] = _newString;
    }

    function setFullStringArrayDataProject(bytes32 _key, string[] memory _newString) external {
        stringArrayDataProject[_key]= _newString;
    }

    function setUint8DataUser(bytes32 _key, uint8 _newUint8) external {
        uint8DataUser[_key] = _newUint8;
    }

    function setUint16DataUser(bytes32 _key, uint16 _newUint16) external {
        uint16DataUser[_key] = _newUint16;
    }

    function addUint16ArrayDataUser(bytes32 _key, uint16 _newUint16) external {
        uint16ArrayDataUser[_key].push(_newUint16);
    }

    function setUint16ArrayDataUser(bytes32 _key, uint16 _num, uint16 _newUint16) external {
        uint16ArrayDataUser[_key][_num] = _newUint16;
    }

    function pushUint16ArrayDataUser(bytes32 _key, uint16 _newUint16) external {
        uint16ArrayDataUser[_key].push(_newUint16);
    }

    function setFullUint16ArrayDataUser(bytes32 _key, uint16[] memory _newUint16) external {
        uint16ArrayDataUser[_key] = _newUint16;
    }

    // Просмотр данных проекта:

    function getStringDataProject(bytes32 _key) external view returns (string memory) {
        return stringDataProject[_key];
    }

    function getStringArrayDataProject(bytes32 _key) external view returns (string[] memory) {
        return stringArrayDataProject[_key];
    }

    function getAddressDataProject(bytes32 _key) external view returns (address) {
        return addressDataProject[_key];
    }

    function getAddressArrayDataProject(bytes32 _key) external view returns (address[] memory) {
        return addressArrayDataProject[_key];
    }
    
    function getAddressArrayDataUsers(bytes32 _key) external view returns (address[] memory) {
        return addressArrayDataUsers[_key];
    }

    function getUint16DataProject(bytes32 _key) external view returns (uint16) {
        return uint16DataProject[_key];
    }  

    function getUint16ArrayDataProject(bytes32 _key) external view returns (uint16[] memory) {
        return uint16ArrayDataProject[_key];
    }

    function getUintArrayDataProject(bytes32 _key) external view returns (uint[] memory) {
        return uintArrayDataProject[_key];
    }

    // Изменение данных проекта:

    function setBytes32ArrayDataUser(bytes32 _key, uint16 _num, bytes32 _newBytes32) external {
        bytes32ArrayDataUser[_key][_num] = _newBytes32;
    }

    function addBytes32ArrayDataUser(bytes32 _key, bytes32 _newBytes32) external {
        bytes32ArrayDataUser[_key].push(_newBytes32);
    }

    function setFullBytes32ArrayDataUser(bytes32 _key, bytes32[] memory _newBytes32) external {
        bytes32ArrayDataUser[_key] = _newBytes32;
    }

    function setBytes32DataUser(bytes32 _key, bytes32 _newBytes32) external {
        bytes32DataUser[_key] = _newBytes32;
    }

    function setBoolDataUser(bytes32 _key, bool _new_bool) external {
        boolDataUser[_key] = _new_bool;
    }

    function setAddressDataUser(bytes32 _key, address _addr) external {
        addressDataUser[_key] = _addr;
    }

    function setStringDataProject(bytes32 _key, string memory _newString) external {
        stringDataProject[_key] = _newString;
    }

    function addStringArrayDataProject(bytes32 _key, string memory _newString) external {
        stringArrayDataProject[_key].push(_newString);
    }

    function setStringArrayDataProject(bytes32 _key, uint16 _num, string memory _newString) external {
        stringArrayDataProject[_key][_num] = _newString;
    }

    function setAddressDataProject(bytes32 _key, address _newAddress) external {
        addressDataProject[_key] = _newAddress;
    }

    function addAddressArrayDataProject(bytes32 _key, address _newAddress) external {
        addressArrayDataProject[_key].push(_newAddress);
    }

    function setAddressArrayDataProject(bytes32 _key, uint16 _num, address _newAddress) external {
        addressArrayDataProject[_key][_num] = _newAddress;
    }

    function setFullAddressArrayDataProject(bytes32 _key, address[] memory _newAddress) external {
        addressArrayDataProject[_key] = _newAddress;
    }

    function addAddressArrayDataUsers(bytes32 _key, address _newAddress) external {
        addressArrayDataUsers[_key].push(_newAddress);
    }

    function setAddressArrayDataUsers(bytes32 _key, uint16 _num, address _newAddress) external {
        addressArrayDataUsers[_key][_num] = _newAddress;
    }

    function setFullAddressArrayDataUsers(bytes32 _key, address[] memory _newAddress) external {
        addressArrayDataUsers[_key] = _newAddress;
    }

    function setUint16DataProject(bytes32 _key, uint16 _newUint16) external {
        uint16DataProject[_key] = _newUint16;
    }

    function addUint16ArrayDataProject(bytes32 _key, uint16 _newUint16) external {
        uint16ArrayDataProject[_key].push(_newUint16);
    }

    function setUint16ArrayDataProject(bytes32 _key, uint16 _num, uint16 _newUint16) external {
        uint16ArrayDataProject[_key][_num] = _newUint16;
    }

    function setUintArrayDataProject(bytes32 _key, uint16 _num, uint _newUint) external {
        uintArrayDataProject[_key][_num] = _newUint;
    }

    function setFullUint16ArrayDataProject(bytes32 _key, uint16[] memory _newUint16) external {
        uint16ArrayDataProject[_key] = _newUint16;
    }

    function setFullUintArrayDataProject(bytes32 _key, uint[] memory _newUint) external {
        uintArrayDataProject[_key] = _newUint;
    }
}