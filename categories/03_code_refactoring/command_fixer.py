#!/data/data/com.termux/files/usr/bin/python3
import sys

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    
    typo = sys.argv[1]
    
    # Read candidates from stdin
    candidates = set()
    for line in sys.stdin:
        cand = line.strip()
        if cand and cand != typo:
            candidates.add(cand)
            
    best_match = None
    best_dist = 999
    
    for cand in candidates:
        if abs(len(cand) - len(typo)) > 2:
            continue
        dist = levenshtein_distance(typo, cand)
        if dist < best_dist:
            best_dist = dist
            best_match = cand
            
    if best_match and best_dist <= 2:
        try:
            # Ask the user interactively on /dev/tty
            sys.stderr.write(f"\n\033[1;33mCommand '{typo}' not found. Did you mean '{best_match}'? [Y/n]: \033[0m")
            sys.stderr.flush()
            
            with open('/dev/tty', 'r') as tty:
                choice = tty.readline().strip().lower()
                
            if choice in ('', 'y', 'yes'):
                # Print command to stdout for evaluation
                print(best_match)
                sys.exit(0)
        except Exception:
            pass
            
    sys.exit(1)

if __name__ == '__main__':
    main()
