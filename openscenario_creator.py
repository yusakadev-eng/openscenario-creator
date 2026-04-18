import streamlit as st
from google import genai
from google.genai import types
import xml.dom.minidom
import json
import os
from datetime import datetime

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OpenSCENARIO Creator",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #1a2235;
    --accent-cyan: #00e5ff;
    --accent-green: #00ff88;
    --accent-orange: #ff6b35;
    --text-primary: #e8f0fe;
    --text-muted: #8899aa;
    --border: #2a3a50;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

/* Hide Streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 100%; }

/* App Header */
.app-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px 0 16px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 24px;
}
.app-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent-cyan);
    letter-spacing: -0.5px;
    margin: 0;
    text-shadow: 0 0 20px rgba(0,229,255,0.4);
}
.app-subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
    font-family: 'Space Mono', monospace;
    margin: 2px 0 0 0;
}
.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent-green);
    box-shadow: 0 0 8px var(--accent-green);
    animation: pulse 2s infinite;
    display: inline-block;
    margin-right: 6px;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* Chat messages */
.chat-user {
    background: linear-gradient(135deg, #1e3a5f 0%, #1a2d4a 100%);
    border: 1px solid #2a4a6a;
    border-radius: 12px 12px 4px 12px;
    padding: 12px 16px;
    margin: 8px 0;
    color: var(--text-primary);
    font-size: 0.9rem;
    line-height: 1.5;
}
.chat-assistant {
    background: linear-gradient(135deg, #1a2f1e 0%, #152318 100%);
    border: 1px solid #2a4a2e;
    border-radius: 12px 12px 12px 4px;
    padding: 12px 16px;
    margin: 8px 0;
    color: var(--text-primary);
    font-size: 0.9rem;
    line-height: 1.6;
}
.chat-label-user {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #5599ff;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.chat-label-ai {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--accent-green);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

/* XML Preview Panel */
.xml-panel {
    background: #0d1117;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #c9d1d9;
    white-space: pre-wrap;
    word-break: break-all;
    overflow-y: auto;
    max-height: 60vh;
    line-height: 1.6;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .block-container {
    padding: 1rem 1rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00e5ff22, #00e5ff11);
    border: 1px solid var(--accent-cyan);
    color: var(--accent-cyan);
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.5px;
    border-radius: 6px;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00e5ff44, #00e5ff22);
    box-shadow: 0 0 12px rgba(0,229,255,0.3);
    transform: translateY(-1px);
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #00ff8822, #00ff8811);
    border: 1px solid var(--accent-green);
    color: var(--accent-green);
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    border-radius: 6px;
    width: 100%;
}

/* Text input */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: var(--text-primary);
    border-radius: 8px;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.9rem;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-cyan);
    box-shadow: 0 0 8px rgba(0,229,255,0.2);
}

/* Metrics / info boxes */
.metric-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 0.8rem;
}
.metric-label {
    color: var(--text-muted);
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.metric-value {
    color: var(--accent-cyan);
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    margin-top: 2px;
}

/* Section headings */
.section-head {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-muted);
    margin: 16px 0 8px 0;
    border-bottom: 1px solid var(--border);
    padding-bottom: 6px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 0.5px;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-cyan) !important;
    border-bottom: 2px solid var(--accent-cyan) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: var(--text-primary);
    border-radius: 8px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3a4a60; }

/* Code highlighting in XML */
.xml-tag { color: #79c0ff; }
.xml-attr { color: #ffab70; }
.xml-value { color: #a5d6ff; }
.xml-comment { color: #8b949e; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# ─── System Prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert in OpenSCENARIO (ASAM OpenSCENARIO standard) for autonomous driving simulation.
Your role is to help users create valid OpenSCENARIO XML files through a conversational interface.

## Your Behavior:
1. **Gather requirements** through natural conversation. Ask clarifying questions about:
   - Road/environment setup (straight road, intersection, highway, etc.)
   - Ego vehicle (type, start position, speed, goal)
   - Other entities (vehicles, pedestrians, obstacles)
   - Scenario events (cut-ins, emergency stops, pedestrian crossing, etc.)
   - Weather, time of day, environmental conditions

2. **Generate OpenSCENARIO XML** when you have enough information. Use OpenSCENARIO 1.2 format.

3. **Iteratively improve** the scenario based on user feedback.

4. **XML Generation Rules**:
   - Always produce valid OpenSCENARIO 1.2 XML
   - Include all required elements: FileHeader, ParameterDeclarations, CatalogReferences, RoadNetwork, Entities, Storyboard
   - Use realistic values for positions, speeds, and timing
   - Add comments to explain complex parts
   - When generating XML, wrap it in ```xml ... ``` code blocks

5. **Language**: Respond in the same language the user uses (Japanese or English).

6. **Format**: Keep explanations concise. When updating the scenario, briefly explain what changed.

## Current Scenario State:
Always maintain awareness of the current scenario being built. When you generate XML, it represents the complete current state of the scenario.

Example minimal scenario structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<OpenSCENARIO>
  <FileHeader description="Scenario" author="OpenSCENARIO Creator" date="2024-01-01T00:00:00" revMajor="1" revMinor="2"/>
  <ParameterDeclarations/>
  <CatalogReferences/>
  <RoadNetwork>
    <LogicFile filepath="highway.xodr"/>
  </RoadNetwork>
  <Entities>
    <ScenarioObject name="Ego">
      <Vehicle name="car" vehicleCategory="car">
        <BoundingBox><Center x="1.5" y="0" z="0.9"/><Dimensions width="2.0" length="4.5" height="1.8"/></BoundingBox>
        <Performance maxSpeed="70" maxAcceleration="10" maxDeceleration="10"/>
        <Axles>
          <FrontAxle maxSteering="0.5" wheelDiameter="0.6" trackWidth="1.8" positionX="2.98" positionZ="0.3"/>
          <RearAxle maxSteering="0" wheelDiameter="0.6" trackWidth="1.8" positionX="0" positionZ="0.3"/>
        </Axles>
        <Properties/>
      </Vehicle>
    </ScenarioObject>
  </Entities>
  <Storyboard>
    <Init>
      <Actions>
        <EntityAction entityRef="Ego">
          <AddEntityAction>
            <Position><WorldPosition x="0" y="0" z="0" h="0"/></Position>
          </AddEntityAction>
        </EntityAction>
      </Actions>
    </Init>
    <Story name="MainStory">
      <Act name="MainAct">
        <ManeuverGroup name="EgoManeuver" maximumExecutionCount="1">
          <Actors selectTriggeringEntities="false"><EntityRef entityRef="Ego"/></Actors>
          <Maneuver name="EgoDrive">
            <Event name="StartDriving" priority="overwrite">
              <Action name="SpeedAction">
                <GlobalAction>
                  <EntityAction entityRef="Ego">
                    <LongitudinalAction>
                      <SpeedAction>
                        <SpeedActionDynamics dynamicsShape="step" value="0" dynamicsDimension="time"/>
                        <SpeedActionTarget><AbsoluteTargetSpeed value="15"/></SpeedActionTarget>
                      </SpeedAction>
                    </LongitudinalAction>
                  </EntityAction>
                </GlobalAction>
              </Action>
              <StartTrigger><ConditionGroup><Condition name="StartCond" delay="0" conditionEdge="none"><ByValueCondition><SimulationTimeCondition value="0" rule="greaterThan"/></ByValueCondition></Condition></ConditionGroup></StartTrigger>
            </Event>
          </Maneuver>
        </ManeuverGroup>
        <StartTrigger/>
      </Act>
    </Story>
    <StopTrigger><ConditionGroup><Condition name="EndCond" delay="0" conditionEdge="none"><ByValueCondition><SimulationTimeCondition value="30" rule="greaterThan"/></ByValueCondition></Condition></ConditionGroup></StopTrigger>
  </Storyboard>
</OpenSCENARIO>
```
"""

# ─── Helpers ───────────────────────────────────────────────────────────────────
def extract_xml(text: str) -> str | None:
    """Extract XML from markdown code block or raw XML."""
    import re
    # Try ```xml ... ``` block
    m = re.search(r"```xml\s*([\s\S]*?)```", text)
    if m:
        return m.group(1).strip()
    # Try raw <?xml ...
    m = re.search(r"(<\?xml[\s\S]*)", text)
    if m:
        return m.group(1).strip()
    return None

def pretty_xml(xml_str: str) -> str:
    try:
        dom = xml.dom.minidom.parseString(xml_str.encode("utf-8"))
        return dom.toprettyxml(indent="  ", encoding=None)
    except Exception:
        return xml_str

def count_entities(xml_str: str) -> int:
    return xml_str.count("<ScenarioObject") if xml_str else 0

def count_events(xml_str: str) -> int:
    return xml_str.count("<Event ") if xml_str else 0

def count_acts(xml_str: str) -> int:
    return xml_str.count("<Act ") if xml_str else 0

def get_scenario_summary(xml_str: str) -> dict:
    if not xml_str:
        return {}
    import re
    entities = [m.group(1) for m in re.finditer(r'<ScenarioObject name="([^"]+)"', xml_str)]
    events = [m.group(1) for m in re.finditer(r'<Event name="([^"]+)"', xml_str)]
    road = re.search(r'filepath="([^"]+)"', xml_str)
    stop_time = re.search(r'SimulationTimeCondition value="([^"]+)".*?StopTrigger', xml_str, re.DOTALL)
    return {
        "entities": entities,
        "events": events,
        "road": road.group(1) if road else "未設定",
        "stop_time": stop_time.group(1) + "s" if stop_time else "未設定",
    }

def call_gemini(messages: list) -> tuple[str, str | None]:
    """Call Gemini API (google-genai SDK), return (text_response, xml_or_None)."""
    api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
    client = genai.Client(api_key=api_key)

    # Convert messages to Gemini format (role: user/model)
    history = []
    for m in messages[:-1]:
        role = "user" if m["role"] == "user" else "model"
        history.append(types.Content(role=role, parts=[types.Part(text=m["content"])]))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=history + [types.Part(text=messages[-1]["content"])],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=4096,
        ),
    )
    full_text = response.text
    xml = extract_xml(full_text)
    return full_text, xml

# ─── Session State Init ────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_xml" not in st.session_state:
    st.session_state.current_xml = ""
if "scenario_name" not in st.session_state:
    st.session_state.scenario_name = "my_scenario"
if "version_history" not in st.session_state:
    st.session_state.version_history = []

# ─── Layout ────────────────────────────────────────────────────────────────────
# Header
st.markdown("""
<div class="app-header">
  <div>
    <p class="app-title">⬡ OpenSCENARIO Creator</p>
    <p class="app-subtitle"><span class="status-dot"></span>AI-powered scenario builder · ASAM OpenSCENARIO 1.2</p>
  </div>
</div>
""", unsafe_allow_html=True)

# Main columns
col_chat, col_preview = st.columns([3, 2], gap="large")

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-head">⚙ Scenario Config</div>', unsafe_allow_html=True)

    scenario_name = st.text_input("シナリオ名", value=st.session_state.scenario_name, key="sname_input")
    st.session_state.scenario_name = scenario_name

    st.markdown('<div class="section-head">⚡ Quick Templates</div>', unsafe_allow_html=True)

    templates = {
        "🚗 車線変更カットイン": "高速道路で自車(Ego)が直進中に、隣車線の車両が自車前方に急に割り込むシナリオを作成してください。速度は自車80km/h、割り込み車60km/hで始まり割り込み後80km/hに加速。",
        "🚶 歩行者横断": "市街地の交差点で、自車が直進中に歩行者が横断するシナリオを作成してください。自車速度40km/h、歩行者は自車の10m前方を横断。",
        "🛑 前方車急停止": "高速道路で自車(Ego)が走行中、前方車両が突然急停止するシナリオ。自車120km/h、前方車100km/hから5秒で停止。",
        "🌧 悪天候追従": "雨天・夜間環境で自車が前方車に追従走行するシナリオ。視界不良と路面摩擦低下を考慮。",
    }

    for label, prompt in templates.items():
        if st.button(label, key=f"tpl_{label}"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("シナリオ生成中..."):
                api_msgs = [{"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages]
                reply, xml = call_gemini(api_msgs)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            if xml:
                st.session_state.current_xml = pretty_xml(xml)
                st.session_state.version_history.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "xml": st.session_state.current_xml,
                    "note": label,
                })
            st.rerun()

    st.markdown('<div class="section-head">📊 Scenario Stats</div>', unsafe_allow_html=True)

    summary = get_scenario_summary(st.session_state.current_xml)
    if summary:
        entities_str = ", ".join(summary["entities"]) if summary["entities"] else "—"
        events_str = str(len(summary["events"]))
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">エンティティ</div>
            <div class="metric-value">{len(summary["entities"])} 台/体</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">イベント数</div>
            <div class="metric-value">{events_str}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">道路ファイル</div>
            <div class="metric-value">{summary["road"]}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">終了時刻</div>
            <div class="metric-value">{summary["stop_time"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#8899aa;font-size:0.8rem;">シナリオ未生成</p>', unsafe_allow_html=True)

    st.markdown('<div class="section-head">🕒 Version History</div>', unsafe_allow_html=True)
    if st.session_state.version_history:
        for i, v in enumerate(reversed(st.session_state.version_history[-5:])):
            idx = len(st.session_state.version_history) - i
            if st.button(f"v{idx} · {v['time']} — {v['note'][:18]}", key=f"vh_{i}"):
                st.session_state.current_xml = v["xml"]
                st.rerun()
    else:
        st.markdown('<p style="color:#8899aa;font-size:0.8rem;">履歴なし</p>', unsafe_allow_html=True)

    st.markdown('<div class="section-head">🔄 Controls</div>', unsafe_allow_html=True)
    if st.button("🗑 会話をリセット"):
        st.session_state.messages = []
        st.session_state.current_xml = ""
        st.session_state.version_history = []
        st.rerun()

# ─── Chat Column ───────────────────────────────────────────────────────────────
with col_chat:
    st.markdown('<div class="section-head">💬 Conversation</div>', unsafe_allow_html=True)

    # Welcome message
    if not st.session_state.messages:
        st.markdown("""
        <div class="chat-assistant">
            <div class="chat-label-ai">🤖 AI Assistant</div>
            こんにちは！OpenSCENARIOシナリオビルダーへようこそ。<br><br>
            どんなシナリオを作りたいですか？例えば：<br>
            • 「高速道路での車線変更カットインシナリオ」<br>
            • 「市街地での歩行者飛び出しシナリオ」<br>
            • 「悪天候下での緊急ブレーキシナリオ」<br><br>
            左のクイックテンプレートも使えます！
        </div>
        """, unsafe_allow_html=True)

    # Chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-user">
                    <div class="chat-label-user">👤 You</div>
                    {msg["content"].replace(chr(10), "<br>")}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Strip XML block from display text for cleanliness
                display_text = msg["content"]
                import re
                display_text = re.sub(r"```xml[\s\S]*?```", "📄 *XMLを生成・更新しました（右パネルで確認）*", display_text)
                display_text = display_text.replace("\n", "<br>")
                st.markdown(f"""
                <div class="chat-assistant">
                    <div class="chat-label-ai">🤖 AI Assistant</div>
                    {display_text}
                </div>
                """, unsafe_allow_html=True)

    # Input area
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "メッセージを入力",
            placeholder="例：自車の速度を100km/hに変更して、割り込み車のタイミングを3秒後にしてください",
            height=90,
            label_visibility="collapsed",
        )
        send_col, _ = st.columns([1, 3])
        with send_col:
            submitted = st.form_submit_button("▶ 送信", use_container_width=True)

    if submitted and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        with st.spinner("AIが応答中..."):
            api_msgs = [{"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages]
            reply, xml = call_gemini(api_msgs)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        if xml:
            pxml = pretty_xml(xml)
            st.session_state.current_xml = pxml
            st.session_state.version_history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "xml": pxml,
                "note": user_input.strip()[:20],
            })
        st.rerun()

# ─── Preview Column ────────────────────────────────────────────────────────────
with col_preview:
    tab_xml, tab_dl = st.tabs(["📄 XML Preview", "⬇ Download"])

    with tab_xml:
        if st.session_state.current_xml:
            # Simple syntax coloring using HTML
            highlighted = st.session_state.current_xml
            highlighted = highlighted.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            # Color XML tags
            import re
            highlighted = re.sub(r"&lt;(/?\w[\w:.-]*)([^&]*)&gt;",
                lambda m: f'<span style="color:#79c0ff">&lt;{m.group(1)}</span>{m.group(2)}<span style="color:#79c0ff">&gt;</span>',
                highlighted)
            # Color attribute values
            highlighted = re.sub(r'="([^"]*)"',
                lambda m: f'=<span style="color:#a5d6ff">"{m.group(1)}"</span>',
                highlighted)

            char_count = len(st.session_state.current_xml)
            line_count = st.session_state.current_xml.count("\n")
            st.markdown(f'<p style="color:#8899aa;font-family:Space Mono,monospace;font-size:0.65rem;margin-bottom:8px;">{line_count} lines · {char_count} chars</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="xml-panel">{highlighted}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:60px 20px;color:#8899aa;">
                <p style="font-size:2rem;">📋</p>
                <p style="font-family:'Space Mono',monospace;font-size:0.75rem;">
                    シナリオがまだありません。<br>左のチャットで作成を開始してください。
                </p>
            </div>
            """, unsafe_allow_html=True)

    with tab_dl:
        if st.session_state.current_xml:
            filename = f"{st.session_state.scenario_name}.xosc"
            st.markdown(f"""
            <div class="metric-box" style="margin-bottom:16px;">
                <div class="metric-label">出力ファイル</div>
                <div class="metric-value">{filename}</div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label="⬇ .xosc ファイルをダウンロード",
                data=st.session_state.current_xml,
                file_name=filename,
                mime="application/xml",
                use_container_width=True,
            )

            # Also offer JSON export of conversation
            if st.session_state.messages:
                conv_json = json.dumps(
                    {"scenario": st.session_state.scenario_name, "conversation": st.session_state.messages},
                    ensure_ascii=False, indent=2
                )
                st.download_button(
                    label="💾 会話履歴をJSON保存",
                    data=conv_json,
                    file_name=f"{st.session_state.scenario_name}_conversation.json",
                    mime="application/json",
                    use_container_width=True,
                )
        else:
            st.markdown('<p style="color:#8899aa;font-size:0.85rem;text-align:center;padding:40px 0;">シナリオ生成後にダウンロードできます</p>', unsafe_allow_html=True)
