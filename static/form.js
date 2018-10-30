document.addEventListener('DOMContentLoaded', () => {

    // When the add AP Number button is clicked, add another field to enter another AP Number
    document.querySelector('#add-apno-button').addEventListener('click', () => {
        const apnoButton = document.createElement('div');
        apnoButton.id = 'ap-number-input'
        const apnoInput = document.createElement('input');
        apnoInput.type = 'text';
        apnoInput.name = 'apno-input';
        apnoButton.appendChild(apnoInput);
        document.querySelector('#ap-number-input-list').append(apnoButton);
    });

    // When the delete AP Number button is clicked, remove an AP Number field
    document.querySelector('#delete-apno-button').addEventListener('click', () => {
        let apNumberInputList = document.querySelector('#ap-number-input-list');
        if (apNumberInputList.childElementCount > 1) {
            apNumberInputList.removeChild(apNumberInputList.lastChild);
        }
    })
});