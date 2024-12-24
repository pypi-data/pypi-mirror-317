import typer
from rich import print

app = typer.Typer()

@app.callback()
def callback():
    """
    Jay's Portal Gun CLI
    """
    
@app.command('shoot')
def shoot_gun():
    """
    Shoot the portal gun
    """
    print("Shooting the portal gun")

@app.command("load")
def load_gun():
    """
    Load the portal gun
    """
    print("Loading the portal gun")
    