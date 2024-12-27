#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2024-09-17 17:26:11
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2024-11-21 13:10:47
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\oa_draw.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.11
"""

import math
import warnings

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

__all__ = ["fig_minus", "create_gif", "add_cartopy", "add_gridlines", 'MidpointNormalize', "add_lonlat_unit", "plot_contourf", "plot_contourf_lonlat", "plot_quiver", "plot_contourf_cartopy"]

warnings.filterwarnings("ignore")


def fig_minus(ax_x=None, ax_y=None, cbar=None, decimal=None, add_space=False):
    """
    Description: 将坐标轴刻度中的负号替换为减号

    param {*} ax_x : x轴
    param {*} ax_y : y轴
    param {*} cbar : colorbar
    param {*} decimal : 小数位数
    param {*} add_space : 是否在非负数前面加空格

    return {*} ax_x or ax_y or cbar
    """
    if ax_x is not None:
        current_ticks = ax_x.get_xticks()
    if ax_y is not None:
        current_ticks = ax_y.get_yticks()
    if cbar is not None:
        current_ticks = cbar.get_ticks()
    # 先判断是否需要加空格，如果要，先获取需要加的索引
    if add_space:
        index = 0
        for _, tick in enumerate(current_ticks):
            if tick >= 0:
                index = _
                break
    if decimal is not None:
        # my_ticks = [(round(float(iii), decimal)) for iii in my_ticks]
        current_ticks = [f"{val:.{decimal}f}" if val != 0 else "0" for val in current_ticks]

    out_ticks = [f"{val}".replace("-", "\u2212") for val in current_ticks]
    if add_space:
        # 在非负数前面加两个空格
        out_ticks[index:] = ["  " + m for m in out_ticks[index:]]

    if ax_x is not None:
        ax_x.set_xticklabels(out_ticks)
        return ax_x
    if ax_y is not None:
        ax_y.set_yticklabels(out_ticks)
        return ax_y
    if cbar is not None:
        cbar.set_ticklabels(out_ticks)
        return cbar


# ** 将生成图片/已有图片制作成动图
def create_gif(image_list: list, gif_name: str, duration=0.2):  # 制作动图，默认间隔0.2
    """
    func        : 制作动图，将已有图片拼接
    description : Gif格式动图
    param        {*} image_list 图片列表
    param        {*} gif_name 动图名称（含路径）
    param        {*} duration 动图间隔
    return       {*} 自动保存至指定路径（包含于动图名称中）
    example     :
    """
    import imageio.v2 as imageio

    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, format="GIF", duration=duration)
    print("Gif制作完成！")
    return


# ** 转化经/纬度刻度
def add_lonlat_unit(lon=None, lat=None, decimal=2):
    """
    param        {*} lon : 经度列表
    param        {*} lat : 纬度列表
    param        {*} decimal : 小数位数
    return       {*} 转化后的经/纬度列表
    example     : add_lonlat_unit(lon=lon, lat=lat, decimal=2)
    """

    def _format_longitude(x_list):
        out_list = []
        for x in x_list:
            if x > 180:
                x -= 360
            # degrees = int(abs(x))
            degrees = round(abs(x), decimal)
            direction = "E" if x >= 0 else "W"
            out_list.append(f"{degrees:.{decimal}f}°{direction}" if x != 0 and x != 180 else f"{degrees}°")
        return out_list if len(out_list) > 1 else out_list[0]

    def _format_latitude(y_list):
        out_list = []
        for y in y_list:
            if y > 90:
                y -= 180
            # degrees = int(abs(y))
            degrees = round(abs(y), decimal)
            direction = "N" if y >= 0 else "S"
            out_list.append(f"{degrees:.{decimal}f}°{direction}" if y != 0 else f"{degrees}°")
        return out_list if len(out_list) > 1 else out_list[0]

    if lon and lat:
        return _format_longitude(lon), _format_latitude(lat)
    elif lon:
        return _format_longitude(lon)
    elif lat:
        return _format_latitude(lat)


# ** 添加网格线
def add_gridlines(ax, projection=ccrs.PlateCarree(), color="k", alpha=0.5, linestyle="--", linewidth=0.5):
    # add gridlines
    gl = ax.gridlines(crs=projection, draw_labels=True, linewidth=linewidth, color=color, alpha=alpha, linestyle=linestyle)
    gl.right_labels = False
    gl.top_labels = False
    gl.xformatter = LongitudeFormatter(zero_direction_label=False)
    gl.yformatter = LatitudeFormatter()

    return ax, gl


# ** 添加地图
def add_cartopy(ax, lon=None, lat=None, projection=ccrs.PlateCarree(), gridlines=True, landcolor="lightgrey", oceancolor="lightblue", cartopy_linewidth=0.5):

    # add coastlines
    ax.add_feature(cfeature.LAND, facecolor=landcolor)
    ax.add_feature(cfeature.OCEAN, facecolor=oceancolor)
    ax.add_feature(cfeature.COASTLINE, linewidth=cartopy_linewidth)
    # ax.add_feature(cfeature.BORDERS, linewidth=cartopy_linewidth, linestyle=":")

    # add gridlines
    if gridlines:
        ax, gl = add_gridlines(ax, projection)

    # set longitude and latitude format
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    # set extent
    if lon is not None and lat is not None:
        lon_min, lon_max = lon.min(), lon.max()
        lat_min, lat_max = lat.min(), lat.max()
        ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=projection)


# ** 自定义归一化类，使得0值处为中心点
class MidpointNormalize(mpl.colors.Normalize):
    """
    Description: 自定义归一化类，使得0值处为中心点

    param {*} mpl.colors.Normalize : 继承Normalize类
    return {*}

    Example:
    nrom = MidpointNormalize(vmin=-2, vmax=1, vcenter=0)
    """

    def __init__(self, vmin=None, vmax=None, vcenter=None, clip=False):
        self.vcenter = vcenter
        super().__init__(vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.vcenter, self.vmax], [0, 0.5, 1.0]
        return np.ma.masked_array(np.interp(value, x, y, left=-np.inf, right=np.inf))

    def inverse(self, value):
        y, x = [self.vmin, self.vcenter, self.vmax], [0, 0.5, 1]
        return np.interp(value, x, y, left=-np.inf, right=np.inf)


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------


# ** 设置colorbar格式
class _MyFormatter(mpl.ticker.ScalarFormatter):
    def __init__(self, cticks, fmt=None, useOffset=True, useMathText=True):
        mpl.ticker.ScalarFormatter.__init__(self, useOffset, useMathText)
        self.cticks = cticks
        self.fmt = fmt
        self.vmin = min(cticks)
        self.vmax = max(cticks)
        self.p_n = self.vmin < 0 and self.vmax > 0
        self.magnitude_min = int(math.modf(math.log10(min(abs(cticks[cticks != 0]))))[1])
        self.magnitude_max = int(math.modf(math.log10(max(abs(cticks))))[1])
        # print(self.vmin, self.vmax)

    def __call__(self, x, pos):
        if ((abs(x) < 1e-2) or (abs(x) > 1e4)) and x != 0:
            if self.magnitude_max - self.magnitude_min == 1 and (int(math.modf(math.log10(abs(x)))[1]) == self.magnitude_min):
                a, b = "{:.1e}".format(x).split("e")
                a = float(a) / 10
                b = int(b) + 1
            else:
                a, b = "{:.2e}".format(x).split("e")
                a = float(a)
                b = int(b)
            # return '${}{} \\times 10^{{{}}}$'.format(' ' if (self.p_n and x > 0) else '', a, b)
            return "${}{:.2f}$".format(" " if (self.p_n and x > 0) else "", a)
        elif x == 0:
            return "0"
        else:
            return mpl.ticker.ScalarFormatter.__call__(self, x, pos)


# ** 绘制单张填色图
def plot_contourf(pic_data, picname=None, c_map="rainbow", minmax=None, labels=None, ticks_space=None, ticks=None, figsize=(12, 9)):
    """
    func        : 绘制填色等值线图，单张
    description : 绘制单张填色等值线图，输入参数为横纵坐标、等值数据、图例标注等
    param       {*}pic_data : 填色等值线图的等值数据
    param       {*}picname : 图片保存的文件名(含路径)
    param       {*}c_map    : 颜色映射，默认rainbow
    param       {*}minmax   : 指定绘图的最大、小值，默认不指定
    param       {*}labels   : x、y轴以及图例的标注，默认不标注
    param       {*}ticks_space : x、y轴刻度，以及所显示的标签，默认不显示
    param       {*}figsize  : 图片大小，默认(12,9)
    example     : plot_contourf(pic_data, pictpath, var_name, c_map='bwr', labels=None, ticks_space=None, ticks=None, h=0, figsize=(12, 9))
    """
    cmap = mpl.colormaps.get_cmap(c_map)
    if minmax is not None:
        value_min, value_max = minmax[0], minmax[1]
    else:
        value_min, value_max = pic_data.nanmin(), pic_data.nanmax()
    v_bry = max(abs(value_min), abs(value_max))
    flag = (value_min < 0) and (value_max > 0)
    norm = mpl.colors.TwoSlopeNorm(vmin=-1 * v_bry, vcenter=0, vmax=v_bry) if flag else mpl.colors.Normalize(vmin=value_min, vmax=value_max)
    cticks = [num for num in np.linspace(-1 * v_bry if flag else value_min, v_bry if flag else value_max, 9)] if value_min != value_max else None
    levels = np.linspace(-1 * v_bry, v_bry, 20) if flag else None if value_min == value_max else np.linspace(value_min, value_max, 20)

    shape = np.array(pic_data).shape
    x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))

    fig, ax = plt.subplots(figsize=figsize)
    flag_lc = levels is not None and cticks is not None
    CS = ax.contourf(x, y, pic_data, cmap=cmap, norm=norm, levels=levels, extend="both") if flag_lc else ax.contourf(x, y, pic_data, cmap=cmap, norm=norm, extend="both")
    cb = fig.colorbar(CS, ax=ax, orientation="vertical", shrink=1, format="%.3g", spacing="uniform", ticks=cticks) if cticks is not None else fig.colorbar(CS, ax=ax, orientation="vertical", shrink=1, format="%.3g", spacing="uniform")
    """%.3g采用的是自动调整格式，也可设置为%.3f，则改为3位小数"""

    # 将格式化器设置为自定义的函数
    class_cticks = np.array(cb.get_ticks())
    # print(class_cticks)
    cct = abs(class_cticks[class_cticks != 0])
    if (min(cct) < 1e-2) or max(cct) > 1e4:  # 判断是否需要采用科学计数法
        cb.formatter = _MyFormatter(class_cticks)
        cb.update_ticks()

    if labels is not None:
        cb.set_label(labels["c"])
        plt.xlabel(labels["x"])
        plt.ylabel(labels["y"])
    if ticks_space is not None and ticks is not None:
        plt.xticks(np.arange(0, len(x[0, :]) + 1e-5, ticks_space["x"]), ticks["x"])
        plt.yticks(np.arange(0, len(y[:, 0]) + 1e-5, ticks_space["y"]), ticks["y"])

    plt.title("Min: {:.3g}, Max: {:.3g}".format(pic_data.min(), pic_data.max()))

    plt.savefig(picname, bbox_inches="tight") if picname is not None else plt.show()
    # plt.show()
    plt.clf()
    # 关闭当前figure
    plt.close()


# ** 画等高线图，带经纬度坐标轴
def plot_contourf_lonlat(data, lon, lat, interval=5, picname=None, c_map="rainbow"):
    """
    param        {*} data : 二维数据
    param        {*} lon : 经度
    param        {*} lat : 纬度
    param        {*} interval : 经纬度间隔
    param        {*} picname : 图片保存的文件名(含路径)
    param        {*} c_map : 颜色映射，默认rainbow
    return       {*} 无返回值
    """
    if len(lon.shape) == 2:
        lon = lon[0, :]
    if len(lat.shape) == 2:
        lat = lat[:, 0]
    # interval是经纬度间隔，单位为°
    # 将lon，lat作为坐标轴刻度显示

    def format_longitude(x):
        if x > 180:
            x -= 360
        degrees = int(abs(x))
        direction = "E" if x >= 0 else "W"
        return f"{degrees}°{direction}" if x != 0 and x != 180 else f"{degrees}°"

    def format_latitude(y):
        if y > 90:
            y -= 180
        degrees = int(abs(y))
        direction = "N" if y >= 0 else "S"
        return f"{degrees}°{direction}" if y != 0 else f"{degrees}°"

    plt.contourf(data, cmap=c_map)
    x_space = int(len(lon) * interval / (lon[-1] - lon[0]))
    y_space = int(len(lat) * interval / (lat[-1] - lat[0]))
    plt.xticks(np.arange(0, len(lon), x_space), [format_longitude(lon[i]) for i in range(0, len(lon), x_space)])
    plt.yticks(np.arange(0, len(lat), y_space), [format_latitude(lat[i]) for i in range(0, len(lat), y_space)])
    plt.colorbar()
    plt.savefig(picname, bbox_inches="tight") if picname is not None else plt.show()
    plt.close()


# ** 绘制矢量场
def plot_quiver(u, v, lon, lat, picname=None, cmap="coolwarm", scale=0.25, width=0.002, x_space=5, y_space=5):
    """
    param        {*} u : 二维数据
    param        {*} v : 二维数据
    param        {*} lon : 经度, 1D or 2D
    param        {*} lat : 纬度, 1D or 2D
    param        {*} picname : 图片保存的文件名(含路径)
    param        {*} cmap : 颜色映射，默认coolwarm
    param        {*} scale : 箭头的大小 / 缩小程度
    param        {*} width : 箭头的宽度
    param        {*} x_space : x轴间隔
    param        {*} y_space : y轴间隔
    return       {*} 无返回值
    """
    # 创建新的网格位置变量(lat_c, lon_c)
    if len(lon.shape) == 1 and len(lat.shape) == 1:
        lon_c, lat_c = np.meshgrid(lon, lat)
    else:
        lon_c, lat_c = lon, lat

    # 设置箭头的比例、颜色、宽度等参数
    # scale = 0.25  # 箭头的大小 / 缩小程度
    # color = '#E5D1FA'
    # width = 0.002  # 箭头的宽度
    # x_space = 1
    # y_space = 1

    # 计算矢量的大小
    S = xr.DataArray(np.hypot(np.array(u), np.array(v)))

    mean_S = S.nanmean()

    # 使用 plt.quiver 函数绘制矢量图
    # 通过设置 quiver 函数的 pivot 参数来指定箭头的位置
    quiver_plot = plt.quiver(
        lon_c[::y_space, ::x_space],
        lat_c[::y_space, ::x_space],
        u[::y_space, ::x_space],
        v[::y_space, ::x_space],
        S[::y_space, ::x_space],  # 矢量的大小，可以不要
        pivot="middle",
        scale=scale,
        #  color=color, # 矢量的颜色，单色
        cmap=cmap,  # 矢量的颜色，多色
        width=width,
    )
    # plt.quiverkey(quiver_plot, X=0.90, Y=0.975, U=1, label='1 m/s', labelpos='E', fontproperties={'size': 10})
    plt.quiverkey(quiver_plot, X=0.87, Y=0.975, U=mean_S, label=f"{mean_S:.2f} m/s", labelpos="E", fontproperties={"size": 10})
    plt.colorbar(quiver_plot)
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.savefig(picname, bbox_inches="tight") if picname is not None else plt.show()
    plt.clf()
    plt.close()


# ** 绘制填色图（带经纬度）
def plot_contourf_cartopy(data, lon, lat, picname=None, cmap="rainbow", cn_fill_num=20, fig_size=(12, 9), title="Cartopy", land_color="green", ocean_color="lightgrey"):
    """
    param        {*} data : 二维数据
    param        {*} lon : 经度
    param        {*} lat : 纬度
    param        {*} picname : 图片保存的文件名(含路径)
    param        {*} cmap : 颜色映射，默认rainbow
    param        {*} cn_fill_num : 等值线数量
    param        {*} fig_size : 图片大小，默认(12,9)
    param        {*} title : 图片标题
    param        {*} land_color : 陆地颜色
    param        {*} ocean_color : 海洋颜色
    return       {*} 无返回值
    """
    if len(lon.shape) == 2:
        lon = lon[0, :]
    if len(lat.shape) == 2:
        lat = lat[:, 0]

    data_max = np.nanmax(data)
    data_min = np.nanmin(data)
    levels = np.linspace(data_min, data_max, cn_fill_num)
    cbar_ticks = np.linspace(data_min, data_max, 9)

    fig = plt.figure(figsize=fig_size)
    proj = ccrs.PlateCarree()
    ax = fig.add_subplot(1, 1, 1, projection=proj)

    ax.set_extent([lon[0], lon[-1], lat[0], lat[-1]], crs=proj)

    ax.add_feature(cfeature.LAND, facecolor=land_color, edgecolor="k")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    # ax.add_feature(cfeature.BORDERS, linewidth=0.5, linestyle=":") # 加载国界线

    ax.set_xticks(np.arange(lon[0], lon[-1] + 1e-5, 5), crs=proj)
    ax.set_yticks(np.arange(lat[0], lat[-1] + 1e-5, 5), crs=proj)
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    ax.xaxis.set_major_formatter(lon_formatter)
    lat_formatter = LatitudeFormatter()
    ax.yaxis.set_major_formatter(lat_formatter)
    # plt.title(title, fontsize=16)

    cmap = plt.get_cmap(cmap)
    X, Y = np.meshgrid(lon, lat)

    # Fill color for land and ocean
    # ax.background_patch.set_facecolor(ocean_color)
    ax.patch.set_facecolor(ocean_color)
    ax.add_feature(cfeature.LAND, facecolor=land_color)

    cticks = cbar_ticks
    norm = mpl.colors.BoundaryNorm(cticks, cmap.N)

    cnplot = ax.contourf(X, Y, data, levels=levels, cmap=cmap, norm=norm, transform=proj, extend="both", alpha=1, zorder=0)
    # cllevels = np.linspace(data_min, data_max, 9)
    # clplot = ax.contour(X, Y, data, levels=levels[9::10], colors='k', linewidths=0.5, transform=proj, zorder=1, alpha=0.8, linestyle='--')
    # 添加色标，并选择位置
    divider = make_axes_locatable(ax)
    location = 3
    if location == 1:  # 左侧
        cax = divider.new_horizontal(size="5%", pad=1, axes_class=plt.Axes, pack_start=True)
        fig.add_axes(cax)
        cbar = plt.colorbar(cnplot, cax=cax, orientation="vertical", extend="both")
    elif location == 2:  # 下方
        cax = divider.new_vertical(size="5%", pad=0.3, axes_class=plt.Axes, pack_start=True)
        fig.add_axes(cax)
        cbar = plt.colorbar(cnplot, cax=cax, orientation="horizontal", extend="both")
    elif location == 3:  # 右侧
        cax = divider.new_horizontal(size="5%", pad=0.1, axes_class=plt.Axes)
        fig.add_axes(cax)
        # cbar = plt.colorbar(cnplot, cax=cax, orientation='vertical', extend='both', format='%.0f')
        cbar = fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap, norm=norm), cax=cax, orientation="vertical", extend="both", format="%.3f")
        cax.yaxis.set_ticks_position("right")
        cax.yaxis.set_label_position("right")
    else:  # 上方
        cax = divider.new_vertical(size="5%", pad=0.2, axes_class=plt.Axes)
        fig.add_axes(cax)
        cbar = plt.colorbar(cnplot, cax=cax, orientation="horizontal", extend="both")
    cbar.ax.tick_params(labelsize=10)
    cbar.ax.xaxis.set_tick_params(direction="in", width=1, length=2)
    # 添加cbar_ticks
    # cbar.set_ticks(np.arange(round(levels[0]), round(levels[-1]), round((levels[-1]-levels[0])/9)))  # 设置色标刻度
    # cbar.set_ticks(cbar_ticks)  # 设置色标刻度

    cbar.set_ticks(cticks)
    # cbar.ax.ticks = np.linspace(data_min, data_max, 8)
    # cbar.set_ticks(np.arange(round(levels[0]), round(levels[-1]), round((levels[-1]-levels[0])/9)))  # 设置色标刻度

    # 单独设置label
    cbar.set_label(title, fontsize=10, weight="bold")
    # cax.set_position([0.1, 0.2, 0.02, 0.6]) # 调整色标位置
    fig.savefig(picname, bbox_inches="tight", dpi=600) if picname is not None else plt.show()
    plt.close()



if __name__ == "__main__":
    # ** 绘制填色图
    data = np.random.randn(100, 100)
    picname = "test.png"
    plot_contourf(data, picname, c_map="rainbow", minmax=None, labels=None, ticks_space=None, ticks=None, figsize=(12, 9))
    # ** 绘制矢量场
    u = np.random.randn(100, 100)
    v = np.random.randn(100, 100)
    lon = np.linspace(0, 360, 100)
    lat = np.linspace(-90, 90, 100)
    picname = "test.png"
    plot_quiver(u, v, lon, lat, picname, cmap="coolwarm", scale=0.25, width=0.002, x_space=5, y_space=5)
    # ** 绘制经纬度填色图
    data = np.random.randn(100, 100)
    lon = np.linspace(0, 360, 100)
    lat = np.linspace(-90, 90, 100)
    picname = "test.png"
    plot_contourf_lonlat(data, lon, lat, interval=5, picname=picname, c_map="rainbow")
    # ** 制作动图
    image_list = ["test1.png", "test2.png", "test3.png"]
    gif_name = "test.gif"
    create_gif(image_list, gif_name, duration=0.2)
