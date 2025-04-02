import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import os
import io

# OpenAI 설정
client = OpenAI(api_key="")  # <- 진짜 키로 바꿔줘

# 일기 생성 함수 (GPT-4)
def generate_diary_entry(keywords, text, style):
    prompt = f"""다음 내용을 바탕으로 {style} 스타일로 감성적인 하루 일기를 작성해주세요.
키워드: {', '.join(keywords)}
내용: {text}"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

# GPT-4o가 DALL·E용 프롬프트 생성
def create_dalle_prompt(image_file, style):
    image_bytes = image_file.read()
    base64_img = base64.b64encode(image_bytes).decode("utf-8")
    image_file.seek(0)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"이 이미지를 {style} 애니메이션 스타일로 변환한 그림을 만들 수 있는 DALL·E 프롬프트를 생성해줘."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_img}"}}
                ]
            }
        ]
    )
    return response.choices[0].message.content.strip()

# DALL·E로 이미지 생성
def generate_image_with_dalle(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return response.data[0].url

# 이미지 저장 함수
def save_image(image_file, path):
    with open(path, "wb") as f:
        f.write(image_file.getbuffer())

# ───────────────────────────────
# Streamlit UI 시작
st.set_page_config(page_title="짭스타그램", layout="centered")
st.title("📸 짭스타그램")
st.caption("AI가 당신의 하루를 예술로 바꿔드립니다.")

# 섹션 1: 이미지 업로드 및 저장
st.header("1. 인스타 이미지 업로드")
photo = st.file_uploader("사진을 선택하세요", type=["jpg", "png", "jpeg"])
if photo:
    st.image(photo, caption="업로드된 이미지", use_column_width=True)
    save_path = os.path.join("saved_images", photo.name)
    if st.button("💾 이미지 저장"):
        os.makedirs("saved_images", exist_ok=True)
        save_image(photo, save_path)
        st.success(f"이미지가 {save_path}에 저장되었습니다.")

# 섹션 2: 텍스트 입력
st.header("2. 키워드와 내용을 입력하세요")
keywords = st.text_input("키워드를 입력하세요 (쉼표로 구분)", "")
text = st.text_area("내용을 작성하세요", "")

# 섹션 3: 스타일 선택
st.header("3. 스타일을 선택하세요")
style_options = ["지브리", "이토 준지", "판타지", "호러", "로맨스", "사이버펑크"]
style = st.selectbox("스타일을 선택하세요", style_options)

# 생성 버튼
if st.button("✍️ 일기 작성 및 스타일 이미지 생성"):
    if photo and keywords and text:
        with st.spinner("일기 작성 중..."):
            diary_entry = generate_diary_entry(keywords.split(','), text, style)
        st.subheader("📝 생성된 일기")
        st.write(diary_entry)

        with st.spinner("이미지 변형 중... (GPT가 프롬프트 생성하고, DALL·E가 그림 그리는 중)"):
            dalle_prompt = create_dalle_prompt(photo, style)
            styled_image_url = generate_image_with_dalle(dalle_prompt)

        st.subheader(f"🎨 {style} 스타일로 변환된 이미지")
        st.image(styled_image_url, caption=f"{style} 스타일 이미지", use_column_width=True)

    else:
        st.error("❗ 모든 필드를 채워주세요!")
