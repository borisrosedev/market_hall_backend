
from functools import wraps
import uuid
from datetime import datetime as dt
from pathlib import Path 
from werkzeug.utils import secure_filename
import os
import re
from flask import request, jsonify

def test_info_request(request):
    print("\n" + "="*50)
    print("DEBUG REQUEST INFO")
    print("="*50)
    print(f"🔍 Méthode: {request.method}")
    print(f"🔍 URL: {request.url}")
    print(f"🔍 Path: {request.path}")
    print(f"🔍 Content-Type: {request.content_type}")
    print(f"🔍 Content-Length: {request.content_length}")
    
    print("\n--- HEADERS ---")
    for header, value in request.headers:
        print(f"📋 {header}: {value}")
    
    print("\n--- FILES ---")
    print(f"📁 Nombre de fichiers: {len(request.files)}")
    if request.files:
        for key, file in request.files.items():
            print(f"📎 Clé: '{key}' -> Fichier: '{file.filename}' (type: {type(file)})")
            if file.filename:
                print(f"   📏 Taille estimée: {len(file.read())} bytes")
                file.seek(0)  # Reset le curseur après lecture
    else:
        print("❌ Aucun fichier dans request.files")
    
    print("\n--- FORM DATA ---")
    if request.form:
        for key, value in request.form.items():
            print(f"📝 Form '{key}': {value}")
    else:
        print("❌ Aucune donnée form")
    
    print("\n--- QUERY PARAMS ---")
    if request.args:
        for key, value in request.args.items():
            print(f"🔗 Query '{key}': {value}")
    else:
        print("❌ Aucun paramètre query")
    
    print("="*50)