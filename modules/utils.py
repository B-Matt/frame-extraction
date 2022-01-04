from os import walk, path

def list_files(data_path):
    files_list = list()
    for (dirpath, dirnames, filenames) in walk(data_path):
        files_list += [path.join(dirpath, file) for file in filenames]
    return files_list

def chunk(data, chunk_size):
	for i in range(0, len(data), chunk_size):
		yield data[i: i + chunk_size]