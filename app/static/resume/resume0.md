### 基本情况
+ 姓名：王贤
+ 学校：太原科技大学
+ 专业：网络工程
+ 手机：18335103278
+ 邮箱：1144542900@qq.com
+ 生日：1994.08
+ 毕业时间：2016.06
+ [github](http://www.github.com/shfshanyue)

### 技能
+ 熟悉python常用标准库，对django, flask, webpy等框架有所了解。
+ 熟悉linux常用命令，对git，vi有所了解。
+ 熟悉html5, css3，略微熟悉vue, 对angular, jquery有所了解。
+ 熟悉javascript, 略微熟悉node，ES6，coffee，jade，xss，csrf，express, socket.io有所了解。
+ 熟悉gulp，scss，less，对webpack有所了解。
+ 熟悉http，websocket协议，对tcp/ip，arp有所了解，能够使用firebug，wireshark进行抓包分析。
+ 对mysql，mongo有所了解。
+ 使用过sae，leancloud等云平台。

### 小项目：
+ [网页版记事本](https://github.com/shfshanyue/notebook)
> __vue，html5__
> 使用localstorage存储数据，平时可以用来做笔记。使用mvvm框架，数据驱动DOM，避免频繁操作DOM的而致使的复杂和低效。

+ [百度贴吧的爬取和展示](https://github.com/shfshanyue/notebook)
> __requests，bs4，leancloud，flask，vue，vue-router，webpack__
> 选取的是本校贴吧最火的一篇帖子(一万多回复)。requests和bs4做数据提取，leancloud做数据存储，设置cron每日凌晨更新。前后端进行分离，后端使用flask提供API，设置Access-Crontrol-Allow-Origin头允许跨源。前端使用ajax异步请求数据，vue使用组件进行开发，vue-router做前端路由，webpack提供一些模块打包功能，如sass，babel，postcss，css scoped，hot-reload，使开发变得更加高效。

+ [百度贴吧自动签到及发帖](https://github.com/shfshanyue/tieba_post)
> __requests，firebug__
> 使用requests做持久性Session，使用firebug抓包，模拟数据进行签到发帖。设置cron实现每日自动签到与发帖。
> 可以做更有趣的事，结合bs4进行抢楼，只回复某人贴，调用图灵机器人的API进行智能回复。

+ [百度贴吧爬虫node版](https://github.com/shfshanyue/tieba_spider)
> __superagent，cheerio，async，ES2015，babel__
> superagent做http请求，cheerio分析和提取相应的文本，使用async控制并发数为10。

+ [2048 web版](http://tiankui.avosapps.com/2048)
> __coffee，sass__
> 使用coffee开发为了体验class，箭头函数等带来的便捷以及python式的语法，更像是javascript的语法糖。使用sass的计算性计算格子大小，根据位置设置样式。

+ [群聊天室](http://chater.avosapps.com/chat)
> __socket.io__
> 当浏览器支持websocket，socket.io会使用websocket，不支持时也会自动降级。仅仅使用提供的API，而无须知道原理便可以做出一个聊天室。
