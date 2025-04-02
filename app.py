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

# Streamlit 앱 인터페이스
st.title("짭스타그램")

st.header("인스타 이미지 업로드")
photo = st.file_uploader("사진을 선택하세요", type=["jpg", "png", "jpeg"])

if photo is not None:
    # 이미지 표시
    st.image(photo, caption="업로드된 이미지", use_column_width=True)

    # 이미지 저장 버튼
    save_path = os.path.join("saved_images", photo.name)
    if st.button("이미지 저장"):
        # 이미지를 저장할 디렉토리가 없으면 생성
        if not os.path.exists("saved_images"):
            os.makedirs("saved_images")

        save_image(photo, save_path)
        st.success(f"이미지가 {save_path}에 저장되었습니다.")

st.header("키워드와 내용을 입력하세요")
keywords = st.text_input("키워드를 입력하세요 (쉼표로 구분)", "")
text = st.text_area("내용을 작성하세요", "")

st.header("스타일을 선택하세요")
style_options = ["지브리", "이토 준지", "판타지", "호러", "로맨스"]
style = st.selectbox("스타일을 선택하세요", style_options)

if st.button("일기 작성 및 스타일 이미지 생성"):
    if photo and keywords and text:
        # GPT-4로 일기 작성
        diary_entry = generate_diary_entry(keywords.split(','), text, style)
        st.subheader("생성된 일기")
        st.write(diary_entry)

        # DALL·E로 스타일 변경된 이미지 생성
        styled_image_url = generate_styled_image(photo, style)
        st.subheader(f"{style} 스타일로 변환된 이미지")
        st.image(styled_image_url, caption=f"{style} 스타일 이미지", use_column_width=True)
    else:
        st.error("모든 필드를 채워주세요!")


