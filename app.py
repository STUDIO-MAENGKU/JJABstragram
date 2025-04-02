import streamlit as st
import openai
from PIL import Image
import io
import os

# GPT 및 DALL·E API 키 설정
openai.api_key = ""

# 스타일 옵션을 위한 함수 (GPT-4 모델을 사용)
def generate_diary_entry(keywords, text, style):
    prompt = f"다음 내용을 바탕으로 {style} 스타일로 일기를 작성해주세요:\n"
    prompt += f"키워드: {', '.join(keywords)}\n"
    prompt += f"내용: {text}\n"
    
    # GPT-4로 일기 작성
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 최신 GPT 모델
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response['choices'][0]['message']['content'].strip()

# DALL·E API 호출하여 이미지 스타일 변환
def generate_styled_image(original_image, style):
    # DALL·E API를 사용하여 스타일 변경된 이미지를 생성
    description = f"Upload된 이미지를 바탕으로 {style} 스타일로 변환된 이미지를 생성해주세요."

    response = openai.Image.create(
        prompt=description,
        n=1,
        size="1024x1024",  # 생성할 이미지 크기
    )
    
    # 변환된 이미지 URL을 반환
    image_url = response['data'][0]['url']
    return image_url

# 이미지를 저장하는 함수
def save_image(image, path):
    with open(path, "wb") as f:
        f.write(image.getbuffer())



st.set_page_config(page_title="JJOBstagram", layout="wide")
# 제목 영역 꾸미기
st.markdown("""
    <h1 style='text-align: center; font-size: 48px; margin-bottom: 20px; color: #786458;'>
        📸 JJOB stagram 📸
    </h1>
    <hr style='border: 1px solid #a27652;'>
""", unsafe_allow_html=True)

# 가로 레이아웃: 이미지 업로드 + 텍스트 입력
col1, col2 = st.columns(2)

with col1:
    st.subheader("📷 짭스타 이미지 업로드")
    photo = st.file_uploader("사진을 선택하세요", type=["jpg", "png", "jpeg"])
    
    if photo is not None:
        st.image(photo, caption="업로드된 이미지", use_column_width=True)

        # 이미지 저장 버튼
        save_path = os.path.join("saved_images", photo.name)
        if st.button("💾 이미지 저장"):
            if not os.path.exists("saved_images"):
                os.makedirs("saved_images")
            save_image(photo, save_path)
            st.success(f"✅ 이미지가 `{save_path}`에 저장되었습니다.")

with col2:
    st.subheader("📝 게시물 키워드 및 내용 입력")
    keywords = st.text_input("키워드를 입력하세요 (쉼표로 구분)", "")
    text = st.text_area("내용을 작성하세요", height=200)

# 스타일 선택 (세로로 아래에)
st.markdown("---")
st.subheader("🎨 스타일을 선택하세요")
style_options = ["지브리", "이토 준지", "판타지", "호러", "로맨스"]
style = st.selectbox("스타일을 선택하세요", style_options)

# 버튼 클릭 시 동작
if st.button("🚀 일기 작성 및 스타일 이미지 생성"):
    if photo and keywords and text:
        diary_entry = generate_diary_entry(keywords.split(','), text, style)
        st.subheader("📖 생성된 일기")
        st.write(diary_entry)

        styled_image_url = generate_styled_image(photo, style)
        st.subheader(f"🖼️ {style} 스타일로 변환된 이미지")
        st.image(styled_image_url, caption=f"{style} 스타일 이미지", use_column_width=True)
    else:
        st.error("⚠️ 모든 필드를 채워주세요!")

# 아래에 간단한 푸터 추가
st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 14px; color: grey;'>
        Made with ❤️ by (주)studio-maengku<br>
    </p>
""", unsafe_allow_html=True)