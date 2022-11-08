$(function () {
    
    const csrftoken = Cookies.get('csrftoken')

    $.ajaxSetup({
        contentType: "application/json", 
        headers: {
            "X-CSRFToken": csrftoken 
        }
    })

    $('#change-password-form').on('submit', function (event) {
        event.preventDefault(); 

        var data = {} 
        const messageBox = $('#message-box')

        $(this).serializeArray().forEach(function (item) {
            data[item['name']] = item['value']
        })

        const url = $(this).prop('action')
        let jsonData = JSON.stringify(data)
        $.ajax({
            url, type: "patch", data: jsonData
        }, function (result) {
            console.log(result) 
        }).fail(function (error) {
        //    let tb = JSON.parse(error).tb
           messageBox.html(error)

        }).done(function () {
            messageBox.text("Changed password!")
        }).always(function (result) {
            //
        })
    })
})