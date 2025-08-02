from flask import Flask, render_template, request, redirect
import datetime

app = Flask(__name__)

# Simple in-memory storage
tickets = []
categories = ["General", "Technical", "Billing"]

@app.route('/')
def home():
    return render_template('index.html', tickets=tickets)

@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if request.method == 'POST':
        ticket = {
            "id": len(tickets) + 1,
            "subject": request.form['subject'],
            "description": request.form['description'],
            "category": request.form['category'],
            "status": "Open",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        tickets.append(ticket)
        return redirect('/')
    return render_template('create_ticket.html', categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
