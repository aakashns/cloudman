import fire
from cloudman.utils.gcloud import install_gcloud, open_console


class Install(object):
    """Install cloud platform (AWS/GCP/Azure) specific SDKs and tools"""

    def __init__(self):
        self.gcloud = install_gcloud


class CLI(object):
    def __init__(self):
        self.install = Install()

    def console(self, project=''):
        open_console(project)


def main():
    print('')
    fire.Fire(CLI)


if __name__ == '__main__':
    main()
