from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

BREVO_API_KEY = os.getenv("BREVO_API_KEY")  # Set this in Railway
BREVO_SENDER = "yourname@yourdomain.com"    # Must be a verified sender in Brevo
BREVO_RECEIVER = "youremail@gmail.com"      # Where order notifications go


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')

    print(f"\n📦 New Order Received:\nName: {name}\nPhone: {phone}\nAddress: {address}\n")

    # --- Send email through Brevo API ---
    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "accept": "application/json",
                "api-key": BREVO_API_KEY,
                "content-type": "application/json"
            },
            json={
                "sender": {"name": "Promise Land Orders", "email": BREVO_SENDER},
                "to": [{"email": BREVO_RECEIVER}],
                "subject": f"New Order from {name}",
                "htmlContent": f"""
                    <h2>New Order Received</h2>
                    <p><b>Name:</b> {name}</p>
                    <p><b>Phone:</b> {phone}</p>
                    <p><b>Address:</b> {address}</p>
                """
            }
        )

        if response.status_code == 201:
            print("✅ Email sent successfully via Brevo.")
        else:
            print(f"⚠️ Brevo response: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

    return redirect(url_for('thankyou', name=name))


@app.route('/thankyou')
def thankyou():
    name = request.args.get('name', 'Customer')
    return render_template('thankyou.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
