import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="TikTok Keyword Comment Extractor", layout="centered")

st.title("🔍 TikTok Keyword Comment Extractor")
st.markdown("这个工具可以帮助你提取 TikTok 视频中评论或标题里包含指定关键词的内容，并导出链接。")

# 输入关键词
keywords = st.text_area("请输入关键词（多个关键词请用逗号或换行分隔）：")
keyword_list = [k.strip().lower() for k in re.split(',|\n', keywords) if k.strip()]

# 输入视频链接
video_links_raw = st.text_area("请输入 TikTok 视频链接（每行一个）：")
video_links = [v.strip() for v in video_links_raw.splitlines() if v.strip()]

# 模拟提取（实际应通过 API 或爬虫）
def mock_extract_comments(video_url):
    # 模拟评论数据
    sample_comments = [
        "I love this inflation hoodie!",
        "Where is this from?",
        "Drip hoodie goes crazy 🔥",
        "inflation jeans look cool!",
        "Mid tbh",
        "Anyone know the brand?"
    ]
    sample_title = "OOTD ft. my new drip hoodie 💥"
    return sample_title, sample_comments

# 提取 & 匹配关键词
results = []

if st.button("开始提取"):
    if not keyword_list or not video_links:
        st.warning("请填写关键词和视频链接")
    else:
        with st.spinner("正在提取中..."):
            for url in video_links:
                title, comments = mock_extract_comments(url)
                matched_text = []

                for kw in keyword_list:
                    for text in [title] + comments:
                        if kw in text.lower():
                            matched_text.append(text)

                if matched_text:
                    results.append({
                        "Video URL": url,
                        "Matched Text": "\n".join(set(matched_text))
                    })

        if results:
            df = pd.DataFrame(results)
            st.success(f"共提取到 {len(results)} 条命中视频记录！")
            st.dataframe(df)

            csv = df.to_csv(index=False)
            st.download_button("📥 下载 CSV 文件", data=csv, file_name="matched_comments.csv", mime="text/csv")

        else:
            st.info("没有命中关键词的视频")
