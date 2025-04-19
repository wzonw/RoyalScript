// Global variables
let sessionId = '';
let outputPollInterval = null;
let isProcessRunning = false;

// Initialize when document is ready
$(document).ready(function() {
    // Generate a session ID
    $.get('/generate_session_id', function(data) {
        sessionId = data.session_id;
        $('#session-id').val(sessionId);
        
        // Initialize the terminal output area
        displayTerminalMessage('RoyalScript Web Compiler initialized.', 'terminal-system');
        displayTerminalMessage('Ready for input. Click any button to start.', 'terminal-system');
    });
    
    // Setup event listeners
    setupEventListeners();
    
    // Setup line numbers for code input
    setupLineNumbers();
});

// Set up all event listeners
function setupEventListeners() {
    // Button click handlers
    $('#lexical-btn').click(handleLexicalAnalysis);
    $('#syntax-btn').click(handleSyntaxAnalysis);
    $('#semantic-btn').click(handleSemanticAnalysis);
    $('#run-btn').click(handleRunCode);
    
    // Code input handlers for line numbers
    $('#input-code').on('input scroll', updateLineNumbers);
    $('#input-code').on('keydown', handleTabKey);
    
    // Terminal input handler
    $('#terminal-input').on('keydown', function(e) {
        if (e.keyCode === 13) { // Enter key
            handleTerminalInput();
        }
    });
}

// Handle lexical analysis button click
function handleLexicalAnalysis() {
    const code = $('#input-code').val();
    
    // Clear previous results
    clearTokenLists();
    displayTerminalMessage('Running lexical analysis...', 'terminal-info');
    
    $.ajax({
        url: '/analyze_lexical',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ code: code }),
        success: function(response) {
            if (response.success) {
                displayTokens(response.tokens);
                displayTerminalMessage(response.message, 'terminal-success');
            } else {
                displayTerminalMessage('Lexical analysis failed: ' + response.message, 'terminal-error');
                // Display errors if any
                if (response.errors && response.errors.length > 0) {
                    response.errors.forEach(error => {
                        displayTerminalMessage(`Error: ${error}`, 'terminal-error');
                    });
                }
            }
        },
        error: function(xhr, status, error) {
            displayTerminalMessage('Request failed: ' + error, 'terminal-error');
        }
    });
}

// Handle syntax analysis button click
function handleSyntaxAnalysis() {
    const code = $('#input-code').val();
    
    // Clear previous results
    clearTokenLists();
    displayTerminalMessage('Running syntax analysis...', 'terminal-info');
    
    $.ajax({
        url: '/analyze_syntax',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ code: code }),
        success: function(response) {
            if (response.success) {
                // Display lexical tokens first
                displayTokens(response.tokens);
                displayTerminalMessage(response.message, 'terminal-success');
                
                // Display AST if available
                if (response.ast) {
                    displayTerminalMessage('Abstract Syntax Tree:', 'terminal-info');
                    displayTerminalMessage(response.ast, 'terminal-code');
                }
            } else {
                if (response.stage === 'lexical') {
                    displayTerminalMessage('Lexical errors detected. Fix before syntax analysis.', 'terminal-error');
                } else {
                    displayTerminalMessage('Syntax analysis failed: ' + response.message, 'terminal-error');
                }
                
                // Display errors if any
                if (response.errors && response.errors.length > 0) {
                    response.errors.forEach(error => {
                        displayTerminalMessage(`Error: ${error}`, 'terminal-error');
                    });
                }
            }
        },
        error: function(xhr, status, error) {
            displayTerminalMessage('Request failed: ' + error, 'terminal-error');
        }
    });
}

// Handle semantic analysis button click
function handleSemanticAnalysis() {
    const code = $('#input-code').val();
    
    // Clear previous results
    clearTokenLists();
    displayTerminalMessage('Running semantic analysis...', 'terminal-info');
    
    $.ajax({
        url: '/analyze_semantic',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ code: code }),
        success: function(response) {
            if (response.success) {
                // Display lexical tokens
                displayTokens(response.tokens);
                displayTerminalMessage(response.message, 'terminal-success');
                
                // Display AST if available
                if (response.ast) {
                    displayTerminalMessage('Abstract Syntax Tree:', 'terminal-info');
                    displayTerminalMessage(response.ast, 'terminal-code');
                }
            } else {
                if (response.stage === 'lexical') {
                    displayTerminalMessage('Lexical errors detected. Fix before semantic analysis.', 'terminal-error');
                } else if (response.stage === 'syntax') {
                    displayTerminalMessage('Syntax errors detected. Fix before semantic analysis.', 'terminal-error');
                } else if (response.stage === 'ast') {
                    displayTerminalMessage('AST building failed: ' + response.message, 'terminal-error');
                } else {
                    displayTerminalMessage('Semantic analysis failed: ' + response.message, 'terminal-error');
                }
                
                // Display errors if any
                if (response.errors && response.errors.length > 0) {
                    response.errors.forEach(error => {
                        displayTerminalMessage(`Error: ${error}`, 'terminal-error');
                    });
                }
            }
        },
        error: function(xhr, status, error) {
            displayTerminalMessage('Request failed: ' + error, 'terminal-error');
        }
    });
}

// Handle run code button click
function handleRunCode() {
    const code = $('#input-code').val();
    
    // Clear previous results and stop any running processes
    clearTokenLists();
    stopOutputPolling();
    terminateProcess();
    
    displayTerminalMessage('Running code...', 'terminal-info');
    
    $.ajax({
        url: '/run_code',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ 
            code: code,
            session_id: sessionId
        }),
        success: function(response) {
            if (response.success) {
                displayTerminalMessage(response.message, 'terminal-success');
                
                // Start polling for output
                isProcessRunning = true;
                
                // Make sure input is enabled from the start
                $('#terminal-input').prop('disabled', false).focus();
                console.log("Input enabled at start of program");
                
                startOutputPolling();
            } else {
                if (response.stage === 'lexical') {
                    displayTerminalMessage('Lexical errors detected. Fix before running code.', 'terminal-error');
                } else if (response.stage === 'syntax') {
                    displayTerminalMessage('Syntax errors detected. Fix before running code.', 'terminal-error');
                } else if (response.stage === 'semantic') {
                    displayTerminalMessage('Semantic errors detected. Fix before running code.', 'terminal-error');
                } else {
                    displayTerminalMessage('Failed to run code: ' + response.message, 'terminal-error');
                }
                
                // Display errors if any
                if (response.errors && response.errors.length > 0) {
                    response.errors.forEach(error => {
                        displayTerminalMessage(`Error: ${error}`, 'terminal-error');
                    });
                }
            }
        },
        error: function(xhr, status, error) {
            displayTerminalMessage('Request failed: ' + error, 'terminal-error');
        }
    });
}

// Handle input in the terminal
function handleTerminalInput() {
    const input = $('#terminal-input').val();
    
    // Clear input field regardless
    $('#terminal-input').val('');
    
    // Don't send empty input
    if (!input.trim() && isProcessRunning) {
        return;
    }
    
    if (isProcessRunning) {
        console.log("Sending input:", input);
        
        $.ajax({
            url: '/send_input',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 
                input: input,
                session_id: sessionId
            }),
            success: function(response) {
                console.log("Input response:", response);
                if (!response.is_running) {
                    isProcessRunning = false;
                    $('#terminal-input').prop('disabled', true);
                    stopOutputPolling();
                } else {
                    // Re-focus on the input field
                    $('#terminal-input').focus();
                }
            },
            error: function(xhr, status, error) {
                displayTerminalMessage('Failed to send input: ' + error, 'terminal-error');
            }
        });
    }
}

// Function to handle the process output polling
function startOutputPolling() {
    if (outputPollInterval) {
        clearInterval(outputPollInterval);
    }
    
    outputPollInterval = setInterval(function() {
        if (!isProcessRunning) {
            stopOutputPolling();
            return;
        }
        
        $.ajax({
            url: '/process_output',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ session_id: sessionId }),
            success: function(response) {
                // Process output messages
                if (response.output && response.output.length > 0) {
                    response.output.forEach(item => {
                        switch(item.type) {
                            case 'output':
                                displayTerminalMessage(item.content, 'terminal-output');
                                break;
                            case 'error':
                                displayTerminalMessage(item.content, 'terminal-error');
                                break;
                            case 'input_prompt':
                                displayTerminalMessage(item.content, 'terminal-prompt');
                                // Always enable input and focus when a prompt is detected
                                $('#terminal-input').prop('disabled', false).focus();
                                console.log("Input enabled due to prompt");
                                break;
                            case 'user_input':
                                displayTerminalMessage('> ' + item.content, 'terminal-input-text');
                                break;
                            case 'system':
                                displayTerminalMessage(item.content, 'terminal-system');
                                break;
                            default:
                                displayTerminalMessage(item.content, 'terminal-output');
                        }
                    });
                    
                    // Scroll to bottom after new content
                    const terminal = $('#terminal-output');
                    terminal.scrollTop(terminal[0].scrollHeight);
                }
                
                // Check if process is still running
                if (!response.is_running) {
                    isProcessRunning = false;
                    $('#terminal-input').prop('disabled', true);
                    stopOutputPolling();
                    displayTerminalMessage("Process completed.", 'terminal-system');
                } else if (response.waiting_for_input) {
                    // Make sure input is enabled when waiting for input
                    if ($('#terminal-input').prop('disabled')) {
                        console.log("Enabling input field because waiting_for_input=true");
                        $('#terminal-input').prop('disabled', false).focus();
                    }
                }
            },
            error: function(xhr, status, error) {
                console.error('Error polling for output:', error);
                // Don't stop polling on error, just log it
            }
        });
    }, 250); // Poll more frequently
}

// Stop polling for process output
function stopOutputPolling() {
    if (outputPollInterval) {
        clearInterval(outputPollInterval);
        outputPollInterval = null;
    }
}

// Terminate any running process
function terminateProcess() {
    $.ajax({
        url: '/terminate_process',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ session_id: sessionId }),
        success: function(response) {
            if (response.success) {
                isProcessRunning = false;
                $('#terminal-input').prop('disabled', true);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error terminating process:', error);
        }
    });
}

// Display a message in the terminal
function displayTerminalMessage(message, className) {
    const terminal = $('#terminal-output');
    
    // Create message element
    const messageElement = $('<div></div>')
        .addClass(className)
        .text(message);
    
    // Append to terminal
    terminal.append(messageElement);
    
    // Scroll to bottom
    terminal.scrollTop(terminal[0].scrollHeight);
}

// Display tokens in the token lists
function displayTokens(tokens) {
    if (!tokens || tokens.length === 0) return;
    
    const lexemeList = $('#lexeme-list');
    const tokenList = $('#token-list');
    
    // Clear existing tokens
    lexemeList.empty();
    tokenList.empty();
    
    // Add new tokens
    tokens.forEach(token => {
        lexemeList.append(
            $('<option></option>')
                .text(token.value)
                .data('line', token.line)
        );
        
        tokenList.append(
            $('<option></option>')
                .text(token.type)
                .data('line', token.line)
        );
    });
    
    // Update lexer line numbers
    updateLexerLineNumbers();
}

// Clear token lists
function clearTokenLists() {
    $('#lexeme-list').empty();
    $('#token-list').empty();
    $('#lexer-line-numbers').empty();
}

// Setup line numbers for code input
function setupLineNumbers() {
    updateLineNumbers();
    
    // Initial lexer line numbers (empty)
    updateLexerLineNumbers();
}

// Update line numbers for code input
document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById("input-code");
    const lineNumbers = document.getElementById("input-line-numbers");

    // Update line numbers initially
    updateLineNumbers();

    // Scroll sync
    textarea.addEventListener("scroll", function () {
        lineNumbers.scrollTop = textarea.scrollTop;
    });

    // Update line numbers dynamically
    textarea.addEventListener("input", updateLineNumbers);
    textarea.addEventListener("keyup", updateLineNumbers);

    function updateLineNumbers() {
        const lines = textarea.value.split("\n").length;
        let lineNumberHTML = "";
        for (let i = 1; i <= lines; i++) {
            lineNumberHTML += i + "<br>";
        }
        lineNumbers.innerHTML = lineNumberHTML;
    }
});


// Update lexer line numbers
function updateLexerLineNumbers() {
    const lexemeList = $('#lexeme-list');
    const lineNumbers = $('#lexer-line-numbers');
    
    // Get tokens
    const tokens = lexemeList.find('option');
    if (tokens.length === 0) {
        lineNumbers.empty();
        return;
    }
    
    // Get line numbers from tokens
    const lines = [];
    tokens.each(function() {
        const line = $(this).data('line');
        if (line && !lines.includes(line)) {
            lines.push(line);
        }
    });
    
    // Sort and generate line numbers
    lines.sort((a, b) => a - b);
    lineNumbers.empty();
    lines.forEach(line => {
        lineNumbers.append($('<div></div>').text(line));
    });
}

// Handle tab key in code input
function handleTabKey(e) {
    if (e.keyCode === 9) { // Tab key
        e.preventDefault();
        
        // Insert tab
        const start = this.selectionStart;
        const end = this.selectionEnd;
        
        // Insert 4 spaces
        this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);
        
        // Move cursor
        this.selectionStart = this.selectionEnd = start + 4;
        
        // Update line numbers
        updateLineNumbers();
    }
}

// Window close event - cleanup
$(window).on('beforeunload', function() {
    // Terminate any running process
    terminateProcess();
});