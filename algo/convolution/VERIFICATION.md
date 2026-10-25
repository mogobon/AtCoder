# Codon FPS 移植・検証結果

移植元: [harurun-s-library / FPS.py](https://github.com/lif4635/harurun-s-library/blob/main/library_codon/convolution/FPS.py)

2026-10-25 / Codon 0.19.0 / Linux x86_64 / `codon build -release`

**公式12問344ケースがすべて期待出力に一致。追加141ケースも全件成功。元コードの28関数をすべて実際に呼び出し、コンパイル・実行を確認。**

Library Checker の公開言語設定には Codon が含まれていないため、サイトへの Codon 提出・AC は取得していません。公式リポジトリからテストを全件生成し、公式解答の出力と Codon 実行ファイルの出力を空白区切りで比較したローカル検証です。補助関数の一部には対応する単独問題がないため、下表で公式問題経由の検証と追加検証を区別しています。

指定された extend と pow の上書きを本体に同梱しています。0.20.4 では指定の `__ctlz__` が存在しなかったため、指定の extend を変更せずにコンパイルできる 0.19.0 を使用しました。別バージョンでの実行は未確認です。

## 公式テスト

秒数はこの環境で観測した1ケースの最大実行時間です。別環境での制限時間内通過を保証する数値ではありません。

| 問題 | 一致ケース数 | 最大秒数 |
| --- | ---: | ---: |
| [convolution_mod](https://judge.yosupo.jp/problem/convolution_mod) | 53/53 | 0.431 |
| [inv_of_formal_power_series](https://judge.yosupo.jp/problem/inv_of_formal_power_series) | 25/25 | 0.348 |
| [exp_of_formal_power_series](https://judge.yosupo.jp/problem/exp_of_formal_power_series) | 26/26 | 0.479 |
| [log_of_formal_power_series](https://judge.yosupo.jp/problem/log_of_formal_power_series) | 25/25 | 0.483 |
| [pow_of_formal_power_series](https://judge.yosupo.jp/problem/pow_of_formal_power_series) | 37/37 | 0.947 |
| [division_of_polynomials](https://judge.yosupo.jp/problem/division_of_polynomials) | 35/35 | 0.514 |
| [composition_of_formal_power_series](https://judge.yosupo.jp/problem/composition_of_formal_power_series) | 27/27 | 0.122 |
| [compositional_inverse_of_formal_power_series](https://judge.yosupo.jp/problem/compositional_inverse_of_formal_power_series) | 23/23 | 0.523 |
| [polynomial_taylor_shift](https://judge.yosupo.jp/problem/polynomial_taylor_shift) | 38/38 | 0.310 |
| [kth_term_of_linearly_recurrent_sequence](https://judge.yosupo.jp/problem/kth_term_of_linearly_recurrent_sequence) | 20/20 | 3.448 |
| [sharp_p_subset_sum](https://judge.yosupo.jp/problem/sharp_p_subset_sum) | 24/24 | 0.525 |
| [partition_function](https://judge.yosupo.jp/problem/partition_function) | 11/11 | 0.442 |

## 関数別の確認範囲

「公式経由」は対応問題の実行で関数が呼ばれることを意味します。サイト上の個別 AC を意味しません。

| 元の関数名 | 検証方法 |
| --- | --- |
| `butterfly` | 畳み込み・FPSの公式問題経由、追加の往復変換8ケース |
| `butterfly_inv` | 畳み込み・FPSの公式問題経由、追加の非正規化逆変換8ケース |
| `intt` | exp・合成の公式問題経由、追加の正規化往復変換8ケース |
| `multiply` | convolution_mod 53ケース、他の公式問題経由 |
| `pow2` | 追加のbasic 70ケースで愚直な自乗と比較、空配列を確認 |
| `shrink` | 多項式除算の公式問題経由、basic 70ケース |
| `fps_add` | basic 70ケースで係数ごとに比較 |
| `fps_sub` | 多項式除算・合成逆関数の公式問題経由、basic 70ケース |
| `fps_neg` | basic 70ケースで係数ごとに比較 |
| `fps_div` | division_of_polynomials 35ケース経由、basic 70ケース |
| `fps_mod` | basic 70ケースで愚直な長除算と比較 |
| `fps_divmod` | division_of_polynomials 35ケース |
| `fps_eval` | basic 70ケースで各項の直接評価と比較 |
| `fps_inv` | inv_of_formal_power_series 25ケース、他の公式問題経由 |
| `fps_pow` | pow_of_formal_power_series 37ケース、指数10^18等の追加境界確認 |
| `fps_exp` | exp_of_formal_power_series 26ケース、他の公式問題経由 |
| `fps_log` | log_of_formal_power_series 25ケース、べき乗の公式問題経由 |
| `fps_integral` | logの公式問題経由、basic 70ケース |
| `fps_diff` | log・exp・合成逆関数の公式問題経由、basic 70ケース |
| `LinearRecurrence` | kth_term_of_linearly_recurrent_sequence 20ケース |
| `fps_compsite` | composition_of_formal_power_series 27ケース、追加愚直比較27ケース |
| `fps_compsitional_inv` | compositional_inverse_of_formal_power_series 23ケース、追加愚直比較15ケース |
| `SubsetSum` | sharp_p_subset_sum 24ケース、空入力確認 |
| `MultisetSum` | partition_function 11ケース、一般の個数配列で愚直DP8ケース |
| `tayler_shift` | polynomial_taylor_shift 38ケース、空入力確認 |
| `ntt2d` | 2次元往復変換6ケース、2次元畳み込み経由6ケース |
| `intt2d` | 2次元往復変換6ケース、2次元畳み込み経由6ケース |
| `multiply2d` | 長方形・非2冪の行列を含む6ケースで四重ループと比較 |

追加の `basic` は1ケースで複数関数を確認します。141という合計は起動した入力ケースの数です。

## 主な修正

- `array('I', ...)` を `list[int]` に置換。
- 素朴な積・自乗・長除算で、累積前後に剰余を取り64ビット整数のオーバーフローを回避。
- FPSべき乗の `k` を係数に掛ける際は `k % MOD` を使用。先頭ゼロによるシフトが打ち切り次数以上になる判定も、巨大な `i*k` を計算せずに実施。
- `LinearRecurrence` の各段で分子・分母の長さを実際の取り出し結果に更新。ゼロ分子にも対応。
- 合成逆関数のNewton更新で、`g'` の逆数を必要な次数まで計算するよう修正。旧コードは次数8の小さい例でも末尾が不一致になりました。
- `multiply2d` の最初の2回を逆変換から順変換に修正。`deepcopy` を行ごとのコピーに置換。
- 空の積、打ち切り次数0、末尾ゼロのある多項式除算などを整理。
- Codonで添字アクセスできないイテレータを避け、リストを明示。

## 利用条件・API

- 係数は低次から並べ、入力係数は原則 `0 <= a[i] < 998244353` に正規化してください。
- 元の関数名・引数順を維持しています。`fps_compsite`、`fps_compsitional_inv`、`tayler_shift` の綴りも変更していません。
- `fps_compsite(inner, outer)` は **outer(inner(x))** を返します。両者は同じ長さで、`inner[0] == 0` を前提にします。
- `fps_compsitional_inv(calc, deg)` の `calc(g, d)` は、外側の元の多項式と `g` をそれぞれ長さ `d` に切り詰め・ゼロ埋めして合成し、長さ `d` のリストを返すようにしてください。実例は `verify_driver.py` を参照。
- `fps_inv`: 定数項が非ゼロ。`fps_log`: 定数項が1。`fps_exp`: 定数項が0。
- `fps_pow`: 非負の整数指数。各FPS関数の `deg` は非負、または既定値の `-1`。
- `fps_div`、`fps_mod`、`fps_divmod` は多項式の除算です。ゼロ除算はエラー。商・余りの末尾ゼロは省略されます。
- `butterfly` と `butterfly_inv` は非空の2冪長リストを書き換えます。逆変換は長さ倍された結果になり、`intt` は正規化まで行います。
- `ntt2d`、`intt2d` は行数・列数がともに正の2冪である長方形リストを書き換えます。`intt2d` は正規化まで行います。
- NTTの各軸の長さは `2^23` 以下。畳み込みではゼロ埋め後の長さにこの制約がかかります。
- `multiply2d` は非空の長方形行列2つを受け取り、入力を変更せずに通常の2次元畳み込みを返します。
- `SubsetSum`、`MultisetSum` は正の重みのみを扱います。`d[0] == 0` としてください。

## 再現手順

このフォルダに収録しているのは `fps_codon.py` と本書です。以下は別途配布した検証一式 `fps_codon_verified.zip` を展開したディレクトリで実行する手順です。検証用スクリプトはこのフォルダには含めていません。

必要なものは Codon 0.19.0、Python 3、公式テスト生成用のC++コンパイラです。

```bash
python3 build_verify.py /path/to/codon
python3 test_differential.py ./fps_verify

git clone https://github.com/yosupo06/library-checker-problems.git lc-problems
git -C lc-problems checkout 73876f1cbcf082d2b22722924b924d3d65a2f00e
python3 lc-problems/generate.py -p convolution_mod inv_of_formal_power_series exp_of_formal_power_series log_of_formal_power_series pow_of_formal_power_series division_of_polynomials composition_of_formal_power_series compositional_inverse_of_formal_power_series polynomial_taylor_shift kth_term_of_linearly_recurrent_sequence sharp_p_subset_sum partition_function
python3 verify_official.py ./fps_verify ./lc-problems
```

`fps_codon.py` が提出用の部品です。必要な入力処理をその末尾に追記してください。`verify_driver.py` は検証用で、通常の提出には不要です。

公式リポジトリ: https://github.com/yosupo06/library-checker-problems

言語設定: https://github.com/yosupo06/library-checker-judge/blob/01fa3c63f036611cff8be611dc1c69a5605f6a70/langs/langs.toml
