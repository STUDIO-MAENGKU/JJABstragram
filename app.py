import streamlit as st
import openai
import os

# GPT 및 DALL·E API 키 설정
openai.api_key = ""  # OpenAI API 키 입력

# 스타일 옵션을 위한 함수 (GPT-4 모델을 사용)
def generate_diary_entry(keywords, text):
    prompt = f"다음 내용을 바탕으로 인스타 그램 게시글을 작성해주세요:\n"
    prompt += f"키워드: {', '.join(keywords)}\n"
    prompt += f"내용: {text}\n"
    
    # GPT-4로 일기 작성
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 최신 GPT 모델
        messages=[{
            "role": "system", "content": "You are a helpful Instagram Post Assistant."
        }, {
            "role": "user", "content": prompt
        }],
        max_tokens=500
    )
    return response['choices'][0]['message']['content'].strip()

def generate_styled_image(keywords, style):
    description = f"""다음 키워드의 내용이 담긴 이미지를 {style} 스타일로 생성해주세요. 
    키워드 : {', '.join(keywords)}"""

    response = openai.Image.create(
        prompt=description,
        n=1,
        size="1024x1024",  # 생성할 이미지 크기
    )
    
    # 변환된 이미지 URL을 반환
    image_url = response['data'][0]['url']
    return image_url

# Streamlit 페이지 설정
st.set_page_config(page_title="JJABstagram", layout="wide")

# 제목 영역 꾸미기
st.markdown("""
    <h1 style='text-align: center; font-size: 48px; margin-bottom: 20px; color: #786458;'>
        📸 JJAB stagram 📸
    </h1>
    <hr style='border: 1px solid #a27652;'>
""", unsafe_allow_html=True)

# 가로 레이아웃: 키워드 및 텍스트 입력
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 게시물 키워드 및 내용 입력")
    keywords = st.text_input("키워드를 입력하세요 (쉼표로 구분)", "")
    text = st.text_area("내용을 작성하세요", height=200)

with col2:
    st.markdown("---")
    st.subheader("🎨 스타일을 선택하세요")
    style_options = ["지브리", "이토 준지", "판타지", "호러", "로맨스"]
    style = st.selectbox("스타일을 선택하세요", style_options)
    
    # 버튼 클릭 시 동작
    if st.button("🚀 일기 작성 및 스타일 이미지 생성"):
        if keywords and text:
            # 일기 작성
            diary_entry = generate_diary_entry(keywords.split(','), text)
            st.subheader("✍️ 작성된 일기")
            st.write(diary_entry)
            
            # 스타일 이미지 생성
            styled_image_url = generate_styled_image(keywords.split(','), style)
            st.subheader("🖼️ 스타일 변환된 이미지")
            st.image(styled_image_url, caption=f"스타일: {style}", use_column_width=True)
        else:
            st.error("키워드와 내용을 모두 입력해 주세요!")

# 아래에 간단한 푸터 추가
st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 14px; color: grey;'>
        Made with ❤️ by (주)studio-maengku<br>
    </p>
""", unsafe_allow_html=True)