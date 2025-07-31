import streamlit as st
import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد دالة التنبؤ (مع معالجة الأخطاء)
try:
    from app.predict import predict_statement
    model_loaded = True
except Exception as e:
    st.error(f"error: {e}")
    model_loaded = False

# إعداد الصفحة
st.set_page_config(
    page_title="sentiment analyzer",
    page_icon="🎭",
    layout="centered"
)

# العنوان والوصف
st.title("🎭 sentiment analyzer")
st.markdown("enter any text to analyze its sentiment")

# مربع إدخال النص
text_input = st.text_area(
    "أدخل النص هنا:",
    placeholder="مثال: This movie is absolutely amazing!",
    height=100
)

# زر التحليل
if st.button("🔍 تحليل المشاعر", type="primary"):
    if text_input.strip():
        if model_loaded:
            try:
                # تحليل النص
                result = predict_statement(text_input)
                
                if isinstance(result, tuple):
                    sentiment, confidence = result
                    
                    # عرض النتيجة
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if sentiment == "positive":
                            st.success(f"😊 positive")
                        else:
                            st.error(f"😞 negative")
                    
                    with col2:
                        st.info(f"الثقة: {confidence}")
                        
                else:
                    # إذا كانت النتيجة sentiment فقط
                    if result == "positive":
                        st.success("😊 positive review ")
                    else:
                        st.error("😞 negative review")
                        
            except Exception as e:
                st.error(f"error in predict {e}")
        else:
            st.error("Not found")
    else:
        st.warning("insert text :)" )

# أمثلة للتجربة
st.markdown("---")
st.subheader("examples:")

examples = [
    "This movie is absolutely amazing!",
    "I hate this product, it's terrible",
    "The weather is okay today",
    "I love spending time with my family",
    "This service is disappointing"
]

for example in examples:
    if st.button(f"📝 {example}", key=example):
        st.rerun()
