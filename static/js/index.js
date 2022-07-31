
// init some html elements
const buyableTextField = $("#buyableInput")
const earnableTextField = $("#earnableInput")
const submitBtn = $("#submitBtn")

const buyableDropdown = $("#buyableBtn")
const earnableDropdown = $("#earnableBtn")

// clear and disable text fields
buyableTextField.val("")
earnableTextField.val("")

buyableTextField.prop("disabled", true)
earnableTextField.prop("disabled", true)


function itemClick(element) {
    /*
    When an item is clicked from the dropdown, it will lock the and reset the other field, as well as reset the other dropdown.
     */
    if (element.name === "buyable") {
        earnableTextField.val("")
        earnableTextField.prop("disabled", true)
        buyableTextField.prop("disabled", false)
        buyableDropdown.text(element.text)
        earnableDropdown.text("Earnable")
        buyableTextField.val(element.getAttribute("data-price")) // fill the default price into the text field
    }
    if (element.name === "earnable") {
        buyableTextField.val("")
        buyableTextField.prop("disabled", true)
        earnableTextField.prop("disabled", false)
        earnableDropdown.text(element.text)
        buyableDropdown.text("Buyable")
        earnableTextField.val(element.getAttribute("data-price")) // fill the default price into the text field
    }
}

function submit() {
    /*
    submits the new transaction
     */
    // send to endpoint
    // find active field
    if (buyableTextField.is(":disabled") === false) { // conditions check which field is filled ( buyable or earnable )
        let item = buyableDropdown.text() // get the item and price
        let price = buyableTextField.val()

        $.ajax({ // send to server
            url: "/add-transaction?name=" + item + "&price=" + price,
            complete: function(){
                // window.location.reload(); // reload the page to get the updated data
            }
        })
    } else if (earnableTextField.is(":disabled") === false) {
        // repeat above but for earnable
        let item = earnableDropdown.text()
        let price = earnableTextField.val()

        $.ajax({
            url: "/add-transaction?name=" + item + "&price=" + price,
            complete: function(){
                // window.location.reload(); // reload the page to get the updated data
            }
        })
    }

}