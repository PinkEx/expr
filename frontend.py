import textwrap

import gradio as gr

from backend import tokenize
from backend import translate, get_productions, get_SLR_table, analysis

def render_table(table, title):
    table_html = table.to_html(index=False)
    table_html = f"""
    <div style="text-align: center; margin-bottom: 10px;">
        <strong>{title}</strong>
    </div>
    <div style="overflow: auto; max-height: 300px;">
        <table style="border-collapse: collapse; width: 100%;">
            <thead style="position: sticky; top: 0; background-color: white;">
                {table_html.split('<thead>')[1].split('</thead>')[0]}
            </thead>
            <tbody>
                {table_html.split('<tbody>')[1].split('</tbody>')[0]}
            </tbody>
        </table>
    </div>
    """
    return table_html

# 创建 Gradio 接口
with (gr.Blocks() as demo):
    with gr.Tabs():
        with gr.TabItem("词法扫描器"):
            gr.Markdown("# 词法扫描器")

            code_input = gr.Textbox(lines=1, placeholder="Enter your code here...", label="输入类C源代码")

            process_btn = gr.Button("扫描")

            code_output = gr.Markdown()

            table_output = gr.HTML()

            def update_outputs(source_code):
                code_block, table_block = tokenize(source_code)
                return textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 10px;">
                    <strong>Token串表</strong>
                </div>
                <pre>
                <code>
                {}
                </code>
                </pre>
                """).format(code_block), render_table(
                    table_block, "符号表"
                )

            process_btn.click(fn=update_outputs, inputs=code_input, outputs=[code_output, table_output])

        with gr.TabItem("LR文法分析器"):
            gr.Markdown("# LR文法分析器")

            gr.HTML(
                render_table(
                    get_productions(), "类C语言文法产生式"
                )
            )

            gr.HTML(
                render_table(
                    get_SLR_table(), "类C语言SLR分析表"
                )
            )

            code_input = gr.Textbox(lines=1, placeholder="Enter your code here...", label="输入类C源代码")

            process_btn = gr.Button("编译")

            with gr.Row():
                code_output1 = gr.Markdown()
                code_output2 = gr.Markdown()
                code_output3 = gr.Markdown()

            def update_outputs(source_code):
                code_block1, code_block2, code_block3, success = translate(source_code)

                code_block1 = textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 10px;">
                    <strong>类C源代码</strong>
                </div>
                <pre>
                <code>
                {}
                </code>
                </pre>
                """).format(code_block1)

                code_block2 = textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 10px;">
                    <strong>归约记录</strong>
                </div>
                <pre>
                <code>
                {}
                归约结果: {}
                </code>
                </pre>
                """).format(code_block2, "成功" if success else "失败")

                code_block3 = textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 10px;">
                    <strong>转移记录</strong>
                </div>
                <pre>
                <code>
                {}
                转移结果: {}
                </code>
                </pre>
                """).format(code_block3, "成功" if success else "失败")

                return code_block1, code_block2, code_block3

            process_btn.click(fn=update_outputs, inputs=code_input, outputs=[code_output1, code_output2, code_output3])

        with gr.TabItem("语义分析及中间代码生成"):
            gr.Markdown("# 语义分析及中间代码生成")

            code_input = gr.Textbox(lines=1, placeholder="Enter your code here...", label="输入类C源代码")

            process_btn = gr.Button("分析/生成")

            with gr.Row():
                code_output1 = gr.Markdown()
                code_output2 = gr.Markdown()

            def update_outputs(source_code):
                code_block1, code_block2 = analysis(source_code)

                code_block1 = textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 10px;">
                    <strong>抽象语法树</strong>
                </div>
                <pre>
                <code>
                {}
                </code>
                </pre>
                """).format(code_block1)

                code_block2 = textwrap.dedent("""
                <div style="text-align: center; margin-bottom: 10px;">
                    <strong>中间代码</strong>
                </div>
                <pre>
                <code>
                {}
                </code>
                </pre>
                """).format(code_block2)

                return code_block1, code_block2

            process_btn.click(fn=update_outputs, inputs=code_input, outputs=[code_output1, code_output2])

demo.launch()
