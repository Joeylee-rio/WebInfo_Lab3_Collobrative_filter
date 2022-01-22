"""
implementation:
simple collaborative fliter based on items
"""
import numpy as np
import math

def read_musicfile(filename):
    infos_mat = {}
    with open(filename,"r") as fr:
        for line in fr.readlines():
            line = line.strip().split('\t')
            len_user = len(line) - 1
            music_id = int(line[0])
            infos_mat[music_id] = {}
            for i in range(len_user):
                user4music = line[i+1].strip().split(',')
                user,score = user4music[0],user4music[1]
                if score == '-1':
                    continue
                infos_mat[music_id][int(user)] = int(score)
    return infos_mat

def read_userfile(filename):
    infos_mat = {}

    with open(filename,"r") as fr:
        for line in fr.readlines():
            line = line.strip().split('\t')
            len_user = len(line) - 1
            user_id = int(line[0])
            infos_mat[user_id] = {}
            for i in range(len_user):
                music4user = line[i+1].strip().split(',')
                music,score = int(music4user[0]),int(music4user[1])
                
                if score == -1:
                    infos_mat[user_id][music] = 0
                else:
                    infos_mat[user_id][music] = score

    return infos_mat

def transinfo_user2music(infos):
    
    infost = {}
    for user in infos.keys():
        for music in infos[user].keys():
            infost[music] = {}

    for user in infos.keys():
        for music in infos[user].keys():
            infost[music][user] = infos[user][music]
    return infost

"""
infos_mat = 
{
    (key=1(music_id):value={(key=3(user_id):value=2(score)),......}),
    ...,
    ...
}
"""
def proc_items(infos):
    pass
    avg_dict = {}
    for music_id in infos.keys():
        leng, avg = get_avg(infos[music_id])
        avg_dict[music_id] = avg
        for user in infos[music_id].keys():
            infos[music_id][user] -= avg

    return infos,avg_dict


def get_keys_intersection(infos,music_id1,music_id2):
    return list(set(infos[music_id1].keys()).intersection(set(infos[music_id2].keys())))


def get_avg(item_info):
    pass
    item_len = len(item_info)
    sum = 0
    for key in item_info.keys():
        sum += item_info[key]
    avg = sum * 1. / float(item_len)
    return item_len,avg

def get_inner_product(infos,music_id1,music_id2):
    return sum(infos[music_id1][user]*infos[music_id2][user] for user in get_keys_intersection(infos,music_id1,music_id2))

sim_table = {}
norm_table = {}


def encode(music_id1,music_id2):
    return music_id1*100000 + music_id2

def get_norms(infos):
    for id in infos.keys():
        norm_table[id] = get_norm(infos,id)

def get_sims(infos):
    cnt = 0
    for id1 in infos.keys():
        for id2 in infos.keys():
            
            if norm_table[id1] == 0.0 or norm_table[id2] == 0.0:
                sim_table[encode(id1,id2)] = 0.0
            else:
                sim_table[encode(id1,id2)] = get_inner_product(infos,id1,id2) * 1.0 / (norm_table[id1] * norm_table[id2])
            
            '''
            sim_table[encode(id1,id2)] = 0.01
            '''
def save_sims_table(filename):
    
    with open(filename,"w")as fs:
        for key in sim_table.keys():
            fs.write(str(key)+'\t'+str(sim_table[key])+'\n')

def load_sims_table(filename):
    print("---load_sim_table---")
    cnt = 0
    with open(filename,"r")as fr:
        for line in fr.readlines():
            cnt += 1
            if cnt%10000 == 0:
                print(cnt/10000)
            line = line.strip().split('\t')
            key,value = int(line[0]),float(line[1])
            sim_table[key]=value

def get_norm(infos,music_id):
    return math.sqrt(sum(pow(infos[music_id][user],2) for user in infos[music_id].keys()))

def get_sim(key):
    if key in sim_table.keys():
        return sim_table[key]
    else:
        return 0.0

def get_neiborghoods(infos,save_filepath):
    neiborghoods = {}
    cnt = 0
    for id1 in infos.keys():
        cnt += 1
        if(cnt%10 == 0):print(cnt)
        temp = {}
        for id2 in infos.keys():
            temp[id2] = get_sim(encode(id1,id2))
        top10 = dict(sorted(temp.items(),key=lambda e:e[1],reverse=True)[:10])
        top10 = list(top10.keys())
        neiborghoods[id1] = top10
    with open(save_filepath,"w") as fw:
        for key in neiborghoods.keys():
            fw.write(str(key)+'\t'+str(neiborghoods[key])+'\n')

def load_neiborghoods(save_filepath):
    print("---load_neiborghoods---")
    neiborghoods = {}
    cnt = 0
    with open(save_filepath,"r") as fr:
        
        for line in fr.readlines():
            cnt += 1
            if(cnt %10 == 0):print(cnt)
            line = line.strip().split('\t')
            key = int(line[0])
            neiborghoods[key] = []
            value = line[1].strip('[')
            value = value.strip(']')
            value = value.strip().split(',')
            for id in value:
                neiborghoods[key].append(int(id))
    return neiborghoods


def predict(infos, user, music, avg_dict,N10):
    '''
    predicts scores which this user gave for this music
    '''
    sum = 0.
    for m_id in N10[music]:
        if user in infos[m_id].keys():
            sum += get_sim(encode(music,m_id)) * (infos[m_id][user] + avg_dict[m_id]) * 1. 
    
    temp = 0.
    for m_id in N10[music]:
        temp += get_sim(encode(music,m_id))
    if temp == 0.0:
        score = 0.0
    else:
        score = float(sum)/ temp
    return score

def main():
    '''
    user_id 0~23598
    '''
    user_idmax = 23599
    user_filepath = r'/data2/home/zhaoyi/Web_lab3/DoubanMusic.txt'
    infos_pre = read_userfile(user_filepath)
    infos = transinfo_user2music(infos_pre)
    infos,avg = proc_items(infos)
    '''
    get_norms(infos)
    get_sims(infos)
    save_sim_file = r'/data2/home/zhaoyi/Web_lab3/sim_table.txt'
    save_sims_table(save_sim_file)
    '''
    
    load_sim_file = r'/data2/home/zhaoyi/Web_lab3/sim_table2.txt'
    load_sims_table(load_sim_file)

    save_N10_file = r'/data2/home/zhaoyi/Web_lab3/N10.txt'
    '''
    get_neiborghoods(infos,save_N10_file)
    '''
    N10 = load_neiborghoods(save_N10_file)
    music_list = infos.keys()
    result_filepath = r'/data2/home/zhaoyi/Web_lab3/result.txt'
    
    with open(result_filepath,"w") as fw:
        for i in range(user_idmax):
            print('userid---',i)
            scores = {}
            musiclist4user = infos_pre[i].keys()
            music4predict = list(set(music_list)-set(musiclist4user))
            for music in music4predict:
                scores[music] = predict(infos,i,music,avg,N10)
            '''
            sort for this dict(score) according to score-value
            '''
            top100 = dict(sorted(scores.items(),key=lambda e:e[1],reverse=True)[:100])
            top100 = list(top100.keys())
            fw.write(str(i)+'\t')
            for music in top100:
                fw.write(str(music))
                if music == top100[99]:
                    fw.write('\n')
                else:
                    fw.write(',')

if __name__ == "__main__":
    main()