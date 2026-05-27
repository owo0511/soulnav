## UI 分析（依據 `frontend-spec.md` 對照 `index.html`）

來源：
- `spec/frontend-spec.md`：定義 Dashboard/各頁元件與 mobile-first/導覽方式
- `index.html`：目前實作的 `page0~page5` 與關鍵 UI 元件

### 1. 哪些 UI 區塊可以保留
1. **情緒評估流程（`page0`）的基本互動**  
   - 可保留：心情單選（`.mood-btn` + `moodStandardDesc`）、壓力來源滑桿（`slider-study/social/sleep` + `val-*`）、文字描述輸入（`moodText`）以及提交→載入→結果（`p0-loading`/`p0-result`）。
2. **AI 分析結果的呈現容器**  
   - 可保留：`gemini-box`、`gemini-result-text`（支援 `res.html` 注入）、以及推薦結論區塊（`Gemini 核心評估與推薦`）。
3. **學習/互動內容的「卡片化、短步驟」體驗**  
   - 可保留：`page1` 的課程進度卡（`lesson-card done/cur/lock`）、`page2` 的分頁式訓練面板（`practice-tabs` + `practice-panel`）。
4. **互動訓練的核心模組（呼吸 + 情境決策 + 任務拆解）**  
   - 可保留：`ptab-breath`（`breathCircle/breathCount/breathPhase`）、`ptab-scen`（`dopamine-meter`、`sc0~sc2`、`scenFB`）、`ptab-task`（`taskInput/timeLeft/currentState`，以及 AI 拆解結果：`stepList`、`progFill`、`naviTip`）。
5. **現實挑戰的任務列表與完成回饋**  
   - 可保留：`page3` 兩個挑戰卡（`realList1`/`realList2`）與每張卡的進度區塊（`rPct1/rBar1`、`rPct2/rBar2`）以及回報 AI（`reportText` + `submitReport()`）。
6. **進度追蹤頁的圖表與 AI 洞察位**  
   - 可保留：`page4` 的統計卡（`stat-streak/stat-tasks/stat-badges`）、情緒趨勢圖容器（`cloudChartWrapper`）、行為紀錄容器（`behavior-list-container`）、以及 AI 洞察生成區（`dynamic-insight-container` + `fetchInsight()`）。
7. **AI 回饋與反思引導（`page5`）**  
   - 可保留：`ai-chat` 既有的 Navi 對話訊息容器（`final-navi-analysis`）、反思引導問句（`.reflect-opts`）與送出按鈕（`finalSubmitBtn` + `submitFinalReflection()`）。

### 2. 哪些區塊需要修改
1. **導覽與「Dashboard」定位不符合 spec**  
   - 規格要求 mobile navigation 有 `Dashboard / Learning Topics / Challenges / Progress / Profile`（底部導覽）。
   - 目前 `index.html` 以「`top-bar` 流程步驟 + 左側 sidebar（`nav-item`）」為主，頁面雖有 `page4`（進度/追蹤）但**沒有明確的 Dashboard landing page**（spec 的 Dashboard 需要彙整 emotional summary、AI recommended topics、active adaptive challenges、learning progress overview、quick access、daily insights）。
2. **Learning Topic Page（`page1`）缺少 spec 要的 AI topic 卡資訊**  
   - 目前課程是「單元/進度」導向（`lesson-card done/cur`），但缺少：
     - emotional tags（情緒標籤）
     - recommendation reason（推薦原因）
     - difficulty indicator（難度指標）
     - AI topic cards（AI 生成的主題卡片）
3. **Interactive Activity Page（`page2`）缺少 spec 明確的 self-reflection questions + AI conversation module**  
   - `page2` 有任務拆解輸入與情境互動，但：
     - 自我反思題（self-reflection questions）在互動頁沒有獨立呈現
     - `AI conversation module` 目前主要落在 `page5` 的單次/彙總式回饋（缺少互動式聊天 UI 與多輪對話）
4. **Adaptive Challenge Page（`page3`）缺少 spec 要的 challenge timer**  
   - `page3` 有挑戰任務、完成進度，但搜尋不到明確的 challenge timer / 倒數元件。
5. **User Progress Dashboard（`page4`）缺少 spec 要的 learning statistics / challenge completion history 的完整呈現**  
   - `page4` 有統計卡與圖表（情緒最近紀錄）與「最近完成任務列表」（`behavior-list-container`），但 spec 指向的：
     - challenge completion history（挑戰完成歷史）
     - learning statistics（學習統計）
   - 目前呈現粒度較偏「最近」與「列表/圖」，可能需要更明確的歷史/統計聚合區塊。

### 3. 哪些 AI 功能 UI 尚未存在（或與 spec 差距較大）
1. **AI Learning Topics（推薦主題卡）UI 尚未完整存在**
   - 目前未見可對應 spec 的 topic cards 及其 `emotion tags / recommendation reason / difficulty` 等欄位與版面。
2. **AI Conversation Module（互動式聊天）UI 尚未存在於互動頁**
   - `page5` 的 `ai-chat` 比較像彙總回饋訊息（`final-navi-analysis` + 反思選擇），但 `page2` 缺少：
     - 文字輸入（自由聊天）
     - 聊天訊息列表（對話歷史）
     - 多輪交互（送出→回覆）
3. **Adaptive Challenge Timer（挑戰計時器/倒數）UI 尚未存在**
4. **Dashboard 層級的 AI progress insights（彙整型）與 quick access 尚未有完整 Landing 結構**
   - `page4` 有洞察生成，但 spec 的 Dashboard 需要更上層的「彙整入口」視圖，把它與 recommended topics / challenges 摘要一起放在 Dashboard。

### 4. 哪些部分不符合 mobile-first design
1. **導覽形式不符合 spec：缺少 bottom navigation bar**
   - 規格要求底部觸控導覽（Dashboard / Learning Topics / Challenges / Progress / Profile）。
   - 目前是：
     - `top-bar`（`flow-indicator`：多步驟水平流程）
     - 左側 `sidebar`（在 `@media(max-width:920px)` 變成橫向可滾，但仍非 bottom nav）
2. **Dashboard 入口缺位導致「一進 app 先看彙整」不成立**
   - mobile-first 常強調入口即完成任務與資訊掃描。
   - 目前使用者進入後通常從 `page0` 做情緒評估（不是 spec 定義的 Dashboard landing）。
3. **部分體驗受 fixed/overlays 影響，需留意 mobile 上的遮擋與回到原流程**
   - `#login-overlay`、`#scenario-intro` 使用 `position: fixed; inset: 0;`。
   - 雖然合理，但若搭配 sidebar/流程導覽，可能造成使用者視線被流程元件搶走（需在重新設計導覽後一起檢討）。

### 5. 哪些部分需要重新設計成 adaptive learning dashboard
結論：目前 `index.html` 的進度/追蹤分散在 `page3~page4`，情緒評估在 `page0`、AI 回饋在 `page5`，但 spec 要求 Dashboard 是「一個彙整式首頁」，因此需要新增/重組頁面與導覽。

#### 5.1 建議把現有元件「搬到 Dashboard」（符合 spec 的元件對應）
1. **emotional summary（情緒摘要）**
   - 來源：`page0` 的 `moodStandardDesc`、`currentMoodText`、壓力滑桿（`val-study/social/sleep`）與 AI 結果（`gemini-result-text` 摘要）
   - Dashboard 呈現方式：只顯示分類結果 + 今日建議，不要完整呈現整個表單。
2. **AI recommended topics（AI 推薦主題）**
   - 目前 `page1` 是「課程單元進度」，建議調整為 topic cards：可把 `lesson-card` 升級成「主題卡」並補上 reason/difficulty/tags。
3. **active adaptive challenges（主動自適應挑戰）**
   - 來源：`page3` 的挑戰卡與任務列表（`realList1/realList2`）
   - 需要新增：challenge timer（若 spec 是重點），至少要有最明顯的時間/進度提示（`rPct*` + 新 timer 元件）。
4. **learning progress overview（學習進度總覽）**
   - 來源：`page4` 的統計卡（`stat-*`）、情緒圖（`cloudChartWrapper`）、以及完成任務/行為紀錄（`behavior-list-container`）
5. **quick access buttons（快速入口）**
   - 目前散落在各頁的按鈕可抽取，例如：
     - 直接到 `ptab-breath`（呼吸）
     - 直接到「繼續學習」（對應 `openLesson()` 的下一步）
     - 直接到 `page3` 挑戰
     - 直接到 `fetchInsight()`/`page5`
6. **daily emotional insights（每日情緒洞察）**
   - 來源：`page4` 的 `dynamic-insight-container`（`fetchInsight()`）、以及 `page0` 的今日 AI 分析結果
   - Dashboard 上可做成「最新一則洞察卡片」，點擊可展開到 `page4/page5`。

#### 5.2 導覽/頁面層級調整（讓 Dashboard 成為正確首頁）
1. 新增一個明確的 Dashboard 頁（建議沿用目前 page 結構新增 `pageX`，並在 `.nav-item` 與（或取代）`flow-indicator` 中新增對應項）
2. sidebar 目前的「主要功能」可改成 spec 的 5 類目（Dashboard / Learning Topics / Challenges / Progress / Profile）
3. 如要完全符合 spec mobile-first：實作真正的底部導覽列（bottom nav），並把現有 `sidebar` 退居次要或在桌面版才保留。

#### 5.3 需要同步補齊的 spec 缺口（Dashboard 改版時一起做）
- AI recommended topics：新增 topic card 結構與其 AI 欄位（emotion tags / reason / difficulty）
- AI conversation module：把多輪聊天 UI 佈局在互動/反思體驗中（至少要形成可對話的聊天區）
- challenge timer：對 `page3` 挑戰卡補上計時/倒數與狀態
- Progress 統計：在 `page4`（或 Dashboard）增加更清楚的 challenge completion history / learning statistics 聚合
