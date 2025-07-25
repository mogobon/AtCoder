"""
instance
5 3
3 7 2 8 5
"""
# https://kanpurin.hatenablog.com/entry/2021/09/05/163703
# https://kanpurin.hatenablog.com/entry/2021/09/05/163703
class BinaryTrie:
    def __init__(self, max_query=2*10**5, bitlen=4):
        n = max_query * bitlen
        self.nodes = [-1] * (2 * n)
        self.cnt = [0] * n
        self.id = 0
        self.bitlen = bitlen

    def size(self):
        return self.cnt[0]

    # xの個数
    def count(self,x):
        pt = 0
        for i in range(self.bitlen-1,-1,-1):
            y = x>>i&1
            if self.nodes[2*pt+y] == -1:
                return 0
            pt = self.nodes[2*pt+y]
        return self.cnt[pt]

    # xの挿入（可視化付き）
    def insert(self, x, verbose=False):
        # pointer, position(現在の位置)
        pt = 0
        if verbose:
            print(f"\n=== 挿入: {x} (bin: {bin(x)[2:].zfill(self.bitlen)}) ===")
        for i in range(self.bitlen-1, -1, -1):
            # フラグy(子が0か1か)を取得
            y = x >> i & 1
            # 対応する子ノードが存在しない場合
            if self.nodes[2*pt+y] == -1:
                # idを1増やす(insertを呼び出すごとに0から始まっている)
                self.id += 1
                # 新しいノードを作成
                self.nodes[2*pt+y] = self.id # 次辿れるようにするための布石？
                if verbose:
                    print(f"  新ノード作成: {self.id} (親: {pt}, bit: {y}, depth: {self.bitlen-1-i})")
            # ノードが持つ部分木の個数を更新
            self.cnt[pt] += 1
            if verbose:
                print(f"  ノード{pt:4d} 経路: {bin(x)[2:].zfill(self.bitlen)[:self.bitlen-i]} 個数: {self.cnt[pt]}")
            pt = self.nodes[2*pt+y]
        self.cnt[pt] += 1
        if verbose:
            print(f"  葉ノード{pt:4d} 経路: {bin(x)[2:].zfill(self.bitlen)} 個数: {self.cnt[pt]}")
            print("========================")
    def lower_bound(self, x):
        """x以上の最小要素が昇順何番目かを返す"""
        pt = 0
        res = 1
        for i in range(self.bitlen-1, -1, -1):
            if res==-1: break
            # フラグが1で左の子が存在しない場合
            if x>>i&1 and self.nodes[2*pt] != -1:
                # 左の子の部分木の大きさを加算
                res += self.cnt[self.nodes[2*pt]]
            # 次の子へ移動
            pt = self.nodes[2*pt+(x>>i&1)]
        return res
    # xが存在しないときは何もしない
    def erase(self,x):
        if self.count(x) == 0:
            return
        pt = 0
        for i in range(self.bitlen-1, -1, -1):
            y = x >> i & 1
            self.cnt[pt] -= 1
            pt = self.nodes[2*pt+y]
        self.cnt[pt] -= 1
    
    # 昇順x番目(1-indexed)の値
    def kth_elm(self,x):
        assert 1 <= x <= self.size()
        pt, ans = 0, 0
        for i in range(self.bitlen-1, -1, -1):
            ans <<= 1
            # 左の子が存在かつ左の子の部分木の数が0より大きい
            if self.nodes[2*pt] != -1 and x <= self.cnt[self.nodes[2*pt]] > 0:
                if self.cnt[self.nodes[2*pt]]>=x:
                    pt=self.nodes[2*pt]
            else:
                x -= self.cnt[self.nodes[2*pt]]
                pt = self.nodes[2*pt+1]
                ans += 1 # ans |= 1でも良い
        return ans
    
    
def visualize_trie(bt):
    from collections import deque
    print("=== BinaryTrie 可視化 ===")
    q = deque()
    q.append((0, "", bt.cnt[0]))
    max_depth = bt.bitlen
    while q:
        pt, path, cnt = q.popleft()
        if cnt == 0:
            continue
        print(f"ノード: {pt:4d} 経路: {path:>{max_depth}s}  個数: {cnt}")
        left = bt.nodes[2*pt]
        right = bt.nodes[2*pt+1]
        if left != -1:
            q.append((left, path + "0", bt.cnt[left]))
        if right != -1:
            q.append((right, path + "1", bt.cnt[right]))
    print("========================")

# if __name__ == "__main__":
#     bt = BinaryTrie()
#     N, Q = map(int, input().split())
#     A = list(map(int, input().split()))
#     for a in A:
#         bt.insert(a, verbose=False)  # 挿入ごとに詳細表示
#         # visualize_trie(bt)          # 挿入後の全体構造も表示
#     # クエリ部分は必要に応じて
#     for _ in range(Q):
#         x = int(input())
#         print(N+1-bt.lower_bound(x))
    #     visualize_trie(bt)
