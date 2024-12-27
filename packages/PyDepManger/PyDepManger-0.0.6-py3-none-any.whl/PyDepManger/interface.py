import subprocess

class Manger:
    def blueprint(app):
        subprocess.run(["./PyDepManger/bash/blueprint.sh", app])
        
    def java():
        app = "java"
        Manger.blueprint(app)
    
    def python():
        app = "py"
        Manger.blueprint(app)
        
    def data():
        import numpy
        import pandas
        import scipy
        subprocess.run(["./PyDepManger/bash/pacs.sh"])
        

    
    


