abi_struct_0 = """
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_data",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "getAddressContract",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num_project",
				"type": "uint16"
			}
		],
		"name": "getDeadLineInProject",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "deadLineProject",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getLaboratories",
		"outputs": [
			{
				"internalType": "uint16[]",
				"name": "labor",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getLengthProject",
		"outputs": [
			{
				"internalType": "uint16",
				"name": "LengthProject",
				"type": "uint16"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			}
		],
		"name": "getMembersProject",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "membersProjects",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getOwnerContract",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getOwnerProjects",
		"outputs": [
			{
				"internalType": "uint16[]",
				"name": "own_proj",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getPassword",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "pass",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			}
		],
		"name": "getProjectStruct",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "goal",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "loginMentor",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "roleMembers",
				"type": "string"
			},
			{
				"internalType": "string[]",
				"name": "tasksMembers",
				"type": "string[]"
			},
			{
				"internalType": "address[]",
				"name": "members",
				"type": "address[]"
			},
			{
				"internalType": "uint16",
				"name": "numLaboratory",
				"type": "uint16"
			},
			{
				"internalType": "uint16[]",
				"name": "needKnowledge",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num_project",
				"type": "uint16"
			},
			{
				"internalType": "uint16",
				"name": "_num_task",
				"type": "uint16"
			}
		],
		"name": "getReadyOneTaskProject",
		"outputs": [
			{
				"internalType": "uint16",
				"name": "readyTaskProject",
				"type": "uint16"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num_project",
				"type": "uint16"
			}
		],
		"name": "getReadyTaskProject",
		"outputs": [
			{
				"internalType": "uint16[]",
				"name": "readyTasksProject",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getSchSubjects",
		"outputs": [
			{
				"internalType": "uint16[]",
				"name": "schSubjects",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getStatusAddress",
		"outputs": [
			{
				"internalType": "enum MakeStruct0.StatusAddress",
				"name": "status",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			}
		],
		"name": "getStatusProject",
		"outputs": [
			{
				"internalType": "enum MakeStruct0.StatusProject",
				"name": "status",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_student",
				"type": "address"
			}
		],
		"name": "getStudentStrongSide",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "strongSides",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_student",
				"type": "address"
			}
		],
		"name": "getStudentStruct",
		"outputs": [
			{
				"internalType": "string",
				"name": "login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "FIO",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "classLetter",
				"type": "string"
			},
			{
				"internalType": "string[]",
				"name": "strongSides",
				"type": "string[]"
			},
			{
				"internalType": "uint8",
				"name": "class",
				"type": "uint8"
			},
			{
				"internalType": "bytes32",
				"name": "pass",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num_project",
				"type": "uint16"
			}
		],
		"name": "getTaskInProject",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "tasksProject",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_teacher",
				"type": "address"
			}
		],
		"name": "getTeacherStruct",
		"outputs": [
			{
				"internalType": "string",
				"name": "FIO",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "login",
				"type": "string"
			},
			{
				"internalType": "uint16",
				"name": "numDepartment",
				"type": "uint16"
			},
			{
				"internalType": "uint16[]",
				"name": "numSchoolSubjects",
				"type": "uint16[]"
			},
			{
				"internalType": "uint16[]",
				"name": "numLaboratories",
				"type": "uint16[]"
			},
			{
				"internalType": "bytes32",
				"name": "pass",
				"type": "bytes32"
			},
			{
				"internalType": "bool",
				"name": "headTeacher",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "scientistManager",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getUsingAddress",
		"outputs": [
			{
				"internalType": "string",
				"name": "login",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_email",
				"type": "string"
			}
		],
		"name": "getUsingEmail",
		"outputs": [
			{
				"internalType": "bool",
				"name": "usingEmail",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			}
		],
		"name": "getUsingLogin",
		"outputs": [
			{
				"internalType": "address",
				"name": "usingLogin",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "keys",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_new_addr_contract",
				"type": "address"
			}
		],
		"name": "setAddressContract",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num_project",
				"type": "uint16"
			},
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			},
			{
				"internalType": "uint256",
				"name": "_deadLineTask",
				"type": "uint256"
			}
		],
		"name": "setDeadLineInProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num_project",
				"type": "uint16"
			},
			{
				"internalType": "uint256[]",
				"name": "_deadLineTask",
				"type": "uint256[]"
			}
		],
		"name": "setFullDeadLineInProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num_project",
				"type": "uint16"
			},
			{
				"internalType": "uint16[]",
				"name": "_readyTask",
				"type": "uint16[]"
			}
		],
		"name": "setFullReadyTaskProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			},
			{
				"internalType": "string",
				"name": "_goal",
				"type": "string"
			}
		],
		"name": "setGoalInProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "setLengthProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			},
			{
				"internalType": "uint16",
				"name": "_num_memb",
				"type": "uint16"
			},
			{
				"internalType": "address",
				"name": "_newStudent",
				"type": "address"
			}
		],
		"name": "setMembersProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_new_addr_owner",
				"type": "address"
			}
		],
		"name": "setOwnerContract",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_goal",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_mentor",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_roleMembers",
				"type": "string"
			},
			{
				"internalType": "string[]",
				"name": "_tasksMembers",
				"type": "string[]"
			},
			{
				"internalType": "address[]",
				"name": "_members",
				"type": "address[]"
			},
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			},
			{
				"internalType": "uint16",
				"name": "_numLaboratory",
				"type": "uint16"
			},
			{
				"internalType": "uint8",
				"name": "_status",
				"type": "uint8"
			},
			{
				"internalType": "uint16[]",
				"name": "_needKnowledge",
				"type": "uint16[]"
			}
		],
		"name": "setProjectStruct",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num_project",
				"type": "uint16"
			},
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			},
			{
				"internalType": "uint16",
				"name": "_readyTask",
				"type": "uint16"
			}
		],
		"name": "setReadyTaskProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			},
			{
				"internalType": "string",
				"name": "_roleMembers",
				"type": "string"
			}
		],
		"name": "setRoleMembers",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			},
			{
				"internalType": "enum MakeStruct0.StatusAddress",
				"name": "_status",
				"type": "uint8"
			}
		],
		"name": "setStatusAddress",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			},
			{
				"internalType": "enum MakeStruct0.StatusProject",
				"name": "_status",
				"type": "uint8"
			}
		],
		"name": "setStatusProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_strongSide",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "_student",
				"type": "address"
			},
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			}
		],
		"name": "setStudentStrongSide",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_FIO",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_classLetter",
				"type": "string"
			},
			{
				"internalType": "string[]",
				"name": "_strongSides",
				"type": "string[]"
			},
			{
				"internalType": "address",
				"name": "_student",
				"type": "address"
			},
			{
				"internalType": "uint8",
				"name": "_class",
				"type": "uint8"
			},
			{
				"internalType": "bytes32",
				"name": "_pass",
				"type": "bytes32"
			}
		],
		"name": "setStudentStruct",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num_project",
				"type": "uint16"
			},
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			},
			{
				"internalType": "string",
				"name": "_tasks",
				"type": "string"
			}
		],
		"name": "setTaskInProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_FIO",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "_teacher",
				"type": "address"
			},
			{
				"internalType": "uint16",
				"name": "_numDepartment",
				"type": "uint16"
			},
			{
				"internalType": "uint16[]",
				"name": "_numSchoolSubjects",
				"type": "uint16[]"
			},
			{
				"internalType": "uint16[]",
				"name": "_numLaboratories",
				"type": "uint16[]"
			},
			{
				"internalType": "bytes32",
				"name": "_pass",
				"type": "bytes32"
			},
			{
				"internalType": "bool",
				"name": "_headTeacher",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "_scientistManager",
				"type": "bool"
			}
		],
		"name": "setTeacherStruct",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
"""

abi_struct_1 = """
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_data",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_numLaboratory",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "_teacher",
				"type": "address"
			}
		],
		"name": "addLaboratoryTeacher",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			},
			{
				"internalType": "uint16",
				"name": "_lab",
				"type": "uint16"
			}
		],
		"name": "addTeacherNumLaboratories",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getActivesProjects",
		"outputs": [
			{
				"internalType": "uint16[]",
				"name": "own_proj",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getActivesProjectsStudent",
		"outputs": [
			{
				"internalType": "uint16",
				"name": "own_proj",
				"type": "uint16"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_sender",
				"type": "address"
			}
		],
		"name": "getAddedPasswords",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "passUsers",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_sender",
				"type": "address"
			}
		],
		"name": "getAddedUsers",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "addedUsers",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAddressContract",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_numLaboratory",
				"type": "uint256"
			}
		],
		"name": "getLaboratoryHeadlTeacher",
		"outputs": [
			{
				"internalType": "address",
				"name": "_headlteacher",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_numLaboratory",
				"type": "uint256"
			}
		],
		"name": "getLaboratoryStruct",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "_teachers",
				"type": "address[]"
			},
			{
				"internalType": "address",
				"name": "_HeadlTeacher",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_numLaboratory",
				"type": "uint256"
			}
		],
		"name": "getLaboratoryTeachers",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "_teachers",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getOwnerContract",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_num",
				"type": "uint256"
			}
		],
		"name": "getProjectScientistManager",
		"outputs": [
			{
				"internalType": "address",
				"name": "_scientistManager",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_num",
				"type": "uint256"
			}
		],
		"name": "getProjectTeachers",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "_otherTeachers",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getTeacherHeadTeacher",
		"outputs": [
			{
				"internalType": "bool",
				"name": "_head",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getTeacherNumDepartment",
		"outputs": [
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getTeacherNumLaboratories",
		"outputs": [
			{
				"internalType": "uint16[]",
				"name": "_labs",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getTeacherNumSchoolSubjects",
		"outputs": [
			{
				"internalType": "uint16[]",
				"name": "_sub",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			}
		],
		"name": "getTeacherScientistManager",
		"outputs": [
			{
				"internalType": "bool",
				"name": "_manager",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "keys",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr_student",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_addr_teacher",
				"type": "address"
			},
			{
				"internalType": "uint16",
				"name": "_num_project",
				"type": "uint16"
			}
		],
		"name": "setActivesProjects",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_sender",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "_userPass",
				"type": "string"
			}
		],
		"name": "setAddedPasswords",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_sender",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_user",
				"type": "address"
			}
		],
		"name": "setAddedUsers",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_new_addr_contract",
				"type": "address"
			}
		],
		"name": "setAddressContract",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16[]",
				"name": "departments",
				"type": "uint16[]"
			}
		],
		"name": "setDepartments",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_sender",
				"type": "address"
			},
			{
				"internalType": "string[]",
				"name": "_addedPass",
				"type": "string[]"
			}
		],
		"name": "setFullAddedPasswords",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_sender",
				"type": "address"
			},
			{
				"internalType": "address[]",
				"name": "_addedUsers",
				"type": "address[]"
			}
		],
		"name": "setFullAddedUsers",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_numLaboratory",
				"type": "uint256"
			},
			{
				"internalType": "address[]",
				"name": "_teachers",
				"type": "address[]"
			}
		],
		"name": "setFullLaboratoryTeachers",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_address",
				"type": "address"
			},
			{
				"internalType": "uint16[]",
				"name": "_labs",
				"type": "uint16[]"
			}
		],
		"name": "setFullTeacherNumLaboratories",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16[]",
				"name": "laboratories",
				"type": "uint16[]"
			}
		],
		"name": "setLaboratories",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_numLaboratory",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "_headlteacher",
				"type": "address"
			}
		],
		"name": "setLaboratoryHeadlTeacher",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_numLaboratory",
				"type": "uint256"
			},
			{
				"internalType": "address[]",
				"name": "_teachers",
				"type": "address[]"
			},
			{
				"internalType": "address",
				"name": "_HeadlTeacher",
				"type": "address"
			}
		],
		"name": "setLaboratoryStruct",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_new_addr_owner",
				"type": "address"
			}
		],
		"name": "setOwnerContract",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_num",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "_scientistManager",
				"type": "address"
			}
		],
		"name": "setProjectScientistManager",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_num",
				"type": "uint256"
			},
			{
				"internalType": "address[]",
				"name": "_otherTeachers",
				"type": "address[]"
			}
		],
		"name": "setProjectTeachers",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16[]",
				"name": "schSubjects",
				"type": "uint16[]"
			}
		],
		"name": "setSchSubjects",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			},
			{
				"internalType": "bool",
				"name": "_head",
				"type": "bool"
			}
		],
		"name": "setTeacherHeadTeacher",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			},
			{
				"internalType": "uint16",
				"name": "_numDepartment",
				"type": "uint16"
			}
		],
		"name": "setTeacherNumDepartment",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			},
			{
				"internalType": "uint16",
				"name": "_sub",
				"type": "uint16"
			}
		],
		"name": "setTeacherNumSchoolSubjects",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_addr",
				"type": "address"
			},
			{
				"internalType": "bool",
				"name": "_manager",
				"type": "bool"
			}
		],
		"name": "setTeacherScientistManager",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
"""

abi_teacher = """
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_dataContract",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_structs_0",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_structs_1",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "address",
				"name": "hero",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "target",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint16",
				"name": "numProject",
				"type": "uint16"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "text",
				"type": "string"
			}
		],
		"name": "Action",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "uint16",
				"name": "_numProject",
				"type": "uint16"
			},
			{
				"internalType": "address",
				"name": "addressStudent",
				"type": "address"
			}
		],
		"name": "addStudentInProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "_sender",
				"type": "address"
			}
		],
		"name": "auth",
		"outputs": [
			{
				"internalType": "bool",
				"name": "a",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "uint16",
				"name": "_num_proj",
				"type": "uint16"
			},
			{
				"internalType": "string",
				"name": "_newTask",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_date",
				"type": "uint256"
			},
			{
				"internalType": "uint16",
				"name": "_num_task",
				"type": "uint16"
			},
			{
				"internalType": "uint16",
				"name": "_ready",
				"type": "uint16"
			}
		],
		"name": "changeTaskInProjectTeacher",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "constructData",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_nameProject",
				"type": "string"
			},
			{
				"internalType": "uint16",
				"name": "_numLaboratory",
				"type": "uint16"
			}
		],
		"name": "createProjectForTeacher",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "uint16",
				"name": "_numProject",
				"type": "uint16"
			},
			{
				"internalType": "address",
				"name": "addressStudent",
				"type": "address"
			}
		],
		"name": "deleteStudentOutProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "_newStudent",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "_pass_user",
				"type": "string"
			}
		],
		"name": "generateAddressForStudent",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_recipient",
				"type": "address"
			}
		],
		"name": "myTransfer",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_FIO",
				"type": "string"
			},
			{
				"internalType": "uint16[]",
				"name": "_leadsSchoolSubjects",
				"type": "uint16[]"
			},
			{
				"internalType": "uint16[]",
				"name": "_laboratories",
				"type": "uint16[]"
			}
		],
		"name": "registrationForTeacher",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "checkMyActiveProject",
		"outputs": [
			{
				"internalType": "uint16[]",
				"name": "activeProject",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "checkNumAllActiveProject",
		"outputs": [
			{
				"internalType": "uint16[]",
				"name": "activeProject",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "checkNumArhiveProject",
		"outputs": [
			{
				"internalType": "uint16[]",
				"name": "archiveProject",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_numProject",
				"type": "uint16"
			}
		],
		"name": "checkProject",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "goal",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "loginMentor",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "roleMembers",
				"type": "string"
			},
			{
				"internalType": "string[]",
				"name": "tasks",
				"type": "string[]"
			},
			{
				"internalType": "address[]",
				"name": "members",
				"type": "address[]"
			},
			{
				"internalType": "uint16",
				"name": "numLaboratory",
				"type": "uint16"
			},
			{
				"internalType": "uint16[]",
				"name": "numSchoolSubjects",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "_sender",
				"type": "address"
			}
		],
		"name": "checkRegister",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			}
		],
		"name": "checkTaskDeadline",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "tasksMembers",
				"type": "string[]"
			},
			{
				"internalType": "uint256[]",
				"name": "deadLine",
				"type": "uint256[]"
			},
			{
				"internalType": "uint16[]",
				"name": "ready",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_teacher",
				"type": "address"
			}
		],
		"name": "checkTeacher",
		"outputs": [
			{
				"internalType": "string",
				"name": "login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "FIO",
				"type": "string"
			},
			{
				"internalType": "uint16",
				"name": "numDepartment",
				"type": "uint16"
			},
			{
				"internalType": "uint16[]",
				"name": "numSchoolSubjects",
				"type": "uint16[]"
			},
			{
				"internalType": "uint16[]",
				"name": "numLaboratories",
				"type": "uint16[]"
			},
			{
				"internalType": "bytes32",
				"name": "_pass",
				"type": "bytes32"
			},
			{
				"internalType": "bool",
				"name": "headTeacher",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "scientistManager",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
"""

abi_student = """
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_dataContract",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_structs_0",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_structs_1",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "address",
				"name": "hero",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "address",
				"name": "target",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint16",
				"name": "numProject",
				"type": "uint16"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "text",
				"type": "string"
			}
		],
		"name": "Action",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_task",
				"type": "string"
			}
		],
		"name": "addTaskInProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "_sender",
				"type": "address"
			}
		],
		"name": "auth",
		"outputs": [
			{
				"internalType": "bool",
				"name": "a",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_goal",
				"type": "string"
			}
		],
		"name": "changeGoalProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_roleInProject",
				"type": "string"
			}
		],
		"name": "changeRole",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "uint16",
				"name": "_numStrongSide",
				"type": "uint16"
			},
			{
				"internalType": "string",
				"name": "_newStrongSide",
				"type": "string"
			}
		],
		"name": "changeStrongSide",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "uint8",
				"name": "_numTask",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "_newTask",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_date",
				"type": "uint256"
			}
		],
		"name": "changeTaskInProject",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "checkNumArhiveProject",
		"outputs": [
			{
				"internalType": "uint16[]",
				"name": "archiveProject",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_numProject",
				"type": "uint16"
			}
		],
		"name": "checkProject",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "goal",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "loginMentor",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "roleMembers",
				"type": "string"
			},
			{
				"internalType": "string[]",
				"name": "tasks",
				"type": "string[]"
			},
			{
				"internalType": "address[]",
				"name": "members",
				"type": "address[]"
			},
			{
				"internalType": "uint16",
				"name": "numLaboratory",
				"type": "uint16"
			},
			{
				"internalType": "uint16[]",
				"name": "numSchoolSubjects",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "_sender",
				"type": "address"
			}
		],
		"name": "checkRegister",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_student",
				"type": "address"
			}
		],
		"name": "checkStudent",
		"outputs": [
			{
				"internalType": "string",
				"name": "login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "FIO",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "classLetter",
				"type": "string"
			},
			{
				"internalType": "string[]",
				"name": "strongSides",
				"type": "string[]"
			},
			{
				"internalType": "uint8",
				"name": "class",
				"type": "uint8"
			},
			{
				"internalType": "bytes32",
				"name": "_pass",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint16",
				"name": "_num",
				"type": "uint16"
			}
		],
		"name": "checkTaskDeadline",
		"outputs": [
			{
				"internalType": "string[]",
				"name": "tasksMembers",
				"type": "string[]"
			},
			{
				"internalType": "uint256[]",
				"name": "deadLine",
				"type": "uint256[]"
			},
			{
				"internalType": "uint16[]",
				"name": "ready",
				"type": "uint16[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "constructData",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_nameProject",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_loginMentor",
				"type": "string"
			},
			{
				"internalType": "uint16",
				"name": "_numLaboratory",
				"type": "uint16"
			}
		],
		"name": "createProjectForStudent",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_recipient",
				"type": "address"
			}
		],
		"name": "myTransfer",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_login",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_pass",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_FIO",
				"type": "string"
			},
			{
				"internalType": "uint8",
				"name": "_class",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "_classLetter",
				"type": "string"
			}
		],
		"name": "registrationForStudent",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
"""