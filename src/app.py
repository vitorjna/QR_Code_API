import io
import segno
from flask import Flask, request, send_file
import re

error_correction_levels = [ 'l', 'm', 'q', 'h' ]
file_formats = [ 'SVG', 'PNG' ]
mimetype_map = {
    'PNG': 'image/png',
    'SVG': 'image/svg+xml',
}

app = Flask(__name__)

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    data = request.args.get('data')
    if not data:
        return "Please provide 'data' as a query parameter.", 400

    try:
        # Optional parameters
        box_size = request.args.get('size', 10, type=int) # Default size 10
        qr_error_correction = request.args.get('ecc', error_correction_levels[0]).lower() # Default L
        output_format = request.args.get('format', file_formats[0]).upper() # Default SVG
        margin = request.args.get('margin', 4, type=int) # Default margin 4 pixels

        if qr_error_correction not in error_correction_levels:
            return f"Invalid ECC level. Supported levels: {error_correction_levels}", 400

        if output_format not in file_formats:
            return f"Invalid output format. Supported formats: {file_formats}", 400


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
                        omitsize=False)

        else:
            qrcode.save(buf,
                        kind=output_format.lower(),
                        scale=box_size,
                        border=margin)

        buf.seek(0)

        extension = output_format.lower()
        return send_file(buf, mimetype=mimetype_map.get(output_format, 'application/octet-stream'), download_name=f"qr_code.{extension}")

    except Exception as e:
        return f"Error generating QR code: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, ssl_context='adhoc')
