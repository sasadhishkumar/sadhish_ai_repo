# calculator.py
from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML + CSS + JS Calculator (All in one file)
CALCULATOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>India Calculator</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #ff9933, #ffffff, #138808);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #333;
        }
        .calculator {
            background: rgba(255, 255, 255, 0.98);
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            width: 320px;
            text-align: center;
        }
        .flag { font-size: 40px; margin-bottom: 10px; }
        h1 { color: #0A66C2; margin-bottom: 5px; }
        p { color: #7f8c8d; margin-bottom: 20px; }
        #display {
            width: 100%;
            height: 60px;
            font-size: 28px;
            text-align: right;
            padding: 0 15px;
            margin-bottom: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            background: #f8f9fa;
            color: #2c3e50;
        }
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }
        button {
            padding: 18px;
            font-size: 20px;
            font-weight: bold;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .num { background: #ecf0f1; color: #2c3e50; }
        .num:hover { background: #bdc3c7; }
        .op { background: #3498db; color: white; }
        .op:hover { background: #2980b9; }
        .eq { background: #27AE60; color: white; grid-column: span 2; }
        .eq:hover { background: #219a52; }
        .clear { background: #e74c3c; color: white; grid-column: span 2; }
        .clear:hover { background: #c0392b; }
        .footer {
            margin-top: 20px;
            font-size: 12px;
            color: #95a5a6;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <div class="flag">India</div>
        <h1>Calculator</h1>
        <p>Made in India</p>
        
        <input type="text" id="display" value="{{ result|default('0') }}" readonly>
        
        <div class="buttons">
            <button class="clear" onclick="clearDisplay()">C</button>
            <button class="op" onclick="appendToDisplay('/')">/</button>
            
            <button class="num" onclick="appendToDisplay('7')">7</button>
            <button class="num" onclick="appendToDisplay('8')">8</button>
            <button class="num" onclick="appendToDisplay('9')">9</button>
            <button class="op" onclick="appendToDisplay('*')">×</button>
            
            <button class="num" onclick="appendToDisplay('4')">4</button>
            <button class="num" onclick="appendToDisplay('5')">5</button>
            <button class="num" onclick="appendToDisplay('6')">6</button>
            <button class="op" onclick="appendToDisplay('-')">-</button>
            
            <button class="num" onclick="appendToDisplay('1')">1</button>
            <button class="num" onclick="appendToDisplay('2')">2</button>
            <button class="num" onclick="appendToDisplay('3')">3</button>
            <button class="op" onclick="appendToDisplay('+')">+</button>
            
            <button class="num" onclick="appendToDisplay('0')" style="grid-column: span 2;">0</button>
            <button class="num" onclick="appendToDisplay('.')">.</button>
            <button class="eq" onclick="calculate()">=</button>
        </div>
        
        <div class="footer">
            India | {{ now }}
        </div>
    </div>

    <script>
        function appendToDisplay(value) {
            const display = document.getElementById('display');
            if (display.value === '0' && value !== '.') {
                display.value = value;
            } else {
                display.value += value;
            }
        }
        
        function clearDisplay() {
            document.getElementById('display').value = '0';
        }
        
        function calculate() {
            const display = document.getElementById('display');
            try {
                // Replace × with *
                let expression = display.value.replace(/×/g, '*');
                let result = eval(expression);
                display.value = result;
                // Send result to Flask
                fetch('/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: 'expression=' + encodeURIComponent(display.value) + '&result=' + result
                });
            } catch (e) {
                display.value = 'Error';
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    from datetime import datetime
    ist_time = (datetime.utcnow().timestamp() + 5.5*3600)
    now = datetime.fromtimestamp(ist_time).strftime("%I:%M %p IST, %d %B %Y")
    return render_template_string(CALCULATOR_HTML, now=now)

@app.route("/calculate", methods=["POST"])
def calculate():
    # Optional: Log calculation (not used in UI)
    expression = request.form.get("expression", "")
    result = request.form.get("result", "")
    print(f"Calculation: {expression} = {result}")
    return "OK"

if __name__ == "__main__":
    print("India Calculator Running!")
    print("Open: http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)