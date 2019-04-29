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
    //onload: call the above function 
    $(".stockpick-select").each(function() {
        initializeSelect2($(this));
    });
});