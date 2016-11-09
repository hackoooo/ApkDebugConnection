####ApkDebugConnection

一条命令搞定本地端口映射到设备中某个运行的apk的jdwp对应的端口。

####前言
假设我们要debug的apk为 `com.hackooo.example.apk` , 
apk的packageName为`com.hackooo.example` ,
apk启动的Activity为`com.hackooo.example.biz.SplashActivity`.

在debug一些apk的时候，是不是已经厌倦了以下这些重复的步骤：

1. adb shell am start -D -S -W com.hackooo.example/.biz.SplashActivity
2. 然后等待10s左右，告诉你已经超时了
3. 接着 adb shell ps | grep com.hackooo.example 查看对应的进程的pid
4. adb forward tcp:8800 jdwp:{pid,上一步得到的pid}

这几条命令虽然不是很复杂，但敲起来也得十几二十秒，关键是，在debug的时候，要一直重复，非常麻烦。
好了，写个脚本搞定这些无聊的步骤。

####如何使用
首先修改配置文件 env.conf
```
[config]
;adb 路径,修改为你自己的adb的路径
adb = ~/Library/Android/sdk/platform-tools/adb
;aapt 路径，修改为你自己的aapt的路径
aapt = ~/Library/Android/sdk/build-tools/23.0.2/aapt
;设备中apk运行的进程映射到本地的端口，这个随意定，不要与其它端口冲突即可。
targetport = 8800

```
然后执行 `./adbConnect.py {your apk}` (前提是你已经安装了这个apk)

对应到上面的例子，就是`./adbConnect.py com.hackooo.example.apk`

接着就可以用你的Android Studio 连接端口痛快debug啦！

####脚本的基本思路
其实跟手动敲是一样的，只不过在启动应用的时候把超时改短一点，不用等太久。

1. 拿到apk后，用aapt解析出apk的packageName和启动的Activity
2. 执行`adb shell am start -D -S -W {activity}`  , 并加上3s的超时，不用等10s
3. `adb shell ps | grep {packageName}` 拿到进程的pid
4. `adb forward tcp:{targetport} jdwp:{pid}`

---
有任何问题欢迎交流。
