import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

st.set_page_config(page_title="TikTok Keyword Extractor", layout="centered")

st.title("🔍 TikTok Keyword Extractor")
st.write("提取包含关键词的 TikTok 视频评论 & 标题，并导出链接。")

# 输入关键词
keywords = st.text_input("请输入关键词（多个关键词请用逗号分隔）", placeholder="如：inflation, hoodie, streetwear")

# 粘贴视频链接
video_links_input = st.text_area("粘贴多个 TikTok 视频链接（每行一个）", height=200, placeholder="https://www.tiktok.com/@user/video/123456789...")

# 提交按钮
if st.button("开始提取"):
    if not keywords or not video_links_input:
        st.warning("请填写关键词和视频链接。")
    else:
        keyword_list = [kw.strip().lower() for kw in keywords.split(",")]
        video_links = [link.strip() for link in video_links_input.strip().splitlines() if link.strip()]
        
        matched_results = []
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        for link in video_links:
            try:
                response = requests.get(link, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                text_content = soup.get_text(separator=" ").lower()

                for kw in keyword_list:
                    if kw in text_content:
                        matched_results.append({"Keyword": kw, "Video Link": link})
                        break
            except Exception as e:
                st.error(f"无法处理链接：{link}，原因：{e}")

        if matched_results:
            df = pd.DataFrame(matched_results)
            st.success(f"共找到 {len(df)} 条包含关键词的视频链接。")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 下载 CSV 文件", csv, "tiktok_keywords.csv", "text/csv")
        else:
            st.info("未找到任何匹配关键词的链接。")

st.markdown("---")
st.caption("Made with ❤️ by inflation team.")
