import re
import numpy as np
from bs4 import BeautifulSoup
import math

from pyecharts.charts import Bar, Page, Line
from pyecharts import options as opts
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

def get_perf_bar(
    operators_list:list, device_time_cost: dict, chart_title: str, chart_id: str
):
    perf_bar = (
        Bar(init_opts=opts.InitOpts(width="1400px", height="500px", chart_id=chart_id))
        .add_xaxis(list(device_time_cost.keys()))
        .reversal_axis()
    )
    data = list(device_time_cost.values())
    transposed_data = list(map(list, zip(*data)))
    for operator, time_costs in zip(operators_list, transposed_data):
        perf_bar.add_yaxis(
            operator,
            list(time_costs),
            stack="stack1",
            category_gap="50%",
            label_opts=opts.LabelOpts(is_show=True, position="top"),
        )

    perf_bar.set_global_opts(
        yaxis_opts=opts.AxisOpts(
            type_="category", name="硬件资源", position="left", offset=10
        ),
        xaxis_opts=opts.AxisOpts(
            type_="value",
            name="耗时(ms)",
            position="right",
            offset=10,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="red")
            ),
        ),
        title_opts=opts.TitleOpts(title=f"{chart_title}",pos_left="center",pos_bottom="bottom"),
    )
    return perf_bar

def get_perf_table(operators_list:list, device_time_cost: dict):
    data = list(device_time_cost.values())
    transposed_data = list(map(list, zip(*data)))
    for i, _ in enumerate(transposed_data):
        transposed_data[i] = [operators_list[i]] + transposed_data[i]

    cols = ["操作"]
    for key in device_time_cost.keys():
        cols.append(key+"(ms/Frame)")
    perf_table = Table()
    perf_table.add(cols, transposed_data)
    perf_table.set_global_opts(
        title_opts=ComponentTitleOpts(title="平均耗时表")
        # title_opts=opts.TitleOpts(title=f"平均耗时表", pos_left="center",pos_bottom="bottom"),
    )
    return perf_table

def get_perf_line(
    device_usage_data: dict,
    date_time_data: list,
    chart_id: str,
    title_str:str,
    axis_opts: dict,
):
    device_usage_line = Line(
        init_opts=opts.InitOpts(width="1500px", height="500px", chart_id=chart_id)
    ).add_xaxis(date_time_data)

    for device, usage in device_usage_data.items():
        device_usage_line.add_yaxis(
            series_name=device,
            y_axis=usage,
            is_smooth=True,
            is_symbol_show=False,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=2),
        )

    device_usage_line.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"实时信息("+title_str+")",
            pos_left="center",
            pos_bottom="bottom"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=50),
            opts.DataZoomOpts(type_="inside", range_start=0, range_end=50),
        ],
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(
            # name=axis_opts["name"], type_="value", max_=axis_opts["max"]
            name=axis_opts["name"], type_="log", max_=axis_opts["max"]
        ),
    )

    return device_usage_line


def analyze_log(log_data:str):
    operators_info = {}
    operator_id = 0
    pattern = r"(Perf,.*?)$"
    for line in log_data:
        match = re.search(pattern, line)
        if match:
            operator_info = {}
            operator_info_list = line.split(",")
            operator_info["device"] = operator_info_list[1].strip()
            operator_info["operator"] = operator_info_list[2]
            operator_info["time"] = int(float(operator_info_list[3].strip().split(" ")[0]))
            operator_info["frames"] = int(float(operator_info_list[4].split(".")[0].split(",")[0]))
            operator_id += 1
            operators_info[operator_id] = operator_info

    return operators_info

def analyze_init_log(log_data:str):
    operators_info = {}
    operator_id = 0
    pattern = r"(PerfInit,.*?)$"
    for line in log_data:
        match = re.search(pattern, line)
        if match:
            operator_info = {}
            operator_info_list = line.split(",")
            operator_info["device"] = operator_info_list[1]
            operator_info["operator"] = operator_info_list[2]+"(Init)"
            operator_info["time"] = int(float(operator_info_list[3].split(" ")[0]))
            operator_info["frames"] = int(float(operator_info_list[4].split(".")[0].split(",")[0]))
            operator_id += 1
            operators_info[operator_id] = operator_info
    return operators_info

def get_time_per_operator(operators_info: dict):
    device_time_cost = {}
    for operator_info in operators_info.values():
        device = operator_info["device"]
        operator = operator_info["operator"]
        time = operator_info["time"]
        fream = operator_info["frames"]
        if device not in device_time_cost:
            device_time_cost[device] = {}
        if operator not in device_time_cost[device]:
            device_time_cost[device][operator] = {
                "time": [],
                "frames": 1,
                "num": 0,
            }

        device_time_cost[device][operator]["time"].append(round(time / 1000, 3))
        device_time_cost[device][operator]["frames"] = fream
        device_time_cost[device][operator]["num"] += 1
    return device_time_cost


def get_average_time(total_time_cost_per_device: dict, operators_list: list):
    average_time_cost_per_device = {}
    for device, time_costs in total_time_cost_per_device.items():
        if device not in average_time_cost_per_device:
            average_time_cost_per_device[device] = []
        for operator in operators_list:
            if operator not in time_costs.keys():
                average_time_cost_per_device[device].append("")
            else:
                average_time_cost_per_device[device].append(
                    round(sum(time_costs[operator]["time"]) / (time_costs[operator]["num"]*time_costs[operator]["frames"]), 3)
                )
    return average_time_cost_per_device

def re_render_page(html_path:str, task_name:str):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    h1 = soup.new_tag("style")
    h1.string = """
    h1 {
        font-size: 36px; 
        text-align: center; 
    }
    """
    soup.head.append(h1)

    h1_tag = soup.new_tag("h1")
    h1_tag.string = f"{task_name} 性能分析"
    soup.body.insert(0, h1_tag)

    for p in soup.find_all("body"):
        p["style"] = "text-align: center;"

    element2 = soup.find(id="bar1")
    if element2:
        current_style = element2.get("style", "")
        new_style = "margin: 0 auto;"
        if "margin" in current_style:
            element2["style"] = re.sub(r"margin:[^;]+", new_style, current_style)
        else:
            element2["style"] = f"{current_style}; {new_style}".strip("; ")

    element3 = soup.find(id="line0")
    if element3:
        current_style = element3.get("style", "")
        new_style = "margin: 0 auto;  margin-top: 40px;"
        if "margin" in current_style:
            element3["style"] = re.sub(r"margin:[^;]+", new_style, current_style)
        else:
            element3["style"] = f"{current_style}; {new_style}".strip("; ")

    element4 = soup.find(id="line1")
    if element4:
        current_style = element4.get("style", "")
        new_style = "margin: 0 auto;"
        if "margin" in current_style:
            element4["style"] = re.sub(r"margin:[^;]+", new_style, current_style)
        else:
            element4["style"] = f"{current_style}; {new_style}".strip("; ")

    for p in soup.find_all("table"):
        p["style"] = (
            "margin: 0 auto; margin-top: 0px; width: 1200px; height: 180px; text-align: left"
        )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

import os

def get_algo_perf_page(algo_perf_log: str, task_name: str):
    with open(algo_perf_log, "r+") as f:
        lines = f.readlines()

    operators_info = analyze_log(lines)
    device_time_cost = get_time_per_operator(operators_info)
    operator_init_info = analyze_init_log(lines)
    device_time_init_cost = get_time_per_operator(operator_init_info)

    device_list = []
    operators_list = []
    for key, value in device_time_cost.items():
        if key not in device_list:
            device_list.append(key)
        for operator, _ in value.items():
            if operator not in operators_list:
                operators_list.append(operator)

    for key, value in device_time_init_cost.items():
        if key not in device_list:
            device_list.append(key)
        for operator, _ in value.items():
            if operator not in operators_list:
                operators_list.append(operator)

    total_time_cost_per_device = {}
    for device in device_list:
        if device not in total_time_cost_per_device.keys():
            total_time_cost_per_device[device] = []
        for opertaor in operators_list:
            try:
                operator_info = device_time_cost[device][opertaor]
                total_time_cost_per_device[device].append(operator_info["time"])
            except KeyError:
                total_time_cost_per_device[device].append("")

    time_dict_img = {}
    time_dict_batch = {}
    time_images_max_values = []
    time_batchs_max_values = []
    len_images = 0
    len_batchs = 0
    batch_size = 1
    for device, time_costs in device_time_cost.items():
        for op, detal in time_costs.items():
            if(detal["frames"] != 1):
                batch_size = detal["frames"]

    for device, time_costs in device_time_cost.items():
        for op, detal in time_costs.items():
            key_new = "{}_{}".format(device, op)
            if(detal["frames"] != 1):
                if len(detal["time"]) > len_batchs:
                    len_batchs = len(detal["time"])
                len_temp = len(detal["time"])*detal["frames"]
                detal_image = {"time": [None] * len_temp}
                for i in range(0, len_temp):
                    detal_image["time"][i] =  round(detal["time"][int(i/batch_size)] /batch_size, 3)
                time_dict_img[key_new]=detal_image["time"]
                time_dict_batch[key_new] = detal["time"]
                time_images_max_values.append(max(detal_image["time"]))
                time_batchs_max_values.append(max(detal["time"]))
            else:
                if len(detal["time"]) > len_images:
                    len_images = len(detal["time"])
                len_temp = int(len(detal["time"])/batch_size)
                detal_batch = {"time": [None] * len_temp}
                for i in range(0, len_temp):
                    value_sum = 0
                    for j in range(0,batch_size):
                        value_sum = value_sum+detal["time"][i*batch_size+j]
                    detal_batch["time"][i] =  round(value_sum, 3)

                time_dict_img[key_new]=detal["time"]
                time_dict_batch[key_new]=detal_batch["time"]
                time_images_max_values.append(max(detal["time"]))
                time_batchs_max_values.append(max(detal_batch["time"]))

    realtime_images_opts = {"name": "时间", "max": math.ceil(max(time_images_max_values))}
    realtime_batchs_opts = {"name": "时间", "max": math.ceil(max(time_batchs_max_values))}

    ordered_images_list = list(range(len_images))
    if batch_size == 1:
        len_batchs = len_images
    ordered_batchs_list = list(range(len_batchs))
    # for key, value in time_dict.items():
    #     time_dict[key] = value[-len_min:]
    
    perf_info = Page()
    average_time_cost_per_device = get_average_time(device_time_cost, operators_list)
    average_time_init_per_device = get_average_time(device_time_init_cost, operators_list)

    for key, value in average_time_init_per_device.items():
        for i, k in enumerate(value):
            if average_time_cost_per_device[key][i] == "" and k != "":
                average_time_cost_per_device[key][i] = k

    perf_info.add(
        get_perf_table(
            operators_list, average_time_cost_per_device
        ),
        get_perf_bar(
            operators_list,
            average_time_cost_per_device,
            chart_title="平均耗时情况",
            chart_id="bar1",
        ),
        get_perf_line(
            time_dict_batch,
            ordered_batchs_list,
            chart_id="line0",
            title_str="One Batch",
            axis_opts=realtime_batchs_opts,
        ),
        get_perf_line(
            time_dict_img,
            ordered_images_list,
            chart_id="line1",
            title_str="One Image",
            axis_opts=realtime_images_opts,
        ),
    )

    perf_info.render("{}.html".format(task_name))
    re_render_page("./{}.html".format(task_name), task_name)
    print("Algorithm performance information is stored in {}.html".format(task_name))
