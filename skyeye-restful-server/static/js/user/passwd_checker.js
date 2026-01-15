function PasswordChk(pwd, repwd) {
    if (pwd.val() == '') {
        alert('비밀번호를 입력하세요');
        pwd.focus();
        return false;
    }
    if (pwd.val().indexOf(' ') > -1) {
        alert("공백은 입력할 수 없습니다.");
        return false;
    }

    var check1 = /^(?=.*[a-zA-Z])(?=.*[0-9]).{10,15}$/.test(pwd.val()); //영문,숫자
    var check2 = /^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).{8,15}$/.test(pwd.val()); //영문,숫자,특수문자
    var check3 = /^(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{10,15}$/.test(pwd.val()); //영문,특수문자
    var check4 = /^(?=.*[^a-zA-Z0-9])(?=.*[0-9]).{10,15}$/.test(pwd.val()); //특수문자, 숫자
    if (!(check1 || check2)) {
        alert("영문/숫자 혼용시에는 10~15자리를 사용해야 합니다.\n영문/숫자/특수문자 혼용시에는 8~15자리를 사용해야 합니다.");
        return false;
    }

    // 동일한 문자/숫자 4자 이상
    if (/(\w)\1\1\1/.test(pwd.val())) { // /(\w)\1\1/.test(pwd)
        alert("같은 문자를 4번 이상 사용할 수 없습니다.");
        pwd.focus();
        return false;
    }
    if (isContinuedValue(pwd.val())) {
        alert("비밀번호에 4자 이상의 연속 문자 또는 숫자를 사용하실 수 없습니다.");
        pwd.focus();
        return false;
    }

    if (repwd.val() == '') {
        alert('비밀번호를 다시 한번 더 입력하세요');
        repwd.focus();
        return false;
    }
    if (pwd.val() !== repwd.val()) {
        alert('비밀번호를 둘다 동일하게 입력하세요');
        return false;
    }
    return true;
}

function isContinuedValue(value) {
    console.log("value = " + value);
    var intCnt1 = 0;
    var intCnt2 = 0;
    var temp0 = "";
    var temp1 = "";
    var temp2 = "";
    var temp3 = "";

    for (var i = 0; i < value.length - 3; i++) {
        temp0 = value.charAt(i);
        temp1 = value.charAt(i + 1);
        temp2 = value.charAt(i + 2);
        temp3 = value.charAt(i + 3);

        if (temp0.charCodeAt(0) - temp1.charCodeAt(0) == 1
            && temp1.charCodeAt(0) - temp2.charCodeAt(0) == 1
            && temp2.charCodeAt(0) - temp3.charCodeAt(0) == 1) {
            intCnt1 = intCnt1 + 1;
        }

        if (temp0.charCodeAt(0) - temp1.charCodeAt(0) == -1
            && temp1.charCodeAt(0) - temp2.charCodeAt(0) == -1
            && temp2.charCodeAt(0) - temp3.charCodeAt(0) == -1) {
            intCnt2 = intCnt2 + 1;
        }
    }
    return (intCnt1 > 0 || intCnt2 > 0);
}