(function ($) {
    let is_course_fee_report = window.location.href.indexOf('course_fee_report') > -1;
    let active_filters_data = JSON.parse($('#active-filters-data').text() || "[]");
    let filter_groups_data = JSON.parse($('#filter-groups-data').text() || "{}");
    if (active_filters_data.length === 0) {
        $('a.filter').click();
    } else {
        let activeList = active_filters_data.map(x => x[1]);
        $("a.filter").each(function (idx, el) {
            let el_text = $(el).text();
            if (!activeList.includes(el_text)) {
                $(el).click();
            }
        });
    }
    let reSelectFilter = [];
    $.each(filter_groups_data, function (key, value) {
        let _type = value[0]['type'];
        if (_type && _type.indexOf("date") === 0) {
            reSelectFilter.push(key);
        }
    });

    $("table.filters tr").each(function (idx, el) {
        let el_text = $(el).find("td").eq(0).text().substring(2).trim();
        if (reSelectFilter.includes(el_text)) {
            if (el_text.toLowerCase() == 'đến ngày') {
                $(el).find("select.filter-op option").eq(3).prop('selected', true);
            } else if (el_text.toLowerCase() == 'ngày thu' && is_course_fee_report) {
                $(el).find("select.filter-op option").eq(4).prop('selected', true);
            } else {
                $(el).find("select.filter-op option").eq(2).prop('selected', true);
            }
            $(el).find("select.filter-op").trigger('change');
        }
    });

    $(".filters tr").each(function (idx, value) {
        let _title = $(value).find("td").eq(0).text().substring(2);
        let $el = $(value).find("td").eq(2).find("input");
        $el.attr('placeholder', _title);
        $el.attr('title', _title);
        $el.attr('autocomplete', 'off');
    });
    let payeeId = GetURLParameter('payee');
    let studentId = GetURLParameter('student_id');
    let payeeCourse = GetURLParameter('payee_course');
    if (payeeId || studentId) {
        $('#reverser_course').val(payeeId || studentId).trigger('change');
        if ($('#student').attr('data-role') == "select2") {
            $('#student').val(payeeId || studentId).trigger('change');
        }
    }
    if (payeeCourse) {
        $('#payee_course').val(payeeCourse).trigger('change');
    }
    $(".nav-tabs.actions-nav li").each(function (index) {
        if ($(this).find("ul.field-filters").length > 0) {
            $(this).hide();
        }
    });

    $('#amount,#fee, #paid_fee').on('blur keyup', function () {
        const value = this.value.replace(/,/g, '');
        if (!isNaN(parseFloat(value))) {
            this.value = parseFloat(value).toLocaleString('en-US', {
                style: 'decimal',
                maximumFractionDigits: 0,
                minimumFractionDigits: 0
            });
        } else {
            this.value = '';
        }
    });
    let isJustSubmit = false;
    $(".admin-form").on("submit", function (event) {
        if (!isJustSubmit) {
            event.preventDefault();
            $('input[name="amount"]').val(($('input[name="amount"]').val() || "").replace(/,/g, ''));
            $('input[name="fee"]').val(($('input[name="fee"]').val() || "").replace(/,/g, ''));
            $('input[name="paid_fee"]').val(($('input[name="paid_fee"]').val() || "").replace(/,/g, ''));
            isJustSubmit = true;
            $(".admin-form").submit();
        }
    });


})(jQuery);