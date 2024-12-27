import json
import os
import random
import time

import click
import pandas as pd
from openai import OpenAI
from tqdm import tqdm

api_key = "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"

def _client():
    return OpenAI(api_key=api_key)


def generate_jsonl(excel_file: str, output_path: str, validation_split=0.2):
    """
    生成训练和验证数据
    :param excel_file: 语料库源文件
    :param output_path: 训练文件生成路径
    :param validation_split: 验证数据分割比例（默认为 0.2）
    """
    click.echo(f"从 {excel_file} 加载数据...")

    sheets = pd.read_excel(excel_file, sheet_name=None)
    training_data = os.path.join(output_path, "training_data.jsonl")
    validation_data = os.path.join(output_path, "validation_data.jsonl")
    with open(training_data, "w", encoding="utf-8") as train_file, \
            open(validation_data, "w", encoding="utf-8") as val_file:
        for sheet_name, df in sheets.items():
            click.echo(f"处理工作表: {sheet_name}")
            for _, row in df.iterrows():
                messages = [
                    {"role": "system",
                     "content": "You are an experienced E-commerce translator. Your responsibility is to translate the given Chinese sentence into Japanese."},
                    {"role": "user", "content": row["zh"]},
                    {"role": "assistant", "content": row["ja"]}
                ]
                json_entry = {"messages": messages}

                # 按照验证比例划分
                if random.random() < validation_split:
                    val_file.write(json.dumps(json_entry, ensure_ascii=False) + "\n")
                train_file.write(json.dumps(json_entry, ensure_ascii=False) + "\n")

    click.echo(f"训练数据已保存到 {training_data}")
    click.echo(f"验证数据已保存到 {validation_data}")


def upload_file(file_path):
    """
    上传文件到 OpenAI
    :param file_path: 文件路径
    :param purpose: 文件用途
    :return: 文件 ID
    """
    click.echo(f"正在上传文件: {file_path}")
    response = _client().files.create(file=open(file_path, "rb"), purpose="fine-tune")
    click.echo(f"文件上传成功，文件 ID: {response.id}")
    return response.id


def create_fine_tuning_job(training_file, validation_file, seed=None):
    """
    创建微调任务
    :param training_file: 训练文件 ID
    :param validation_file: 验证文件 ID
    :param seed: 随机种子
    """
    click.echo("正在创建微调任务...")
    response = _client().fine_tuning.jobs.create(
        training_file=training_file,
        validation_file=validation_file,
        model="gpt-4o-mini-2024-07-18",
        seed=seed
    )
    job_id = response.id
    click.echo(f"微调任务已创建，任务 ID: {job_id}")
    click.echo(f"任务状态: {response.status}")
    return job_id


def monitor_job(job_id, poll_interval=10):
    """
    监控微调任务状态
    :param job_id: 任务ID
    :param poll_interval: 状态轮询时间间隔（秒）
    """
    click.echo("开始监控微调任务...")
    start_time = time.time()

    with tqdm(desc="任务状态", unit="轮询", colour="blue") as pbar:
        while True:
            response = _client().fine_tuning.jobs.retrieve(job_id)  # 模拟 API 请求
            status = response.status
            elapsed_time = time.time() - start_time

            # 使用 tqdm 更新状态信息
            pbar.set_description(f"任务状态: {status}")
            pbar.set_postfix_str(f"耗时: {int(elapsed_time // 60)} 分 {int(elapsed_time % 60)} 秒")
            pbar.update(1)

            if status in ["succeeded", "failed"]:
                break
            time.sleep(poll_interval)

    fine_tuned_model = response.fine_tuned_model
    click.echo(f"任务 {job_id} 完成，状态: {status}")
    if status == "succeeded":
        click.echo(f"微调后的模型名称: {fine_tuned_model}")
