import eel
import shell

shell.load()
eel.init(shell.getCorePath() + 'web')
shell.afterload()

@eel.expose
def listen():
    text = shell.listen()
    eel.end_listen(text)()
    shell.proccess(text)

eel.start('index.html', size=(400, 400))
