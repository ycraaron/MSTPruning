# random select a point
# iterate to find all its adjoin point
# edges
import MySQLdb

class Node():
    def __init__(self, vertex_id, distance):
        self.id = vertex_id
        self.weight = distance

    def get_id(self):
        return self.id

    def get_weight(self):
        return self.weight

def gen_adj_matrix():
    edge_file = open("/Users/aaron/downloads/data_new/resultMST.txt.100k", "r")

    graph = [[] for node in xrange(9039)]

    edge_tuple = []
    for line in edge_file:
        item = line.split(" ")
        edge = (item[0], item[1], item[2])
        edge_tuple.append(edge)

    for v1, v2, weight in edge_tuple:
        if float(weight) == 0:
            graph[int(v1)].append(Node(v2, weight))
            graph[int(v2)].append(Node(v1, weight))

    return graph

def core():
    g = gen_adj_matrix()
    #print g
    rm_node_id = []
    ls_cluster = []
    ls_skip_node_id = []
    for i in xrange(0, len(g)):
        # check whether it could be a new root of a cluster
        #print ls_skip_node_id
        if i not in ls_skip_node_id and len(g[i]) > 1:
            # then find the adj nodes of this root
            ls_adj_node_id = []
            for node in g[i]:
                child_id = int(node.get_id())
                ls_adj_node_id.append(child_id)
                # add the child node to skip list if it only have 1 adj node.
                if len(g[child_id]) == 1:
                    ls_skip_node_id.append(child_id)
            ls_adj_node_id.insert(0,i)
            ls_cluster.append(set(ls_adj_node_id))
            #print i , len(ls_adj_node_id), ls_adj_node_id
            #print "Skip",i

    for i in xrange(0, len(g)):
        if i not in ls_skip_node_id and len(g[i]) == 1:
            for node in g[i]:
                print node.get_id()

    #count_inter = 0
    # 34 intersections:

    #for clus in ls_cluster:
        #print clus
    #print "Number of clusters:", len(ls_cluster)
    remove_set_index = []
    for i in xrange(0, len(ls_cluster)):
        cluster_1 = ls_cluster[i]
        for j in xrange(i+1, len(ls_cluster)):
            cluster_2 = ls_cluster[j]
            if len(cluster_1.intersection(cluster_2)) > 0:
                ls_cluster[i] = ls_cluster[i].union(cluster_2)
                remove_set_index.append(j)
                #print cluster_1.intersection(cluster_2)
    #print len(remove_set_index)

    remove_set_index = set(remove_set_index)
    remove_set_index = list(remove_set_index)
    remove_set_index.sort()
    remove_set_index.reverse()
    #print remove_set_index
    #print len(ls_cluster)
    for index in remove_set_index:
        del ls_cluster[index]

    #print len(ls_cluster)
    for i in xrange(0,len(ls_cluster)):
        ls_cluster[i] = list(ls_cluster[i])
        ls_cluster[i].sort()

    # for cluster in ls_cluster:
    #     print cluster

    # for i in xrange(9039):
    #     ls_id = []
    #     if str(i) not in rm_node_id and len(g[i]) > 1:
    #         for node in g[i]:
    #             ls_id.append(node.get_id())
    #             rm_node_id.append(node.get_id())
    #         ls_id.insert(0, i)
    #         #print ls_id
    #         for i in xrange(0,len(ls_id)):
    #             ls_id[i] = int(ls_id[i])
    #         ls_cluster.append(ls_id)

    db_conn = MySQLdb.connect(host="localhost", port=8889, db="linked_reverb", user="root", passwd="root")
    cursor = db_conn.cursor(MySQLdb.cursors.DictCursor)
    i = 1
    #for cluster_list in ls_cluster:
        #for m in xrange(0,len(cluster_list)):
        #    cluster_list[m] = str(cluster_list[m]+1)
        #ls_tu = tuple(cluster_list)
        #format_strings = ','.join(['%s'] * len(cluster_list))
        #sql = "UPDATE base SET cluster_id = " + str(i) + " WHERE id IN(%s)" % format_strings
        #print sql, ls_tu
        #print cursor.execute(sql, ls_tu)
        #print db_conn.commit()
        #i=i+1



core()
