
def read_simfile(filename1,filename2):
    sims_table = {}
    cnt = 0
    with open(filename1,"r") as fr,open(filename2,"w")as fw:
        for line in fr.readlines():
            cnt += 1
            if(cnt%10000==0):print(cnt/10000)
            line_proc = line.strip().split('\t')
            if line_proc[1] == "0.0":
                continue
            else:
                fw.write(line)


filename1=r"C:\Users\Strawberry\Desktop\Web_info_lab3\sim_table.txt"
filename2=r"C:\Users\Strawberry\Desktop\Web_info_lab3\sim_table2.txt"
read_simfile(filename1,filename2)