#coding:utf-8
import sys
import os

base_title = "test"
entry = os.listdir(base_title)
for entity in entry:
    if entity == ".DS_Store":
        continue
    entry_path = base_title + "/" + str( entity )
    test_dir = "tag_test/" + str( entity )
    os.mkdir(test_dir)
    entry_tmp = os.listdir( entry_path )
    for entry_file in entry_tmp:
        if entry_file == "map.txt" or entry_file == ".DS_Store":
            continue
        doc_true = []
        entry_path_ = entry_path + "/" + str( entry_file )
        doc = os.listdir( entry_path_ )
        for doc_tmp in doc:
            if doc_tmp == "urls.txt":
                continue
            file_path = entry_path_ + "/" + str( doc_tmp )
            f = open(file_path, "r")
            for line in f:
                tmp = line.strip().split(" ")
                tmp_ = [x for x in tmp if len(x) != 0 ]
                if len( tmp_ ) == 0:
                    continue
                _tmp = ''.join(tmp_)
                doc_true.append(_tmp)
                print _tmp
            # exit()
            f.close()
        true_doc = ''.join(doc_true)
        f = open(test_dir+"/"+str(entry_file), "w")
        f.write(true_doc)
        f.close()
        print entry_path_
        exit()
