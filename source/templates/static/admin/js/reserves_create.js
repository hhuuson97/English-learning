function call_course(student, first) {
    $.get("../../coursefee/ajax/lookup/", {
            "query": student,
            "name": "course"
        }
    ).then(function (data) {
        let elementGroup = $("select#course");
        let payeeCourse = GetURLParameter('payee_course');
        elementGroup.html('');
        $('#reverser_course').select2('data', null);
        data.forEach(function (value) {
            if (value.length > 0) {
                let html = `<option value='${value[0]}'>${value[1]}</option>`;
                elementGroup.append(html);
                if (value[0] == payeeCourse && first){
                    $('#reverser_course').select2('data', {id: value[0], text: value[1]});
                }
            }
        });
        if (data.length == 1){
            $('#reverser_course').select2('data', {id: data[0][0], text: data[0][1]});
        }
    });
}

(function ($) {
    let studentId = GetURLParameter('student_id');
    if (studentId) {
        call_course(studentId, true);
    }
})(jQuery);