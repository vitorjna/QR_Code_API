import io
import qrcode
import qrcode.image.svg
from flask import Flask, request, send_file

# Map error correction levels
error_correction_map = {
    'L': qrcode.constants.ERROR_CORRECT_L,
    'M': qrcode.constants.ERROR_CORRECT_M,
    'Q': qrcode.constants.ERROR_CORRECT_Q,
    'H': qrcode.constants.ERROR_CORRECT_H,
}

mimetype_map = {
    'PNG': 'image/png',
    'JPEG': 'image/jpeg',
    'BMP': 'image/bmp',
    'GIF': 'image/gif',
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
        error_correction_level = request.args.get('ecc', 'L').upper() # Default L
        output_format = request.args.get('format', 'SVG').upper() # Default SVG
        margin = request.args.get('margin', 4, type=int) # Default margin 4 pixels

        qr_error_correction = error_correction_map.get(error_correction_level, qrcode.constants.ERROR_CORRECT_L)

        # Validate output format
        if output_format not in ['PNG', 'JPEG', 'BMP', 'GIF', 'SVG']:
            return "Invalid output format. Supported formats: PNG, SVG, JPEG, BMP, GIF.", 400

        qr = qrcode.QRCode(
            version=None,
            error_correction=qr_error_correction,
            box_size=box_size,
            border=margin
        )
        qr.add_data(data)
        qr.make(fit=True)

        if output_format == "SVG":
            img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage,
                                fill_color="pink",
                                back_color="white")
            buf = io.BytesIO(img.to_string())
            buf.seek(0)
        
        else:
            img = qr.make_image(fill_color="black", back_color="white")
            buf = io.BytesIO()
            img.save(buf, format=output_format)
            buf.seek(0)
        
        extension = output_format.lower()
        return send_file(buf, mimetype=mimetype_map.get(output_format, 'application/octet-stream'), download_name=f"qr_code.{extension}")

    except Exception as e:
        return f"Error generating QR code: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, ssl_context='adhoc')