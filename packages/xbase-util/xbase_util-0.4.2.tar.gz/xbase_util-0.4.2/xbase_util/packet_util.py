import re

from scapy.layers.inet import TCP

from xbase_util.xbase_constant import plain_content_type_columns, packetKeyname, src_dst_header, statisticHeader, \
    features_key, plain_body_columns


def content_type_is_plain(packet):
    """
    从单个包（包括header和body）中获取content-type并判断是否为可见类型
    :param packet:
    :return:
    """
    if ":" not in packet:
        return False
    for item in packet.replace("-", "_").replace(" ", "").lower().split("\n"):
        if "content_type" in item:
            if ":" not in item:
                continue
            content_type = item.split(":")[1].replace("\r", "").strip()
            return content_type in plain_content_type_columns
    return False


def filter_visible_chars(data):
    """
    过滤不可见字符，仅保留可打印的ASCII字符
    :param data:
    :return:
    """
    return ''.join(chr(b) for b in data if 32 <= b <= 126 or b in (9, 10, 13))


def get_all_columns(
        contains_packet_column=False,
        contains_src_dst_column=False,
        contains_statistic_column=False,
        contains_features_column=False,
        contains_plain_body_column=False,
        contains_pcap_flow_text=False
):
    result_columns = []
    if contains_packet_column:
        result_columns += packetKeyname
    if contains_src_dst_column:
        result_columns += src_dst_header
    if contains_statistic_column:
        result_columns += statisticHeader
    if contains_features_column:
        result_columns += features_key
    if contains_plain_body_column:
        result_columns += plain_body_columns
    if contains_pcap_flow_text:
        result_columns.append(contains_pcap_flow_text)
    return result_columns


def get_all_packets_by_regx(packets):
    """
    通过正则pcap获取所有包的数据
    :param packets:
    :return:
    """
    streams = b""
    for pkt in packets:
        if TCP in pkt:
            streams += bytes(pkt[TCP].payload)
    text = filter_visible_chars(streams)
    pattern = r"(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) \/[^\s]* HTTP\/\d\.\d"
    requests = re.split(f"(?={pattern})", text, re.M)
    all_packets = []
    for item in requests:
        if len(re.findall(pattern, item)) != 0:
            request_text = ""
            response_text = ""
            response_text_list = re.findall(r"HTTP/\d\.\d \d{3}[\s\S]*", item)
            if len(response_text_list) != 0:
                # 有响应数据
                response_text = response_text_list[0]
            if response_text == "":
                # 没有响应数据，那么全是请求数据
                request_text = item
            else:
                # 有响应数据，用正则获取请求数据
                request_re = re.search(
                    r"(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) \/[^\s]* HTTP\/\d\.\d[\s\S]*?\r\n\r\n", item)
                if request_re:
                    request_text = request_re.group(0)
                else:
                    request_text = ""
            all_packets.append({"req": request_text, "res": response_text})
    return all_packets
