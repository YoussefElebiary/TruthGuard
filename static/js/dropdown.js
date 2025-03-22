const dropdownItems = document.querySelectorAll('.dropdown-item');
const modelDropdownButton = document.getElementById('modelDropdown');
const selectedModelInput = document.getElementById('selected-model');

dropdownItems.forEach(item => {
    item.addEventListener('click', function (e) {
        e.preventDefault();
        const selectedValue = item.getAttribute('data-value');
        modelDropdownButton.textContent = item.textContent;
        selectedModelInput.value = selectedValue;
    });
});