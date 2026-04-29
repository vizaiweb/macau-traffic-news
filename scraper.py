<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <style>
        :root {
            --red: #e63946;
            --gold: #ffca28;
            --bg: #050505;
        }

        /* 強制三段式佈局，絕不重疊 */
        body {
            margin: 0; padding: 0; background: var(--bg); color: white;
            font-family: "PingFang HK", sans-serif;
            height: 100vh; width: 100vw;
            display: grid;
            grid-template-rows: 12vh 1fr 12vh; /* 頂部、中間、底部比例固定 */
            overflow: hidden;
        }

        /* 頂部標題與按鈕 */
        .header {
            background: var(--red);
            display: flex; align-items: center; justify-content: center;
            position: relative; padding: 0 20px;
        }
        .date { position: absolute; left: 20px; font-size: 2.5vh; }
        .title-text { font-size: 4vh; font-weight: bold; max-width: 60%; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .btns { position: absolute; right: 20px; display: flex; gap: 10px; }
        .btn { padding: 8px 15px; background: rgba(255,255,255,0.2); border: 1px solid white; color: white; cursor: pointer; border-radius: 5px; }

        /* 中間內文區：放大 20% 字體 (約 6.5vh) */
        .main {
            display: flex; justify-content: center; align-items: center;
            padding: 0 8vw; overflow: hidden; position: relative;
        }
        #ui-text {
            font-size: 6.5vh; line-height: 1.6; text-align: justify;
            width: 100%; transition: opacity 0.3s;
        }
        .page-num { position: absolute; bottom: 20px; right: 30px; color: rgba(255,255,255,0.3); font-size: 3vh; }

        /* 底部走字區 */
        .footer {
            background: #111; border-top: 5px solid var(--gold);
            position: relative; overflow: hidden; display: flex; align-items: center;
        }
        #marquee { white-space: nowrap; font-size: 6vh; color: var(--gold); position: absolute; font-weight: bold; }

        /* 啟動遮罩 */
        #overlay {
            position: fixed; inset: 0; background: rgba(0,0,0,0.95);
            z-index: 9999; display: flex; justify-content: center; align-items: center;
        }
        .start-btn { padding: 30px 60px; font-size: 4vh; background: var(--red); color: white; border: none; border-radius: 10px; cursor: pointer; }
    </style>
</head>
<body>

<div id="overlay"><button class="start-btn" onclick="init()">啟動廣播監控系統</button></div>

<header class="header">
    <div id="ui-date" class="date">--/--/----</div>
    <div id="ui-title" class="title-text">載入中...</div>
    <div class="btns">
        <button class="btn" onclick="location.reload()">重新整理</button>
        <button class="btn" onclick="window.speechSynthesis.cancel()">靜音</button>
    </div>
</header>

<main class="main">
    <div id="ui-text">正在對接 data.json...</div>
    <div id="ui-page" class="page-num"></div>
</main>

<footer class="footer">
    <div id="marquee">等待新聞抓取中...</div>
</footer>

<script>
    let pages = [];
    let isRunning = false;
    let mPos = window.innerWidth;
    const synth = window.speechSynthesis;

    async function init() {
        document.getElementById('overlay').style.display = 'none';
        isRunning = true;
        await loadData();
        animateMarquee();
        setInterval(loadData, 600000); // 10分鐘更新一次
    }

    async function loadData() {
        try {
            const res = await fetch('data.json?v=' + Date.now());
            const d = await res.json();
            document.getElementById('ui-title').innerText = d.title;
            document.getElementById('ui-date').innerText = d.date;
            document.getElementById('marquee').innerText = "【最新交通消息】" + d.title;

            // 修正分頁邏輯：確保第一段不丟失
            // 按照標點符號切分，並過濾掉空值
            pages = d.fullText.split(/([。；！？])/).reduce((acc, cur, idx, arr) => {
                if (idx % 2 === 0) {
                    let sentence = cur + (arr[idx+1] || "");
                    if (sentence.trim().length > 2) acc.push(sentence);
                }
                return acc;
            }, []);

            startBroadcast();
        } catch (e) { console.log("等待數據生成中..."); }
    }

    async function startBroadcast() {
        const textEl = document.getElementById('ui-text');
        const pageEl = document.getElementById('ui-page');

        for (let i = 0; i < pages.length; i++) {
            if (!isRunning) break;
            textEl.style.opacity = 0;
            await new Promise(r => setTimeout(r, 300));
            
            textEl.innerText = pages[i];
            pageEl.innerText = `${i+1} / ${pages.length}`;
            textEl.style.opacity = 1;

            await speak(pages[i]);
            await new Promise(r => setTimeout(r, 1200));
        }
        // 全文讀完後，重新加載數據循環播放
        loadData();
    }

    function speak(t) {
        return new Promise(res => {
            const u = new SpeechSynthesisUtterance(t);
            u.lang = 'zh-HK'; 
            u.rate = 0.95;
            u.onend = res;
            u.onerror = res;
            synth.speak(u);
        });
    }

    function animateMarquee() {
        const m = document.getElementById('marquee');
        mPos -= 2.2;
        if (mPos < -m.offsetWidth) mPos = window.innerWidth;
        m.style.transform = `translateX(${mPos}px)`;
        requestAnimationFrame(animateMarquee);
    }
</script>

</body>
</html>
