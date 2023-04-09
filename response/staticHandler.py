import os
from pathlib import Path

from response.requestHandler import RequestHandler

class StaticHandler(RequestHandler):
    def __init__(self, static_path):
        self.filetypes = {
            ".js" : "text/javascript",
            ".css" : "text/css",
            ".jpg" : "image/jpeg",
            ".png" : "image/png",
            ".html": "text/html",
            "notfound" : "text/plain"
        }
        self.static_path = static_path

    def find(self, file_path):
        # TODO: Security Validate Extension Requested
        # TODO: Don't allow symlinks
        split_path = os.path.splitext(file_path)
        extension = split_path[1]
        
        try:
            file_path = str(Path("{static_path:s}{file_path:s}".format(static_path = self.static_path, file_path = file_path)).resolve())

            if self.isPathTraversal(file_path, self.static_path):
                raise Exception("Path Traversal")
                        
            
            if extension in (".jpg", ".jpeg", ".png"):
                self.contents = open(file_path, 'rb')
            else:
                self.contents = open(file_path, 'r')
            
            self.setContentType(extension)
            self.setStatus(200)
            return True
        except Exception as e:
            print(e)
            self.setContentType('notfound')
            self.setStatus(404)
            return False

    def setContentType(self, ext):
        self.contentType = self.filetypes[ext]
    
    '''
    Check if an attacker is trying to traverse out of the directory path
    '''
    def isPathTraversal(self, path: str, directory: str):
        subPath = Path(path).resolve()
        dirPath = Path(directory).resolve()
        
        try:
            subPath.relative_to(str(dirPath))
            return False
        except:
            return True