import typer
from typing import List
from .hikDriver import hikDriver

app = typer.Typer()

def main():
    app()




@app.command()
def reboot(ip_list: List[str], password: str):
    ''' 批量重启指定IP设备
    :param ip_list:
    :param password:
    :return:
    '''
    for ip in ip_list:
        device = hikDriver(ip=ip, password=password)
        device.device_reboot()


@app.command()
def get_info(ip_list: List[str], password: str):
    for ip in ip_list:
        device = hikDriver(ip=ip, password=password)
        temp_info = device.get_device_info()
        typer.echo(temp_info)


if __name__ == '__main__':
    main()

