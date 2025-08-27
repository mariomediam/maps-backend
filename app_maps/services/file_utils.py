from django.core.files.uploadedfile import UploadedFile

class FileUtils:
    def get_file_information(self, file: UploadedFile):

        file_size = file.size
        content_type = file.content_type
        file_name = file.name
        file_extension = file.name.split('.')[-1]

        return {
            'file_size': file_size,
            'content_type': content_type,
            'file_name': file_name,
            'file_extension': file_extension
        }
    
    