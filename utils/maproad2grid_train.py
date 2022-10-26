import networkx as nx
import pickle
import os
data_path = '/data/GeQian/g2s_2/gmm-data0.125/data/'
pkl_path = '/data/GeQian/g2s_2/gmm-data0.125/train_used_pkl/'
if not os.path.exists(pkl_path):
    os.mkdir(pkl_path)
# road_graph = nx.read_gml(data_path + 'road_graph.gml', destringizer=int)
road_graph = pickle.load(open(data_path + 'road_graph.pkl', 'rb'))
trace_graph = nx.read_gml(data_path + 'train_trace_graph.gml', destringizer=int)

trace_graph_grid_set = set()
grid2traceid_dict = {}
for k, v in dict(trace_graph.nodes()).items():
    pair = (v['gridx'], v['gridy'])
    # trace_graph_grid_set.add(pair)
    if pair in grid2traceid_dict.keys():
        print('smt wrong ! {pair} appears more than once')
    grid2traceid_dict[pair] = k

pickle.dump(grid2traceid_dict, open(pkl_path + 'grid2traceid_dict.pkl', 'wb'))
print('finished')


def road2grid():
    road2grid_dict = {}
    grid2road_dict = {}
    for k, v in dict(road_graph.nodes()).items():
        road2grid_dict[int(k)] = []
        for i in range(v['x1'], v['x2'] + 1):
            for j in range(v['y1'], v['y2'] + 1):
                if (i, j) not in grid2traceid_dict.keys():
                    continue
                road2grid_dict[int(k)].append((i, j))
                if (i, j) not in grid2road_dict.keys():
                    grid2road_dict[(i, j)] = []

                grid2road_dict[(i, j)].append(int(k))
        # assert(road2grid_dict[int(k)]!=[])

    pickle.dump(grid2road_dict, open(pkl_path + 'grid2road_dict.pkl', 'wb'))
    pickle.dump(road2grid_dict, open(pkl_path + 'road2grid_dict.pkl', 'wb'))
    return grid2road_dict, road2grid_dict


grid2road_dict, road2grid_dict = road2grid()


def road2traceid():
    road2grid_dict = pickle.load(open(pkl_path + 'road2grid_dict.pkl', 'rb'))
    grid2traceid_dict = pickle.load(open(pkl_path + 'grid2traceid_dict.pkl', 'rb'))
    road2traceid_dict = {}
    for road, grid_ls in road2grid_dict.items():
        # print(road, grid_ls)
        road2traceid_dict[road] = []
        for grid in grid_ls:
            road2traceid_dict[road].append(grid2traceid_dict[grid])
    # print(road2traceid_dict)
    pickle.dump(road2traceid_dict,
                open(pkl_path + 'road2traceid_dict.pkl', 'wb'))
    return road2traceid_dict


def traceid2road():
    road2traceid_dict = pickle.load(open(pkl_path + 'road2traceid_dict.pkl', 'rb'))
    traceid2road_dict = {}
    for road, traceid_ls in road2traceid_dict.items():
        for traceid in traceid_ls:
            if traceid not in traceid2road_dict.keys():
                traceid2road_dict[traceid] = []
            traceid2road_dict[traceid].append(road)
    pickle.dump(traceid2road_dict, open(pkl_path + 'traceid2road_dict.pkl', 'wb'))
    return traceid2road_dict


road2traceid_dict = road2traceid()
traceid2road_dict = traceid2road()
road_numof_grids = {k: len(v) for k, v in road2grid_dict.items()}