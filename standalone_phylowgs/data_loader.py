print("Starting data load...")
import phylowgs_mh

def load_ssm_data(filename):
    data = []
    with open(filename, 'r') as f:
        header = f.readline()
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 3: continue
            datum = phylowgs_mh.Datum()
            # Map id string 'sN' to integer N
            datum.id = int(parts[0][1:])
            # SSM format: a is comma-sep at col 2, d is comma-sep at col 3
            datum.a = [int(p) for p in parts[2].split(',')]
            datum.d = [int(p) for p in parts[3].split(',')]
            data.append(datum)
    return data
