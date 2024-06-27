import Pyro5.server
import Pyro5.core
from moku.instruments import MultiInstrument

MIM = MultiInstrument('192.168.50.57', force_connect=True, platform_id=4) #192.168.50.57 Moku pro 3

daemon = Pyro5.server.Daemon(host="localhost")
ns = Pyro5.core.locate_ns()
uri = daemon.register(MIM)
ns.register("MokuMIM",uri)
daemon.requestLoop()