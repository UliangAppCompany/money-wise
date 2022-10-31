
$(function () {
    var data = {}
    var postUrl = JSON.parse($('#post-url').text())
    var button = $('#login-form-submit-button')

    const csrftoken = Cookies.get('csrftoken')

    $.ajaxSetup({
        contentType: "application/json", 
        headers: {
            "X-CSRFToken": csrftoken 
        }
    })

    $('#login-form').on("submit", function (event) {
        event.preventDefault()
        button.prop("disabled", true)
        
        $(this).serializeArray()
            .forEach(function (item) {
                data[item['name']] = item['value']
            })
        // console.log(data, postUrl)
        var payload = JSON.stringify(data)

        $.post(postUrl, payload, function (result) {
            console.log(result)
        }).done(function() {
            $('#auth-message').text("Authenticated!")
        }).done(function () {
            $(this).css("display", "none")
        }).fail(function (error) {
            const traceback = JSON.parse(error.responseText).message
            $('#auth-message').text(traceback)
        }).always(function () {
            if (button.prop("disabled")) {
                button.prop("disabled", false)
            }
        })

    })
})