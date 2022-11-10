class httpService {
    constructor({
        formElem = $('form'), 
        contentType = 'application/json', 
        csrfHeaderName = 'X-CSRFToken', 
        successHandlers = [
            (responseData, status, jqXHR) => { }, 
         ], 
        completeHandlers = [
            (jqXHR, status) => { }, 
        ], 
        errorHandlers = [
            (jqXHR, status, errorThrown) => { }
        ], 
        timeout = 5000, 
        ajaxSettings = {}
    } = {}) {

        $.ajaxSetup({
            contentType,
            headers: {
                [csrfHeaderName]: Cookies.get('csrftoken')
            },
            method: formElem.prop('method'),  
            complete: [...completeHandlers], 
            success: [responseData => console.log(responseData), ...successHandlers], 
            error: [jqXHR => console.log(jqXHR), ...errorHandlers],
            timeout, 
            ...ajaxSettings
        });

        this.send = this.send.bind(this);
        this._data = {};
        this.formElem = formElem; 
    }

    get data() {
        this.formElem.serializeArray().forEach(item => {
            this._data[item['name']] = item['value']
        })
        return this._data
    }

    send(event) {
        event.preventDefault();

        $.ajax({
            url: this.formElem.prop('action'), 
            data: JSON.stringify( this.data )
        })
    }
}



