$(function () {
    var postUrl = JSON.parse($("#post-url").text());
    var ledgerUrl = JSON.parse($("#ledger-url").text());
    
    $('input[type="submit"]').on("submit", function (event) {
        event.preventDefault();
        $(this).prop("disabled", true);

        var form = $('#add-account-form');
        var dataArray = form.serializeArray();
        var data = {};
        dataArray.forEach(function (elem) {
            data[elem['name']] = elem['value']
        });

        $.post(postUrl, data, function (result) {
            console.log(result)
        })
            .fail(function (error) {
                console.log(error)
            })
            .always(function (result) {
                button = $('#submit-and-continue-button')
                if (button.prop('disabled')) {
                    button.prop('disabled', false)
                }
            });
        if ($(this).is('#submit-button')) {
            window.location.href = ledgerUrl;
        }
        form.trigger("reset");
    })
})