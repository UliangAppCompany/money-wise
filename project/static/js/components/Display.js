class Display {
    constructor({
        displayElem = $('div'), 
    } = {}) {
        this.displayElem = displayElem
    }

    flash (message) {
        this.displayElem.html(message)
    } 

}