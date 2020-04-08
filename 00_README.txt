

	資産市場の簡易シミュレーション
	(Created: 2019-05-29, Time-stamp: <2019-06-11T12:16:28Z>)


** 概要

「土地」と「知的財産」からなる資産市場のシンプルなシミュレーションまた
はゲームを Python で行う。そこには贅沢品と賃金だけからなる商品市場をか
らめる。

「知的財産」市場の総額を一定に保つよう各期減価しさえすれば、自然な借金
増加と「平均への回帰」があるために、資産市場の現金が商品市場に流入する
ことでのバランスの崩れを、商品市場の賃金からの借金返済の現金が資産市場
へ還流することで補い、自然に再度バランスが取れ、ほぼ定常状態に致ること
が確認された。


** はじめに

《ミクロ経済学の我流シミュレーション》の micoro_economy_*.py は今ひと
つ安定しなかった。初期値にも敏感に反応し、初期値のわずかな変化があとあ
とにかなり影響しているらしいことがあった。「定常状態」に致るとき、それ
が初期値と同じようになれば安定するのではないかという考えが私にはある。
そのためには定常状態になるための流入を別に作ったり、初期値をよりよいも
のにする必要があると考える。

特に大きく初期値と変わるのは、貯蓄であった。貯蓄の初期値は指数分布にし
ているが、シミュレーションが進むとだんだん平等になっていき、指数分布で
なくなる。そもそも指数分布はどのようなときに現れるか、それに関する記事
が《なぜ統計学では釣り鐘型の分布が使われ、物理現象では右肩下がりの分布
が使われるのか - 小人さんの妄想》にあった。そこでは『富の分布について』
という記事が再引用されている。

> 富の分布について（駒澤大学学術機関リポジトリより）
>
> http://repo.komazawa-u.ac.jp/opac/repository/all/33054/
> 
> > Random sharing model偶然に出会った、二人の経済主体の間で二人の富の
> > 総額をランダムに分割する、という交換ルールを何回も繰り返すモデルで
> > ある。(…)このモデルは、偶然に出会った2人が自分たちの所有する富の総
> > 和を、ギャンブルで分け合うモデルと言う様にも解釈できよう。(…)この
> > ルールに基づいて富の交換を、分布の形が変化しなくなるまで繰り返すと
> > 富の分布は指数分布になることが知られている。

「偶然に出会った2人が自分たちの所有する富の総和を、ギャンブルで分け合
う」ということの経済的意味は何だろう？ このままでは毎回、指数分布にな
るようにランダムに設定しなおす形でしか micro_economy_*.py に活かせそう
にない。それではあまり意味がない。

指数分布が本来の性質であるとした場合、贅沢品の購入は、とにかくお金を持っ
ていれば購入し、贅沢品は「資産」にカウントされるようなことはないから、
(過剰)消費を通じた富(資産)の平等がはかられているという見方もできるのか
もしれない。…と考えるに致り、そこから、資産取引を別に考えてはどうだろ
う？…と考えるに致った。これが本稿の実験を行うに致った動機的な部分であ
る。

資産取引としては以前の私の記事《外作用的簡易経済シミュレーションのアイ
デアと Perl による実装》の simple_market_0.pl の考え方を持ってこれない
だろうか？ 資産に応じて資産を生み、その売買が起こるとき、売った側は現金
(マウナスの借金)を手に入れ、買った側には借金ができる。

売った側の現金は贅沢品消費で取り崩され平等になっていく。借金があるうち
は贅沢品消費はできず、借金返済にまわす。…とするのが現実的でないか。必
需品購入した上で残った給与の半分を借金返済にまわし、残りを贅沢品消費に
していったらどうだろう？ micro_economy_*.py の特徴から、給与から資産市
場にまわるのは贅沢品消費だけを考えればよさそうだ。

しかし、この場合、売った側の現金は商品取引の利益として吸い上げられ市場
からなくなるから、借金だけが残ることになる。借金はたまり続け、すべての
人が、借金をし、半分返済、半分贅沢品購入…ということになり、借金の意味
がなくなるのではないか？

いや、借金返済の現金がある。これは資産市場の現金が商品市場に吸い上げら
れるのとは逆で、商品・給与市場の現金が資産市場に還流することになる。両
者がバランスする条件とは何だろうか？ これを確かめるのがとりあえずの本
稿の目的になる。

資産市場だけでモデルを作るにはどうしたらいいだろう？ 資産市場に必要だ
と私が思う特徴を書き出してみる。

  * 借金があるほうが売り易い。資産があるほうが、高く売れる。

  * 現金+資産があるほうが借金のチャンス＝資産を買うチャンスがある。

  * 現金をたくさん持っている者が贅沢品を買うのが、平等化のチャンスになる。

  * 贅沢品を買って現金を減らすのは資産があり借金があるという状態にしや
    すくするため？

贅沢品を買って現金を減らしても、借金状態に陥るほうが資産が買われやすく
なり、高く資産が売れることで逆に現金を手に入れ、再び資産を手に入れるチャ
ンスが広がる…とできるのではないか。

「借金があるほうが売り易い。資産があるほうが、高く売れる。…贅沢品を買っ
て現金を減らすのは資産があり借金があるという状態にしやすくするため？」
という部分。借金をする者としない者がいて、それが期を経るごとに借金をす
る者が有利になり、遺伝的アルゴリズムに似て、借金をしない者が淘汰されて
いく…というモデルも考えられる。しかし、定常状態を導くのが目標で、淘汰
されるような部分は定常状態にはないから、そこは淘汰されきった状態のみを
考えればよいとして、そこまでは踏み込まない。

「定常状態」にしたいという動機があったが、上のアイデアのままでは、資産
が一方的に増えることになる。まぁ、「散逸構造」みたいなものもあってだか
らすぐダメだとはならないが、普通に考えれば、資産の総額を一定にする操作
があればよい。増えた分を全体からさっぴけばよい。

ただ、土地などのことを考えるとこの考え方は「リアル」ではない。そこで、
資産として毎期総額を無理矢理一定にするために取引等がなければ自然に減価
していく「知的財産」と減価のない「土地」を資産の代表として別々にとらえ
ることにする。

「土地」は減価しないかわりに増価しない。現実だと、固定資産税があって所
有にコストがかかったりするが、それは今回、考えないことにする。

「知的財産」は持っていると、知的財産をさらに手に入れやすくなるとする。
買う側の知財が多いほうが、多くの知財を受け取れる。売る側は知財が多いほ
うが価格が高く売れる。資産の評価額は、売買価格より高くなるようにする。

知的財産の売買に少し土地もからませたい。

現実では土地があると借りやすくなるということがある。それをマネるには、
知的財産 + 土地 - 借金 だけ借りられるようにするか…。これは、リアルか
もしれないが、経済の成長を弱めるので、今回は取り入れないことにする。

知的財産は、上の「富の分布」を参考に、売る側と買う側の知的財産を足し合
わせた額について乱数をかけようか？ そして、双方の知財額で按分して支払
う。…と。…いや、これだと土地を活かす余裕がなくなる。売る側の土地も足
すか？…。しかし、こうすると売る側のほうが知財を多く持ってるとおかしな
ことになりそうだ。

足し合わせて乱数というのはやめる。売る側の 知的財産+log(土地) に関して
乱数を取り売買価格を得る。そして、買う側が 1 + log(知的財産) 倍の評価額
を資産として詰むことにする。log(知的財産) は log が効き過ぎる場合は
sqrt などを使えばよい。log() は模式的にそう述べてるだけで詳しい関数は
後述する。

持ってる現金は土地に変えたいものである。知的財産は、現金の多寡よりも、
むしろ失業に関連してそうな気がするが、今回はそれは考えないでおこう。あ
と知財を持つのは、個人というより会社な気がするが、それも今回は無視しよ
う。

どうして借金をしまくって資産を買わないのか？ それは、資産の価値を見出せ
ないから…とする。土地については、売る側が売る気になっていないから。知
的財産については発見がないから。

知的資産は、一度発見すると、それを何度でも売れる…というのは、知的財産
は売っても減らず、何度でも売れることで、それをシミュレートできていると
考えよう。

さて、次からはプログラムのアルゴリズム等を説明していこう。プログラム名
は simple_market_a1_*.py である。

なお、プログラムで変数名を作るとき、「土地」は普通に Land だが、「知的
財産」は Intellectual Property を略して Intellprop と書いていることは、
ここで述べておこう。

また、取引に関わる個人は Player と呼んでる。Playerの数は 1000
(--population=1000) とした。「--何か」はプログラムのオプションである。


** 現金と借金

現金と借金は一つの liability という Player のプロパティになっている。
現金を持っているとはすなわち liability がマイナス値であることである。
これは simple_market_0.pl のころに決めたことを引き継いでいる。

資産取引においてはこの liability のやりとりで現金・借金の付け換えを行
う。資産市場のみを相手にするだけなら、liability は相方で必ず等価交換さ
れるから、Player 全体で集計すると、必ず 0 にバランスするのが大きな特徴
である。

ただ、本稿においては、現金としてさらに savings という商品市場における
貯蓄を別に考慮することになる。savings と liability は別に集計する。商
品市場からは贅沢品の購入時に savings の値を超えて現金が必要になったと
き、liability がマイナスならば、それを使うことができるとする。

逆に liability がプラスならば、借金返済として、給与から必需品を除いた
ものの半分が資産市場に還流することになる。

この商品市場からの流出入により、Player 全体で集計すると、必ず 0 にバラ
ンスするという特徴が失われる。これを無理矢理バランスさせるためのオプショ
ンとして、{{--devaluation-of-liability}} が用意されている。これについ
ては後述する。

各個人の Liablity の初期値は分散 σ = 100.0 の正規分布が基本で、全部の
和が 0 になるよう少し加工している(--initial-liability-sigma=100.0)。


** 資産市場

資産は現金を持つものほど買いやすく、借金のある者ほど売りやすいとする。
それを実現するのに、本稿では、liability の順番でソートし、その順番が i
番目の者について、0 から (a/1000) * i + b の一様乱数を発生させ、その乱
数の値で再びソートし、その上位 300 名(--transactions-of-land=300,
--transactions-of-intellprop=300) が取引を行うとする。最初のソートのと
きに、もちろん liability の額は問題になるが、liability の差がとても大き
くても順位的な差しか考慮されないことには注意すべきかもしれない。

なお、ここでの a, b は b = 1.0 で、a は土地の場合は 0.8
(--coeff-of-land-buyer=0.8, --coeff-of-land-seller=0.8)、知的財産の場合
は 0.3 (--coeff-of-intellprop-buyer=0.3,
--coeff-of-intellprop-seller=0.3) とする。知的財産は才能の問題が大きく、
借金してようとアイデアが出ないときは出ないので、知的財産のほうが、借金
の効果が薄いようにした。

実際、liability が最上位の者と最下位の者の差がどれぐらいあるかは、アー
カイブに同梱の exp_01_01.py で測ることができる。

<source>
$ python exp_01_01.py --a=0.3
0.19 0.304 0.359

$ python exp_01_01.py --a=0.8
0.061 0.313 0.457
</source>

--a が --coeff-* で指定する者に相当する。三つの数値は上位 300 の中に、
元最下位の者が入った割合、元500位の者が入った割合、元最上位のものが入っ
た割合を順に示している。(乱数を使っているので実行結果はその都度、少し異
るだろう。)

取引のボリュームが 300 で一定なのは少し「リアル」ではないかもしれない
が、--coeff-* などを連動して変えることも難しく、とりあえずこうしている。


** 土地の譲渡価格

土地は、サラリーマンなどが売るとすれば、土地は家一軒分取引されて、半分
だけ売るとかすることはない。非常に大きな土地を持っている者が大きく土地
を売るということはあるかもしれないが、基本は、分譲するものである。…と
いうところから考えて、それを簡易にモデル化するには、土地の単位を 10
(--land-unit=10.0) として一つの取引では、この単位でだけ売買が起こるとし
た。ただし、売り手に選ばれた者が土地を持っていない場合は、その取引はキャ
ンセルされるが、取引数を改めて計算することはないものとした。

土地の初期値はだいたい 20 (--initial-land-mean=20.0)の指数分布にした。
ただし、単位を 10 に揃えるため 20/10 が平均になるように指数分布を発生
させてそれを四捨五入した上で 10 倍している。


** 知的財産の譲渡価格

譲渡価格は、売り手の資産の状況で決まり基本的には、所持知的財産額を上限
にして乱数的に決まるとしたい。ただ、それに若干土地も関係させるものとす
る。知的財産がなくても土地を持っていれば、高めに知的財産を生産できると
考えるのである。

そして買い手は、その譲渡価格以上の資産価値を見出して知的財産を買い、自
分のところの知的財産と組み合わせることで、実際その価値以上の価値を資産
として積み上げることとする。このとき資産の評価は譲渡価格以上で基本的に
は所持知的財産額以下にするが、所持知的財産額が少ないときは、それ以上に
なることも許すとする。

このような目的を設計したプログラムにおいて、譲渡価格は 0 から 所持知的
財産 + f(所持土地) までの一様乱数で決める。ここで f(x) は a * (1 + x)
とする。f(10) = 10 であるようにということで a = 10 / log(10) となる。

積み上げる資産価格は、譲渡価格を P として、P から f(買い手の所持知的財
産額)までの一様乱数で決める。ここで f(x) は sqrt(a * x) + P で、f(P) =
1.5 P ぐらいが良かろうとそれを解いて、a = 0.25 * P とする。ここで所持知
的財産が大きいときの評価額が少し高めになるよう sqrt を使った
(--intellprop-transform=sqrt) が、log の形を使う方法
(--intellprop-transform=log) も一応用意している。

このあたりの詳しいアルゴリズムは、プログラムを読んでもらったほうが早い
かもしれない。

知的財産の初期値は 20 (--initial-intellprop-mean=20.0)の指数分布にした。


** 商品市場

商品市場は、基本的に micro_economy_*.py から贅沢品に関する部分だけを抜
き出し、価格を固定したものになる。乱数的に動くのは、雇用者の数(または失
業者の数)で、600 から 900 までの一様乱数で決めている
(--min-working=600, --max-working=900)。

賃金の額は 30.0、必需品の価格は 10.0、贅沢品の価格は 15.0、必需品の必要
量は 2.0 (--price-of-wages=30.0, --price-of-necessaries=10.0,
--price-of-luxuries=15.0, --needs-of-necessaries=2.0)。

贅沢品の購入に向けられる額は、30.0 - 10.0 * 2 = 10.0 となる。
micro_economy_*.py の場合はそれで決まっていたが、本稿では、もし借金があ
る場合、そのうち返済率 0.5 の分だけが借金返済に回る (--repayment-rate=0.5)。

「リアル」に考えれば借金が多いほど返済を多くする必要があるが、利子率な
どで指定しようとすると、給与の額は一定のため贅沢品を買えない者が続出す
るだろう。むしろ、借金だらけの者もある程度は贅沢品が買えるほうが「リア
ル」だと考え、このようにしている。

贅沢品需要について micro_economy_*.py の記事は次のように書いている。

> 目安となる基準額は今期の新規貯蓄から決まり、それは新規貯蓄の３倍とす
> る。貯蓄が基準額を越える部分の 1/3 を基準額に足した額がその者の需要の
> 強さとし、最適化のパラメータとして与えられる贅沢品の価格よりそれが上
> であれば、その者は贅沢品を需要するとする。

基本的に同じであるが、これまでの貯蓄には、liability がマイナスの場合、
それが考慮されてその絶対値がプラスされることと、新規貯蓄から借金返済分
が引かれることが異っている。

貯蓄と liability を使うときはまず貯蓄が使われ、それが 0 になったら
liability から回されるという形を取る。このとき liability から出された
分を Erosion と呼ぶ。

このあたりも、プログラムを参照したほうがわかりやすいかもしれない。

貯蓄の初期値は平均 10 の指数分布にした。この 10 という数値は、上の「贅
沢品の購入に向けられる額」から来ている。


** 知的財産総額の切り下げ

定常状態にするために知的財産が増えたとき、総額を一定に保つため、全体を
按分して知的財産総額を抑える。知的財産総額が元 p で増えた分を h とする
と、各所持知的財産額に p/(p+h) を掛けたものを、新しい所持知的財産額に
する。

ただし、デフォルトではこの操作を行っておらず --devaluation-of-intellprop
というオプションを付けることではじめてこの操作がなされる。が、基本、こ
のオプションは付けて実験を行う。


** Liability の切り下げ

Erosion と借金返済は原理的には必ずしも釣り合うわけではない。そのため、
総 Erosion - 総返済額を徳政令的に各借金(プラスの liability を持つ者)か
らさっぴく。それを行うのが--devaluation-of-liability オプションである。

もし、総 Erosioin - 総返済額がマイナスになれば、そのときは、現金所持者
現金から按分して減らす(マイナスの liability を持つ者のliability をプラ
ス方向に増やす)ことにする。

特殊な場合として、借金総額や現金総額が、abs(総 Erosioin - 総返済額)よ
りも少ない場合がありえるが、その場合は全 liability を 0 とする。

このオプションを付けなくても、借金が一方的に増えたりしないというのが本
稿の結論の一つである。


** 実験

デフォルトでは 20 期実験する(--trial=20)が、ここでは 100 期ずつ実験して
いこう。実験では、コマンドラインに出力される他に Matplotlib を使って、
土地(Land)、知的財産(Intellprop)、貯蓄(Savings)、Liability のヒストグラ
ムを表示する。ちなみにグラフの表示に 1 秒のウエイトを入れている
(--pause=1.0)が、短くしたい場合は 0 はダメなので 0.01 などを指定すると
良い。

<source>
$ python simple_market_a1_01.py --trials=100 --devaluation-of-intellprop
Term: 1
Increase of Intellprop:Savings:Liability : 5829.335614638505:1069.3167302136153:-1065.6832697863806
Total Intellprop:Land:Savings:Liability : 25808.152885063595:19930.0:11044.520408220562:-1065.683269786382
Working: 662
Demand of Luxuries: 299
Total Erosion:Repay : 418.9332647874295:1484.6165345738143
MinLiability == MaxIntellprop ? : False
MaxLiability == MaxIntellprop ? : False

Term: 2
Increase of Intellprop:Savings:Liability : 6069.8490815588775:1999.7442398422645:-1000.2557601577341
Total Intellprop:Land:Savings:Liability : 26048.666351983975:19930.0:13044.26464806282:-2065.939029944117
Working: 804
Demand of Luxuries: 336
Total Erosion:Repay : 567.0943859972828:1567.3501461550125
MinLiability == MaxIntellprop ? : False
MaxLiability == MaxIntellprop ? : False

：
：(途中省略)
：

Term: 98
Increase of Intellprop:Savings:Liability : 5597.875181672069:61.55028035804389:-88.4497196419652
Total Intellprop:Land:Savings:Liability : 25576.692452097388:19930.0:10766.151351493178:-7959.052326513775
Working: 786
Demand of Luxuries: 514
Total Erosion:Repay : 880.5417744638687:968.9914941058191
MinLiability == MaxIntellprop ? : False
MaxLiability == MaxIntellprop ? : False

Term: 99
Increase of Intellprop:Savings:Liability : 5457.650222081142:122.62638375602364:7.626383756019095
Total Intellprop:Land:Savings:Liability : 25436.467492506483:19930.0:10888.77773524921:-7951.425942757758
Working: 736
Demand of Luxuries: 483
Total Erosion:Repay : 907.8063663722769:900.179982616259
MinLiability == MaxIntellprop ? : False
MaxLiability == MaxIntellprop ? : False

Term: 100
Increase of Intellprop:Savings:Liability : 5854.33634042152:698.6881503090663:-366.3118496909301
Total Intellprop:Land:Savings:Liability : 25833.15361084686:19930.0:11587.46588555827:-8317.737792448683
Working: 870
Demand of Luxuries: 509
Total Erosion:Repay : 814.0524613737276:1180.3643110646617
MinLiability == MaxIntellprop ? : False
MaxLiability == MaxIntellprop ? : False

</source>

100期目には fig_sma1_01.png が表示されている。

まず出力の見方であるが、増分(Increase)や集計(Total)についてまず注意すべ
きは --devaluation-of-intellprop や --devaluation-of-liability (今回は
使ってないが…)の処理をする前に、その計算が行われているということであ
る。--devaluation-of-liability を使うと毎期 Liability はほぼ 0 になるが、
このためそうは表示されない。

MinLiability == MaxIntellprop ? と MaxLiability == MaxIntellprop ? につ
いては前者は最小の liability の者すなわち現金を一番持っている者が、一番
知的財産を持っているかを問うている。その次のものは一番借金を持っている
者が、一番知的財産を持っているかを問うている。最初の問いが True になる
ことは珍しく、二番目の問いが True になるのは頻繁ではないがしばしばある。


コマンドラインの結果で注目すべきは、Total Liability であ
る。--devaluation-of-liability をしていないにもかかわらず、-8000 から
-9000 の間で落ち着き一方に向かってずっと増えていったりはしない。

なぜそうなるかは難しい。皆が借金だらけになれば、資産を売った分は、借金
返済にまわるためほぼ給与市場に流入しない上に、給与市場から返済がある分、
釣り合いが取れるようになるのではないか…とまず考えたのだが、今、
Liability のグラフを見ると借金をしていない者はそれなりにいて、そのほう
が多いくらいだ。これは後で他の実験をしてもう少し考えよう。

その前に、グラフに注目しよう。土地に関しては、指数分布のような形でほぼ
安定する。知的財産については、0 で少し下がる山型になるのはずっとだいた
そのようになる。これは特徴的な分布だが何分布なのだろうか？ Liability に
ついては正規分布風だが --bins=100 にしてヒストグラムを細かくすると 0
だけとても大きくなっているのがわかる。これは借金がちょうど完済する場合
に liability が 0 になるのが現れていると思われる。

貯蓄は 30 を上限として 0 以外は一様分布か、整数的なとがりのある分布になっ
ていて、とても指数分布には見えない。動機として、定常状態を求め初期値と
一致させたいみたいなことを言ったが、これではどういう分布にしたらいいの
か今ひとつよくわからない。


** 土地取引の効果

土地取引をなくしてみよう。--initial-land-mean を 0 にするとゼロ除算エ
ラーが出てしまうので、--initial-land-mean=0.1 に設定する。

<source>
$ python simple_market_a1_01.py --trials=100 \
    --devaluation-of-intellprop --initial-land-mean=0.1
</source>

すると、大きな効果はないが、知的財産のグラフが 0 付近が少なめの山型に
なる。これはなぜだろう？ 土地のない分、知的財産価格は低めになるはずな
のに…。

これは、土地取引がある場合、土地があれば知的財産が高く売れるという設定
のため、所持知的財産額が ゼロ付近でも現金需要がある程度満たされ、知的財
産の売り手として取引に参加することが減るからだと思われる。


** 「借金があるほど資産を売りやすい」ことの効果

Erosion と返済が何期かで見るとバランスしていくことについて考えよう。

借金のある者のほうが資産を売りやすく、現金のある者のほうがが買いやすい
から、返済が多くて全 liability が減った場合も、Erosion が多くて全
liability が増えた場合も、逆側に補正が効くのではないかと考えた。もしそ
うなら、「借金のある者のほうが資産を売りやすい…」といった特徴をなくせ
ば、バランスされないことになるはずである。これを試すには --coeff-* を
0 にすればよい。

<source>
$ python simple_market_a1_01.py --trials=100 \
    --devaluation-of-intellprop \
    --coeff-of-intellprop-buyer=0.0 --coeff-of-intellprop-seller=0.0 \
    --coeff-of-land-buyer=0.0 --coeff-of-land-seller=0.0 \
</source>

すると、Total Liability は、-3000 から -6000 の間をフラフラするが、ど
ちらか一方に進むということはなく、バランスしていると言える。なぜだろう？
乱数には何度も尖った選択はなされず「平均への回帰」が起きがちであるため、
それが逆側に補正するのだろうか。

実際、グラフを見ていると、そういう効果がないのに Liability や Interprop
に大きな外れ値が生まれてこない。これは「平均への回帰」が起きているため
と考えられる。

逆に、--coeff-* の傾きを強くしてみよう。

<source>
$ python simple_market_a1_01.py --trials=100 \
    --devaluation-of-intellprop \
    --coeff-of-intellprop-buyer=0.8 --coeff-of-intellprop-seller=0.8 \
    --coeff-of-land-buyer=0.8 --coeff-of-land-seller=0.8 \
</source>

すると、Total Liability は -9000 から -11000 ぐらいをフラフラする。フ
ラフラする範囲が変わっているが、どうして増えたり減ったりしているのかは
私にはわからない。

しかし、Liability を増減できるということは、贅沢品を買える人が増えると
いうことで、これは micro_economy_*.py と組み合わせて経済のコントロール
に使える部分かもしれない…と思って、今度は Demand of Luxuries (贅沢品
需要)に注目して再実行するも、500 付近でほとんど変わらない。Total
Liability が 2000 違うと言っても人数で割れば 2 違う程度だから、それも
当然かもしれない。


** 返済率の効果

贅沢品需要の増減をコントロールする他の方法はないかと、手ごろな返済率を
変えてより贅沢品が売れないか試してみた。

<source>
$ python simple_market_a1_01.py --trials=100 \
    --devaluation-of-intellprop --repayment-rate=0.1
</source>

が、なぜか贅沢品需要はがほぼ変わらない。返済率を 0.1 にすると、貯蓄に回
る分が増えるはずだが、返済が減ってバランスして Erosion も減り、全体とし
て借金体質になることで、貯蓄が増える効果が打ち消されているものと思われ
る。

逆に返済率を 0.9 にしても需要がほぼ変わらない。これは貯蓄に回る分が減る
はずだが、Erosion が増えて、その効果が打ち消されるからではないか。

ちなみに、Erosion と全返済のバランスと全 Liability については、返済率を
0.9 にすると全 Liability は -11000 から -13000 ぐらいでバランスする。逆
に返済率 0.1 の場合、フラフラするが、基本的には増加傾向が続く。どこかで
増加傾向が終る可能性もあるが、バランスのためには返済率が一定以上必要な
のかもしれない。


また --devaluation-of-intellprop を外すのもやってみた、贅沢品需要は少し
大きくなって、これまで 500 だったのが 600 ぐらいにまで上がるが、その程
度である。借金・現金はとめどなく大きくなる。

<source>
$ python simple_market_a1_01.py --trials=100
Term: 1
Increase of Intellprop:Savings:Liability : 5763.594343374316:1663.3216614328194:-1356.6783385671893
Total Intellprop:Land:Savings:Liability : 25425.137822272096:20500.0:11582.95793474365:-1356.678338567196
Working: 725
Demand of Luxuries: 282
Total Erosion:Repay : 228.99943958187134:1585.6777781490625
MinLiability == MaxIntellprop ? : False
MaxLiability == MaxIntellprop ? : True

：
：(途中省略)
：

Term: 100
Increase of Intellprop:Savings:Liability : 1260252811001.291:390.0:829.9999551773071
Total Intellprop:Land:Savings:Liability : 7404254390941.694:20500.0:7995.0:110815.36373853683
Working: 847
Demand of Luxuries: 594
Total Erosion:Repay : 2725.0:1895.0
MinLiability == MaxIntellprop ? : False
MaxLiability == MaxIntellprop ? : False

</source>


** 結論

全 Erosion と全返済はバランスする。おそらくそれは「平均への回帰」がある
ためである。そのためには返済率が一定以上は必要なようである。

バランスした上で、全 Liability はどちらかの方向に一定程度傾くが、その傾
きは贅沢品需要に影響を及ぼすには力が弱すぎる。

返済率を変えるのは、贅沢品需要に影響をほぼ及ぼさない。需要が 500 付近
ということは個人のちょうど半数なので、それは Liability が正規分布的で
Liability がプラスのものとマイナスのものがいることのほうが大事というこ
とかもしれない。

ただ、上では示さなかったが、贅沢品価格を動かした場合は需要は比較的動く。
そう作ったので当然だが、Liability がプラスとマイナスで半々だから需要も
半分の 500 ぐらいに必ずなるというわけではなさそうだ。ちなみに、そうした
上で返済率を変えても意味はなさそうだった。

定常状態を求めるのは、あまりうまくいっていない。指数関数や正規分布その
ままというわけにはいかないらしいことはハッキリした。


今後の課題としては、全 Erosion と全返済のバランスの理由をハッキリさせ、
それがどういう額でバランスするかも示せればカッコイイが、それは私には手
があまる問題のように思う。

次に、これは micro_economy_*.py とあわせることを目標にして、そうプログ
ラムを組んだが、実際、合わせるとなると、資産があるほうが失業する可能性
が高いということをシステムに組み込むべきではないか？…など考えるべきこ
とは多い。いずれやるとは思うが、しばらくはゆっくり他のことを考えたい。

そして、現実「リアル」への今回のことの示唆であるが、それも難しい。ある
程度リアル寄りにもした部分があるが、あまりにも簡易過ぎるのも事実で、ほ
とんど現実への示唆はない。資産市場と商品市場の流出入はあまり考えなくて
もバランスするかもしれない…というのは、それが完全に混ざってしまってい
る現実ではあまり意味もないだろうし。

ただ、個人的には「黒歴史」になるかもと危惧していた simple_market_0.pl
を少し発展させられたことは大きな収穫だと思っている。今回はそれで多とし
たい。


** 参考

Python や Matplotlib についてググっていろいろ参考にしているが、それに
ついては割愛する。また、過去に読んだ経済学・数学・工学の書籍にもよると
ころが大きいだろうが、それも割愛する。それらにはとても感謝している。

  * 『人工市場 - 市場分析の複雑系アプローチ』(和泉 潔 著, 森北出版,
    2003年)。市場のシミュレーションをする意義などの解説のほか、具体的に
    は遺伝的アルゴリズムを用いた外国為替市場のマルチエージェントモデル
    (AGEDASI TOF)の紹介がある。基本的に本稿とはほぼまったく無関係だが、
    p.44 にあるシミュレーションが「ヤッコー」すなわち「ヤッてみたらコー
    なった」式でしかないものになりがちという批判は、残念ながら本稿には
    あてはまるかもしれない。

    https://www.amazon.co.jp/dp/4627850115

  * 《なぜ統計学では釣り鐘型の分布が使われ、物理現象では右肩下がりの分
    布が使われるのか - 小人さんの妄想》。富の分布についてコンタクトし
    て交換…というものが、指数分布を導くことを示している。「コンタクト
    プロセス」とはまた違うが…。

    https://rikunora.hatenablog.com/entry/20170321/p1

  * 《ミクロ経済学の我流シミュレーション》。micoro_economy_*.py。私が
    書いた商品市場のシミュレーション。近い将来、この
    simple_market_a1_*.py と組み合わせたい。

    http://jrf.cocolog-nifty.com/society/2018/03/post.html

  * 《外作用的簡易経済シミュレーションのアイデアと Perl による実装》。
    simple_market_0.pl。今回の記事が更新した経済モデルと言える。が、
    「入れ子構造」や「カタストロフィックな遷移」というアイデアは今回、
    まったく活かされていないので、そこは留意すべき。

    http://jrf.cocolog-nifty.com/society/2011/01/post.html


** 作者

JRF ( http://jrf.cocolog-nifty.com/society/ )


** ライセンス

パブリックドメイン。 (数式のような小さなプログラムなので。)

自由に改変・公開してください。



	資産市場の簡易シミュレーション その２ 論理的モデル進化
	(Created: 2019-06-10)


** 概要

前回のモデルでは知的財産を高く手に入れたほうが、後日高く売れるようになっ
ていた。そのような「経済」であるとわかっていれば、知的財産を高く売る者
を需要側は強く需要するはずである。むしろ、それが新たな「定常状態」のルー
ルになるべきだ。

…と「論理的」に考えはじめたところから、モデルの細かな部分を調整し、そ
の調整した結果が正しいか見るためレポートを充実させる…ということを繰り
返し、モデルをブラッシュアップ(特徴を失わない進歩すなわち「進化」)させ
ていった。

結果、土地は多く持つ者が売るが、そういう者は得てして現金を持っているた
めすぐに別の土地を買い、土地持ちの地位は変わりにくく、一方、知的財産市
場に参入するのは債務者で、贅沢品を買うための手元現金を得るため…となっ
た。

今回はその記録である。


** 準備

これから使うプログラムは実験をいろいろ行ったあと最終的にできた
simple_market_a1_02.py である。これを実験最初のころに遡っておこなうには、
逆にオプションをたくさん付ける必要がある。前回に相当するような実行を行
うには次のように行う。(前回いつも付けてたように --trials=100 と
--devaluatioin-of-intellprop を付ける。)

<source>
$ python simple_market_a1_02.py --trials=100 --pause=1.0 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=cash --sort-of-intellprop-seller=liability \
  --sort-of-land-buyer=cash --sort-of-land-seller=liability \
  --coeff-of-intellprop-buyer=0.3 --coeff-of-intellprop-seller=0.3 \
  --coeff-of-land-buyer=0.8 --coeff-of-land-seller=0.8
Term: 1
Increase of Intellprop:Savings:Liability : 5546.915438333963:2189.8440880233775:-1630.155911976628
Total Intellprop:Land:Savings:Liability : 25378.886167304667:19840.0:11712.441155971996:-1630.1559119766305
Gross Transactions of Intellprop:Land : 4562.819084509181:2410.0
Working: 880
Total Erosion:Repay : 417.153032662548:2047.3089446391768
Demand of Luxuries: 332
Luxuries Bought By Repayer:Number of Erosion:Other : 37:103:192
Number of Liability Minus:Plus : 498:502
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 138:781:620:242:138
Value of MinLiability:MaxLiability : -114.95583429172373:169.14798760983854
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 1:0:0:0:1
Luxuries Mean:Min : 0.332:0
MaxLand Sell:MaxLand Buy ? : False:False
Rank Change Mean: 0.0

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 6119.702110814331:152.64610115180585:-32.35389884819779
Total Intellprop:Land:Savings:Liability : 25951.672839784987:19840.0:11048.949384447938:-7838.647683500699
Gross Transactions of Intellprop:Land : 5008.237910667426:1740.0
Working: 788
Total Erosion:Repay : 926.4275174052559:958.7814162534519
Demand of Luxuries: 513
Luxuries Bought By Repayer:Number of Erosion:Other : 45:152:316
Number of Liability Minus:Plus : 681:319
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 851:763:428:181:446
Value of MinLiability:MaxLiability : -112.8873420790991:122.68306733672749
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 30:9:21:31:25
Luxuries Mean:Min : 24.459:0
MaxLand Sell:MaxLand Buy ? : False:True
Rank Change Mean: 667.418

：
：(途中省略)
：

Term: 100
Increase of Intellprop:Savings:Liability : 5480.019294631496:-133.10627572434896:126.89372427565468
Total Intellprop:Land:Savings:Liability : 25311.99002360202:19840.0:11221.215714458163:-9476.381353490462
Gross Transactions of Intellprop:Land : 4436.48008873659:1650.0
Working: 757
Total Erosion:Repay : 1002.7209946110845:875.8272703354348
Demand of Luxuries: 522
Luxuries Bought By Repayer:Number of Erosion:Other : 39:157:326
Number of Liability Minus:Plus : 688:312
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 337:512:470:135:718
Value of MinLiability:MaxLiability : -144.70654502779354:122.90178488095415
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 60:48:46:74:84
Luxuries Mean:Min : 49.945:17
MaxLand Sell:MaxLand Buy ? : False:False
Rank Change Mean: 781.327

</source>

この先は実行結果を早く見るため --trials=50, --pause=0.5 にする。

前回よりおおむね表示が増えている。それはおいおい説明していこう。


** 知的財産を持っている者ほどよく売れる

知的財産の値決めの特徴から、どうせ手に入れるのならば、知的財産をすでに
多く持っている者から買えば、価格は高いが、高い資産価値のある知的財産が
手に入る。知的財産の取引が起こるとき、需要側は知的財産を持っている者を
選ぼうとする。

これを今回のモデルで表現するには、知的財産の売り手を選ぶのにソートする
とき、知的財産を持っているほうが、売りやすいという形にすればよい。それ
を試すのが、--sorf-of-intellprop-seller=ascend のオプションである。

知的財産を売る側は強く求められるので coeff を 0.8 に、買う側は、高い者
も安い者も共に買いたいだろうということで coeff を 0.3 にした。土地につ
いては現金を持っている者が買おうとするが、売る側は誰もあまり売りたくな
いとみて、買う側の coeff を 0.8、売る側の coeff を 0.3 にした。

こうすることで、知的財産を持つものが、現金を持ちやすくなり、やがて、土
地持ちになるということを予想した。

ちなみに coeff は、前回説明したように、ソートのあと乱数を取るときどれぐ
らい有利になるかの傾斜で、今回は 0.3 と 0.8 の数値を使っているが、0.3
だとそれほど有利にならず、0.8 だとはっきり有利になる…ぐらいの意味があ
る。

<source>
$ python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=cash --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=cash --sort-of-land-seller=liability \
  --coeff-of-intellprop-buyer=0.3 --coeff-of-intellprop-seller=0.8 \
  --coeff-of-land-buyer=0.8 --coeff-of-land-seller=0.3

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 6635.450260042777:-25.03210930689238:214.9678906930967
Total Intellprop:Land:Savings:Liability : 25682.31440043844:19060.0:12412.324503576267:-7971.855787905884
Gross Transactions of Intellprop:Land : 5507.428619933474:1780.0
Working: 702
Total Erosion:Repay : 1354.72638103297:1139.7584903398688
Demand of Luxuries: 484
Luxuries Bought By Repayer:Number of Erosion:Other : 55:200:229
Number of Liability Minus:Plus : 573:427
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 76:664:939:13:756
Value of MinLiability:MaxLiability : -217.8911328617038:144.40466804826806
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 38:18:20:30:46
Luxuries Mean:Min : 24.269:3
MaxLand Sell:MaxLand Buy ? : False:False
Rank Change Mean: 611.092
</source>

結果、グラフの形に大きな変化はない。確かに、知的財産の減価がある状況で
は、「知的財産を高く買ってすぐな者」＝「Liability が高い者」が、知的財
産が高いという性質があるだろうから、Liability が高い者から買う…という
ので十分だったのかもしれない。

「知的財産を持つものが、現金を持ちやすくなり、やがて、土地持ちになる」
というのを調べるために作ったレポートの部分が、
「MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset」になる。こ
れは、プログラムのはじめにプレイヤーに名前となる番号を振っておき、
Liabilitiy 最小：Liability最大：知的財産 最大：土地 最大：純資産 最大の
者を毎期、表示している。

見てみると、知的財産持ちが土地持ちになるということはなさそうだ。これは
もしかすると知的財産市場が小さいためかと思い、--initial-intellprop-mean
を大きくして試してみた。

<source>
$ python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=cash --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=cash --sort-of-land-seller=liability \
  --coeff-of-intellprop-buyer=0.3 --coeff-of-intellprop-seller=0.8 \
  --coeff-of-land-buyer=0.8 --coeff-of-land-seller=0.3 \
  --initial-intellprop-mean=100

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 27873.191409255407:48.64602082730562:613.6460208273038
Total Intellprop:Land:Savings:Liability : 125643.37437923622:19480.0:12593.81113261288:-5016.921125130977
Gross Transactions of Intellprop:Land : 22746.136408461047:1650.0
Working: 680
Total Erosion:Repay : 2554.289893090724:1940.6438722634177
Demand of Luxuries: 491
Luxuries Bought By Repayer:Number of Erosion:Other : 107:305:79
Number of Liability Minus:Plus : 413:587
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 600:436:288:930:600
Value of MinLiability:MaxLiability : -2321.2806916370164:979.3710339405629
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 50:15:13:50:50
Luxuries Mean:Min : 24.451:4
MaxLand Sell:MaxLand Buy ? : False:True
Rank Change Mean: 554.643

</source>

しかし、上の --sort-of-intellprop-seller=liability で
--initial-intellprop-mean=100 としたものに比べて、Liability の裾野は大
きくなっているようだが、知的財産持ちが土地持ちになっている兆候はない。
知的財産の価値を高く維持するためには知的財産を買い続ける必要があり、土
地を買う余裕がないためであろう。

ところで、これで現金のないところからあるところに流れるという道を崩した
わけであるが、それならば、そもそも現金にとらわれない経済も考えられる。
土地を持っているところから土地を持っていないところへ、知的財産を持って
いるところから持っていないところへという経済も考えられるかもしれない。
それを試すのが、--sort-of-intellprop-buyer=descend
--sort-of-intellprop-seller=ascend --sort-of-land-buyer=land
--sort-of-land-seller=land というオプションである。

<source>
$ python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=descend --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=land --sort-of-land-seller=land \
  --coeff-of-intellprop-buyer=0.3 --coeff-of-intellprop-seller=0.8 \
  --coeff-of-land-buyer=0.8 --coeff-of-land-seller=0.3

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 6878.186644256661:-311.7778235269707:-301.77782352696886
Total Intellprop:Land:Savings:Liability : 26568.033185811302:20570.0:11486.385000801945:-9022.099909818839
Gross Transactions of Intellprop:Land : 5758.0897063917455:2830.0
Working: 845
Total Erosion:Repay : 1138.7147776907943:1440.4926012177602
Demand of Luxuries: 564
Luxuries Bought By Repayer:Number of Erosion:Other : 80:199:285
Number of Liability Minus:Plus : 612:388
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 246:754:239:879:246
Value of MinLiability:MaxLiability : -223.62303808760427:190.07905347340343
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 31:12:21:42:31
Luxuries Mean:Min : 24.957:5
MaxLand Sell:MaxLand Buy ? : False:True
Rank Change Mean: 792.855
</source>

結果、グラフは、土地は山型になり、知的財産は、右に伸びた部分があるが山
型がはっきり出てくる。平等なのは良いのだが、この分布は現実的でなさ過ぎ
る。こういう社会主義的分配モデルは、市場経済を考えるにはおかしいだろう。

この他、ソートの方法をいろいろ試したみた。

土地に関しては、土地を持っている者のほうが売れるようにする／売れないよ
うにする。現金を持ってる方が買うようにする／買わないようにする／土地を
持ってない者が買うようにする…などを試した結果、土地を持っている者が売
り、現金を持っている者が買うとするのが一番、安定していると思うようになっ
た。「安定」とは、比較的平等で、0 ばかりが多くなく、それでいて、一番の
土地持ちは離れてあるような、指数分布風になるということである。

知的財産についてもいろいろ試してみた。知的財産の安い者が売り知的財産が
高い者が買うパターンは比較的平等だが、知的財産全体の増分が少ない。知的
財産の高い者が売り、知的財産の高い者が買うパターンは、指数分布的になり、
増分が多く、これはこれで一つの理想形のように思う。知的財産が高い者が売
り、現金のある者が買うパターンも、そこそこ安定している＝全 Liability が
一方的に増えたりしないようであった。

そこで折衷的に、土地の多い者が売るが、現金のある者が買い、知的財産は知
的財産を持っている者が知的財産を持っている者から買うというモデルにする
ことにする。こうすることで、土地をまず買うことが知的財産市場への参入権
に近くなることになり、土地と知的財産の interation があるという感じで、
バランスが良いのではないか？…と考えた。

coeff については、知的財産を売る側は強く求められるので coeff を 0.8 に、
買う側は、それほど関係がないということで coeff を 0.3 にした。土地につ
いては現金を持っている者が買おうとするが、売る側は誰もあまり売りたくな
いとみて、買う側の coeff を 0.8、売る側の coeff を 0.3 にした。

<source>
$ python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=ascend --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=cash --sort-of-land-seller=land \
  --coeff-of-intellprop-buyer=0.3 --coeff-of-intellprop-seller=0.8 \
  --coeff-of-land-buyer=0.8 --coeff-of-land-seller=0.3

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 7935.2095717518605:-4.08898841872724:-149.08898841872906
Total Intellprop:Land:Savings:Liability : 28522.045882611186:19820.0:11773.448073125446:-4492.136441046578
Gross Transactions of Intellprop:Land : 6439.898550210103:2400.0
Working: 757
Total Erosion:Repay : 1232.8436928635838:1381.9326812823106
Demand of Luxuries: 495
Luxuries Bought By Repayer:Number of Erosion:Other : 83:193:219
Number of Liability Minus:Plus : 572:428
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 53:940:299:396:53
Value of MinLiability:MaxLiability : -275.8459691878705:222.8932191396125
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 44:4:28:39:44
Luxuries Mean:Min : 23.703:3
MaxLand Sell:MaxLand Buy ? : False:False
Rank Change Mean: 656.367
</source>

こうすると土地は割と指数関数的でありながら、そこそこ平等になる。土地の
多い者が売っているのに最大値が下がりにくいのはなぜだろう？

「MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset」を見てみる
と土地 最大の者がなかなか変化していない。

そこで作ったのがレポートの「MaxLand Sell:MaxLand Buy ?」の項目である。
これは、土地 最大の者が土地を売ったか、買ったかを示している。

これを毎期見ていると、土地 最大の者は売る機会は意外に少なく見える…とい
うのは売ってすぐはしばしば土地最大でなくなることがあるためであろうし、
買う機会は意外に多く見える。これは買ったから土地最大になった面もあるが、
それ以上に現金を十分持っているため売った金で土地をすぐ買い戻すからだと
考えられる。

土地単価はずっと 10 で、その中から贅沢品を買うこともあるはずなのだが、
一方、土地を持っていれば、土地の分、知的財産が売りやすくなるという特徴
が私のモデルにはあったため、そこで得た現金を土地取引にまわすことができ
るものと思われる。

これが「現実的」なモデルになっているとまずは考える。

この先、土地の多い者が売るが、現金のある者が買うという設定は固定する。


** 逆転のチャンス

いろいろな設定で地位上昇がどれぐらいあるかも調べてみた。個人の最大順位、
最低順位を記録してその(累積)変動の平均を表示した。それがレポートの
Rank Change Mean の項目である。

これまでのところで 667.418, 611.092, 554.643, 792.855, 656.367 と変化は
あるにはあるが、思ったほど違いはないとも言えるかもしれないが、550 と
800 近いのは大きな変化だと考えるべきなのだろう。

土地の多い者が売るが、現金のある者が買うという設定を固定すると、知的財
産を持っている者が知的財産を持っている者を買うときは上のように 656.367。
知的財産を持っていない者が知的財産を持っている者から買うとしたときは
687.057。知的財産を持っている者が知的財産を持っていない者から買うとした
ときは 722.907。知的財産を持っていない者が知的財産を持っていない者から
買う場合、750.252。

貧しい者どうしで取引したほうが良いという意外な結果になる。

現金のある者が知的財産を持っている者から買うとしたときは、663.106。現金
のある者が知的財産を持っていない者から買うとしたときは、743.453。借金の
ある者が知的財産を持っている者から買うとしたときは 688.839。借金のある
者が知的財産を持っていない者から買うとしたときは  716.653。

現金のある者が貧しい者から買えば良いとなる。

上の「社会主義モデル」が Rank Change Mean の大きな変化があるのは、土地
の上位と下位の差が小さいため上下がしやすいからであろう。一方、知的財産
持ちの地位はどのモデルでも激しく変化する。それを調べるのが
--asset-rank=intellprop のオプションである。これを指定して Rank Change
Mean を調べると「社会主義モデル」で、911.47。元の変化が少ない、土地は、
土地持ちが売り現金持ちが買い、知的財産は、知的財産持ちが売り知的財産持
ちが買うという「現実的 」モデルでは Rank Change Mean は、874.126。


** いくつかの予想と結果

先の「現実的」モデル、知的財産を持っている者が知的財産を持っている者か
ら買うとした場合、知的財産の評価に土地がからむことの効果で
--initial-intellprop-mean が小さいほど変動が大きいと予想する。試してみ
ると、--initial-intellprop-mean=20 が上の 656.367。それを 100 にすると
589.652。逆に 10 にすると、669.426。小さいほうは弱いが想定どおりの結果
を得た。

逆に、土地ランクが知的財産にどれぐらい影響を受けるか調べるため
--asset-rank=land として、直上と同じように「現実的」モデル
で --initial-intellprop-mean を変化させてみた。影響は軽微
で、--initial-intellprop-mean:Rank Change Mean = 10:705.34,
20:709.127, 100:722.686 である。知的財産を売った現金で土地が買われるこ
とはあるようだが、その影響は少なそうだ。

Liability が大きくなっても、それを抑制する手段が社会的にない。
Liability は際限なく大きくなるのではないかと予想した。

それを確認するのが「Value of MinLiability:MaxLiability」である。それは
上で確かめていただければわかるように、「現実的」モデルで、Liability に
抑制が効かないはずの場合でも、Liability の最大値はそれほど大きくならな
かったのは少し不思議である。推移を見ていても一方的に大きくなるという感
じではなかった。


** 「現実的」モデル再考

「定常状態」を考えると、知的財産は買わないほうが有利ではないか？ ほと
んどの者は知的財産を買おうとせず、一部の者のみ Liability を気にせず知
的財産を買う…それが「現実的」モデルということでではないか。

そういうことであれば、ほとんどの者は知的財産は売りたいかもしれないが買
おうとしない。すでに知的財産のある者だけが価値維持のために買おうとする
ということで買う側の coeff の傾斜を強く、すなわち
--coeff-of-intellprop-buyer=0.8 にすればよいだろう。

一方、売る側については二つの考え方がある。一つはこれまで通り、買う側の
需要を考え、高い者ほどよく売れるというものである。このと
き、--coeff-of-intellprop-seller=0.8 にすればよい。もう一つは、売る側に
立って、皆が売ろうとしているという面を強調し、前回のように誰が知的財産
を創るかは運の要素が強いと考えるのである。このと
き、--coeff-of-intellprop-seller=0.3 にすればよい。

いずれもにしても、やや意外なことに Liability の最大値が際限なく大きくな
るということはなさそうだ。--coeff-of-intellprop-seller=0.8 のほうが知
的財産最大の者(MaxIntellprop) がやがて純資産最大の者(MaxAsset) になるな
どドラマがあるので、そちらのほうがよさそうに思う。これを新「現実的」モ
デルとする。

<source>
python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=ascend --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=cash --sort-of-land-seller=land \
  --coeff-of-intellprop-buyer=0.8 --coeff-of-intellprop-seller=0.8 \
  --coeff-of-land-buyer=0.8 --coeff-of-land-seller=0.3

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 7205.496610344628:-169.11165912155047:65.88834087845134
Total Intellprop:Land:Savings:Liability : 27006.837357255998:19680.0:11483.732920268245:-6888.655691132185
Gross Transactions of Intellprop:Land : 5842.166655180663:2400.0
Working: 767
Total Erosion:Repay : 1294.6346068293064:1228.746265950857
Demand of Luxuries: 527
Luxuries Bought By Repayer:Number of Erosion:Other : 61:200:266
Number of Liability Minus:Plus : 598:402
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 759:949:415:151:572
Value of MinLiability:MaxLiability : -279.53217282780383:245.23138262445127
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 39:9:12:28:39
Luxuries Mean:Min : 24.944:6
MaxLand Sell:MaxLand Buy ? : True:True
Rank Change Mean: 669.082
</source>

あと、後述のため、--coeff-of-intellprop-seller=0.3 の場合も載せておこ
う。

<source>
python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=ascend --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=cash --sort-of-land-seller=land \
  --coeff-of-intellprop-buyer=0.8 --coeff-of-intellprop-seller=0.3 \
  --coeff-of-land-buyer=0.8 --coeff-of-land-seller=0.3

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 6133.165607545234:-670.7183330615608:264.28166693842377
Total Intellprop:Land:Savings:Liability : 24752.955182139896:18240.0:11765.008297993281:-6560.379935692357
Gross Transactions of Intellprop:Land : 4885.240870731993:2420.0
Working: 634
Total Erosion:Repay : 1200.5759008755501:936.2942339371128
Demand of Luxuries: 485
Luxuries Bought By Repayer:Number of Erosion:Other : 54:171:260
Number of Liability Minus:Plus : 631:369
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 425:623:623:675:822
Value of MinLiability:MaxLiability : -270.7852020784404:199.19868532306873
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 31:18:18:39:43
Luxuries Mean:Min : 24.588:5
MaxLand Sell:MaxLand Buy ? : False:True
Rank Change Mean: 694.192
</source>


** 贅沢品需要

平等さを測る指標として、グラフの平坦さや、Rank Change Mean を見てきた
が、それ以外に、実際どれだけ贅沢品を買う余裕があったかを調べることがで
きる。それがこれまでレポートの中に出て来た「Luxuries of
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset」や「Luxuries
Mean」である。

贅沢品は基本、現金持ちまたは土地持ちが一番買っているようだ。土地持ちは
金まわりがいいのだろう。ただ、初期はそうではないのは、金持ちが土地持ち
になってからその効果が出るということだろう。知的財産取引でトップにいる
者は、贅沢品をあまり買えていない場合も普通に買えている場合もあり、マチ
マチなようだ。

直前の節で、--coeff-of-intellprop-seller=0.3 の場合、現金が知的財産を持
つ者から持たない者へ移転されることで、平均の贅沢品需要が増えるのではな
いかと予想した。が、そうならなかった。24.944 から 24.588 へとわずかだが
逆に減っている。知的財産を持つ者の現金が不足するからだろうと思われる。
知的財産を持つ者は、安く知財を買って高く知財を売ることで現金を作り出す
のだと思われ、借金一辺倒になるわけではないようだ。


** 返済率の謎

前回の実験で「返済率」すなわち --repayment-rate を変えても贅沢品需要が
変化しないことがわかったが、これが不思議であった。それを調べるために作っ
たレポートが、「Luxuries Bought By Repayer:Number of Erosion:Other」の
部分である。ここで --repayment-rate を 0.5 から 0.1 や 0.9 に変化させて
みると「贅沢品のうち返済者に買われた分」＝「Bought By Repayer」の部分は
確かにかなり変化するのだが、それを他が補うようだ。「他」というのは
「贅沢品を買うときに Erosion が起きた数」＝「Number of Erosion」と「両
者を除いた数」＝「Other」も変化するということである。

そこで気になって調べることにしたのが、「Liability の現金持ちと借金持ち
の割合」＝「Number of Liability Minus:Plus」である。これを見ると、返済
率が変われば、割合が変わっていて、これが影響してそうだ。0.1 だと借金持
ちが多いが返済が少なく、0.9 だと借金持ちが少ないが返済が多い。


** インパクト実験

前回、なんとか贅沢品需要がコントロールできないかと考えた。半ば無理矢理
にでも…ということで --cash-margin というのを考えた。機能としては消費者
金融的で、借金があってもそのマージンの分だけはさらに借金して贅沢品が買
えるというものである。

しかし、これも効果はほぼ一時的なようである。最初借りて消費できても結局
使い過ぎれば再び貯めなければならなくなる。ただ、一時的な効果はある…と
いうことを確かめるために 30 期になったときに cash margin を足し 40 期に
なったら同額引く --add-cash-margin-30 というオプションを作り試してみた
ら、やはり 30 期になったら消費が増え、40期になったら大きく落ち込むよう
になった。新「現実的」モデルで試す。

<source>
python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=ascend --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=cash --sort-of-land-seller=land \
  --coeff-of-intellprop-buyer=0.8 --coeff-of-intellprop-seller=0.8 \
  --coeff-of-land-buyer=0.8 --coeff-of-land-seller=0.3 \
  --add-cash-margin-30=10

：
：(途中省略)
：

Term: 29
Increase of Intellprop:Savings:Liability : 7791.132233834742:-235.45183627346705:109.54816372653022
Total Intellprop:Land:Savings:Liability : 28028.136611414506:18180.0:12255.783012081369:-5307.897378226973
Gross Transactions of Intellprop:Land : 6309.120447039216:2350.0
Working: 753
Total Erosion:Repay : 1410.8310482996262:1301.2828845730928
Demand of Luxuries: 525
Luxuries Bought By Repayer:Number of Erosion:Other : 68:200:257
Number of Liability Minus:Plus : 582:418
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 557:628:720:606:190
Value of MinLiability:MaxLiability : -204.93925725207373:199.09862556208765
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 19:6:17:25:29
Luxuries Mean:Min : 14.049:0
MaxLand Sell:MaxLand Buy ? : True:True
Rank Change Mean: 557.554

Term: 30
Increase of Intellprop:Savings:Liability : 8073.831354290269:-1678.652930256123:81.34706974387518
Total Intellprop:Land:Savings:Liability : 28310.83573187001:18180.0:10577.130081825238:-5226.550308483097
Gross Transactions of Intellprop:Land : 6595.2450820565755:2490.0
Working: 859
Total Erosion:Repay : 1554.3025713190277:1472.9555015751491
Demand of Luxuries: 690
Luxuries Bought By Repayer:Number of Erosion:Other : 107:249:334
Number of Liability Minus:Plus : 588:412
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 190:628:923:581:192
Value of MinLiability:MaxLiability : -223.35789263969403:214.4828973789294
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 30:6:21:14:16
Luxuries Mean:Min : 14.739:0
MaxLand Sell:MaxLand Buy ? : False:False
Rank Change Mean: 564.21

：
：(途中省略)
：

Term: 39
Increase of Intellprop:Savings:Liability : 7675.163990340396:-239.09269846934512:995.9073015306536
Total Intellprop:Land:Savings:Liability : 27912.168367920174:18180.0:8682.83147266685:-375.8489176414813
Gross Transactions of Intellprop:Land : 6371.880654867939:2360.0
Working: 625
Total Erosion:Repay : 2157.9599305449774:1162.0526290143234
Demand of Luxuries: 499
Luxuries Bought By Repayer:Number of Erosion:Other : 51:261:187
Number of Liability Minus:Plus : 541:459
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 69:18:263:25:190
Value of MinLiability:MaxLiability : -262.54165605571256:243.77615472632732
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 36:15:19:31:39
Luxuries Mean:Min : 19.588:0
MaxLand Sell:MaxLand Buy ? : True:True
Rank Change Mean: 617.397

Term: 40
Increase of Intellprop:Savings:Liability : 6793.819754953867:2456.263364447026:-38.73663555297526
Total Intellprop:Land:Savings:Liability : 27030.824132533628:18180.0:11139.094837113873:-414.5855531944548
Gross Transactions of Intellprop:Land : 5509.310114839025:2330.0
Working: 719
Total Erosion:Repay : 1365.7613536898755:1404.4979892428523
Demand of Luxuries: 313
Luxuries Bought By Repayer:Number of Erosion:Other : 37:177:99
Number of Liability Minus:Plus : 524:476
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 69:562:517:25:923
Value of MinLiability:MaxLiability : -257.54165605571256:244.7290675071564
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 37:17:15:32:30
Luxuries Mean:Min : 19.901:0
MaxLand Sell:MaxLand Buy ? : False:False
Rank Change Mean: 622.648

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 7513.211257871157:33.71824372233641:-26.281756277644718
Total Intellprop:Land:Savings:Liability : 27750.21563545087:18180.0:12187.111088884149:-2031.5693014241672
Gross Transactions of Intellprop:Land : 6218.458256222911:2460.0
Working: 681
Total Erosion:Repay : 1184.7108298257897:1210.9925861034471
Demand of Luxuries: 450
Luxuries Bought By Repayer:Number of Erosion:Other : 59:174:217
Number of Liability Minus:Plus : 540:460
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 202:555:189:581:202
Value of MinLiability:MaxLiability : -387.3609180919569:227.40028482253902
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 45:14:25:34:45
Luxuries Mean:Min : 24.626:4
MaxLand Sell:MaxLand Buy ? : True:False
Rank Change Mean: 664.211
</source>

「贅沢品需要」＝「Demand of Luxuries」に注目して欲しい。それまで 500
ぐらいをうろうろしていたのが30期に一気に 600 を越えるが、39期になると
その効果は完全になくなっており、40期に --cash-margin がなくなると、今
度は 400 未満に落ち込んでしまう。しばらくして 50 期になるとすっかり回
復はしている…となる。

そういえば、価格の効果は一時的ではなかったということで、税を増減したこ
とに相当する --add-price-of-wages-30 と --add-price-of-luxuries-30 を作
り試してみた。--add-price-of-wages-30 は意外なことに、30 期では逆効果に
なる。それは、贅沢品需要の決定において、給与に比べて貯蓄が十分にあるこ
とが関係している(curS * 3 が base になっている)から
だ。--add-price-of-luxuries-30 の場合はそういうことはないが、ただ、いき
なり効くという感じではなくジワジワ効くようだ。

「金融政策」は効果が一時的で、「消費税」の増減が一番効果があり、長期的
性質も良い。…となるわけだが、micro_economy_*.py と組み合わせたとき、こ
れら「税」の効果は、明らかではなく、価格がモデルの外側のためこういうこ
とが言えるだけで、モデルの内側で対応されれば、cash margin や repayment
rate と同じような感じになるのかもしれないのは注意すべきであろう。


** 新「現実的」モデル再考

借金地獄に陥ってしまうと、そこから復帰するチャンスがなくなるのではない
か？ それをなくすには、土地をまず買ってそこから知財を買ってもらうという
形が一番いいのではないか。

土地は現金があるほうが買おうとするが、ない者も逆転のために買おうとする
ため --coeff-of-land-buyer=0.3 とする。土地の多い者ほど土地を売るという
ことはないが、多い者は金持ちであることが多く、すぐ買い戻せるのに対し、
土地の少ない者はとにかくその土地にしがみつき売ろうとしない…ということ
で--coeff-of-land-seller=0.8 とする。つまり 0.3 と 0.8 をこれまでと逆に
する。

<source>
python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=ascend --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=cash --sort-of-land-seller=land \
  --coeff-of-intellprop-buyer=0.8 --coeff-of-intellprop-seller=0.8 \
  --coeff-of-land-buyer=0.3 --coeff-of-land-seller=0.8

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 8786.44117651806:757.9733941569448:-432.0266058430543
Total Intellprop:Land:Savings:Liability : 29498.444328506244:20780.0:11503.489328162783:-4599.383373485249
Gross Transactions of Intellprop:Land : 7230.2769181629255:2890.0
Working: 878
Total Erosion:Repay : 1058.6112456197102:1490.637851462768
Demand of Luxuries: 506
Luxuries Bought By Repayer:Number of Erosion:Other : 67:192:247
Number of Liability Minus:Plus : 597:403
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 88:970:439:172:88
Value of MinLiability:MaxLiability : -378.1308967105777:319.33606558832236
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 40:11:33:21:40
Luxuries Mean:Min : 24.879:3
MaxLand Sell:MaxLand Buy ? : True:True
Rank Change Mean: 713.207
</source>

これを第三「現実的」モデルとする。「現実的」なのに、Rank Change Mean が
669.082 から 713.207 に改善している。貧しい者の抵抗をある程度、組み入れ
たからであろう。


** 土地と知的財産、再考

土地上位者がその地位を維持できるのは、贅沢品消費しても、いくぶん土地が
あることで知的財産が売れて現金が入ってくるからと思われる。よって、知的
財産評価に土地をからませないようにすれば、土地上位が頻繁に入れ替わるよ
うになるだろう。それを --intellprop-land-mag=0.0 で指定できるようにし
て第三「現実的」モデルで試すと、そのような結果が得られた。これはこれま
での「現実的」モデルのように --coeff-of-land-seller=0.3 では観測しにく
い。

<source>
python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=ascend --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=cash --sort-of-land-seller=land \
  --coeff-of-intellprop-buyer=0.8 --coeff-of-intellprop-seller=0.8 \
  --coeff-of-land-buyer=0.3 --coeff-of-land-seller=0.8 \
  --intellprop-land-mag=0.0

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 4870.038493898726:616.0192090046239:-273.98079099538427
Total Intellprop:Land:Savings:Liability : 23976.550170616505:19220.0:11870.618252621334:-8113.657289470478
Gross Transactions of Intellprop:Land : 3809.136802651196:2890.0
Working: 863
Total Erosion:Repay : 918.6125904769074:1192.5933814722828
Demand of Luxuries: 516
Luxuries Bought By Repayer:Number of Erosion:Other : 57:169:290
Number of Liability Minus:Plus : 643:357
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 537:11:62:405:537
Value of MinLiability:MaxLiability : -314.4350006300058:204.7780823707758
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 34:15:20:28:34
Luxuries Mean:Min : 24.15:1
MaxLand Sell:MaxLand Buy ? : False:False
Rank Change Mean: 727.086
</source>


** 逆転一発モデル

これまでのところで知的財産を買うのは不利にしかならないことが明らかになっ
てきた。多くの人は知的財産を売りたいがために知的財産を必要とするかもし
れないが、知的財産を買う人間がいないのでは意味がない。

なぜ、買えば不利になるだけの知的財産を買おうとするのだろうか。それはそ
もそも不利な地位にあるから一発逆転を狙うからではないかと考え直した。

例えば、Liability のある者ほど一発逆転を狙って知的財産購入に参加するモ
デル、これは --sort-of-intellprop-buyer=liability で指定できる。または、
純資産を持っていないほど知的財産購入に参加するモデル、これ
は、--sort-of-intellprop-buyer=poor で指定できるようにした。

第三「現実的」モデルを元に実験する。

<source>
python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=liability --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=cash --sort-of-land-seller=land \
  --coeff-of-intellprop-buyer=0.8 --coeff-of-intellprop-seller=0.8 \
  --coeff-of-land-buyer=0.3 --coeff-of-land-seller=0.8

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 7473.942875879551:441.9786856861265:-403.02131431387306
Total Intellprop:Land:Savings:Liability : 28174.251857084902:18510.0:11254.588250117762:-2139.12726662186
Gross Transactions of Intellprop:Land : 6110.665738376889:2730.0
Working: 872
Total Erosion:Repay : 1254.9305707055203:1657.9518850193913
Demand of Luxuries: 525
Luxuries Bought By Repayer:Number of Erosion:Other : 78:235:212
Number of Liability Minus:Plus : 564:436
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 458:208:208:686:458
Value of MinLiability:MaxLiability : -173.69583341020456:224.14318664012495
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 29:17:17:29:29
Luxuries Mean:Min : 24.755:5
MaxLand Sell:MaxLand Buy ? : False:False
Rank Change Mean: 765.526
</source>


<source>
python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=rigid \
  --sort-of-intellprop-buyer=poor --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=cash --sort-of-land-seller=land \
  --coeff-of-intellprop-buyer=0.8 --coeff-of-intellprop-seller=0.8 \
  --coeff-of-land-buyer=0.3 --coeff-of-land-seller=0.8

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 6595.1984961163835:409.7428267654377:-190.25717323455183
Total Intellprop:Land:Savings:Liability : 26749.15163200843:18920.0:10893.912696559186:-2228.097252774705
Gross Transactions of Intellprop:Land : 5336.587256637077:2690.0
Working: 810
Total Erosion:Repay : 1111.636047374629:1301.8932206091877
Demand of Luxuries: 500
Luxuries Bought By Repayer:Number of Erosion:Other : 51:203:246
Number of Liability Minus:Plus : 587:413
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 469:655:203:677:541
Value of MinLiability:MaxLiability : -157.49700869068928:178.48945802931615
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 32:19:15:42:20
Luxuries Mean:Min : 24.928:3
MaxLand Sell:MaxLand Buy ? : True:False
Rank Change Mean: 783.034
</source>

ソートが poor でも liability でも Rank Change Mean は大して変わらない
が、liability にしたほうが最大 Liability が大きくなる。が、際限なく大
きくなる様子でもないのは少し不思議で、一安心。

実験したとき、MaxLiability の贅沢品消費がやたらと少なかったりした。ど
うも失業者が消費できないのが関係してそうだ。そこで、最低の贅沢品消費が
どれぐらいかをこの段階になってやっと知ろうとして作ったレポートが、
Luxuries Min になる。

しばらくいろいろ考え直してみて、--sort-of-intellprop-buyer=liability の
ほうが正しいと思えるようになった。なぜなら、知的財産を買ったそのときは
知的財産の評価額が払った額より大きいのだから、純資産はプラスになり、そ
れで満足するということになりかねない。あくまで現金が得られるまで知的財
産を買うほうが自然なように思う。そうすることで、失業者が消費をできるチャ
ンスが増えるのではないか。しかし、Luxuries Min を観測すると、良くない。
また、「一発逆転」はどうもできていない。

知的財産を多く持っている者はさらに多く買おうとするという効果も考慮した
い。そうすることで高く知財を手に入れられる者が多くなり、失業者の消費チャ
ンスも増えないか。--sort-of-intellprop-buyer=hybrid がそれ。でも、それ
もうまくいかない。Luxuries Min はなかなか上がって来ない。これはあまり
意味がなかった。


** 手元現金

失業者が消費をできるチャンスを増やそうと、土地や知的財産のその期の売り
上げ(cur_sell)からなら、贅沢品を買ってもよいとしてみた。それを試すの
が、--cash-on-hand=loose になる。cur_sell から返済もすべきか迷ったが、
Erosion にされなかった分はすべて liability に反映されることでヨシとした。

<source>
python simple_market_a1_02.py --trials=50 --pause=0.5 \
  --devaluation-of-intellprop --asset-rank=net --cash-on-hand=loose \
  --sort-of-intellprop-buyer=liability --sort-of-intellprop-seller=ascend \
  --sort-of-land-buyer=cash --sort-of-land-seller=land \
  --coeff-of-intellprop-buyer=0.8 --coeff-of-intellprop-seller=0.8 \
  --coeff-of-land-buyer=0.3 --coeff-of-land-seller=0.8

：
：(途中省略)
：

Term: 50
Increase of Intellprop:Savings:Liability : 7421.155081635061:154.51083462616043:-45.4891653738423
Total Intellprop:Land:Savings:Liability : 26475.727558419687:19960.0:6969.278396206698:2461.0137016147955
Gross Transactions of Intellprop:Land : 6113.564321908445:2910.0
Working: 788
Total Erosion:Repay : 1659.601230033405:1705.0903954072478
Demand of Luxuries: 512
Luxuries Bought By Repayer:Number of Erosion:Other : 142:275:129
Number of Liability Minus:Plus : 585:415
MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 374:778:638:114:723
Value of MinLiability:MaxLiability : -148.8548138143931:226.28476997726528
Luxuries of MinLiability:MaxLiability:MaxIntellprop:MaxLand:MaxAsset : 42:6:22:26:28
Luxuries Mean:Min : 25.426:6
MaxLand Sell:MaxLand Buy ? : True:False
Rank Change Mean: 735.212
</source>

今回は、グラフも載せておこう。fig_sma1_02.png がそれになる。

結果、--sort-of-intellprop-buyer=liability でも Luxuries Min がかなり改
善された。最大 Liability も一方的に増える感じではない。

直前に試した --sort-of-intellprop-buyer=liability --cash-on-hand=loose
なものを第四「現実的」モデルとする。

手元現金を得るため、借金持ちが知財市場に参入するというストーリー。「一
発逆転」はとても難しくても手元現金が欲しいということなら、意味がある。
ただ、現金を浪費しがちということで、Rank Change Mean は悪くなるのを予
想したが、今回はそうなっている。


** 全 Liability の増大

なお、--initial-intellprop-mean=100 などにすると、最大 Liability の増大
はそれほどでもないが、全 Liability は確実に増大する。これは 
--cash-on-hand=rigid でもそうで、第三「現実的」モデルまではなんとか全
Liability の増大は抑えられているが、それ以降はまったくダメになる。そも
そも最初の「現実的」モデルでさえ増大はしていく。これらは些細な変更に対
して頑健ではないということで「現実的」と言えないのかもしれない。

デフォルトの --initial-intellprop-mean=20 の場合、それが抑えられている
のは知的財産に対する土地の効果で知的財産を売るのが黒字になるからかもし
れない。しかし、その割には「土地と知的財産、再考」のところの例は、土地
の効果がなくても全 Liability の増大は起きておらず、よくわからないことに
なっている。

知的財産の平均を増やすときは、わずかに給与を増やして返済額が増えるよう
にしないといけないのかもしれない。何度か試してそうすれば釣り合いが取れ
る数値(+1 から +3)があるようだった。その数値の求め方が将来わかって、そ
れも加味できるなら頑健さは保たれているというべきで「現実的」と呼び続け
てもいのかもしれない。


** 結論

実験で試行錯誤しながらモデルを「改善」していていったのをそのまま書いて
みた。

階級変動があるからすなわちモデルが正しいという見方はしなかったが、それ
を参考にしたこともある。これは社会政策的アプローチだろう。

一方、値決めの性質などから、「現実的」ということを追及していった面もあ
る。これはインセンティブ指向のアプローチだろう。

できたモデルは中庸のモデルだが、ある意味論理的な帰結でもある。その帰結
たる第四「現実的」モデルの特徴をまとめると次のようになる。

  * 知的財産の値決めの特徴から、知的財産を持っている者の物が強く需要さ
    れるため、売る者は知的財産を持っている者が確実に多い。
  
  * 知的財産を買わずに売ろうとする者は多い。知的財産の購入に参入するも
    のは、手元現金を得るための借金持ちが多い。

  * 借金地獄に陥いらないために、土地をまず買ってそこから知財を買っても
    らうという形が一番よいだろう。土地は現金があるほうが買おうとするが、
    ない者も逆転のために買おうとするため、傾きは緩い。

  * 土地の多い者ほど土地を売るということはないが、多い者は金持ちである
    ことが多くすぐ買い戻せるのに対し、土地の少ない者はとにかくその土地
    にしがみつき売ろうとしないため、結果的に土地の多い者のほうが確実に
    売っているとする。

第四「現実的」モデルではなく第三「現実的」モデルにする場合は、2番目の
ものが次のようになる。

  * 知的財産を買わずに売ろうとする者は多い。知的財産を購入する者は知的
    財産の価値を維持するため買い増そうとする知的財産をすでに持っている
    者である。

一つの指針を決めて、それで人工知能なり遺伝的アルゴリズムなりで、経済が
自動的に構成されたならまだしも、今回は、曖昧な基準で「中庸」の結果を出
したに過ぎず、それにどれだけ意味があるかと問われると弱い。


途中、インパクト実験として、途中の期に無理矢理の変化を起こす実験もした。
これはひょっとしたら記事を分けたほうが良かったかもしれないが、分けたと
しても短くなり過ぎるので、こちらにまとめた。

インパクト実験の結果としては、「金融政策」は効果が一時的で、「消費税」
の増減が一番効果があり、長期的性質も良い。…とはしたが、「税」の効果は、
他のモデルと組み合わせたときには明らかではなく、価格がモデルの外側のた
めこういうことが言えるだけで、モデルの内側で対応されればどうなるかわか
らないのは注意すべきであろう。


** 参考

前回にまとめてある。


** 作者

JRF ( http://jrf.cocolog-nifty.com/society/ )


** ライセンス

パブリックドメイン。 (数式のような小さなプログラムなので。)

自由に改変・公開してください。



(This file was written in Japanese/UTF8.)
