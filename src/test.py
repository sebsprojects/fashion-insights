from hdfs import InsecureClient

if __name__ == "__main__":
    host = "localhost"
    port = 9870
    hdfs_user = "hadoop"
    hdfs_base_url = f"http://{host}:{port}"

    client = InsecureClient(hdfs_base_url, user=hdfs_user)

    # Test data storage in hdfs
    hdfs_directory = "/user/hadoop/data"
    hdfs_file_path = f"{hdfs_directory}/README.md"
    local_file_path = "../README.md"

    client.makedirs(hdfs_file_path)
    resp = client.upload(hdfs_file_path, local_file_path, overwrite=True)
    print(resp)