# localOnlineDisk

Aplikacja, za pomocą której użytkownik może zarządzać zawartością dysku komputerowego z poziomu strony internetowej. Główne funkcjonalności:

- przesyłanie plików na dysk
- pobieranie plików z dysku
- usuwanie plików z dysku
- tworzenie struktury katalogów (dodawanie/usuwanie katalogów)
- wyświetlanie danych o plikach (rozmiar, data dodania, itp.)
- udostępnianie plików w postaci linków do pobrania
- możliwość współdzielenia zasobów pomiędzy użytkownikami, dodanymi do znajomych
- szyfrowanie zawartości dysku lub pojedynczego pliku
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
           * to_user - other user ID
           * created - date
    * friendsList/
      * GET - get a list of friends of the current user
    * removefriend/
      * POST - removes friend from friends list  
        Params:
          * from_user - other user ID
          * created - date
    * acceptRequest/
      * POST - accepts request from user
        Params:
          * from_user - other user ID
          * created - data
     * rejectRequest/
       * POST - rejects request from user
         Params:
          * from_user - other user ID
          * created - data
     * unreadRequestList/
       * GET - get a list of unread requests sent to current user
     * unrejectedRequestList/
       * GET - get a list of unrejected requests sent to current user
     * rejectedRequestList/
       * GET - get a list of rejected requests sent to current user
     * stats/?dir={path}
       * GET - get download statistics for selected directory (it has to start with '/')  
               response objects with count = -1 indicate directories  
               if query parameter 'dir' id not present, get statistics for root folder  
               Example:  
               
               /api/v1/users/stats/?dir=/test/a # get download statistics for the content of /test/a 
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
        * is_public - if file/directory should be public (accessible by non logged in users)
        * shared_with - list of users (friends) which should have access to the resource
  * share/{uuid}
    * GET - download or list shared resource indicated by {uuid}
    * DELETE - unshare a resource
  * share/{uuid}/{path} - {uuid} should be a directory
    * GET - download or list shared resource indicated by {path} inside {uuid}
  * share/my/
    * GET - list all files and directories shared by me
  * encrypt/{path}
    * POST - encrypt or decrypt a file; new file will have the suffix '~encrypted' added, this way 
    it can be distinguished between encrypted and unencrypted files (the old file will be deleted)  
      Params:
        * password - passwod used for encryption/decryption
        * decrypt - optional parameter; when used the file wile be decrypted
        (value of parameter is not important); when absent file will be encrypted
