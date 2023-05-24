'''
It is an API that allows you to create a file with the extension txt, to read the content of the created file, to modify the content and delete this file.
Source who helped me to do it : https://www.geeksforgeeks.org/python-introduction-to-web-development-using-flask/ and also the application Postman disponible on https://www.postman.com/qingshenhuihiu/workspace/jupyter-notebook/overview
https://blog.finxter.com/how-to-convert-json-to-pandas-dataframe/
https://moncoachdata.com/blog/filtrer-un-dataframe-pandas/
https://www.toppr.com/guides/python-guide/references/methods-and-functions/csv/python-csv-read-and-write-csv-files/#:~:text=The%20writerows()%20method%20is,be%20written%20using%20this%20method.
https://www.pythontutorial.net/python-basics/python-read-csv-file/
https://pythonacademy.com.br/blog/importar-csv-no-pandas
https://pythonacademy.com.br/blog/series-no-pandas
https://pythonacademy.com.br/blog/dataframes-do-pandas
https://www.youtube.com/watch?v=P4NedNx-Nc0
https://www.hashtagtreinamentos.com/try-e-except-no-python?gad=1&gclid=CjwKCAjw36GjBhAkEiwAKwIWyc8Oy8-dJ86-wgXkcSkd_IYV607JwihNlm4e40wpMyiHn37g3pTPmhoCcDoQAvD_BwE
https://towardsdatascience.com/how-to-convert-json-into-a-pandas-dataframe-100b2ae1e0d8
https://www.geeksforgeeks.org/how-to-disable-python-warnings/
https://rollbar.com/blog/python-valueerror/
https://www.geeksforgeeks.org/how-to-append-a-new-row-to-an-existing-csv-file/
https://www.geeksforgeeks.org/python-os-path-exists-method/
'''
from flask import Flask, request, jsonify
import os
import pandas as pd
import csv as csv
from csv import writer, DictWriter

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


#Requisição para criar um arquivo csv
@app.route('/create_file_csv', methods = ['POST'])
    
def createfilecsv():
    '''
    The createfilecsv function is responsible for receiving the contents of the columns and rows of a csv file.
    Args : filename : is the name the file  
           columns : is the name of each columns
           dataset : is the content of each row according to the columns
           film_list : it's the DataFrame (it's just the materialization of your file with its content)
           return the file csv created
    ''' 
    file_name = request.json.get('file_name')
    response = {}

    if os.path.exists(file_name):
        response['Notification'] = 'You can_t editate the  file anymore ;( '

    else:
        columns = request.json['columns']
        dataset = request.json['dataset']
        film_list = pd.DataFrame(dataset, columns=columns)
        film_list.to_csv(file_name, index=False, header=True)
        response['Notification'] = f'Your movie list has been successfully created as {file_name}'
        

    
    return jsonify(response)


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


#Requisição para ler um arquivo csv
@app.route('/read_file_csv', methods = ['GET'])

def readfilecsv():
    '''
    The readfilecsv function is responsible for reading the csv file.
    Args : filename : is the name the file  
           return the file csv created in reading mode
    ''' 

    file_name = request.json.get('file_name')
    response = {}

    try:
               reader = pd.read_csv(file_name)
               reader_return = reader.to_json()
               response['Notification'] = reader_return

    except:
        response['Notification'] = 'You should tcheck the name of your file :( !'
    
    return jsonify(response)


#Requisição para editar um .txt já existente
@app.route('/editar_file', methods = ['PUT'])

def editfile():
    '''
    The editfile function is responsible to editate the file like add new text
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


# Requisição para editar um arquivo .csv jà existente
@app.route('/edit_file_csv', methods = ['PUT'])

def editfilecsv():
    '''
    The editfilecsv function is responsible to editate the file like add new line(s) (row(s))
    Args : filename : is the name the file  
    columns: must contain the name of each columns (must be the same as created)
    value_add : must contain the values of the row(s).
    return the editate
    '''

    file_name = request.json.get('file_name')
    columns = request.json.get('columns')
    value_add = request.json.get('value_add')
    response = {}

    try:
                
        with open(file_name, 'a+', newline = '') as file:
            new_filecsv = DictWriter(file, fieldnames = columns)
            new_filecsv.writerow(value_add[0])
            #new_content = pd.read_csv(file_name)
            #reader_return = new_content.to_json()
            response['Notification'] = 'New line added with success, good job, go to the previous section to see the update :) !'
            #response['Notification']= reader_return
            
            
    except:
        response['Notification'] = 'You should tcheck the name of your file :( !'

    return jsonify(response)


# Requisição para selecionar de uma linha até uma outro em um arquivo csv
@app.route('/read_select_line', methods = ['PUT'])

def readselectline():
    '''
    The readselectline function is responsible for selecting a line intervel in the file.
    Args :
        start_value : must be given a positive integer value desired,
        end_value : must be given a positive integer wanted,
        file_name: must receive the name of the file.
        return the range selected
    '''
    start_value = request.json.get('start_value')
    end_value = request.json.get('end_value')
    file_name = request.json.get('file_name')
    response = {}
    #lines = []
    
    try: 
            file_reader = pd.read_csv(file_name)
            #print(len(file_read))
            if end_value > len(file_reader):
                response['Notification'] = 'The end value is out of range'
            else : 
                file_read_line = file_reader.iloc[start_value-1 : end_value]
                lines = file_read_line.to_json()
                #print((lines))
                response['Notification'] = lines

    except:
        response['Notification'] = 'You should tcheck the name of your file :( !'

    return jsonify(response)


#Requisição para filtrar
@app.route('/select_range', methods = ['PUT'])

def selectrange():

    '''
    The selectrange function is responsible for selecting a line intervel in the file.
    Args :
        file_name: must receive the name of the file.
        value_x : (int) must be a positive integer value desired
        columns_numeric : (str) is the name of the column where the filter must be applied ()
        return the file csv with value < to value_x
    '''

    file_name = request.json.get('file_name')
    value_x = request.json.get('value_x')
    columns_numeric = request.json.get('columns_numeric')
    response = {}
     
    try:  
        file_reader =pd.read_csv(file_name)
        filters = file_reader.loc[file_reader[columns_numeric] < value_x]
        print(type(filters))
        lines = filters.to_json()
        response['Notification'] = lines

    except:
        response['Notification'] = 'You should tcheck the name of your file or tcheck if you pass the correct column numeric name'

    return jsonify(response)


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


