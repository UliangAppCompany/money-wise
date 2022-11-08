export class ajaxService {
    constructor({
        beforeSubmit, 
        afterSubmit, 
        formDataProcessor = function(item) {
            this.data[item['name']] = item['value']
        }, 
        success = [], 
        complete = function (_, result) {
            console.log(result)
        }, 
        contentType = 'application/json', 
        csrfHeaderName = 'X-CSRFToken', 
        dataType = 'json', 
        formElem = $('form'), 
        error = function (error, textStatus, errorThrown) {
            const { tb } = JSON.parse(error.responseText)
            $('message-box').html(
                `<p>${textStatus}</p><p>${errorThrown}<p>${tb}</p>`
            )
        }, 
        ajaxSettings = {}
    } = {}) {

        $.ajaxSetup({
            contentType,
            headers: {
                [csrfHeaderName]: Cookies.get('csrftoken')
            },
            method: formElem.prop('method'),  
            complete, 
            success, 
            error,
            dataType,  
            ...ajaxSettings
        });

        this.submit.bind(this);
        formDataProcessor.bind(this); 
        this.formDataProcessor = formDataProcessor; 
        this.data = {};
        this.beforeSubmit = beforeSubmit; 
        this.afterSubmit = afterSubmit; 
        this.formElem = formElem; 
    }

    submit(event) {
        event.preventDefault();
        this.beforeSubmit();

        this.formElem.serializeArray().forEach(this.formDataProcessor);

        $.ajax({
            url: this.formElem.prop('action'), 
            data: JSON.stringify( this.data )
        }).always(this.afterSubmit)
    }
}



