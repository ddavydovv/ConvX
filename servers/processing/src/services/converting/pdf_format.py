import io
from pdf2docx import Converter

from servers.processing.src.utils.s3.client import s3_client


class PdfMessageHandler:

    @classmethod
    def func_convert_PDF_WORD(cls, body):
        user_id = str(body['user_id'])
        category = str(body['category'])
        mode = str(body['mode'])
        filename = str(body['filename'])
        filepath = str(body['filepath'])

        file_stream = s3_client.download_file(filepath)
        file_stream.seek(0)
        file_stream.read()

        output_word_file = f'{filepath.split('/')[3].split('.')[0]}.docx'
        output_word_stream = io.BytesIO()

        cv = Converter(stream=file_stream)
        cv.convert(output_word_stream, start=0, end=None)
        cv.close()

        output_word_stream.seek(0)
        s3_path = f'{user_id}/{category}/{mode}/{output_word_file}'
        s3_client.upload_file(s3_path, output_word_stream)

        body['processed_filepath'] = s3_path
        body['processed_filename'] = f'{filename.split('.')[0]}.docx'

        return body