import argparse
import re
import numpy as np
from bs4 import BeautifulSoup

from pyecharts.charts import Bar, Page, Line
from pyecharts import options as opts
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

def get_device_usage_info(log_path:str):
    tpu_useage_data = []
    cpu_useage_data = []
    vpu_useage_data = []
    vpp_useage_data = []

    mem_tpu_data = []
    mem_vpu_data = []
    mem_vpp_data = []
    mem_host_data = []

    date_time_data = []

    with open(log_path, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            if line.find("DATE_TIME") >= 0:
                date_time_data.append(line.split("|")[1].split(" ")[1])

            if line.find("TPU_USAGE(%)") >= 0:
                temp_value = line.split("|")[-2]
                values = temp_value.split(" ")
                tpu_u = 0
                for value in values:
                     tpu_u = tpu_u + float(value)
                tpu_u = tpu_u / len(values)
                tpu_useage_data.append(tpu_u)


            if line.find("VPP_USAGE(%)") >= 0:
                vpp_all = line.split("|")[-2].split("|")[0].split(",")
                vpp_temp = []
                for vpp_use in vpp_all:
                    if len(vpp_use) > 0:
                        vpp_temp.append(float(vpp_use))
                if len(vpp_temp) > 0:
                    vpp_useage_data.append(float(np.average(vpp_temp)))
                else:
                    vpp_useage_data.append(0)

            if line.find("VPU_USAGE(%)") >= 0:
                vpu_all = line.split("|")[-2].split("|")[0].split(",")
                vpu_temp = []
                for vpu_use in vpu_all:
                    if len(vpu_use) > 0:
                        vpu_temp.append(float(vpu_use))
                if len(vpu_temp) > 0:
                    vpu_useage_data.append(vpu_temp)
                else:
                    vpu_useage_data.append([0])

            if line.find("CPU_ALL_USAGE(%)") >= 0:
                cpu_useage_data.append(float(line.split("|")[-2].split(",")[0]))

            if line.find("TPU_MEM_USAGE(%)") >= 0:
                mem_tpu_data.append(float(line.split("|")[-2]))

            if line.find("VPU_MEM_USAGE(%)") >= 0:
                mem_vpu_data.append(float(line.split("|")[-2]))

            if line.find("VPP_MEM_USAGE(%)") >= 0:
                mem_vpp_data.append(float(line.split("|")[-2]))

            if line.find("SYSTEM_MEM_USAGE(%)") >= 0:
                mem_host_data.append(float(line.split("|")[-2]))


    if len(tpu_useage_data) > 2000:
        tpu_useage_data = tpu_useage_data[-2000:]
    if len(cpu_useage_data) > 2000:
        cpu_useage_data = cpu_useage_data[-2000:]   
    if len(vpu_useage_data) > 2000:
        vpu_useage_data = vpu_useage_data[-2000:]
    if len(vpp_useage_data) > 2000:
        vpp_useage_data = vpp_useage_data[-2000:]

    if len(mem_tpu_data) > 2000:
        mem_tpu_data = mem_tpu_data[-2000:]
    if len(mem_host_data) > 2000:
        mem_host_data = mem_host_data[-2000:]   
    if len(mem_vpu_data) > 2000:
        mem_vpu_data = mem_vpu_data[-2000:]
    if len(mem_vpp_data) > 2000:
        mem_vpp_data = mem_vpp_data[-2000:]
    if len(date_time_data) > 2000:
        date_time_data = date_time_data[-2000:]

    data_array = np.array(vpu_useage_data)
    hash_rata = {
        "TPU(%)": tpu_useage_data,
        "CPU(%)": cpu_useage_data,
        "VPP(%)": vpp_useage_data,
    }

    for i in range(0, data_array.shape[1]):
        hash_rata[f"VPU{i}(%)"] = data_array[:, i].tolist()

    if len(cpu_useage_data) != 0 and len(cpu_useage_data) == len(mem_host_data) == len(
        date_time_data
    ):
        samples_num = len(cpu_useage_data)
    else:
        raise ValueError("not equal to CPU_USAGE, please check your log")

    for key in hash_rata.keys():
        if len(hash_rata[key]) == 0:
            hash_rata[key] = [0] * samples_num

    memory_usage = {
        "TPU_MEM(%)": mem_tpu_data,
        "VPU_MEM(%)": mem_vpu_data,
        "VPP_MEM(%)": mem_vpp_data,
        "HOST_MEM(%)": mem_host_data,
    }

    for key in memory_usage.keys():
        if len(memory_usage[key]) == 0:
            memory_usage[key] = [0] * samples_num

    return hash_rata, memory_usage, date_time_data

def get_clk_soc_info(log_path:str):
    tpu_clk_data = []
    cpu_clk_data = []
    vpu_clk_data = []

    date_time_data = []

    with open(log_path, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            if line.find("DATE_TIME") >= 0:
                date_time_data.append(line.split("|")[1].split(" ")[1])

            if line.find("CPU_CLK(Hz)") >= 0:
                temp_value = float(line.split("|")[1]+'.0')
                cpu_clk_data.append(temp_value/1000000)
            
            if line.find("TPU_CLK(Hz)") >= 0:
                temp_value = float(line.split("|")[1]+'.0')
                tpu_clk_data.append(temp_value/1000000)

            if line.find("VPU_CLK(Hz)") >= 0:
                temp_value = float(line.split("|")[1]+'.0')
                vpu_clk_data.append(temp_value/1000000)

    if len(tpu_clk_data) > 2000:
        tpu_clk_data = tpu_clk_data[-2000:]
    if len(cpu_clk_data) > 2000:
        cpu_clk_data = cpu_clk_data[-2000:]  
    if len(vpu_clk_data) > 2000:
        vpu_clk_data = vpu_clk_data[-2000:]  
    if len(date_time_data) > 2000:
        date_time_data = date_time_data[-2000:] 
    
    hash_rata = {
        "CPU_CLK(MHz)": cpu_clk_data,
        "TPU_CLK(MHz)": tpu_clk_data,
        "VPU_CLK(MHz)": vpu_clk_data,
    }
    if len(cpu_clk_data) != 0 and len(tpu_clk_data) and len(vpu_clk_data) == len(date_time_data):
        samples_num = len(cpu_clk_data)
    else:
        raise ValueError("not equal to CPU_USAGE, please check your log")

    for key in hash_rata.keys():
        if len(hash_rata[key]) == 0:
            hash_rata[key] = [0] * samples_num

    return hash_rata, date_time_data

def get_memory_info(log_path:str):
    result_dict = {}
    count = 0
    with open(log_path, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            if line.find("DDR_SIZE(MiB)") >= 0:
                result_dict["DDR(MiB)"] = line.split("|")[1]
                count = count + 1
            if line.find("SYSTEM_MEM(MiB)") >= 0:
                result_dict["系统内存(MiB)"] = line.split("|")[1]
                count = count + 1
            if line.find("TPU_MEM(MiB)") >= 0:
                result_dict["TPU内存(MiB)"] = line.split("|")[1]
                count = count + 1
            if line.find("VPP_MEM(MiB)") >= 0:
                result_dict["VPP内存(MiB)"] = line.split("|")[1]
                count = count + 1
            if line.find("VPU_MEM(MiB)") >= 0:
                result_dict["VPU内存(MiB)"] = line.split("|")[1]
                count = count + 1
            if count >= 5:
                break
        return result_dict
    
def get_vesion_info(log_path:str):
    result_dict = {}
    count = 0
    with open(log_path, "r") as file:
        while True:
            line = file.readline()
            if not line:
                break
            if line.find("CPU_MODEL") >= 0:
                result_dict["CPU_MODEL"] = line.split("|")[1]
                count = count + 1
            if line.find("SYSTEM_TYPE") >= 0:
                result_dict["操作系统"] = line.split("|")[1]
                count = count + 1
            if line.find("DTS_NAME") >= 0:
                result_dict["设备树"] = line.split("|")[1]
                count = count + 1
            if line.find("SDK_VERSION") >= 0:
                if line.find("||") >= 0:
                    count = count + 1
                    continue
                result_dict["SDK"] = line.split("|")[1]
                count = count + 1
            if line.find("LIBSOPHON_VERSION") >= 0:
                result_dict["libsophon"] = line.split("|")[1]
                count = count + 1
            if line.find("SOPHON_MEDIA_VERSION") >= 0:
                result_dict["sophon-media"] = line.split("|")[1]
                count = count + 1
            if count >= 6:
                break
        return result_dict


def get_work_mode_soc(log_path:str):
    is_soc = True
    with open(log_path, "r") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                if line.find("WORK_MODE") >= 0:
                    if line.find("PCIE") >= 0:
                        is_soc = False
                    break
    return is_soc
                    
def get_perf_line(
    device_usage_data: dict,
    date_time_data: list,
    chart_id: str,
    axis_opts: dict,
    chart_title: str=None,
):
    device_usage_line = Line(
        init_opts=opts.InitOpts(width="100%", height="400px", chart_id=chart_id)
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
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
        ],
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(
            name=axis_opts["name"], type_="value", max_=axis_opts["max"]
        ),
    )

    if chart_title is not None:
         device_usage_line.set_global_opts(
            title_opts=opts.TitleOpts(title=f"{chart_title}"),
         )
    return device_usage_line

def re_render_page(html_path:str, task_name:str):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    h1 = soup.new_tag("style")
    h1.string = """
    h1 {
        font-size: 36px; 
        text-align: center; 
        margin: 0;
        padding: 0;
    }
    """
    soup.head.append(h1)

    h1_tag = soup.new_tag("h1")
    h1_tag.string = f"{task_name} 资源使用分析"
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

    for element in soup.find_all("line"):
        current_style = element.get("style", "")
        new_style = "margin: 0 auto;  margin-top: 40px;"
        if "margin" in current_style:
            element["style"] = re.sub(r"margin:[^;]+", new_style, current_style)
        else:
            element["style"] = f"{current_style}; {new_style}".strip("; ")

    for p in soup.find_all("table"):
        p["style"] = (
            "margin: 0 auto; margin-top: 0px; width: 80%; text-align: left"
        )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

def get_basic_info_table_cols(basic_info:dict, title:str):
    headers = list(basic_info.keys())
    rows = [list(basic_info.values())]

    perf_table = Table()
    perf_table.add(headers, rows)
    perf_table.set_global_opts(
        title_opts=ComponentTitleOpts(title=title)
    )
    return perf_table

def get_basic_info_table_rows(basic_info:dict, title:str, headers:list=["信息","版本号"]):
    rows = []
    
    for key,value in basic_info.items():
        rows.append([key,value])

    perf_table = Table()
    perf_table.add(headers, rows)
    perf_table.set_global_opts(
        title_opts=ComponentTitleOpts(title=title)
    )
    return perf_table

def get_device_usage_page(log_path:str, task_name:str):
    
    hash_rata, memory_usage, date_time_data = get_device_usage_info(log_path)
    device_opts = {"name": "设备", "max": 100}
    memory_opts = {"name": "内存", "max": 100}
    usage_info = Page()

    if(get_work_mode_soc(log_path)):
        meminfo = get_memory_info(log_path)
        version_info = get_vesion_info(log_path)
        usage_info.add(
            get_basic_info_table_cols(version_info,"版本信息"),
            get_basic_info_table_cols(meminfo,"内存布局"),
        )

    usage_info.add(
        get_perf_line(
            hash_rata,
            date_time_data,
            chart_id="line0",
            axis_opts=device_opts,
        ),
        get_perf_line(
            memory_usage,
            date_time_data,
            chart_id="line1",
            axis_opts=memory_opts,
        ),
    )

    if(get_work_mode_soc(log_path)):
        clk_data, date_data = get_clk_soc_info(log_path)
        clk_opts = {"name": "频率", "max": 2500}
        usage_info.add(
            get_perf_line(
                clk_data,
                date_data,
                chart_id="line2",
                axis_opts=clk_opts,
            ),
        )

    usage_info.render("{}.html".format(task_name))
    re_render_page("./{}.html".format(task_name), task_name)
    print("Device utilization information is stored in {}.html".format(task_name))