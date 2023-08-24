import os

def search_files(directory):
    results = {}
    for filename in os.listdir(directory):
        prefix = filename[:3]
        if prefix in ['cat', 'dog', 'pet']:
            with open(os.path.join(directory, filename), 'r') as file:
                for line in file:
                    if 'some_keyword' in line:
                        if prefix not in results:
                            results[prefix] = []
                        results[prefix].append(line.strip())
    return results
