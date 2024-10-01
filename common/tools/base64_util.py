#!/usr/bin/env python3

import base64
import argparse
import pyperclip


def encode_file_to_base64(file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()  # 读取文件
        base64_encoded_data = base64.b64encode(file_data)  # 编码为 Base64
        base64_message = base64_encoded_data.decode('utf-8')  # 转换为字符串
    return base64_message


def decode_file_to_base64(base64_message, out_file_path):
    base64_bytes = base64_message.encode('utf-8')
    file_data = base64.b16decode(base64_bytes)
    with open(out_file_path, "wb") as file:
        file.write(file_data)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("operation", choices=["encode", "decode"], help="Operation to perform")
    arg_parser.add_argument("file_path", nargs="?", help="hand file path")

    args = arg_parser.parse_args()

    if args.operation == "encode":
        base_ = encode_file_to_base64(args.file_path)
        print(base_)
        pyperclip.copy(base_)
        print('Copied to clipboard')
    else:
        decode_file_to_base64(args.file_path, args.file_path)
