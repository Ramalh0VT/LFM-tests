let displayValue = '';
let currentOperator = '';
let prevValue = null;

function appendNumber(number) {
    displayValue += number;
    updateDisplay();
}

function calculate(operator) {
    if (prevValue !== null) {
        const currentValue = parseFloat(displayValue);
        switch (currentOperator) {
            case '+':
                prevValue += currentValue;
                break;
            case '-':
                prevValue -= currentValue;
                break;
            case '*':
                prevValue *= currentValue;
                break;
            case '/':
                prevValue /= currentValue;
                break;
        }
        displayValue = prevValue.toString();
        currentOperator = '';
        updateDisplay();
    } else {
        currentOperator = operator;
    }
}

function clearDisplay() {
    displayValue = '';
    currentOperator = '';
    prevValue = null;
    updateDisplay();
}

function updateDisplay() {
    document.getElementById('display').value = displayValue;
}

// Initial update to display
updateDisplay();

