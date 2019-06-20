import fire
from cloudman import gcp


class CLI(object):
    def __init__(self):
        self.install = gcp.install_gcloud

    def console(self, project=''):
        gcp.open_console(project)

    def create(self, name, disk='50GB'):
        gcp.create(name, disk)

    def delete(self, name):
        gcp.delete(name)

    def list(self):
        gcp.list_disks()

    def start(self, name, gpu='nogpu', machine='auto', spot=True):
        gcp.start(name, gpu, machine, spot)

    def stop(self, name):
        gcp.stop(name)

    def ssh(self, name):
        gcp.ssh(name)

    def jupyter(self, name):
        gcp.launch_jupyter(name)


def main():
    print('')
    fire.Fire(CLI)


if __name__ == '__main__':
    main()
