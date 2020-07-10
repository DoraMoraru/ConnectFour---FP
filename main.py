from repos import Repo
from service import Service
from ui import UI
from valid import Valid

v = Valid()
r = Repo()
s = Service(r)
ui = UI(s)
ui.run()