from tempfile import NamedTemporaryFile

from webdav3.client import Client


class WebDav:
    def __init__(self, dav_options: dict) -> None:
        self.dav_options = dav_options
        self.client = Client(dav_options)

    def remove_if_exist(self, remote_path: str):
        exist: bool = self.client.check(remote_path)
        if exist:
            self.client.clean(remote_path)

    def get_txt_content(self, remote_path: str):
        with NamedTemporaryFile("wb+") as f:
            self.client.download_sync(remote_path, f.name)
            f.seek(0)
            txt = f.read().decode()
        return txt

    def upload_file(self, local_path: str, remote_path: str):
        self.remove_if_exist(remote_path)
        self.client.upload_sync(remote_path, local_path)

    def upload_txt(self, txt: str, remote_path: str):
        self.remove_if_exist(remote_path)
        with NamedTemporaryFile("wb+") as f:
            f.write(txt.encode())
            f.seek(0)
            self.client.upload_sync(remote_path, f.name)
