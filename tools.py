def get_time(city):
    import datetime
    return f"The time in {city} is {datetime.datetime.now()}"

def create_file(file_name,file_type):
    with open(f"{file_name}.{file_type}","w")as f:
        f.write("new file")
    return "The file has been created"
def read_file(file_name,file_type):
    with open(f"{file_name}.{file_type}","r")as f:
        content=f.read()
        return content
def edit_file(file_name,file_type,content):
    with open(f"{file_name}.{file_type}","w")as f:
        f.write(content)
        return "The file has been edited"
def delete_file(file_name,file_type):
    import os
    os.remove(f"{file_name}.{file_type}")
