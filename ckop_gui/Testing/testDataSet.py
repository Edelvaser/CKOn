#-------------------Регистрация учителя------------------------------------
# string memory _login, 
# string memory _pass, 
# string memory _FIO, 
# uint16[] memory _leadsSchoolSubjects, 
# uint16[] memory _laboratories)
regTeacher_wrong = [
    ["", "", "", [], []],
    ["", "123", "Иванов И.И.", [0, 1], [100, 102]], # error
    ["aaaa", "", "Иванов И.И.", [0, 1], [100, 102]],
    ["aaaa", "123", "", [0, 1], [100, 102]], # error
    ["aaaa", "123", "Иванов И.И.", [], [100, 102]], # error
    ["aaaa", "123", "Иванов И.И.", [0, 1], []],
    ["aaaa", "123", "Иванов И.И.", [12, 14], [100, 102]],
    ["aaaa", "123", "Иванов И.И.", [1, 4], [100, 1202]],
    ["aaaa", "123", "Иванов И.И.", [1, 4], [100, 102]],
]

regTeacher_ok = [
    ["aaaa", "123", "Иванов И.И.", [0, 1], [100, 102]],
    ["aaaa", "123", "Иванов И.И.", [0, 1], [100, 102]],
    ["aaaa", "111", "Иванов И.И.", [0, 1], [100, 102]],
    ["bbbb", "123", "Иванов И.И.", [0, 1], [100, 102]],
]