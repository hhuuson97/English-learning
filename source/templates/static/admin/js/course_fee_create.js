let feeCourse = [];

function call_course(student, first) {
    $.get("../ajax/lookup/", {
            "query": student,
            "name": "course"
        }
    ).then(function (data) {
        let elementGroup = $("select#course");
        let payeeCourse = GetURLParameter('payee_course');
        elementGroup.html('');
        $('#course').select2('data', null);
        $("#amount").attr('placeholder', '');
        feeCourse = data;
        data.forEach(function (value) {
            if (value.length > 0) {
                let html = `<option value='${value[0]}'>${value[1]}</option>`;
                elementGroup.append(html);
                if (value[0] == payeeCourse && first){
                    $('#course').select2('data', {id: value[0], text: value[1]});
                }
            }
        });
        if (data.length == 1){
            $('#course').select2('data', {id: data[0][0], text: data[0][1]});
            $("#amount").attr('placeholder', 'Học phí còn nợ: ' + data[0][2])
        }
    });
}

(function ($) {

    $("#student_id").on('change', function (obj) {
        call_course(obj.val);
        $("input#payer").val(obj.added.text.split("#")[1])
    });
    $("#course").on('change', function (obj) {
        feeCourse.forEach(function(value){
           if (value[0] == obj.val){
                $("#amount").attr('placeholder', 'Học phí còn nợ: ' + value[2])
           }
        });
    });

    let studentId = GetURLParameter('student_id');
    let amount = GetURLParameter('amount');
    if (studentId) {
        $.get("../ajax/lookup/", {
                "query": studentId,
                "name": "student_detail"
            }
        ).then(function (data) {
            if (data.length > 0) {
                let added = {id: data[0][0], text: data[0][1]};
                $('#student_id').select2('data', added);
                call_course(data[0][0], true);
            }
        })
    }
    if (amount){
        $("#amount").val(Math.abs(amount.split(",").join("")))
    }
})(jQuery);