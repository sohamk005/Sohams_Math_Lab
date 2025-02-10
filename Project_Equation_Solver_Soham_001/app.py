from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    eq_type = data.get('type', '')  # Prevent KeyError

    if eq_type == 'quadratic':
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
        c = float(data.get('c', 0))

        if a == 0:
            return jsonify(error="Coefficient 'a' cannot be zero for a quadratic equation"), 400

        D = (b**2) - (4*a*c)
        if D >= 0:
            x1 = (-b + (D**0.5)) / (2*a)
            x2 = (-b - (D**0.5)) / (2*a)
            roots = [x1, x2]
        else:
            roots = ["Complex roots"]

        # Plot the quadratic equation
        x = np.linspace(-10, 10, 400)
        y = a*x**2 + b*x + c
        plt.figure()
        plt.plot(x, y, label=f'{a}x^2 + {b}x + {c}')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.legend()

    elif eq_type == 'cubic':
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
        c = float(data.get('c', 0))
        d = float(data.get('d', 0))

        if a == 0:
            return jsonify(error="Coefficient 'a' cannot be zero for a cubic equation"), 400

        roots = solve_cubic(a, b, c, d)

        # Plot the cubic equation
        x = np.linspace(-10, 10, 400)
        y = a*x**3 + b*x**2 + c*x + d
        plt.figure()
        plt.plot(x, y, label=f'{a}x^3 + {b}x^2 + {c}x + {d}')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.legend()

    else:
        return jsonify(error="Invalid equation type"), 400

    # Save plot to a string in base64 format
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return jsonify(roots=roots, plot_url=plot_url)

def solve_cubic(a, b, c, d):
    """Find the real roots of the cubic equation ax^3 + bx^2 + cx + d = 0 using numpy."""
    coefficients = [a, b, c, d]
    roots = np.roots(coefficients)  # Finds all roots (real and complex)
    real_roots = [r.real for r in roots if np.isreal(r)]  # Keep only real roots
    return real_roots

if __name__ == '__main__':
    app.run(debug=True)
