
# Verify https://judge.yosupo.jp/submission/277247
def dijkstra(edge: list[set[tuple[int, int]]], s: int) -> tuple[list[int], list[int]]:
    """
    始点sから各頂点への最短距離を求める

    Parameters
    ----------
    :param edge: 隣接リスト
    :param s: 始点

    Returns
    -------
    :return: (dis, prev)
    1. dis: 各頂点への最短距離のリスト
    2. prev: 最短経路での各頂点の親のリスト
    """

    prev = [-1]*n # 経路復元用
    dis = [inf]*n

    from heapq import heapify,heappop,heappush
    que = []
    dis[s] = 0
    heappush(que, (dis[s], s)) 

    while que:
        
        cur_dis, cur_node = heappop(que)
        
        if dis[cur_node] < cur_dis:
            continue
        
        for next_node, weight in edge[cur_node]:
            next_dis = cur_dis + weight
            if dis[next_node] > next_dis:
                dis[next_node] = next_dis
                prev[next_node] = cur_node
                heappush(que, (next_dis, next_node))
    
    return (dis, prev)

def restore_path(prev, t):
    path = []
    while t != -1:
        path.append(t)
        t = prev[t]
    return path[::-1]

dis, prev = dijkstra(edge, s)

path = restore_path(prev, t)

if dis[t] == inf: exit(print(-1))

print(dis[t], len(path)-1)
