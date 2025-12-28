import os
import secrets
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

def service_info() -> dict:
    # Cloud Run injects these at runtime; locally they may be missing.
    return {
        "service": os.environ.get("K_SERVICE", "local"),
        "revision": os.environ.get("K_REVISION", "local"),
        "project": os.environ.get("GOOGLE_CLOUD_PROJECT", "local"),
        "region": os.environ.get("REGION", "unknown"),
    }

@app.get("/")
def index():
    name = os.environ.get("NAME", "YOUR_NAME")
    info = service_info()

    return f"""
    <html>
      <head>
        <title>Cloud Run Campus Coupon</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body style="font-family: sans-serif; max-width: 760px; margin: 40px auto; padding: 0 16px;">
        <h1>✅ Hello, {name}!</h1>
        <p>Your Flask app is running on <b>Cloud Run</b>.</p>

        <h3>Service Info</h3>
        <ul>
          <li><b>Service</b>: {info["service"]}</li>
          <li><b>Revision</b>: {info["revision"]}</li>
          <li><b>Project</b>: {info["project"]}</li>
          <li><b>Region</b>: {info["region"]}</li>
        </ul>

        <h3>Try the protected endpoint</h3>
        <p><code>GET /api/coupon</code></p>
        <p>Requires header: <code>X-API-KEY: &lt;your secret&gt;</code></p>

        <h3>Health</h3>
        <p><a href="/healthz">/healthz</a></p>
      </body>
    </html>
    """, 200

@app.get("/healthz")
def healthz():
    return "ok", 200

@app.get("/api/coupon")
def coupon():
    expected_key = os.environ.get("API_KEY")  # injected from Secret Manager via Cloud Run
    if not expected_key:
        return jsonify(
            error="API_KEY not configured.",
            hint="Attach Secret Manager secret to Cloud Run as env var API_KEY.",
        ), 503

    got_key = request.headers.get("X-API-KEY", "")
    if got_key != expected_key:
        return jsonify(error="Unauthorized. Provide correct X-API-KEY header."), 401

    prefix = os.environ.get("COUPON_PREFIX", "GDSC")
    ttl = int(os.environ.get("COUPON_TTL_SECONDS", "300"))

    code = f"{prefix}-{secrets.token_hex(2).upper()}"  # e.g., GDSC-3FA9
    return jsonify(
        coupon=code,
        expires_in=ttl,
        issued_at=int(time.time()),
        **service_info()
    ), 200

if __name__ == "__main__":
    # Cloud Run listens on PORT; locally default to 8080.
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
