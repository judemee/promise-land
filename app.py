from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# -----------------------------
# EMAIL CONFIGURATION
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'j.uzowulu@gmail.com'  # replace with your Gmail
app.config['MAIL_PASSWORD'] = 'wsvw oxws syxd qbuq'     # use an app password (see below)
app.config['MAIL_DEFAULT_SENDER'] = ('OJ Evolves', 'your_email@gmail.com')

mail = Mail(app)

# -----------------------------
# ROUTES
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')

    print(f"New Order Received:\nName: {name}\nPhone: {phone}\nAddress: {address}\n")

    # Send email notification
    try:
        msg = Message(
            subject=f"New Order from {name}",
            recipients=['your_email@gmail.com'],  # change to where you want notifications
            body=f"""
New order received from your landing page:

Name: {name}
Phone: {phone}
Address: {address}

Check WhatsApp for quick response.
"""
        )
        mail.send(msg)
        print("✅ Order email sent successfully.")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

    return redirect(url_for('thankyou', name=name))

@app.route('/thank-you')
def thankyou():
    name = request.args.get('name', 'Customer')
    return render_template('thankyou.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
