import csv
from dataclasses import dataclass
from typing import List, Dict
import asyncio
from zhipu_client import ZhipuClient

# 模拟LLM的本地化处理函数（实际使用时可替换为API调用）
def local_llm(query: str) -> dict:
    """模拟LLM返回结构化数据示例"""
    knowledge_db = {
        "勾股定理": {
            "definition": "直角三角形斜边平方等于两直角边平方之和",
            "dependencies": ["三角形基本性质", "平方运算"],
            "applications": ["距离计算", "几何证明"],
            "misconceptions": ["适用于所有三角形"]
        }
    }
    return knowledge_db.get(query, {})

@dataclass
class KnowledgeNode:
    id: str
    name: str
    definition: str
    unit: str
    level: str = "记忆层"
    
class KnowledgeGraphBuilder:
    def __init__(self):
        self.nodes = {}
        self.relations = []
        self.strategies = []
        self.llm = ZhipuClient()
    
    def add_node(self, node: KnowledgeNode):
        """添加知识点节点并自动生成ID"""
        node_id = f"N{len(self.nodes)+1:03d}"
        self.nodes[node_id] = node
        return node_id
    
    def build_from_curriculum(self, curriculum: List[Dict]):
        """根据教学大纲构建知识图谱"""
        for chapter in curriculum:
            # 模拟LLM知识提取
            knowledge_data = asyncio.run(self.llm.get_concept_analysis(chapter["name"]))
            
            # 创建知识节点
            node_id = self.add_node(KnowledgeNode(
                id="",
                name=chapter["name"],
                definition=knowledge_data.get("definition", ""),
                unit=chapter["unit"]
            ))
            
            # 构建关联关系
            for dep in knowledge_data.get("dependencies", []):
                if dep in self.nodes.values():
                    self.relations.append({
                        "source": self.get_id_by_name(dep),
                        "target": node_id,
                        "relation": "前置知识"
                    })
    
    def export_csv(self):
        """导出CSV文件"""
        # 生成节点表
        with open('knowledge_nodes.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id','name','type','definition','unit','cognitive_level','example','misconception'
            ])
            writer.writeheader()
            for nid, node in self.nodes.items():
                writer.writerow({
                    'id': nid,
                    'name': node.name,
                    'type': '核心概念',
                    'definition': node.definition,
                    'unit': node.unit,
                    'cognitive_level': node.level,
                    'example': "",
                    'misconception': ""
                })
        
        # 生成关系表（示例）
        with open('knowledge_relations.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['source','target','relation_type','weight','description'])
            for rel in self.relations:
                writer.writerow([rel['source'], rel['target'], '前置知识', 0.8, ''])

class CurriculumLoader:
    @staticmethod
    def load_sample_curriculum():
        """示例教学大纲数据结构"""
        return [
            {
                "unit": "八年级下册-三角形",
                "name": "勾股定理",
                "position": 2.3
            },
            {
                "unit": "九年级上册-函数",
                "name": "一次函数",
                "position": 3.1
            }
        ]

# 使用示例
if __name__ == "__main__":
    builder = KnowledgeGraphBuilder()
    curriculum = CurriculumLoader.load_sample_curriculum()
    builder.build_from_curriculum(curriculum)
    builder.export_csv() 