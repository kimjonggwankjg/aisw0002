import os
import openai
import streamlit as st

# OpenAI API 키 설정
os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
openai.api_key = os.environ.get("OPENAI_API_KEY")

st.title("변명거리 & 이미지 생성기! 🤥")
st.write("변명거리와 이미지를 손쉽게 생성해보세요!")

# 세션 상태 초기화 (처음 실행 시)
if "generate_again" not in st.session_state:
    st.session_state.generate_again = False  # 다시 생성 버튼 상태 관리
if "lie" not in st.session_state:
    st.session_state.lie = ""

# 변명거리 생성
lie = st.text_input("어떤 상황인가요?", value=st.session_state.lie)
if st.button("변명거리 생성"):
    if lie.strip():
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "입력받은 상황의 변명거리를 여러 가지 만들어줘 그리고 아래에 영어로 번역해줘"},
                    {"role": "user", "content": lie},
                ],
                temperature=0.7,  # 다양성을 조정하는 파라미터
            )
            result = response["choices"][0]["message"]["content"]
            st.write(result)
            st.session_state.generate_again = True  # 다시 생성 버튼 활성화
            st.session_state.lie = lie  # 입력값 상태 유지
        except openai.error.OpenAIError as e:
            st.error(f"변명 생성 중 오류가 발생했습니다: {e}")
    else:
        st.warning("상황을 입력해주세요!")

# 다시 생성 버튼 (이전 변명을 기반으로 새로운 변명 생성)
if st.session_state.generate_again:
    if st.button("변명거리가 이게 뭐야! 다시 만들어와!"):
        st.write("다시 만들어 드릴게요....")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "입력받은 상황의 아주아주 굉장히 창의적인 변명거리를 간략하게 만들어줘 아래에 영어로 번역도 해주고"},
                    {"role": "user", "content": st.session_state.lie},
                ],
                temperature=0.9,  # 더 창의적인 응답을 위해 높게 설정
            )
            result = response["choices"][0]["message"]["content"]
            st.write(result)
        except openai.error.OpenAIError as e:
            st.error(f"변명 다시 생성 중 오류가 발생했습니다: {e}")

# 이미지 생성
st.write("---")
st.write("마음에 드는 변명을 적어주세요! 영어로 ㅎㅎ")
input_prompt = st.text_input("어떤 이미지를 생성할까요? 좀 간단하게 영어로 적어야 잘되용 (예: 버스를 놓친 그림)")
if st.button("이미지 생성"):
    if input_prompt.strip():
        try:
            response = openai.Image.create(
                prompt=input_prompt,
                n=1,
                size="1024x1024",
            )
            image_url = response['data'][0]['url']
            st.image(image_url, caption=f"'{input_prompt}'에 대한 이미지", use_column_width=True)
        except openai.error.OpenAIError as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
    else:
        st.warning("이미지 생성에 필요한 입력값을 입력해주세요!")
