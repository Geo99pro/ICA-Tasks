'''
It is an API that allows you to create a file with the extension txt, to read the content of the created file and to modify the content of this file.
Source who helped me to do it : https://www.geeksforgeeks.org/python-introduction-to-web-development-using-flask/ and also the application Postman disponible on https://www.postman.com/qingshenhuihiu/workspace/jupyter-notebook/overview
'''
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

#Requisição para criar um arquivo txt
@app.route('/create_file',  methods = ['POST'])

def createfile():
    '''
    The createfile function is responsible for receiving the file creation request from any client. 
    Args : filename : is the name the file  
           content_of_the_file : is  the content of the file (Ex : My name is Loïck)
    ''' 
    file_name = request.json.get("file_name")
    content_of_the_file= request.json.get("content_of_the_file")

    with open(file_name+'.txt', "w") as file:
        file.write(content_of_the_file)
    return jsonify({'The name of your file is': file_name, 
                    'It contains the following text' : content_of_the_file})


#Requisição para ler um arquivo txt
@app.route('/read_file', methods = ['GET'])

def readfile():

    '''
    The readfile function is responsible to read the file and return the content of the file and his name. 
    Args : filename : is the name the file  
    '''
    file_name = request.json.get("file_name")

    with open(file_name+'.txt', 'r') as file:
        content_of_the_file = file.read()
    return jsonify({'This is the content of this file' : content_of_the_file,
                    'The name of the file you are reading is': file_name})


#Requisição para editar um .txt já existente
@app.route('/editar_file', methods = ['PUT'])

def editfile():
    '''
    The editfile function is responsible to read the file and return the new content of the file
    Args : filename : is the name the file  
    NB : the name of file should be the same as created, otherwise you should create one or verify correctly the name of the file. 
    '''

    file_name = request.json.get('file_name')
    content_of_the_file = request.json.get('content_of_the_file')

    if os.path.isfile(file_name):
        
        with open(file_name, 'a+') as file:
            file.write(content_of_the_file)
        return jsonify({'Notification': 'The file has been edited. Go to the section read to see your update ;)'})
    else : 
        return jsonify({'Notification': 'Please look correctly the name of the file or create one :('})

#Requisição para apagar un arquivo .txt já existente
@app.route('/delete_file', methods = ['DELETE'])


def deletefile():
    '''
    The deletefile function is responsible to delete the file and return one notification as like the file is deleted
    Args : filename : is the name the file  
    '''
    file_name = request.json.get('file_name')
    if os.path.isfile(file_name):
        os.remove(file_name)
        return jsonify({'Notification': 'File deleted with success'})
    else:
        return jsonify({'Notification': 'This file you are trying to delete does not exist. Verify the name and try it again or creat one.'})
        

if __name__ == '__main__': 
    app.run()


