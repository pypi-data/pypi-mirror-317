import re

from scapy.layers.inet import TCP

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


def get_body(param, is_src):
    body = param.split("\r\n\r\n")[1].strip()
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
            res_field['plain_body_src'] = get_body(req, is_src=True)
        if content_type_is_plain(res):
            res_field['plain_body_dst'] = get_body(res, is_src=False)

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
