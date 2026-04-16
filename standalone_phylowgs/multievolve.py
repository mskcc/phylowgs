print("Starting multievolve worker...")
import argparse
import multiprocessing
import phylowgs_mh
from data_loader import load_ssm_data

def run_chain(chain_id, args, data):
    nodes = [] # Logic to initialize nodes from params
    # ...
    ratio = phylowgs_mh.run_mh_loop(nodes, data, args.mh_iterations, 0.1)
    print(f"Processing data for chain {chain_id}"); print(f"Chain {chain_id} complete. Acceptance ratio: {ratio}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-chains", type=int, default=4)
    parser.add_argument("--gpu", action="store_true"); parser.add_argument("--mh-iterations", type=int, default=1000)
    parser.add_argument("--ssms", required=True)
    args = parser.parse_args()

    data = load_ssm_data(args.ssms)
    
    pool = multiprocessing.Pool(processes=args.num_chains)
    for i in range(args.num_chains):
        pool.apply_async(run_chain, (i, args, data))
    
    pool.close()
    pool.join()
