import splunklib.client as client
from splunklib import results


def get_splunk_pa(start_time, end_time, splunk_host,
                  splunk_port,
                  splunk_username,
                  splunk_password,
                  splunk_scheme="https",
                  splunk_filter="THREAT AND NOT informational"):
    """
    获取PA威胁信息
    :param splunk_filter:
    :param start_time:
    :param end_time:
    :param splunk_host:
    :param splunk_port:
    :param splunk_username:
    :param splunk_password:
    :param splunk_scheme:
    :return:
    """
    service = client.connect(
        host=splunk_host,
        port=splunk_port,
        scheme=splunk_scheme,
        username=splunk_username,
        password=splunk_password
    )
    job = service.jobs.oneshot(
        """search index=idx_pa 
FILTER_TEXT
| rex field=_raw  "THREAT,(?P<LOG_TYPE>.+?),.*?,(?P<PA_DATE>.*?),(?P<SIP>.*?),(?P<DIP>.*?),(?:.*?,.*?,.*?){7},(?P<S_PORT>.*?),(?P<D_PORT>.*?),.*?,.*?,.*?,(?P<PROTOCOL>.*?),(?P<DENY_METHOD>.*?),(?P<THREAT_SUMMARY>.*?),(?P<SEVERITY>medium|high|critical|low),"  
| eval RAW_BAK=_raw 
| eval THREAT_TIME = strftime(strptime(PA_DATE, "%Y/%m/%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
| rex mode=sed field=_raw "s/.*?,\w{8}-\w{4}-\w{4}-\w{4}-\w{12},/start_ama_flag,/g"
| rex field=_raw "start_ama_flag,.*?,.*?,(?<XFF_IP>.*?),"
| eval _raw=RAW_BAK
| table THREAT_TIME,SIP,S_PORT, DIP, D_PORT,XFF_IP,PROTOCOL, DENY_METHOD, THREAT_SUMMARY, SEVERITY
| dedup THREAT_TIME,SIP,S_PORT, DIP, D_PORT,XFF_IP,PROTOCOL
            """.replace("FILTER_TEXT", splunk_filter), **{
            "earliest_time": start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "latest_time": end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "output_mode": "json",
            "count": 20000
        })
    return [item for item in results.JSONResultsReader(job) if isinstance(item, dict)]


def get_splunk_waf(start_time, end_time, splunk_host,
                   splunk_port,
                   splunk_username,
                   splunk_password,
                   splunk_scheme="https"):
    # splunk里面用这个
    """
sourcetype=changting:waf
| rex field=_raw (?P<THREAT_TIME>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2})
| rex field=_raw "\"src_ip\":\"(?<SIP>[^\"]+)\""
| rex field=_raw "\"protocol\":\"(?<PROTOCOL>[^\"]+)\""
| rex field=_raw "\"src_port\":(?<S_PORT>\d+)"
| rex field=_raw "\"dest_ip\":\"(?<DIP>[^\"]+)\""
| rex field=_raw "\"dest_port\":(?<D_PORT>\d+)"
| rex field=_raw "\"risk_level\":\"(?<SEVERITY>[^\"]+)\""
| rex field=_raw "\"action\":\"(?<DENY_METHOD>[^\"]+)\""
| rex field=_raw "\"reason\":\"(?<THREAT_SUMMARY>[^\"]+)\""
| rex field=_raw "\"x_forwarded_for\":\"(?<XFF_IP>[^\"]+)\""
| table THREAT_TIME,SIP,S_PORT,DIP,D_PORT,XFF_IP,PROTOCOL,DENY_METHOD,THREAT_SUMMARY,SEVERITY
| dedup THREAT_TIME,SIP,S_PORT,DIP,D_PORT,XFF_IP,PROTOCOL
    """
    service = client.connect(
        host=splunk_host,
        port=splunk_port,
        scheme=splunk_scheme,
        username=splunk_username,
        password=splunk_password
    )
    # | rex field=_raw "\\"src_port\\":(?<S_PORT>\d+)"
    # | rex field=_raw "\\"dest_port\\":(?<D_PORT>\d+)"
    exp = """search sourcetype=changting:waf
| rex field=_raw "(?P<THREAT_TIME>\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\+\\d{2}:\\d{2})"
| rex field=_raw "\\"dest_ip\\":\\"(?<DIP>[^\\"]+)\\"" 
| rex field=_raw "\\"src_ip\\":\\"(?<SIP>[^\\"]+)\\""
| rex field=_raw "\\"src_port\\":(?<S_PORT>\\d+)"
| rex field=_raw "\\"dest_port\\":(?<D_PORT>\\d+)"
| rex field=_raw "\\"protocol\\":\\"(?<PROTOCOL>[^\\"]+)\\""
| rex field=_raw "\\"x_forwarded_for\\":\\"(?<XFF_IP>[^\\"]+)\\""
| rex field=_raw "\\"action\\":\\"(?<DENY_METHOD>[^\\"]+)\\""
| rex field=_raw "\\"reason\\":\\"(?<THREAT_SUMMARY>[^\\"]+)\\""
| rex field=_raw "\\"risk_level\\":\\"(?<SEVERITY>[^\\"]+)\\""
| eval THREAT_TIME = strftime(strptime(THREAT_TIME, "%Y-%m-%dT%H:%M:%S"), "%Y-%m-%d %H:%M:%S")
| dedup THREAT_TIME,SIP,S_PORT,DIP,D_PORT,XFF_IP,PROTOCOL
| table THREAT_TIME,SIP,S_PORT,DIP,D_PORT,XFF_IP,PROTOCOL,DENY_METHOD,THREAT_SUMMARY,SEVERITY
        """
    job = service.jobs.oneshot(
        exp, **{
            "earliest_time": start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "latest_time": end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "output_mode": "json",
            "count": 20000
        })
    return [item for item in results.JSONResultsReader(job) if isinstance(item, dict)]
