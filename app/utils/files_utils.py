def allowed_file(filename, allowed_extensions):
    """ checks if a file extension is allowed """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
