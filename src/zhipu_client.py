import os
import httpx
from dotenv import load_dotenv

load_dotenv()

class ZhipuClient:
    def __init__(self):
        self.api_key = os.getenv("ZHIPU_API_KEY")
        self.base_url = "https://open.bigmodel.cn/api/paas/v3/"

    async def get_concept_analysis(self, concept: str) -> dict:
        """安全获取知识结构分析"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""请用JSON格式返回初中数学概念的结构化分析：
        {concept}需要包含：
        1. 核心定义（50字内）
        2. 3个前置知识点
        3. 2个典型应用场景
        4. 1个常见学习误区
        格式示例：
        {{
            "definition": "...",
            "dependencies": ["...", "..."],
            "applications": ["...", "..."],
            "misconceptions": ["..."]
        }}"""
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}chat/completions",
                    headers=headers,
                    json={
                        "model": "glm-4",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.3
                    },
                    timeout=10
                )
                response.raise_for_status()
                return self._parse_response(response.json())
            except httpx.HTTPError as e:
                print(f"API请求失败: {str(e)}")
                return {}

    def _parse_response(self, data: dict) -> dict:
        """安全解析API响应"""
        try:
            content = data['choices'][0]['message']['content']
            return eval(content)  # 实际使用时应替换为JSON解析
        except (KeyError, SyntaxError) as e:
            print(f"响应解析失败: {str(e)}")
            return {} 