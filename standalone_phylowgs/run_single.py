import sys
sys.path.insert(0, '.')
import phylowgs_mh
from data_loader import load_ssm_data

data = load_ssm_data('/Users/kumarn1/work/neoantigen/phylowgs/.sbx/gemini-phylowgs-worktrees/optimization/ssm_data.txt')
nodes = [] # initialize empty for now
print(f"Running MH on {len(data)} items...")
ratio = phylowgs_mh.run_mh_loop(nodes, data, 500, 0.1)
print(f"Complete. Ratio: {ratio}")
