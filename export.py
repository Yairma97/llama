import json
from pymilvus import connections, utility, Collection

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

def export_milvus_data(host='localhost', port='19530', export_dir='./milvus_data', exclude_fields=None):
    """
    导出Milvus数据（排除指定字段）
    :param exclude_fields: 要排除的字段列表，默认排除content_vector
    """
    exclude_fields = exclude_fields or ["content_vector"]

    try:
        connections.connect(host=host, port=port, timeout=10)
        print(f"Connected to Milvus: {host}:{port}")

        import os
        os.makedirs(export_dir, exist_ok=True)

        for collection_name in utility.list_collections():
            print(f"\nProcessing: {collection_name}")

            col = Collection(collection_name)
            print(col)
            print(col.schema.fields)
            # 动态获取需要导出的字段
            valid_fields = [
                field.name
                for field in col.schema.fields
                if field.name not in exclude_fields
            ]
            print(f"Exporting fields: {valid_fields}")

            # 分页参数配置
            query_params = {
                "expr": "",
                # "output_fields": valid_fields,  # 使用过滤后的字段列表
                "output_fields": ["*"],
                "limit": 10000,
                "offset": 0
            }

            total = 0
            all_data = []
            while True:
                try:
                    results = col.query(**query_params)
                except Exception as e:
                    print(f"Query error: {str(e)}")
                    break

                if not results:
                    break

                # 处理特殊数据类型
                for item in results:
                    processed = {}
                    for k, v in item.items():
                        if hasattr(v, 'tolist'):  # 处理向量等numpy类型
                            processed[k] = v.tolist()
                        elif isinstance(v, bytes):  # 处理二进制数据
                            processed[k] = f"BINARY_DATA({len(v)} bytes)"
                        else:
                            processed[k] = v
                    all_data.append(processed)

                total += len(results)
                query_params["offset"] += len(results)
                print(f"Progress: {total} entities")

            # 保存数据
            # if all_data:
            #     filename = f"{export_dir}/{collection_name}.json"
            #     with open(filename, 'w') as f:
            #         json.dump(all_data, f, default=str, indent=2)
            #     print(f"Excluded fields: {exclude_fields}")
            #     print(f"Exported {len(all_data)} entities to {filename}")
            # else:
            #     print("No data found")
            if all_data:
                # 初始化变量
                file_index = 0
                current_file_size = 0
                current_data_chunk = []
                batch_size = 500  # 初始批量大小，可以根据数据的平均大小调整

                for index, item in enumerate(all_data):
                    # 将数据项添加到当前数据块
                    current_data_chunk.append(item)

                    # 每处理一定数量的数据后，检查当前数据块的大小
                    if (index + 1) % batch_size == 0 or index == len(all_data) - 1:
                        # 序列化当前数据块为 JSON 格式并计算大小
                        serialized_data = json.dumps(current_data_chunk, default=str, indent=2).encode('utf-8')
                        estimated_size = len(serialized_data)

                        # 如果当前数据块大小超过限制，则写入文件并开始新的数据块
                        if estimated_size > MAX_FILE_SIZE:
                            # 写入当前数据块到文件
                            filename = f"{export_dir}/{collection_name}_{file_index}.json"
                            with open(filename, 'w') as f:
                                json.dump(current_data_chunk, f, default=str, indent=2)
                            print(f"Exported {len(current_data_chunk)} entities to {filename}")

                            # 重置当前数据块和文件大小计数器
                            current_data_chunk = []
                            file_index += 1

                            # 动态调整批量大小
                            batch_size = max(1, batch_size // 2)  # 如果超出限制，减小批量大小
                        else:
                            # 如果当前数据块大小未超过限制，尝试增加批量大小
                            batch_size = min(len(all_data) - index, batch_size * 2)

                # 写入最后一个数据块（如果还有剩余数据）
                if current_data_chunk:
                    filename = f"{export_dir}/{collection_name}_{file_index}.json"
                    with open(filename, 'w') as f:
                        json.dump(current_data_chunk, f, default=str, indent=2)
                    print(f"Exported {len(current_data_chunk)} entities to {filename}")

                print(f"Excluded fields: {exclude_fields}")
            else:
                print("No data found")

    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        connections.disconnect()


if __name__ == "__main__":
    # 调用示例：排除content_vector和optional_bin_field
    export_milvus_data(
        host="localhost",
        port="19530",
        export_dir="./milvus_backup",
        exclude_fields=["content_vector", "optional_bin_field"]  # 可配置多个排除字段
    )