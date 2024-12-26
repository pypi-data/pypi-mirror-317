from flask import Flask, render_template, jsonify
import random
import os

def create_app():
    app = Flask(__name__)
    
    # Data lists for random selections
    app.config['COLORS'] = ["Red", "Blue", "Green", "Purple", "Orange", "Yellow", "Pink"]
    app.config['FOODS'] = ["Pizza", "Sushi", "Burger", "Pasta", "Tacos", "Ice Cream"]
    app.config['COUNTRIES'] = ["Japan", "Italy", "France", "Brazil", "Canada", "Australia"]
    app.config['MOVIES'] = ["Inception", "The Matrix", "Interstellar", "Avatar", "The Dark Knight"]
    app.config['ANIMALS'] = ["Tiger", "Elephant", "Penguin", "Dolphin", "Lion", "Panda"]

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/get_random/<int:choice>')
    def get_random(choice):
        if choice == 1:
            result = random.choice(app.config['COLORS'])
        elif choice == 2:
            result = random.choice(app.config['FOODS'])
        elif choice == 3:
            result = random.choice(app.config['COUNTRIES'])
        elif choice == 4:
            result = random.choice(app.config['MOVIES'])
        elif choice == 5:
            result = random.choice(app.config['ANIMALS'])
        else:
            return jsonify({"error": "Invalid choice"})
        
        message = f'Hurray! You got {result}. Explore more at <a href="https://speakingcharacter.ai/" target="_blank">https://speakingcharacter.ai/</a>'
        return jsonify({"result": result, "message": message})

    return app

def run_app(host='0.0.0.0', port=8080):
    app = create_app()
    app.run(host=host, port=port)

if __name__ == '__main__':
    run_app() 