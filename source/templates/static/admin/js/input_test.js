function buildAnswer() {
    let elAnswer = $("#answers");
    elAnswer.find("option").remove();
    elAnswer.val(null).trigger('change');
    $.each(questionList, function (index, value) {
        let option = new Option(value.short_code || value.question, value.id, true, value.points > 0);
        elAnswer.append(option).trigger('change');
    });
    elAnswer.select2();
}

function buildQuestionList(){
    let html_body = "";
    $.each(questionList, function (index, value) {
        html_body += `<div class="left_title"><b>${value.short_code}</b></div>
            <div class="right_title"><span class="max-width-200 text_overflow_hide ${value.points > 0 ? "text-green": ""}">${value.code} - ${value.question || value.name}</span></div>`;
    });
    let question_html = `
<div class="left_title header">Thứ tự</div><div class="right_title header">Câu hỏi</div>
<div class="left_title header">Thứ tự</div><div class="right_title header">Câu hỏi</div>
    ${html_body}`;
    $(".group-questions").html(question_html);
    buildAnswer();
}
(function ($) {
    $("input#test").on('change', function (obj) {
        let value = obj.val;
        $.get("ajax/lookup/", {
                "query": value,
                "name": "question"
            }
        ).then(function (data) {
            questionList = data;
            selectedQuestionList = [];
            buildQuestionList();
        })
    });

    let studentId = GetURLParameter('student_id');
    let studentCode = GetURLParameter('student_code');
    if (studentId || studentCode) {
        $.get("ajax/lookup/", {
                "query": studentId ? studentId : studentCode,
                "name": studentId ? "student_id" : "student"
            }
        ).then(function (data) {
            if (data.length > 0) {
                let added = {id: data[0][0], text: data[0][1]};
                $('#student').select2('data', added);
            }
        })
    }
    buildQuestionList();
})(jQuery);