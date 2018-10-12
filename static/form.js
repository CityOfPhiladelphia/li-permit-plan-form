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
});