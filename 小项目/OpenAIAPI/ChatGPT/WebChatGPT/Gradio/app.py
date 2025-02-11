import os
import random
import sys

import gradio as gr

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
import matplotlib
from Models.model import CallChatGPT3

matplotlib.pyplot.switch_backend("Agg")

SEED = 51
SESSIONNUM = 1
SESSIONINDEX = 0


# 一、聊天
def chatbot_interaction_1st(question, messages):
    messages = messages or []
    if question:
        answer_list, _ = gpt_model(question)
        answer = answer_list[SESSIONINDEX]
    else:
        answer = "很高兴遇见你！我是一个AI语言模型，我能为你提供准确和公正的信息！"
    messages.append((question, answer))
    text = ""

    return messages, messages, text


def clear_text_1st():
    messages1 = ""
    messages2 = None
    text = ""

    return messages1, messages2, text


def reset_session_1st():
    gpt_model.reset_messages()
    messages1 = ""
    messages2 = None
    text = ""

    return messages1, messages2, text


# 二、问答
def chatbot_interaction_2st(question):
    if question:
        answer_list, _ = gpt_model(question)
        answer = answer_list[SESSIONINDEX]
        # TODO: Latex渲染bug的缓解方案
        answer = answer.replace(r"$\sqrt{}$", "√")
        answer = answer.replace(r"$\sqrt{ }$", "√")
    else:
        answer = "很高兴遇见你！我是一个AI语言模型，我能为你提供准确和公正的信息！"
    text = ""

    return answer, text


def clear_text_2st():
    answer = "<br>"
    text = ""

    return answer, text


def reset_session_2st():
    gpt_model.reset_messages()
    answer = "<br>"
    text = ""

    return answer, text


# 日志
def password_generator(seed=51):
    random.seed(seed)
    num_list = list(range(1, 10))
    random.shuffle(num_list)
    password = ""
    for num in num_list:
        password += str(num)
    password = str(int(password) // 2)

    return password


def load_logs_1st(logs, filename, password):
    if password == password_generator(SEED):
        if not filename:
            text1 = "名称错误，无权操作！"
            text2 = ""
            return logs, text1, text2
        else:
            logspath = os.path.join(gpt_model.logsdir, filename)

        if os.path.exists(logspath) and (
            os.path.splitext(os.path.basename(logspath))[-1] == ".log"
        ):
            with open(logspath, "r") as f:
                logs = f.read()
            # TODO: Latex渲染问题的缓解方案
            logs = logs.replace(r"$\sqrt{}$", "√")
            logs = logs.replace(r"$\sqrt{ }$", "√")
            text1 = f"日志「{filename}」已导入！"
            text2 = ""
        else:
            text1 = "名称错误，无权操作！"
            text2 = ""
    else:
        text1 = ""
        text2 = "密码错误，无权操作！"

    return logs, text1, text2


def clear_text_3st():
    logs = "<br>"
    text1 = ""
    text2 = ""

    return logs, text1, text2


def detele_logs_1st(logs, filename, password):
    if password == password_generator(SEED):
        if not filename:
            text1 = "名称错误，无权操作！"
            text2 = ""
            return logs, text1, text2
        else:
            logspath = os.path.join(gpt_model.logsdir, filename)

        if os.path.exists(logspath) and (os.path.splitext(filename)[-1] == ".log"):
            os.remove(logspath)
            text1 = f"日志「{filename}」已删除！"
            text2 = ""
        else:
            text1 = "名称错误，无权操作！"
            text2 = ""
    else:
        text1 = ""
        text2 = "密码错误，无权操作！"

    return logs, text1, text2


def reset_session_3st(logs, password):
    if password == password_generator(SEED):
        gpt_model.reset_logger()
        text1 = f"当前日志已重置！"
        text2 = ""
    else:
        text1 = ""
        text2 = "密码错误，无权操作！"

    return logs, text1, text2


if __name__ == "__main__":
    # 后端
    gpt_model = CallChatGPT3(
        api_key="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",
        model="gpt-3.5-turbo",
        n=SESSIONNUM,
    )

    # 前端
    # TODO 改进UI使其布局更加合理
    with gr.Blocks() as demo:
        with gr.Box():
            gr.Markdown(
                "<center><h1>OpenAI</h1><h5>Welcome To Play - Code By HaoDaXia</h5></center>"
            )
            """控件显示"""
            # 一、聊天
            with gr.Tab(label="聊天", id=0):
                init_state = gr.State()
                with gr.Column():
                    with gr.Accordion(label="Bot"):
                        out_text_1st = gr.Chatbot(show_label=False)
                    in_text_1st = gr.Textbox(
                        label="输入",
                        show_label=False,
                        lines=5,
                        max_lines=10,
                        placeholder="请输入文字！",
                    )
                    with gr.Box():
                        with gr.Column():
                            start_btn_1st = gr.Button("开始")
                            with gr.Accordion(label="More", open=False):
                                with gr.Row():
                                    clear_btn_1st = gr.Button("清空")
                                    reset_btn_1st = gr.Button("重启")
                    gr.Examples(
                        ["你好！"],
                        [in_text_1st],
                    )

            # 二、问答
            with gr.Tab(label="问答", id=1):
                with gr.Column():
                    with gr.Accordion(label="Bot"):
                        with gr.Box():
                            out_text_2st = gr.Markdown("<br>")
                    in_text_2st = gr.Textbox(
                        label="输入",
                        show_label=False,
                        lines=5,
                        max_lines=10,
                        placeholder="请输入问题！",
                    )
                    with gr.Box():
                        with gr.Column():
                            ask_btn_1st = gr.Button("提问")
                            with gr.Accordion(label="More", open=False):
                                with gr.Row():
                                    clear_btn_2st = gr.Button("清空")
                                    reset_btn_2st = gr.Button("重启")
                    gr.Examples(
                        ["什么是人工智能？"],
                        [in_text_2st],
                    )

            # TODO: 20230305 -> 写完论文: 增加语音对话特性与增加绘图特性
            # 三、对话
            with gr.Tab(label="对话", id=2):
                gr.Markdown(
                    "<center><h3>此模块将提供语音对话功能，类似Siri与小爱同学</h3><h3>敬请期待...</h3></center>"
                )
            # 四、绘画
            with gr.Tab(label="绘画", id=3):
                gr.Markdown(
                    "<center><h3>此模块将提供强化Prompt描述的绘画功能</h3><h3>敬请期待...</h3></center>"
                )

            # 日志
            with gr.Tab(label="日志", id=4):
                with gr.Column():
                    with gr.Accordion(label="Log"):
                        with gr.Box():
                            log_text_1st = gr.Markdown("<br>")
                    in_text_3st = gr.Textbox(
                        label="输入",
                        show_label=False,
                        lines=1,
                        max_lines=1,
                        placeholder="请输入名称！",
                    )
                    in_text_4st = gr.Textbox(
                        label="输入",
                        show_label=False,
                        lines=1,
                        max_lines=1,
                        placeholder="请输入密码！",
                    )
                    with gr.Box():
                        with gr.Column():
                            load_btn_1st = gr.Button("导入")
                            with gr.Accordion(label="More", open=False):
                                with gr.Row():
                                    clear_btn_3st = gr.Button("清空")
                                    detele_btn_1st = gr.Button("删除")
                                    reset_btn_3st = gr.Button("重启")

        """控件行为"""
        # 一、对话
        start_btn_1st.click(
            chatbot_interaction_1st,
            inputs=[in_text_1st, init_state],
            outputs=[out_text_1st, init_state, in_text_1st],
        )
        clear_btn_1st.click(
            clear_text_1st, inputs=[], outputs=[out_text_1st, init_state, in_text_1st]
        )
        reset_btn_1st.click(
            reset_session_1st,
            inputs=[],
            outputs=[out_text_1st, init_state, in_text_1st],
        )

        # 二、问答
        ask_btn_1st.click(
            chatbot_interaction_2st,
            inputs=[in_text_2st],
            outputs=[out_text_2st, in_text_2st],
        )
        clear_btn_2st.click(
            clear_text_2st, inputs=[], outputs=[out_text_2st, in_text_2st]
        )
        reset_btn_2st.click(
            reset_session_2st, inputs=[], outputs=[out_text_2st, in_text_2st]
        )

        # 日志
        load_btn_1st.click(
            load_logs_1st,
            inputs=[log_text_1st, in_text_3st, in_text_4st],
            outputs=[log_text_1st, in_text_3st, in_text_4st],
        )
        clear_btn_3st.click(
            clear_text_3st, inputs=[], outputs=[log_text_1st, in_text_3st, in_text_4st]
        )
        detele_btn_1st.click(
            detele_logs_1st,
            inputs=[log_text_1st, in_text_3st, in_text_4st],
            outputs=[log_text_1st, in_text_3st, in_text_4st],
        )
        reset_btn_3st.click(
            reset_session_3st,
            inputs=[log_text_1st, in_text_4st],
            outputs=[log_text_1st, in_text_3st, in_text_4st],
        )

    demo.launch(server_name="127.0.0.1", server_port=7865, share=True, debug=True)
