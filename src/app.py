import io
import os
import re
import segno
from dotenv import load_dotenv
from flask import Flask, request, send_file

error_correction_levels = [ 'l', 'm', 'q', 'h' ]
file_formats = [ 'SVG', 'PNG' ]
mimetype_map = {
    'PNG': 'image/png',
    'SVG': 'image/svg+xml',
}

HTML_START_ERROR = r"<p style='color:red;'>"
HTML_END_ERROR = r"</p>"

app = Flask(__name__)

generate_qr_help = """
<h3>Welcome to the QR Code API!</h3>
<p>To generate a QR code, send a GET request to the <code>/generate_qr</code> endpoint with the following parameters:</p>

<h4>Required:</h4>
<ul>
    <li><strong>data</strong>: The data to encode in the QR code (e.g., text, URL).</li>
</ul>

<h4>Optional:</h4>
<ul>
    <li><strong>size</strong>: The size of each box (pixel) in the QR code. Default is 10. (Type: integer)</li>
    <li><strong>ecc</strong>: Error Correction Level. Controls the amount of data that can be recovered if the QR code is damaged.
        <ul><li>Supported: l (Low), m (Medium), q (Quartile), h (High). Default is 'l'.</li></ul>
    </li>
    <li><strong>format</strong>: The output format of the QR code image.
        <ul><li>Supported: SVG, PNG. Default is 'SVG'.</li></ul>
    </li>
    <li><strong>margin</strong>: The quiet zone around the QR code in modules. Default is 4. (Type: integer)</li>
    <li><strong>color_qr</strong>: The color of the QR code modules. Default is black. (Type: string, e.g., 'red', 'FF0000', 'FF0000FF'). Note: The '#' symbol for hex codes must be omitted or URL-encoded as '%23'. Supports RRGGBBAA for transparency.</li>
    <li><strong>color_bg</strong>: The background color of the QR code. Default is white. (Type: string, e.g., 'blue', '0000FF', '0000FFFF'). Note: The '#' symbol for hex codes must be omitted or URL-encoded as '%23'. Supports RRGGBBAA for transparency.</li>
</ul>

<h4>Examples:</h4>
<ul>
    <li><code>/generate_qr?data=Hello%20World</code></li>
    <li><code>/generate_qr?data=https://example.com&size=20&ecc=h&format=PNG&margin=5</code></li>
    <li><code>/generate_qr?data=ColorExample&color_qr=blue&color_bg=yellow</code></li>
</ul>
"""

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    data = request.args.get('data')
    if not data:
        return f"{HTML_START_ERROR}Please provide 'data' as a query parameter.{HTML_END_ERROR}</br></br>" + generate_qr_help, 400

    try:
        # Optional parameters
        box_size = request.args.get('size', 10, type=int) # Default size 10
        qr_error_correction = request.args.get('ecc', error_correction_levels[0]).lower() # Default L
        output_format = request.args.get('format', file_formats[0]).upper() # Default SVG
        margin = request.args.get('margin', 4, type=int) # Default margin 4 pixels
        qr_color = request.args.get('color_qr', "#000000") # Default black
        qr_background = request.args.get('color_bg', "#FFFFFF") # Default white

        if qr_error_correction not in error_correction_levels:
            return f"{HTML_START_ERROR}Invalid ECC level. Supported levels: {error_correction_levels}{HTML_END_ERROR}</br></br>" + generate_qr_help, 400

        if output_format not in file_formats:
            return f"{HTML_START_ERROR}Invalid output format. Supported formats: {file_formats}{HTML_END_ERROR}</br></br>" + generate_qr_help, 400


        buf = io.BytesIO()
        qrcode = segno.make(data, error=qr_error_correction, micro=False)

        if output_format == "SVG":
            qrcode.save(buf,
                        kind=output_format.lower(),
                        scale=box_size,
                        border=margin,
                        xmldecl=False,
                        svgclass=None,
                        lineclass=None,
                        omitsize=False,
                        light=qr_background,
                        dark=qr_color)

        else:
            qrcode.save(buf,
                        kind=output_format.lower(),
                        scale=box_size,
                        border=margin,
                        light=qr_background,
                        dark=qr_color)

        buf.seek(0)

        extension = output_format.lower()
        return send_file(buf, mimetype=mimetype_map.get(output_format, 'application/octet-stream'), download_name=f"qr_code.{extension}")

    except Exception as e:
        return f"Error generating QR code: {e}", 500

if __name__ == '__main__':
    load_dotenv()
    cert_path = os.getenv('CERT_PATH')
    key_path = os.getenv('KEY_PATH')

    if cert_path and key_path:
        app.run(host='0.0.0.0', port=7777, ssl_context=(cert_path, key_path))
    else:
        print("Warning: SSL certificate paths not found in .env. Running with adhoc SSL context.")
        app.run(host='0.0.0.0', port=7777, ssl_context='adhoc')
