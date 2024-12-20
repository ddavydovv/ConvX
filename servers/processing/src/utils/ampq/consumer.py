import asyncio
import json
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import aiormq
from aiormq.abc import DeliveredMessage

from servers.processing.src.config import settings
from servers.processing.src.services.converting.pdf_format import PdfMessageHandler
# from servers.processing.src.services.converting.csv_format import CsvMessageHandler
# from servers.processing.src.services.converting.xlsx_format import ExcelMessageHandler
# from servers.processing.src.services.converting.txt_format import TxtMessageHandler
# from servers.processing.src.services.converting.docx_format import WordMessageHandler

from servers.processing.src.utils.ampq.publisher import RabbitMQPublisher
from servers.processing.src.utils.exec import run_in_executor


callback_functions = {
    'PDF_WORD': PdfMessageHandler.func_convert_PDF_WORD,
    # 'PDF_TXT': PdfMessageHandler.func_convert_PDF_TXT,
    # 'WORD_PDF': WordMessageHandler.func_convert_WORD_PDF,
    # 'WORD_TXT': WordMessageHandler.func_convert_WORD_TXT,
    # 'EXCEL_CSV': ExcelMessageHandler.func_convert_EXCEL_CSV,
    # 'CSV_EXCEL': CsvMessageHandler.func_convert_CSV_EXCEL,
    # 'TXT_WORD': TxtMessageHandler.func_convert_TXT_WORD,
    # 'TXT_PDF': TxtMessageHandler.func_convert_TXT_PDF,
    # 'TXT_CSV': TxtMessageHandler.func_convert_TXT_CSV
}


class RabbitMQConsumer:

    @classmethod
    async def consume(cls, exchange_name, exchange_type, queue_name, routing_key, prefetch_count):
        connection = await aiormq.connect(settings.rabbit.url)
        channel = await connection.channel()
        await channel.exchange_declare(
            exchange_name,
            exchange_type=exchange_type
        )
        declare_ok = await channel.queue_declare(queue_name)
        await channel.queue_bind(
            queue=declare_ok.queue,
            exchange=exchange_name,
            routing_key=routing_key
        )
        await channel.basic_qos(prefetch_count=prefetch_count)
        await channel.basic_consume(
            declare_ok.queue,
            partial(
                cls.on_message
            ),
            no_ack=False
        )
        await asyncio.Future()

    @staticmethod
    async def on_message(message: DeliveredMessage):
        body: list = json.loads(message.body.decode())
        with ProcessPoolExecutor() as executor:
            body = await run_in_executor(
                executor,
                callback_functions.get(body['mode']),
                body
            )
        await message.channel.basic_ack(delivery_tag=message.delivery.delivery_tag)
        await RabbitMQPublisher.publish(
            exchange_name='processing_documents_finished',
            exchange_type='direct',
            routing_key='processing_documents_finished_key',
            body=body
        )