import phylowgs_mh
import numpy as np

def run_mcmc(iters=1000, std=0.5):
    print("Starting accelerated MCMC...")
    acceptance_ratio = phylowgs_mh.metropolis_loop(iters, std, 1, 1, 1)
    print(f"MCMC complete. Acceptance ratio: {acceptance_ratio}")

if __name__ == "__main__":
    run_mcmc()
