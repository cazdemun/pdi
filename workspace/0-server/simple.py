from flask import Flask, make_response, render_template, Response, url_for, jsonify
app = Flask(__name__)

@app.route('/')
def simple():
    print("HOLA COMO ESTAS ADSFASDFAS")
    import cv2
    import base64
    img = cv2.imread('../Aviones.jpg')
    im = cv2.imread('../bird.png')
    ret, jpeg = cv2.imencode('.jpg', img)
    ret1, jpeg1 = cv2.imencode('.png', im)
    img_list = []
    img_list.append(jpeg.tobytes())
    img_list.append(jpeg1.tobytes())
    
    retval, buffer = cv2.imencode('.png', im)
    response = make_response(buffer.tobytes())

    #response.headers['Content-Type'] = 'image/png'
    return response
    
@app.route('/gallery')
def get_gallery():
    import cv2
    im_names = []
    img = cv2.imread('../Aviones.jpg')
    im = cv2.imread('../bird.png')
    ret, jpeg = cv2.imencode('.jpg', img)
    ret1, jpeg1 = cv2.imencode('.png', im)
    print(im_names)
    im_names.append(jpeg.tobytes())
    im_names.append(jpeg1.tobytes())
    return render_template("gallery.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)