# localOnlineDisk

Aplikacja, za pomoc¹ której u¿ytkownik mo¿e zarz¹dzaæ zawartoœci¹ dysku komputerowego z poziomu strony internetowej. G³ówne funkcjonalnoœci:

- przesy³anie plików na dysk
- pobieranie plików z dysku
- usuwanie plików z dysku
- tworzenie struktury katalogów (dodawanie/usuwanie katalogów)
- wyœwietlanie danych o plikach (rozmiar, data dodania, itp.)
- udostêpnianie plików w postaci linków do pobrania
- mo¿liwoœæ wspó³dzielenia zasobów pomiêdzy u¿ytkownikami, dodanymi do znajomych
- szyfrowanie zawartoœci dysku lub pojedynczego pliku
- wznowienie pobierania plików w przypadku przerwania pobierania
- statystyki pobierania

### 1. Installation
#### 1.1 Prerequisites
Python 3 with pip has to be installed and visible in the command line. 
#### 1.2 Setup
- Download or clone this repository.  
- Run setup.bat from the command line.

### 2. Usage
To start the web server simply run setup.bat again or type:  
`cd drf # change directory`  
`manage.py runserver # run server`

### 3. Files
Files are stored inside the project directory in a folder called Storage.
Each new user gets his own directory inside it named after his username.
### 4. API reference
* api/v1/
  * users/
    * list/
      * GET - get list of all users
    * send/
      * POST - send friendship request to another user  
        Params:
          * to_other - user id
    * friendslist/
      * GET - get a list of friends of the current user
    * removefriend/
      * POST - remove friend from friends list  
        Params:
          * to_other - user id
  * rest-auth/  
    * https://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html
  * files/
    * GET - get a list of files in the root directory for the current user  
    * POST - upload a file to the root directory  
      Params:
        * f - file
  * files/{path}
    * GET - download the file or list the directory indicated by {path} 
    * POST - upload a file to the directory indicated by {path}  
      Params:
        * f - file  
      If no params given, create directory {path}
    * DELETE - delete file or directory {path}
  * share/
    * GET - get all files and directories shared with current user  
    * POST - share a file or directory  
      Params:
        * path - path to file/directory
        * is_public - if file/directory should be public (accesible by non logged in users)
        * shared_with - list of users (friends) which should have access to the resource
  * share/{uuid}
    * GET - download or list shared resource indicated by {uuid}
    * DELETE - unshare a resource
  * share/{uuid}/{path} - {uuid} should be a directory
    * GET - download or list shared resource indicated by {path} inside {uuid}
    * POST - not working yet
    * DELETE - not working yet
  * share/my/
    * GET - list all files and directories shared by me