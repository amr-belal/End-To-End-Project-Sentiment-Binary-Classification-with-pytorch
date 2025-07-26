
def get_html_content():
    """محتوى HTML للواجهة الرئيسية"""
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>محلل المشاعر - Sentiment Analyzer</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                max-width: 600px;
                width: 100%;
                text-align: center;
            }
            
            h1 {
                color: #333;
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            
            .input-group {
                margin-bottom: 25px;
                text-align: right;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #555;
            }
            
            textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #e1e5e9;
                border-radius: 12px;
                font-size: 16px;
                font-family: inherit;
                resize: vertical;
                min-height: 120px;
                transition: all 0.3s ease;
                text-align: right;
            }
            
            textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .btn {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 15px 40px;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
            }
            
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .result {
                margin-top: 30px;
                padding: 25px;
                border-radius: 15px;
                text-align: right;
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.5s ease;
            }
            
            .result.show {
                opacity: 1;
                transform: translateY(0);
            }
            
            .result.positive {
                background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
                border-right: 5px solid #28a745;
            }
            
            .result.negative {
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                border-right: 5px solid #dc3545;
            }
            
            .result.error {
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                border-right: 5px solid #dc3545;
            }
            
            .loading {
                display: none;
                margin: 20px 0;
            }
            
            .spinner {
                width: 40px;
                height: 40px;
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .examples {
                margin-top: 20px;
                text-align: right;
            }
            
            .example-btn {
                display: inline-block;
                margin: 5px;
                padding: 8px 15px;
                background: rgba(102, 126, 234, 0.1);
                border: 1px solid #667eea;
                border-radius: 20px;
                color: #667eea;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 14px;
            }
            
            .example-btn:hover {
                background: #667eea;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 محلل المشاعر</h1>
            
            <div class="input-group">
                <label for="textInput">أدخل النص لتحليل مشاعره:</label>
                <textarea 
                    id="textInput" 
                    placeholder="اكتب النص هنا... مثال: 'This movie is amazing!' أو 'أحب هذا الفيلم'"
                ></textarea>
            </div>
            
            <button class="btn" onclick="analyzeSentiment()">
                تحليل المشاعر
            </button>
            
            <div class="examples">
                <p><strong>جرب هذه الأمثلة:</strong></p>
                <span class="example-btn" onclick="setExample('This movie is absolutely amazing!')">مثال إيجابي</span>
                <span class="example-btn" onclick="setExample('I hate this terrible product.')">مثال سلبي</span>
                <span class="example-btn" onclick="setExample('أحب هذا المنتج كثيراً')">مثال عربي</span>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>جاري تحليل المشاعر...</p>
            </div>
            
            <div class="result" id="result">
                <!-- النتائج ستظهر هنا -->
            </div>
        </div>

        <script>
            // رابط الـ API (نفس السيرفر)
            const API_BASE = window.location.origin;
            
            function setExample(text) {
                document.getElementById('textInput').value = text;
            }
            
            async function analyzeSentiment() {
                const textInput = document.getElementById('textInput');
                const resultDiv = document.getElementById('result');
                const loadingDiv = document.getElementById('loading');
                const btn = document.querySelector('.btn');
                
                const text = textInput.value.trim();
                
                if (!text) {
                    showResult('error', 'من فضلك أدخل نصاً لتحليل مشاعره.');
                    return;
                }
                
                // إظهار التحميل
                btn.disabled = true;
                btn.textContent = 'جاري التحليل...';
                loadingDiv.style.display = 'block';
                resultDiv.classList.remove('show');
                
                try {
                    // إرسال طلب للـ API
                    const response = await fetch(`${API_BASE}/api/predict`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: text })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok && data.success) {
                        const prediction = data.prediction;
                        const sentimentArabic = prediction.sentiment === 'positive' ? 'إيجابي' : 'سلبي';
                        const emoji = prediction.sentiment === 'positive' ? '😊' : '😞';
                        
                        showResult(
                            prediction.sentiment,
                            `${emoji} المشاعر: <strong>${sentimentArabic}</strong>`,
                            `الثقة: <strong>${prediction.confidence}</strong>`,
                            `النص المُدخل: "${data.input}"`
                        );
                    } else {
                        showResult('error', `خطأ: ${data.detail || 'خطأ غير معروف'}`);
                    }
                    
                } catch (error) {
                    showResult('error', `خطأ في الاتصال: ${error.message}`);
                } finally {
                    // إخفاء التحميل
                    btn.disabled = false;
                    btn.textContent = 'تحليل المشاعر';
                    loadingDiv.style.display = 'none';
                }
            }
            
            function showResult(type, ...messages) {
                const resultDiv = document.getElementById('result');
                
                let html = '';
                messages.forEach(message => {
                    html += `<p>${message}</p>`;
                });
                
                resultDiv.innerHTML = html;
                resultDiv.className = `result ${type}`;
                
                setTimeout(() => {
                    resultDiv.classList.add('show');
                }, 100);
            }
            
            // السماح بالإرسال عند الضغط على Enter
            document.getElementById('textInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    analyzeSentiment();
                }
            });
        </script>
    </body>
    </html>
    """

def get_test_html():
    """صفحة اختبار مطور"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Test Page</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .test-section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
            button { padding: 10px 20px; margin: 5px; cursor: pointer; }
            .result { margin-top: 10px; padding: 10px; background: #f0f0f0; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>API Test Interface</h1>
        
        <div class="test-section">
            <h3>Health Check</h3>
            <button onclick="testHealth()">Test /api/health</button>
            <div id="health-result" class="result"></div>
        </div>
        
        <div class="test-section">
            <h3>Prediction Test</h3>
            <input type="text" id="test-text" placeholder="Enter text to analyze" style="width: 300px; padding: 8px;">
            <button onclick="testPredict()">Test /api/predict</button>
            <div id="predict-result" class="result"></div>
        </div>
        
        <script>
            const API_BASE = window.location.origin;
            
            async function testHealth() {
                try {
                    const response = await fetch(`${API_BASE}/api/health`);
                    const data = await response.json();
                    document.getElementById('health-result').innerHTML = 
                        `<strong>Status:</strong> ${response.status}<br>
                         <strong>Response:</strong> <pre>${JSON.stringify(data, null, 2)}</pre>`;
                } catch (error) {
                    document.getElementById('health-result').innerHTML = `<strong>Error:</strong> ${error.message}`;
                }
            }
            
            async function testPredict() {
                const text = document.getElementById('test-text').value;
                if (!text) {
                    alert('Please enter text to analyze');
                    return;
                }
                
                try {
                    const response = await fetch(`${API_BASE}/api/predict`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text: text })
                    });
                    const data = await response.json();
                    document.getElementById('predict-result').innerHTML = 
                        `<strong>Status:</strong> ${response.status}<br>
                         <strong>Response:</strong> <pre>${JSON.stringify(data, null, 2)}</pre>`;
                } catch (error) {
                    document.getElementById('predict-result').innerHTML = `<strong>Error:</strong> ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """