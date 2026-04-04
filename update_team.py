import os

# 获取所有 MD 文件
md_files = [f for f in os.listdir('.') if f.endswith('.md')]

for filename in md_files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换负责人
    content = content.replace('**负责人**: 私人助手（伊）', '**负责人**: 项目经理')
    
    # 替换团队表格 - 多步替换
    # 1. 替换项目负责人行
    content = content.replace(
        '| 项目负责人 | 私人助手（伊） | 整体流程管理、需求制定、SDD 文档、验收 |',
        '| 项目经理 | 项目经理 | 整体流程管理、需求制定、项目推进、验收 |'
    )
    # 2. 替换开发人员行
    content = content.replace(
        '| 开发人员 | 开发 K | 代码开发与实现 |',
        '| 开发 | 开发 | 代码开发与实现、技术架构设计 |'
    )
    # 3. 替换测试人员行
    content = content.replace(
        '| 测试人员 | 测试 C | 测试计划与用例、质量验收 |',
        '| 测试 | 测试 | 测试计划与用例、质量验收 |'
    )
    
    # 4. 在项目经理和开发之间插入产品行（如果还没有的话）
    if '| 项目经理 | 项目经理 |' in content and '| 产品 | 产品 |' not in content:
        content = content.replace(
            '| 项目经理 | 项目经理 | 整体流程管理、需求制定、项目推进、验收 |\n| 开发 | 开发 |',
            '| 项目经理 | 项目经理 | 整体流程管理、需求制定、项目推进、验收 |\n| 产品 | 产品 | 产品设计、需求分析、用户体验 |\n| 开发 | 开发 |'
        )
    
    # 5. 替换下一步行动中的开发 K 和测试 C
    content = content.replace('开发 K 确认技术栈', '开发确认技术栈')
    content = content.replace('测试 C 输出测试计划框架', '测试输出测试计划框架')
    content = content.replace('测试 C', '测试')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'✅ Updated: {filename}')

print('\n所有文档已更新完成！')
