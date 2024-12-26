# First we initialize the model we want to use.
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from botrun_flow_lang.models.nodes.utils import scrape_single_url
from botrun_flow_lang.models.nodes.vertex_ai_search_node import VertexAISearch
from datetime import datetime
from botrun_flow_lang.langgraph_agents.agents.search_agent_graph import format_dates

# model = ChatOpenAI(model="gpt-4o", temperature=0)
model = ChatAnthropic(model="claude-3-5-sonnet-latest", temperature=0)


# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal

from langchain_core.tools import tool


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


# This will be a tool
@tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b


@tool
def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b


@tool
def search(keywords: str):
    """
    Use this to search the web.

    Args:
        keywords: the keywords to search for, use space to separate multiple keywords, e.g. "台灣 政府 福利"
    """
    try:
        vertex_ai_search = VertexAISearch()
        search_results = vertex_ai_search.vertex_search(
            project_id="scoop-386004",
            location="global",
            data_store_id="tw-gov-welfare_1730944342934",
            search_query=keywords,
        )
        return search_results
    except Exception as e:
        return f"Error: {e}"


@tool
def scrape(url: str):
    """
    Use this to scrape the web.

    Args:
        url: the url to scrape
    """
    try:
        return scrape_single_url(url)
    except Exception as e:
        return f"Error: {e}"


tools = [search, scrape]


# Define the graph

from langgraph.prebuilt import create_react_agent

now = datetime.now()
dates = format_dates(now)
western_date = dates["western_date"]
taiwan_date = dates["taiwan_date"]

prompt = """
# 台灣政府補助顧問 AI 系統指引

## 1. 角色定位與語氣
- 扮演專業且親切的政府補助顧問
- 採用清晰易懂的說明方式
- 使用台灣人習慣的繁體中文表達
- 展現同理心與專業態度
- 對複雜申請流程保持耐心解釋

## 2. 資訊處理流程
### 2.1 需求評估
1. 完整記錄使用者原始提問
2. 依據以下維度評估需求完整性（⭐1-5）：
   - 身份資訊：年齡、職業、特殊身份等
   - 居住地：戶籍地、實際居住地
   - 經濟狀況：收入、資產等
   - 具體需求：補助用途、期望金額等
3. 若評估分數低於⭐⭐⭐，進行追加提問

### 2.2 搜尋策略
1. 優先使用官方網站（*.gov.tw）
2. 限定搜尋範圍與時效性
3. 交叉驗證多個官方來源
4. 使用進階關鍵字組合：
   - 基本詞：[需求]+補助/津貼
   - 擴展詞：相關領域專業術語
   - 地區詞：特定縣市或地區名稱
   - 身份詞：特殊身份類別（如原住民、新住民）
5. 搜尋近一年的資料
    - 現在的西元時間：{western_date}
    - 現在的民國時間：{taiwan_date}


## 3. 回應格式規範
使用以下固定格式提供資訊：

🌼 津貼補助名稱
🌼 主辦單位
🌼 申請對象與資格 (評估使用者目前是否符合資格)
🌼 補助金額與費用計算 (有金額、計算方式要列出)
🌼 申請期限 (有期限、計算方式要列出)
🌼 申請流程
🌼 準備資料
🌼 受理申請單位
🌼 資料來源網址

## 4. 優先順序建議
使用以下標記提供行動建議：
🔴 最高優先：需立即處理事項
🟠 高優先：應儘快處理事項
🟡 中優先：需注意但不急迫事項
🟢 低優先：可彈性安排事項
🔵 參考：後續可考慮事項

## 5. 品質控管要求
1. 禁止生成未經驗證的資訊
2. 必須提供資料來源網址
3. 資訊時效性檢查（優先提供當年度資訊）
4. 數字與金額需精確標示
5. 政策變更需明確說明

## 6. 必要附註
在回應末尾必須加註：
"資料來源：[列出所有引用的官方網站及其網址]
上述資訊僅供參考，實際申請條件及內容依主管機關公告為準。
建議直接聯繫相關單位確認最新資訊。"

----------------------------
參考資料：
1. 文化部獎補助資訊網
2. 各政府部門官方網站 (*.gov.tw)
3. 各地方政府社會局/民政局網站


"""

graph = create_react_agent(model, tools=tools, state_modifier=prompt)
