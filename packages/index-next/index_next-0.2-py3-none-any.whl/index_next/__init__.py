import os
import fcntl


def get_next_index(used_indices_file="used_indices.txt"):
    if not os.path.exists(used_indices_file):
        with open(used_indices_file, "a") as f:
            pass

    with open(used_indices_file, "r+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)

        indices = []
        for line in f.readlines():
            try:
                indices.append(int(line.strip()))
            except:
                continue

        next_index = 0
        while next_index in indices:
            next_index += 1
        f.write(str(next_index) + "\n")

    return next_index
