from litter.uploader.base import Uploader


class LitterboxUploader(Uploader):
    def __init__(self, filename, time):
        self.filename = filename
        self.file_host_url = "https://litterbox.catbox.moe/resources/internals/api.php"
        self.time = time

    def execute(self):
        file = open(self.filename, "rb")
        try:
            data = {
                "reqtype": "fileupload",
                "time": self.time,
                "fileToUpload": (file.name, file, self._mimetype()),
            }
            response = self._multipart_post(data)
        finally:
            file.close()

        return response.text
