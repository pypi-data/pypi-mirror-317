import re

from scapy.layers.inet import TCP
from scapy.packet import Raw

from xbase_util.xbase_constant import plain_content_type_columns, packetKeyname, src_dst_header, statisticHeader, \
    features_key, plain_body_columns
from xbase_util.xbase_util import firstOrZero


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


def get_all_packets_by_reg(packets):
    req_pattern = re.compile(r"(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) \/[^\s]* HTTP\/\d\.\d[\s\S]*?\r\n\r\n",
                             re.DOTALL)
    req_res_pattern = re.compile(
        r"(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) \/[^\s]* HTTP\/\d\.\d[\s\S]*?(?=HTTP/\d\.\d \d{3} [a-zA-Z]+|$)",
        re.DOTALL)
    res_pattern = re.compile(r"HTTP/\d\.\d \d{3} [a-zA-Z]+.*", re.DOTALL)
    tcp_packet_map = {}
    for packet in packets:
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            raw_data = bytes(packet[Raw].load)
            ack = f"{packet[TCP].ack}"
            seq = packet[TCP].seq
            time = packet[TCP].time
            if f"{packet[TCP].ack}" not in tcp_packet_map:
                tcp_packet_map[ack] = {
                    "data": raw_data,
                    "time": [time],
                    "seq": [seq],
                    "last_seq": seq,
                    "ack": ack,
                    "len": [len(raw_data)],
                    "last_len": len(raw_data)
                }
            else:
                tcp_packet_map[ack]['data'] += raw_data
                tcp_packet_map[ack]['time'].append(time)
                tcp_packet_map[ack]['seq'].append(seq)
                tcp_packet_map[ack]['last_len'] = len(raw_data)
                tcp_packet_map[ack]['last_seq'] = seq
    packet_list = []
    for ack, data_set in tcp_packet_map.items():
        data_str = data_set['data'].decode("utf-8", errors="ignore")
        request_re = re.search(req_pattern, data_str)
        if request_re is None:
            continue
        next_ack = f"{data_set['last_len'] + data_set['last_seq']}"
        packet_data = data_set['data']
        request_time = data_set['time']
        req_len = len(packet_data)
        res_len = 0
        while True:
            # 持续往下一个包找，直到下一个包是请求为止，因为下一个包可能还是属于这个包的一部分，也可能是响应的一部分
            # 下一个包的ack存在
            if next_ack not in tcp_packet_map:
                print("没找到新的ack")
                break
            new_packet = tcp_packet_map[next_ack]
            # 判断新的包是不是响应包

            res_match = re.search(res_pattern, filter_visible_chars(new_packet['data']))
            if res_match is None:
                req_len += len(new_packet['data'])
            else:
                print("匹配到响应")
                res_len += len(new_packet['data'])
            # 判断新的包是不是第二个请求包
            if re.search(req_pattern, new_packet['data'].decode("utf-8", errors="ignore")):
                print("这个包是个新的请求包的开头，停止查找")
                break
            packet_data += new_packet['data']
            request_time += new_packet['time']
            next_ack = f"{new_packet['last_len'] + new_packet['last_seq']}"
        map = {}
        data = filter_visible_chars(packet_data)
        match_req = re.search(
            req_res_pattern,
            data)
        match_res = re.search(res_pattern, data)
        map['data'] = packet_data
        map['req_len'] = req_len
        map['res_len'] = res_len
        map['time'] = request_time
        map['req'] = match_req.group() if match_req is not None else ""
        map['res'] = match_res.group() if match_res is not None else ""
        packet_list.append(map)
    return packet_list


def get_body(param):
    body = "".join([item.strip() for item in param.split("\r\n\r\n") if item.strip() != "" and "HTTP/" not in param])
    return "" if body is None else body


def get_header_value(header_set, value):
    result = [item for item in header_set if value in item]
    if len(result) != 0:
        return result[0].replace(f"{value}:", "").strip()
    else:
        return ""


def get_detail_by_package(packets_from_pcap, publicField, use_regx):
    """
    通过pcap的数量分离session并完善相关字段
    :param packets_from_pcap: 通过PcAp解析出的包
    :param publicField: 原始的session单条数据
    :return: 完整的单条数据
    """
    res_field = publicField.copy()
    if use_regx:
        req = packets_from_pcap['req']
        res = packets_from_pcap['res']
    else:
        res = packets_from_pcap["response"]
        req = packets_from_pcap["request"]
    res_field["initRTT"] = firstOrZero(res_field.get("initRTT", 0))
    res_field["length"] = firstOrZero(res_field.get("length", 0))
    request_lines = req.strip().split("\n")
    http_request_lines = [item for item in request_lines if "HTTP" in item]
    if len(http_request_lines) != 0:
        first_line = http_request_lines[0].split(" ")
        res_field['http.clientVersion'] = str(first_line[2]).replace("\n", "").replace("\r", "")
        res_field['http.path'] = first_line[1]
        res_field['http.method'] = first_line[0]
    else:
        res_field['http.clientVersion'] = ''
        res_field['http.path'] = ''
        res_field['http.method'] = ''
    res_field['http.request-referer'] = get_header_value(header_set=request_lines, value="Referer")
    res_field['http.request-content-type'] = get_header_value(header_set=request_lines,
                                                              value="Content-Type")
    res_field['http.hostTokens'] = get_header_value(header_set=request_lines, value="Host")

    if use_regx:
        res_field['plain_body_src'] = ""
        res_field['plain_body_dst'] = ""
        if content_type_is_plain(req):
            res_field['plain_body_src'] = get_body(req)
        if content_type_is_plain(res):
            res_field['plain_body_dst'] = get_body(res)

    response_lines = res.strip().split("\n")
    http_response_lines = [item for item in response_lines if "HTTP" in item]
    if len(http_response_lines) != 0:
        first_line = http_response_lines[0].strip().split(" ")
        res_field['http.statuscode'] = first_line[1]
        res_field['http.serverVersion'] = first_line[0].split("/")[1]
    else:
        res_field['http.statuscode'] = ""
        res_field['http.serverVersion'] = ""
    res_field['http.response-server'] = get_header_value(header_set=response_lines, value="Server")
    res_field['http.response-content-type'] = get_header_value(header_set=response_lines,
                                                               value="Content-Type")
    for response in list(set(response_lines + request_lines)):
        key_value = response.replace("\r", "").split(":")
        if len(key_value) == 2:
            key = key_value[0].replace(" ", "").replace("-", "_").lower()
            value = key_value[1].replace(" ", "")
            if f"src_{key}" in src_dst_header:
                res_field[f"src_{key}"] = value
            if f"dst_{key}" in src_dst_header:
                res_field[f"dst_{key}"] = value
    return res_field
