from flask import Flask, request, jsonify
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to the Number Classification API Visit /api/classify-number?number=<your_number> to use the API."

def is_prime_number(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
        return True
    
def is_perfect_number(n):
    """Check if a number is perfect."""
    if n < 2:
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)
    return sum_factors == n    

def sum_of_digits(n):
    """Calculate the sum of the digits of a number."""
    return sum(int(digit) for digit in str(abs(n)))

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    num_digits = len(digits)
    return n == sum(d ** num_digits for d in digits)

def get_fun_fact(n):
    """Fetch a fun fact about the number from the Number APi."""
    response = requests.get(f"http://numbersapi.com/{n}/math")
    if response.status_code == 200:
        return response.text.strip() # Remove extra whitespace
    
    return "No fun fact available."
        
@app.route('/api/classify-number', methods=['GET', 'OPTIONS'])
@cross_origin()
def classify_number():
    if request.method == 'OPTIONS':
        return '', 200
    
    number_str = request.args.get('number')
    if number_str is None or not number_str.lstrip('-').isdigit():
        return jsonify({
            "number": "alphabet",
            "error": True
        }), 400
        
    number = int(number_str)    
    original_number = number
        
    number = abs(number)   
    
    is_prime = is_prime_number(number)
    is_perfect = is_perfect_number(number)
    digit_sum = sum_of_digits(number)
    fun_fact = get_fun_fact(number)
    
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    if "armstrong" in properties:
        digits = [int(d) for d in str(number)]
        num_digits = len(digits)
        armstrong_explanation = " + ".join(f"{d}^{num_digits}" for d in digits)
        fun_fact = f"{number} is an Armstrong number because {armstrong_explanation} = {number}"    
    
    fun_fact_with_comments = f"{fun_fact} //gotten from the numbers API"
    digit_sum_with_comment = f"{digit_sum} // sum of its digits"
    
    return jsonify({
        "number": number,
        "is_prime": is_prime,
        "is_perfect": is_perfect,
        "properties": properties,
        "digit_sum": digit_sum_with_comment,
        "fun_fact": fun_fact_with_comments,
    })
    
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "number": "alphabet",
        "error": True
    }), 404 
    
@app.route('/test')
def test():
    return "Hello, Flask is working!"
            
            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
               