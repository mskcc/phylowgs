import phylowgs_mh
from data_loader import load_ssm_data

# Use a dummy data file for testing
data = load_ssm_data('/Users/kumarn1/work/neoantigen/phylowgs/.sbx/gemini-phylowgs-worktrees/optimization/ssm_data.txt')
print("Testing CPU likelihood...")
cpu_llh = phylowgs_mh.compute_likelihood(data, False)
print(f"CPU LLH: {cpu_llh}")

print("Testing GPU likelihood...")
try:
    gpu_llh = phylowgs_mh.compute_likelihood(data, True)
    print(f"GPU LLH: {gpu_llh}")
except Exception as e:
    print(f"GPU failed: {e}")
