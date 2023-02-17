# 相对位置的起点, 是执行python的文件位置. 规定：总是在autodl下, 执行main.py或test.py
# 日志log、参数params暂存总是在logs、model文件（logs/model/autodl三个文件平行放在working space中）


# 所以可以固定日志log、参数params暂存的文件夹地址如下：
######################### 对任意proj适用 ######################### 
online_log_dir = '../logs'
online_model_save_dir = '../model'

reveal_cnt_in_train = 30 # 训练过程中披露次数. train loss/train accuracy等
eval_cnt_in_train = 6 # 训练过程中模型衡量次数. valid loss/valid accuracy等


######################## 根据proj自由设定 ######################## 
proj_name = 'transformer'

# 读入的数据存储位置
base_data_dir = '../../data'
seq2seq_dir = 'seq2seq'
eng2fra_train_fname = 'eng2fra.txt'
eng2fra_valid_fname = 'eng2fra_valid.txt'
eng2fra_test_fname = 'eng2fra_test.txt'

# 读入的模型存储位置
local_model_save_dir = '../../model'