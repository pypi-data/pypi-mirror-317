import os.path

import click

from cagu_toolkit.service.gpt import generate_jsonl
from cagu_toolkit.service.gpt import upload_file, create_fine_tuning_job, monitor_job


@click.group()
def gpt():
    """GPT"""
    pass


@gpt.command(name='train-corpus')
@click.option(
    '-f', '--file',
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="指定语料库文件路径"
)
@click.option(
    '-d', '--dir',
    required=False,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
    help="指定jsonl文件生成路径",
    default='.'
)
def train_corpus(file, dir):
    """语料训练"""
    generate_jsonl(excel_file=file, output_path=dir)
    click.echo("请检查生成的训练文件")
    goon = click.prompt("是否继续？", type=bool, default='Y')
    if not goon:
        return
    training_file_id = upload_file(os.path.join(dir, "training_data.jsonl"))
    validation_file_id = upload_file(os.path.join(dir, "validation_data.jsonl"))

    job_id = create_fine_tuning_job(
        training_file=training_file_id,
        validation_file=validation_file_id,
        seed=105
    )

    monitor_job(job_id=job_id)
