// SPDX-License-Identifier: GPL-3.0
pragma solidity > 0.8.0 < 0.9.0;

import "./Support.sol";

contract Teacher_1 is Support {

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

    function changeRole(
        string memory _login, 
        string memory _pass,
        string memory _roleInProject,
        uint16 _numProject,
        uint16 _numUser) 
        public onlyTeacher() userRegistered(_login, _pass, msg.sender) teachersProject(_numProject)
    {
        structs_0.setRoleMembers(_numProject, _numUser, _roleInProject);

        emit Action(msg.sender, address(0), _numProject, "Successfully change role");
    }

    function send_response_teacher(
        string memory _login,
        string memory _pass,
        uint16 _num,
        uint16 _status)
        // 0 - запрос отправлен, 1 - запрос принят, 2 - запрос отклонен
    public onlyTeacher() userRegistered(_login, _pass, msg.sender)
    {
        address teacher;
        uint16 status;

        (teacher, status) = structs_1.getRequestStudent(_num);

        if (teacher == msg.sender){
            address[] memory membersProjects = structs_0.getMembersProject(_num);
            structs_1.setRequestStudent(_num, msg.sender, _status);
            structs_1.setActivesProjects(membersProjects[0], msg.sender, _num);
            emit Action(msg.sender, address(0), 0, "Response created");
        } else {
            emit Action(msg.sender, address(0), 0, "Not your request");
        }
    }

    function changeStatus(
        string memory _login, 
        string memory _pass, 
        uint16 _num_proj, 
        uint16 _status)
        public onlyTeacher() userRegistered(_login, _pass, msg.sender) teachersProject(_num_proj)
    {
        uint16 old_status = uint16(structs_0.getStatusProject(_num_proj));
        // MakeStruct0.StatusProject status = MakeStruct0.StatusProject(_status);

        if (old_status != 0 && _status != old_status && _status!= 0){
            structs_0.setStatusProject(_num_proj, MakeStruct0.StatusProject(_status));
            emit Action(msg.sender, address(0), _num_proj, "Status change");
            return;
        }
        emit Action(msg.sender, address(0), _num_proj, "ERROR: error status");
    }
}