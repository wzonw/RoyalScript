// Add this to your static/js/script.js file or create a new one
document.addEventListener('DOMContentLoaded', function() {
    const outputContainer = document.getElementById('output-container');
    const lexicalBtn = document.getElementById('lexical-btn');
    const syntaxBtn = document.getElementById('syntax-btn');
    const semanticBtn = document.getElementById('semantic-btn');
    const inputCode = document.getElementById('input-code');
    const lineNumbers = document.getElementById('line-numbers');
    const lexemeContainer = document.getElementById('lexeme-container');
    const tokenContainer = document.getElementById('token-container');
    
    // Update line numbers when the code changes
    inputCode.addEventListener('input', updateLineNumbers);
    inputCode.addEventListener('scroll', syncScroll);
    
    function updateLineNumbers() {
        const numberOfLines = inputCode.value.split('\n').length;
        lineNumbers.innerHTML = Array(numberOfLines)
            .fill(0)
            .map((_, i) => `<div>${i + 1}</div>`)
            .join('');
    }
    
    function syncScroll() {
        lineNumbers.scrollTop = inputCode.scrollTop;
    }
    
    // Initialize line numbers
    updateLineNumbers();
    
    // Terminal interaction globals
    let isWaitingForInput = false;
    let currentInputLine = null;
    let eventSource = null;

    // Event listeners for compiler buttons
    lexicalBtn.addEventListener('click', function() {
        performAnalysis('/analyze_lexical');
    });
    
    syntaxBtn.addEventListener('click', function() {
        performAnalysis('/analyze_syntax');
    });
    
    semanticBtn.addEventListener('click', function() {
        performAnalysis('/analyze_semantic');
    });
    
    // Function to perform analysis
    function performAnalysis(endpoint) {
        const code = inputCode.value;
        
        if (!code.trim()) {
            addOutputLine('Please enter some code first.', 'error');
            return;
        }
        
        // Clear previous outputs
        clearOutput();
        
        // Close any existing EventSource
        if (eventSource) {
            eventSource.close();
            eventSource = null;
        }
        
        // If semantic analysis is successful and ready to run
        if (endpoint === '/analyze_semantic') {
            fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'code=' + encodeURIComponent(code)
            })
            .then(response => response.json())
            .then(data => {
                // Display the compiler messages
                data.message.split('\n').forEach(line => {
                    let cssClass = '';
                    if (line.includes('✅')) cssClass = 'success';
                    if (line.includes('❌')) cssClass = 'error';
                    addOutputLine(line, cssClass);
                });
                
                // If semantic analysis was successful and generated Python code
                if (data.success && data.ready_to_run) {
                    // Display the Python code if needed
                    // addOutputLine('Generated Python code:', 'success');
                    // addOutputLine(data.python_code);
                    
                    // Start the interactive execution
                    startInteractiveExecution();
                }
                
                // Update token displays
                updateTokenDisplays(data);
            })
            .catch(error => {
                addOutputLine('Error: ' + error, 'error');
            });
        } else {
            // For lexical and syntax analysis
            fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'code=' + encodeURIComponent(code)
            })
            .then(response => response.json())
            .then(data => {
                // Display the results
                data.message.split('\n').forEach(line => {
                    let cssClass = '';
                    if (line.includes('✅')) cssClass = 'success';
                    if (line.includes('❌')) cssClass = 'error';
                    addOutputLine(line, cssClass);
                });
                
                // Update token displays
                updateTokenDisplays(data);
            })
            .catch(error => {
                addOutputLine('Error: ' + error, 'error');
            });
        }
    }
    
    // Update token displays
    function updateTokenDisplays(data) {
        if (data.lexemes && data.tokens) {
            lexemeContainer.innerHTML = '';
            tokenContainer.innerHTML = '';
            
            for (let i = 0; i < data.lexemes.length; i++) {
                const lexemeItem = document.createElement('div');
                lexemeItem.className = 'token-item';
                lexemeItem.textContent = data.lexemes[i];
                lexemeContainer.appendChild(lexemeItem);
                
                const tokenItem = document.createElement('div');
                tokenItem.className = 'token-item';
                tokenItem.textContent = data.tokens[i];
                tokenContainer.appendChild(tokenItem);
            }
        }
    }
    
    // Start interactive execution
    function startInteractiveExecution() {
        addOutputLine('Starting program execution...', 'success');
        addOutputLine('------------OUTPUT------------');
        
        // Close any existing EventSource
        if (eventSource) {
            eventSource.close();
            eventSource = null;
        }
        
        // Create an EventSource for streaming output
        eventSource = new EventSource('/run_interactive');
        
        eventSource.onmessage = function(event) {
            const message = event.data;
            
            // Check if the message indicates waiting for input
            if (message.includes('input(') || message.includes('Input:') || message.endsWith('?') || message.endsWith(': ')) {
                // Display the prompt
                const promptLine = document.createElement('div');
                promptLine.className = 'output-line';
                promptLine.textContent = message;
                outputContainer.appendChild(promptLine);
                
                // Create an input element in a new line
                createInputLine();
                
                // Autofocus the input element
                currentInputLine.focus();
                
                // Mark as waiting for input
                isWaitingForInput = true;
                
            } else {
                // Regular output
                addOutputLine(message);
            }
            
            // Scroll to the bottom
            outputContainer.scrollTop = outputContainer.scrollHeight;
        };
        
        eventSource.onerror = function(error) {
            addOutputLine('Stream error or connection closed', 'error');
            eventSource.close();
            eventSource = null;
            isWaitingForInput = false;
        };
    }
    
    // Create an input line
    function createInputLine() {
        // Get the last printed line (prompt)
        const lines = outputContainer.querySelectorAll('.output-line');
        const lastLine = lines[lines.length - 1];
    
        if (!lastLine) return;
    
        // Create input field and place it inline
        const inputField = document.createElement('input');
        inputField.type = 'text';
        inputField.className = 'output-input';
        inputField.autocomplete = 'off';
        inputField.spellcheck = false;
        inputField.style.marginLeft = '4px'; // spacing after colon
    
        inputField.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && isWaitingForInput) {
                e.preventDefault();
                const userInput = inputField.value;
                inputField.disabled = true;
                isWaitingForInput = false;
    
                fetch('/send_input', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'input=' + encodeURIComponent(userInput)
                });
    
                currentInputLine = null;
            }
        });
    
        // Append input to the same line
        lastLine.appendChild(inputField);
        inputField.focus();
        currentInputLine = inputField;
    }
    
    // Function to add an output line
    function addOutputLine(text, cssClass = '') {
        const line = document.createElement('div');
        line.className = 'output-line ' + cssClass;
        line.textContent = text;
        outputContainer.appendChild(line);
        
        // Scroll to the bottom
        outputContainer.scrollTop = outputContainer.scrollHeight;
    }
    
    // Function to clear the output
    function clearOutput() {
        outputContainer.innerHTML = '';
        isWaitingForInput = false;
        currentInputLine = null;
    }
    
    // Handle any keyboard interactions globally
    document.addEventListener('keydown', function(e) {
        // If we're waiting for input and the input field is not focused
        if (isWaitingForInput && currentInputLine && document.activeElement !== currentInputLine) {
            // Focus the input field
            currentInputLine.focus();
        }
    });
});