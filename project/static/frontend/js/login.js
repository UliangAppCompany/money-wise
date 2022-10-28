
$(function () {
    var form = $('#login-form')
    var data = {}
    var postUrl = JSON.parse($('#post-url').text())

    $('#login-form-submit-button').on("submit", function (event) {
        event.preventDefault()
        $(this).prop("disable", true)

        form.serializeArray()
            .forEach(function (item) {
                data[item['name'] = item['value']]
            })

        $.post(postUrl, data, function (result) {
            console.log(result)
        }).fail(function (error) {
            console.log(error)
        }).always(function (result) {
            if ($(this).prop("disable")) {
                $(this).prop("disable", false)
            }
        })

    })
})