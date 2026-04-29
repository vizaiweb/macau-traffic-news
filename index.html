<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DSAT 交通廣播監控系統</title>
    <style>
        :root {
            --red: #e63946;
            --gold: #ffca28;
            --bg: #050505;
            --header-h: 12vh;
            --footer-h: 12vh;
        }

        /* 全域佈局：固定三段式，禁止捲動 */
        body {
            margin: 0; padding: 0; background: var(--bg); color: white;
            font-family: "PingFang HK", "Microsoft JhengHei", sans-serif;
            height: 100vh; width: 100vw;
            display: grid;
            grid-template-rows: var(--header-h) 1fr var(--footer-h);
            overflow: hidden;
        }

        /* 1. 頂部區域 */
        .header {
            background: var(--red);
            display: flex; align-items: center; justify-content: center;
            position: relative; z-index: 100;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }

        .date-display {
            position: absolute; left: 20px;
            font-size: 2.5vh; font-family: Arial, sans-serif;
        }

        /* 標題自適應容器 */
        #ui-title {
            width: 55%;
            text-align: center;
            font-weight: 900;
            line-height: 1.2;
            display: flex;
            align-items: center;
            justify-content: center;
            /* 預設大小，JS會根據長度調整 */
            font-size: 4.5vh; 
        }

        .controls {
            position: absolute; right: 20px;
            display: flex; gap: 10px;
        }

        .btn {
            background: rgba(0, 0, 0, 0.3);
            border: 1.5px solid white;
            color: white;
            padding: 8px 18px;
            font-size: 2vh;
            font-weight: bold;
            cursor: pointer;
            border-radius: 6px;
            transition: all 0.2s;
        }
        .btn:hover { background: white; color: var(--red); }
        .btn:active { transform: scale(0.95); }

        /* 2. 中間內容顯示區 */
        .main-content {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 0 7vw;
            position: relative;
            z-index: 50;
            overflow: hidden;
        }

        #ui-text {
            font-size: 6.5vh; /* 放大 20% */
            line-height: 1.6;
            text-align: justify;
            width: 100%;
            transition: opacity 0.4s;
            font-weight: 500;
        }

        .page-info {
            position: absolute;
            bottom: 20px; right: 30px;
            font-size: 3vh;
            color: rgba(255, 255, 255, 0.2);
        }

        /* 3. 底部走字區 */
        .footer {
            background: #111;
            border-top: 5px solid var(--gold);
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            z-index: 100;
        }

        #marquee {
            white-space: nowrap;
            font-size: 6vh;
            color: var(--gold);
            position: absolute;
            font-weight: bold;
            will-change: transform;
        }

        /* 啟動遮罩 */
        #overlay {
            position: fixed; inset: 0;
            background: rgba(0,0,0,0.98);
            z-index: 9999;
            display: flex; justify-content: center; align-items: center;
        }
        .start-btn {
            padding: 30px 70px; font-size: 4vh;
            background: var(--red); color: white;
            border: none; border-radius: 15px; cursor: pointer;
            box-shadow: 0 10px 30px rgba(230, 57, 70, 0.4);
        }
    </style>
</head>
<body>

    <div id="overlay">
        <button class="start-btn" onclick="initSystem()">啟動廣播監控系統</button>
    </div>

    <header class="header">
        <div id="ui-date" class="date-display">--/--/----</div>
        <div id="ui-title">載入數據中...</div>
        <div class="controls">
            <button class="btn" onclick="ctrlPlay()">播放</button>
            <button class="btn" onclick="ctrlPause()">暫停</button>
            <button class="btn" onclick="ctrlStop()">停止</button>
        </div>
    </header>

    <main class="main-content">
        <div id="ui-text">對接 data.json 序列中...</div>
        <div id="ui-page" class="page-info"></div>
    </main>

    <footer class="footer">
        <div id="marquee">正在檢查最新交通資訊流...</div>
    </footer>

    <script>
        let pages = [];
        let curIdx = 0;
        let isPlaying = false;
        let marqueePos = window.innerWidth;
        const synth = window.speechSynthesis;
        let currentUtterance = null;

        // 1. 初始化系統
        async function initSystem() {
            document.getElementById('overlay').style.display = 'none';
            await loadData();
            animateMarquee();
            // 每10分鐘檢查一次新新聞
            setInterval(loadData, 600000); 
        }

        // 2. 獲取並處理數據
        async function loadData() {
            try {
                const response = await fetch('data.json?t=' + Date.now());
                const data = await response.json();
                
                // 標題處理與自適應字體
                const titleEl = document.getElementById('ui-title');
                titleEl.innerText = data.title;
                if (data.title.length > 28) {
                    titleEl.style.fontSize = "2.8vh";
                } else if (data.title.length > 18) {
                    titleEl.style.fontSize = "3.5vh";
                } else {
                    titleEl.style.fontSize = "4.5vh";
                }

                document.getElementById('ui-date').innerText = data.date;
                document.getElementById('marquee').innerText = "【最新交通消息】" + data.title;

                // 智慧分頁邏輯：確保第一段不遺漏 + 長句拆分
                const rawSentences = data.fullText.split(/([。；！？])/).filter(Boolean);
                pages = [];
                let buffer = "";

                for (let i = 0; i < rawSentences.length; i++) {
                    buffer += rawSentences[i];
                    // 如果這段文字包含標點，或長度超過 65 字，就切分為一頁
                    if (rawSentences[i].match(/[。；！？]/) || buffer.length > 65) {
                        pages.push(buffer.trim());
                        buffer = "";
                    }
                }
                if (buffer) pages.push(buffer.trim());

                // 如果當前沒在播放，則開始
                if (!isPlaying) {
                    curIdx = 0;
                    ctrlPlay();
                }
            } catch (e) {
                console.error("無法載入數據:", e);
                document.getElementById('ui-text').innerText = "等待 data.json 更新中...";
            }
        }

        // 3. 播報核心邏輯
        async function broadcast() {
            if (!isPlaying || curIdx >= pages.length) {
                if (curIdx >= pages.length && isPlaying) {
                    curIdx = 0; // 全文播完，從頭循環
                    setTimeout(broadcast, 2000);
                }
                return;
            }

            const textEl = document.getElementById('ui-text');
            const pageEl = document.getElementById('ui-page');

            // 切換動畫
            textEl.style.opacity = 0;
            
            setTimeout(() => {
                textEl.innerText = pages[curIdx];
                pageEl.innerText = `${curIdx + 1} / ${pages.length}`;
                textEl.style.opacity = 1;

                // 設定語音
                currentUtterance = new SpeechSynthesisUtterance(pages[curIdx]);
                currentUtterance.lang = 'zh-HK'; // 粵語播報
                currentUtterance.rate = 0.92;    // 語速略慢
                
                currentUtterance.onend = () => {
                    if (isPlaying) {
                        curIdx++;
                        setTimeout(broadcast, 1000);
                    }
                };

                currentUtterance.onerror = () => {
                    if (isPlaying) {
                        curIdx++;
                        broadcast();
                    }
                };

                synth.speak(currentUtterance);
            }, 400);
        }

        // 4. 控制功能
        function ctrlPlay() {
            if (!isPlaying) {
                isPlaying = true;
                if (synth.paused) {
                    synth.resume();
                } else {
                    broadcast();
                }
            }
        }

        function ctrlPause() {
            isPlaying = false;
            synth.pause();
        }

        function ctrlStop() {
            isPlaying = false;
            curIdx = 0;
            synth.cancel();
            document.getElementById('ui-text').innerText = "播報已停止。";
            document.getElementById('ui-page').innerText = "";
        }

        // 5. 底部走字動畫
        function animateMarquee() {
            const m = document.getElementById('marquee');
            marqueePos -= 2.2; // 捲動速度
            if (marqueePos < -m.offsetWidth) {
                marqueePos = window.innerWidth;
            }
            m.style.transform = `translateX(${marqueePos}px)`;
            requestAnimationFrame(animateMarquee);
        }
    </script>
</body>
</html>
