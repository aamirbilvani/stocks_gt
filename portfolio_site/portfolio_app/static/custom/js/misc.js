//function to initialize select2
function initializeSelect2(selectElementObj) {
    selectElementObj.select2({
        width: "80%",
        placeholder: 'Select a Stock',
    });
}

$('.stockpick-row').formset({
    addText: 'Add',
    deleteText: 'Remove',
    prefix: 'stockpicks'
});

$(document).ready(function() {
    //onload: initialize select2
    $(".stockpick-select").each(function() {
        initializeSelect2($(this));
    });

    //onload: initialize datepicker
    $(".date-picker-input").each(function() {
        triggerElement = $(this).next().find('button.datepicker-trigger')[0]
        $(this).datepicker({
            format:'yyyy-mm-dd',
            autoHide:true,
            trigger:$(triggerElement),
        });
    });
});