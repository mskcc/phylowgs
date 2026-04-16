import phylowgs_mh

node = phylowgs_mh.Node()
node.id = 1
node.pi = [0.1, 0.9]
node.cids = [2, 3]

print(f"Node created: ID={node.id}, PI={node.pi}, CIDS={node.cids}")

datum = phylowgs_mh.Datum()
datum.id = 101
datum.a = [10, 20]
datum.d = [100, 200]

print(f"Datum created: ID={datum.id}, A={datum.a}, D={datum.d}")
