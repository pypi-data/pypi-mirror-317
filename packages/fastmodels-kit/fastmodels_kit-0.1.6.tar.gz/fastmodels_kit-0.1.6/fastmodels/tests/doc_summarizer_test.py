# -*- coding: utf-8 -*-

from fastmodels import Client

# 初始化客户端
client = Client(
    api_key="",
    project_id=""
)

stream = False
response = client.easyllm.doc_summarizer.create(
    easyllm_id="5sxZZviFgUXoiZF4wznk8I",
    prompt="滴滴&美团账单复核COP\\n\\n一、滴滴&美团使用规则\\n\\n企业滴滴用车规则\\n因公外出：无时间限制，需备注用车事项。\\n公司活动：公司集体活动可用车，需备注用车事项。\\n加班用车（工作日）：工作日工作至晚上21:00，可选用工作日加班打车，1次/天，公司为出发地。\\n加班用车（节假日）：节假日加班，可选用节假日加班打车，2次/天，打车目的地和起始地为公司，如有特殊情况需要多次往返，可超过该用车次数。\\n差旅用车：出差期间可打车前往机场、高铁站等地点乘坐交通工具或从该地点返回（待定），以及该差旅期间因公行程。\\n\\n企业美团点餐规则\\n工作日：工作日加班至晚上21:00，可于当日16:00-次日凌晨02:00使用美团点加班餐。\\n节假日：节假日到公司加班，可于当日时间段:11:00-14:00/17:00-00:00点加班餐。\\n出差期间使用加班餐需遵循上述加班规则。\\n仅支持配送到office(美团后台已配置)，到店自取或用餐视为违规。\\n\\n以下为每月滴滴&美团需检查违规项说明，可根据员工实际工作情况核对，若确认违规情况属实，员工需退回对应金额。\\n类型\\t序号\\t检查事项\\t检查方法\\n滴滴\\t1\\t工作日加班，最晚人脸打卡记录在21点前或无打卡记录；\\n节假日加班，无打卡记录\\t根据员工打卡记录，匹配员工当天的最晚打卡时间，判断是否加班\\n\\t2\\t工作日加班，出发地址非base office及附近\\n节假日加班，到达地或出发地非base office及附近\\t根据员工的实际出发地和实际目的地，判断是否为base office及附近\\n\\t3\\t员工打车权限为因公外出、公司活动、差旅用车的情况\\t根据打车日期、时间和员工备注判断是否属实\\n美团\\t1\\t加班点餐的配送地址非base office\\t根据员工备注“到店自取、堂食、更改地址”等，或者取货地址不是base office判断\\n\\t2\\t工作日最晚打卡记录在21点前或无打卡记录，节假日无打卡记录的\\t根据员工打卡记录，匹配员工当天的最晚打卡时间，根据打卡时间判断",
    stream=stream

)

# 打印输出
if stream:
    for chunk in response:
        for choice in chunk.choices:
            print(f"Index: {choice.index}, Content: {choice.delta.content}, Finish Reason: {choice.finish_reason}")
else:
    print(response.choices[0].message.content)