import Pyro5.client
MIM = Pyro5.client.Proxy("PYRONAME:MokuMIM")
print(MIM.get_connections()) 