# pingscope
Measuring and graphing ping

## Concept
Returns the ping result as an integer value in milliseconds and outputs an image

### Ping result
```
#{"Dst": "www.google.com", "Count": 5}
12
11
11
12
11
#{"Avg": 12, "Min": 11, "Max": 12, "ElapsedTime": 5.056681200047024}
```

### PNG
![](./images/usage.png)

## What is ping
### Purpose
- Confirm communication with communication partner and measure response speed

### Command
`ping www.google.com -n 5`

### Result
```
www.google.com [x.x.x.x]に ping を送信しています 32 バイトのデータ:
x.x.x.x からの応答: バイト数 =32 時間 =10ms TTL=119
x.x.x.x からの応答: バイト数 =32 時間 =11ms TTL=119
x.x.x.x からの応答: バイト数 =32 時間 =11ms TTL=119
x.x.x.x からの応答: バイト数 =32 時間 =13ms TTL=119
x.x.x.x からの応答: バイト数 =32 時間 =13ms TTL=119

x.x.x.x の ping 統計:
    パケット数: 送信 = 5、受信 = 5、損失 = 0 (0% の損失)、
ラウンド トリップの概算時間 (ミリ秒):
    最小 = 10ms、最大 = 13ms、平均 = 11ms
```

## What is possible
1. Returns the ping execution result as an integer value in milliseconds
2. Output ping results as images

## Reason for development
- I would like to obtain the round trip time (hereinafter referred to as __RTT__), which is the ping result, as an integer value in milliseconds to make it easier to process
- I want to output RTT as an image so that I can understand it at a glance
- I want to express the stability of RTT using color

## RTT tiers
|Rank|Range|Color image|Color name|Color code|
|:-:|:-:|:-:|:-:|:-:|
|S|0 - 9ms|![](https://via.placeholder.com/16/0000ff/FFFFFF/?text=%20)|Blue|#0000FF|
|A|10 - 14ms|![](https://via.placeholder.com/16/a0d8ef/FFFFFF/?text=%20)|Skyblue|#87CEEB|
|B|15 - 19ms|![](https://via.placeholder.com/16/00ff00/FFFFFF/?text=%20)|Green|#00FF00|
|C|20 - 29ms|![](https://via.placeholder.com/16/ffff00/FFFFFF/?text=%20)|Yellow|#FFFF00|
|D|30 - 49ms|![](https://via.placeholder.com/16/ee7800/FFFFFF/?text=%20)|Orange|#FFA500|
|E|50ms over|![](https://via.placeholder.com/16/ff0000/FFFFFF/?text=%20)|Red|#FF0000|

## Versions

|Version|Summary|
|:--|:--|
|0.1.6|Release pingscope|

## Installation
### [pingscope](https://pypi.org/project/pingscope/)
`pip install pingscope`

## CLI
### ping
Execute ping and create image

#### 1. Image(PNG) conversion by CLI execution

```
ping # <ping file name> <dst>
  [With value]
    -c|--count     5  # Count
    -m|--max-count 30 # Max count
```
`pingscope ping google www.google.com`
```
google.ping is done.
google.png is done.
```
