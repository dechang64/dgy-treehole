"""共享 CSS — 所有页面通过 inject_css() 注入"""

CSS = """<style>
/* 隐藏 Streamlit 默认元素 */
#MainMenu, footer, header {visibility: hidden}
.block-container {padding-top: 0.5rem; padding-bottom: 2rem; max-width: 520px}

/* 全局字体 */
.stApp {font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', serif}

/* 卡片样式 */
.card {
    background: #f5f0e8;
    border-radius: 12px;
    padding: 1.2rem;
    margin: 0.8rem 0;
    border: 1px solid #e8dfd0;
}
.card-dark {
    background: #2c1810;
    color: #f5f0e8;
    border-radius: 12px;
    padding: 1.2rem;
    margin: 0.8rem 0;
}

/* 场景卡片 */
.scene-card {
    background: linear-gradient(135deg, #f5f0e8, #e8dfd0);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 0.5rem 0;
    border: 1px solid #d4c5a9;
    cursor: pointer;
    transition: all 0.3s;
}
.scene-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(44,24,16,0.12);
    border-color: #b8860b;
}

/* 聊天气泡 */
.chat-ai {
    background: #e8dfd0;
    border-radius: 16px 16px 16px 4px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    max-width: 85%;
}
.chat-user {
    background: #2c1810;
    color: #f5f0e8;
    border-radius: 16px 16px 4px 16px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    max-width: 85%;
    margin-left: auto;
}

/* 标签 */
.tag {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    background: rgba(184,134,11,0.1);
    color: #b8860b;
    border-radius: 99px;
    font-size: 0.8rem;
    margin: 0.15rem;
}

/* 模式指示器（已停用 — 演示模式不再展示给用户） */
/* .mock-badge {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    background: rgba(192,57,43,0.1);
    color: #c0392b;
    border-radius: 99px;
    font-size: 0.7rem;
} */

/* Hero 头部 */
.hero {
    background: linear-gradient(135deg, #2c1810, #4a2c1a 50%, #3d1f0e);
    padding: 2.5rem 1.5rem 2rem;
    color: #f5f0e8;
    text-align: center;
    position: relative;
    overflow: hidden;
    border-radius: 0 0 16px 16px;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 30% 50%, rgba(184,134,11,0.12), transparent 60%);
    pointer-events: none;
}
.hero h1 {
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: 0.4rem;
    position: relative;
}
.hero .sub {
    opacity: 0.7;
    font-size: 0.85rem;
    margin: 0.4rem 0 0.8rem;
    position: relative;
}
.hero .motto {
    font-size: 0.8rem;
    opacity: 0.5;
    font-style: italic;
    position: relative;
}

/* 安全徽章 */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.3rem 0.8rem;
    background: rgba(45,106,79,0.1);
    color: #2d6a4f;
    border-radius: 99px;
    font-size: 0.75rem;
}

/* 结果卡片 */
.result-type {
    font-size: 2.5rem;
    font-weight: 800;
    color: #c0392b;
    text-align: center;
    letter-spacing: 0.3rem;
    margin: 0.5rem 0;
}
.result-desc {
    text-align: center;
    font-size: 0.9rem;
    color: #8b7355;
    margin-bottom: 0.8rem;
}
.result-scene {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.8rem;
    background: #fff;
    border-radius: 12px;
    border: 1px solid #e8dfd0;
    margin-bottom: 0.8rem;
}
.result-scene .icon {
    font-size: 2rem;
    width: 48px;
    text-align: center;
}
.result-scene .name {
    font-weight: 600;
    font-size: 0.95rem;
    color: #2c1810;
}
.result-scene .info {
    font-size: 0.8rem;
    color: #8b7355;
    margin-top: 0.1rem;
}
.result-reason {
    background: #f5f0e8;
    border-radius: 12px;
    padding: 0.8rem;
    margin: 0.8rem 0;
    font-size: 0.85rem;
    line-height: 1.7;
    color: #2c1810;
}
.result-quote {
    text-align: center;
    font-style: italic;
    color: #8b7355;
    font-size: 0.85rem;
    padding: 0.8rem;
    border-left: 3px solid #b8860b;
    margin: 0.8rem 0;
}

/* 星座按钮 */
.zodiac-btn {
    background: #fff;
    border: 1px solid #e8dfd0;
    border-radius: 12px;
    padding: 0.6rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}
.zodiac-btn:hover {
    border-color: #b8860b;
    box-shadow: 0 4px 12px rgba(44,24,16,0.08);
}

/* 星盘卡片 */
.chart-planet {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.5rem 0.7rem;
    background: #fff;
    border-radius: 10px;
    margin: 0.3rem 0;
    border: 1px solid #e8dfd0;
}
.chart-planet .p-icon {
    font-size: 1.3rem;
    width: 32px;
    text-align: center;
    flex-shrink: 0;
}
.chart-planet .p-info { flex: 1; }
.chart-planet .p-name { font-size: 0.78rem; font-weight: 600; }
.chart-planet .p-sign { font-size: 0.7rem; color: #8b7355; }
.chart-planet .p-desc { font-size: 0.72rem; color: #2c1810; margin-top: 0.1rem; line-height: 1.5; }

/* 星盘总结 */
.chart-summary {
    background: linear-gradient(135deg, #2c1810, #4a2c1a);
    color: #f5f0e8;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.8rem 0;
    text-align: center;
}

/* 元素标签 */
.elem-label {
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.3rem 0;
    margin-top: 0.5rem;
}

/* 动画 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeIn 0.5s ease-out; }

/* ── 树洞页面树皮纹理背景 ── */
.treehole-body {
    position: relative;
}
/* 用伪元素叠加树皮纹理 */
.treehole-body::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        /* 树皮竖纹 */
        repeating-linear-gradient(
            87deg,
            transparent 0px,
            transparent 18px,
            rgba(44,24,16,0.04) 18px,
            rgba(44,24,16,0.04) 20px,
            transparent 20px,
            transparent 48px
        ),
        /* 横向年轮纹理 */
        repeating-linear-gradient(
            0deg,
            transparent 0px,
            transparent 12px,
            rgba(44,24,16,0.025) 12px,
            rgba(44,24,16,0.025) 14px,
            transparent 14px,
            transparent 36px
        ),
        /* 整体暗角，让边缘更像树洞入口 */
        radial-gradient(
            ellipse at 50% 30%,
            transparent 20%,
            rgba(44,24,16,0.08) 100%
        );
    pointer-events: none;
    z-index: 0;
}
/* 确保内容在纹理之上 */
.treehole-body > * {
    position: relative;
    z-index: 1;
}

/* ── 静默释放模式动画 ── */
@keyframes pulseRing {
    0%   { box-shadow: 0 0 0 0 rgba(184,134,11,0.4); }
    70%  { box-shadow: 0 0 0 16px rgba(184,134,11,0); }
    100% { box-shadow: 0 0 0 0 rgba(184,134,11,0); }
}
.pulse-ring {
    animation: pulseRing 2s ease-out infinite;
    border-radius: 50%;
}
@keyframes gentleFloat {
    0%,100% { transform: translateY(0px); }
    50%       { transform: translateY(-8px); }
}
.gentle-float { animation: gentleFloat 3s ease-in-out infinite; }
@keyframes floatUp {
    0%,100% { transform: translateY(0px); }
    50%       { transform: translateY(-12px); }
}
.float { animation: floatUp 3s ease-in-out infinite; }

/* ── 树洞 Hero：古树内腔，从洞里看出去 ── */
.treehole-hero {
    position: relative;
    background:
        /* 顶部一道冷月白光（穿过树缝） */
        radial-gradient(
            ellipse 80% 30% at 50% 0%,
            rgba(255,245,220,0.18) 0%,
            rgba(255,245,220,0.05) 40%,
            transparent 70%
        ),
        /* 底部苔痕幽绿 */
        radial-gradient(
            ellipse 100% 50% at 50% 100%,
            rgba(45,106,79,0.25) 0%,
            transparent 60%
        ),
        /* 主体：深棕木心 */
        linear-gradient(180deg, #2c1810 0%, #1a0e08 50%, #0f0805 100%);
    color: #f5f0e8;
    padding: 2.5rem 1.5rem 2rem;
    text-align: center;
    border-radius: 0 0 24px 24px;
    margin-bottom: 1.2rem;
    overflow: hidden;
    box-shadow: inset 0 0 80px rgba(0,0,0,0.6);
}
/* 树洞内壁竖纹：模拟年轮+木纹 */
.treehole-hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        repeating-linear-gradient(
            85deg,
            transparent 0px,
            transparent 14px,
            rgba(245,240,232,0.04) 14px,
            rgba(245,240,232,0.04) 16px
        ),
        radial-gradient(
            ellipse at 50% 50%,
            transparent 30%,
            rgba(0,0,0,0.4) 100%
        );
    pointer-events: none;
    z-index: 0;
}
.treehole-hero > * { position: relative; z-index: 1; }

.treehole-hero .moon {
    font-size: 2.8rem;
    filter: drop-shadow(0 0 18px rgba(255,235,180,0.6));
    display: block;
    margin-bottom: 0.4rem;
    animation: gentleFloat 4s ease-in-out infinite;
}

.treehole-hero h2 {
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: 0.4rem;
    margin: 0.3rem 0 0.5rem;
    color: #f5f0e8;
}

.treehole-hero .sub {
    font-size: 0.88rem;
    color: #d4c5a9;
    letter-spacing: 0.1rem;
    margin: 0;
}

.treehole-hero .quote {
    margin-top: 1rem;
    font-size: 0.78rem;
    color: #8b7355;
    font-style: italic;
    letter-spacing: 0.05rem;
    opacity: 0.85;
}

/* 落叶飘入动画 */
@keyframes fallIn {
    0%   { transform: translateY(-30px) rotate(0deg); opacity: 0; }
    20%  { opacity: 1; }
    100% { transform: translateY(40px) rotate(180deg); opacity: 0; }
}
.falling-leaf {
    display: inline-block;
    animation: fallIn 5s ease-in-out infinite;
}
.falling-leaf:nth-child(2) { animation-delay: 1.5s; }
.falling-leaf:nth-child(3) { animation-delay: 3s; }

/* ── 场景卡片网格 ── */
.scene-card-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    margin: 0.6rem 0;
}
@media (max-width: 768px) {
    .scene-card-grid {
        grid-template-columns: 1fr;
    }
}

/* 卡片可点视觉提示 */
.scene-card-clickable {
    cursor: pointer;
    transition: all 0.3s;
    margin-bottom: 0.3rem !important;
}
.scene-card-clickable:hover {
    border-color: #b8860b !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(44,24,16,0.12);
}

/* 场景按钮: 紧贴卡片下沿, 文字链接样式, 视觉融入卡片 */
.scene-card-grid [data-testid="stButton"] button {
    background: transparent !important;
    background-color: transparent !important;
    color: #b8860b !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 0.85rem !important;
    padding: 0.4rem 0.6rem !important;
    margin-top: 0 !important;
    margin-bottom: 0.5rem !important;
    font-weight: 500 !important;
    text-decoration: none !important;
    text-align: right !important;
    border-radius: 0 !important;
}
.scene-card-grid [data-testid="stButton"] button:hover {
    background: rgba(184,134,11,0.08) !important;
    color: #b8860b !important;
    text-decoration: underline !important;
}
.scene-card-grid [data-testid="stButton"] button:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* ── 导航：flex-wrap 自动换行 ── */
.nav-flex-wrap {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 0.4rem !important;
    margin: 0.4rem 0 !important;
    justify-content: flex-start;
    width: 100% !important;
}
.nav-flex-wrap > * {
    flex: 0 1 auto !important;
    margin: 0 !important;
}
.nav-flex-wrap a,
.nav-flex-wrap [data-testid="stPageLink-NavLink"],
.nav-flex-wrap a[data-testid="stPageLink-NavLink"] {
    width: auto !important;
    min-width: 0 !important;
    flex: 0 0 auto !important;
    display: inline-block !important;
    box-sizing: border-box !important;
}
/* 移动端：每个按钮 30% (一行 3 个) */
@media (max-width: 768px) {
    .nav-flex-wrap a,
    .nav-flex-wrap [data-testid="stPageLink-NavLink"] {
        flex: 0 1 calc(33.33% - 0.3rem) !important;
        text-align: center !important;
        font-size: 0.78rem !important;
        padding: 0.4rem 0.2rem !important;
        max-width: calc(33.33% - 0.3rem) !important;
    }
}
/* 桌面端 (>= 769px)：每个按钮均分 7 等分 (大约 14% 一行 7 个) */
@media (min-width: 769px) {
    .nav-flex-wrap a,
    .nav-flex-wrap [data-testid="stPageLink-NavLink"] {
        flex: 0 1 calc(14.28% - 0.4rem) !important;
        max-width: calc(14.28% - 0.4rem) !important;
        text-align: center !important;
        min-width: 90px !important;
    }
}

/* ── 移动端适配 (max-width: 768px) ── */
@media (max-width: 768px) {
    /* 整体容器窄一点 */
    .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    /* 场景卡片和按钮更紧凑 */
    .scene-card {
        padding: 1rem !important;
    }
}

/* 全局：section-title 加点呼吸感 */
.section-title {
    font-size: 1.05rem;
    font-weight: 600;
    margin: 0.8rem 0 0.4rem;
    color: #2c1810;
}
</style>"""

import streamlit as st

def inject_css():
    """在任意页面注入全局 CSS"""
    st.markdown(CSS, unsafe_allow_html=True)
