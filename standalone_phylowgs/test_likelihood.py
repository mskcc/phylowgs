import phylowgs_mh

data = []
d1 = phylowgs_mh.Datum()
d1.id = 1
d1.a = [10]
d1.d = [100]
data.append(d1)

nodes = []
n1 = phylowgs_mh.Node()
n1.id = 1
nodes.append(n1)

llh = phylowgs_mh.compute_likelihood(nodes, data)
print(f"Computed likelihood: {llh}")
