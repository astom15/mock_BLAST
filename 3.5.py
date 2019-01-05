#Finally, we will make it so that if a k-mer that is
#present in the database string is also in the query string
#in multiple locations, then a search should be made from each
#occurrence of the k-mer in the query string, spanning outward
#left and right of each occurrence. To do that use kmer4.py that
#is found under the Resources>Lab 3 (file kmer4.txt) to build up a
#list of all occurrences of each distinct k-mer in the query
#string, and use it to implement this change.
def readfile(string):
    with open(string) as o:
        lines = [line.rstrip() for line in o]
    return lines

def readfile2(sequence):
    with open(sequence) as o:
        seq = o.read().replace('\n','')
    return seq

def make_dict(q, s, k):
    kmer = {}
    db = {}
    for i in range(0, len(q) - k + 1):
        if q[i:i+k] not in kmer.keys():
            kmer[q[i:i+k]] = [i]
        else:
            kmer[q[i:i+k]].append(i)
    for j in range(0, len(s) - k + 1):
        if s[j:j+k] not in db.keys():
            db[s[j:j+k]] = [j]
        else:
            db[s[j:j+k]].append(j)
    return kmer, db

def find_HSPs(q, s, kmer, db, k):
    HSP = {}
    for i, j in enumerate(kmer):
        for m, n in enumerate(db):
            if j == n:
                for y in kmer[j]:
                    for z in db[n]:
                        left = check_left(q, s, y, z)
                        right = check_right(q, s, y, z, k)
                        if q[y - left: y + right + k + 1] == s[z-left: z + right + k + 1] and q[y - left: y + right + k + 1] not in HSP.keys():
                            HSP[q[y - left: y + right + k + 1]] = (y - left , y + right + k, z - left, z + right + k)
                        else:
                            continue
    return HSP

def check_left(sequence_entry, string_entry, i, j):
    L = 0
    try:
        while sequence_entry[i-1] == string_entry[j-1]:
            L += 1
            i -= 1
            j -= 1
    except IndexError:
        return L
    return L

def check_right(sequence_entry, string_entry, i, j, k):
    L = 0
    try:
        while sequence_entry[i + k + 1] == string_entry[j + k + 1]:
            L += 1
            i += 1
            j += 1
    except IndexError:
        return L
    return L

def return_threshold(hsps, L):
    longest = []
    for i, j in enumerate(hsps):
        longest.append(len(j))
    length = max(longest)
    for i, j in enumerate(hsps):
        if len(j) == length:
            print("The longest matching substring \'{}\' has length {}.".format(j, length))
            print("{}: {}".format(j, hsps[j]))


def main():
    string = 's.txt'
    sequence = 'q2.txt'
    q = readfile2(sequence)
    st = readfile2(string)
    k = int(input("Enter a k: "))
    L = int(input("Enter a threshold L: "))
    kmer, db = make_dict(q, st, k)
    hsp = find_HSPs(q, st, kmer, db, k)
    return_threshold(hsp, L)

if __name__ == '__main__':
    main()
