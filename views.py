import os
# os.environ["DISPLAY"]=":5"
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from subprocess import call, Popen
# import os
# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '/media/ab/Projects/OpenShift/scad2PNG/scad2PNG/static'
app.config['DESIGNS_FOLDER'] = '/media/ab/Projects/OpenShift/scad2PNG/scad2PNG/static/design'
app.config['PNG_FOLDER'] = '/media/ab/Projects/OpenShift/scad2PNG/scad2PNG/static/png'
# app.config['UPLOAD_FOLDER'] = '/var/www/scad2PNG/scad2PNG/static/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'scad', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation

@app.route('/<design>')
def index(design):
    return render_template( design + '.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
    # Get the name of the uploaded file
        # file = request.files['file']
        design = request.form['design']
        print design
        # print len(request.form)
        var = ["custom_text_1=\""+request.form.get('custom_text_1',"")+"\"",
                "custom_text_2=\""+request.form.get('custom_text_2',"")+"\"",
                "custom_text_3=\""+request.form.get('custom_text_3',"")+"\"",
                "custom_text_4=\""+request.form.get('custom_text_4',"")+"\""]

        print var
        png_name = design+"_"+ request.form.get('custom_text_1',"")+"_"+request.form.get('custom_text_2',"") + ".png"
        print png_name
        # openscad --render --projection=p --camera=0,0,0,55,0,25,200 --imgsize=1000,1000  -o "test2.png" 8bit_msgKeychain.scad
        if design == "8bits":
            design_file = os.path.join(app.config['DESIGNS_FOLDER'], "8bits.scad")
        elif design == "keytag1":
            design_file = os.path.join(app.config['DESIGNS_FOLDER'], "keytag1.scad")
        elif design == "wordsclp":
            design_file = os.path.join(app.config['DESIGNS_FOLDER'], "wordsclp.scad")
        elif design == "VA_1":
            design_file = os.path.join(app.config['DESIGNS_FOLDER'], "VA_1.scad")
        elif design == "CT_1":
            design_file = os.path.join(app.config['DESIGNS_FOLDER'], "CT_1.scad")

        camera_settings = "--camera=0,0,0,55,0,25,400"
        stlcmd = ["openscad","--render","--projection=p","--imgsize=1000,1000",camera_settings,"-o",os.path.join(app.config['PNG_FOLDER'], png_name),design_file]

            # stlcmd = ["openscad","-o",os.path.join(app.config['UPLOAD_FOLDER'], png_name),os.path.join(app.config['UPLOAD_FOLDER'], filename)]
            # var = ['font_size = 1' , 'message = "ash"']
        Dargs = []
        for i in var:
            Dargs.append("-D")
            Dargs.append(str(i))
            print Dargs
        stlout =  stlcmd + Dargs
        print stlout
        Popen(stlout)
                # Redirect the user to the uploaded_file route, which
                # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=os.path.splitext(png_name)[0]))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('preview.html',filename=filename)

@app.route('/stl/<filename>')
def stl_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )
