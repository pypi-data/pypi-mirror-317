import os
import sys


def show_model(
        file_path: str,
        color: str = None,
        opacity: float = 1.0,
        show_edges: bool = False,
        point_size: float = 5.0,
        line_width: float = 1.0,
        lighting: bool = True,
        background_color: str = 'white',
        window_size: tuple = None,
        camera_position: str = 'iso',  # 'xy', 'xz', 'yz', 'iso'
        zoom_factor: float = 1.0,
        style: str = 'surface'  # 'surface', 'wireframe', 'points'
):
    """显示3D模型。

    Args:
        file_path (str): 3D模型文件的路径。只支持 .stl 和 .obj 格式。
        color (str, optional): 模型的颜色。默认为None。
        opacity (float, optional): 透明度，范围0-1。默认为1.0。
        show_edges (bool, optional): 是否显示边缘。默认为False。
        point_size (float, optional): 点的大小(当style='points'时)。默认为5.0。
        line_width (float, optional): 线条宽度。默认为1.0。
        lighting (bool, optional): 是否启用光照。默认为True。
        background_color (str, optional): 背景颜色。默认为'white'。
        window_size (tuple, optional): 窗口大小。默认为(1024, 768)。
        camera_position (str, optional): 相机视角。默认为'iso'。
        zoom_factor (float, optional): 缩放因子。默认为1.0。
        style (str, optional): 渲染样式。默认为'surface'。

    Returns:
        None

    Raises:
        FileNotFoundError: 如果文件不存在。
        ValueError: 如果文件格式不是 .stl 或 .obj。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension not in ['.stl', '.obj']:
        raise ValueError(f"不支持的文件格式: {file_extension}。目前仅支持 .stl 和 .obj 格式")
    if camera_position not in ['xy', 'xz', 'yz', 'iso']:
        raise ValueError(f"不支持的相机视角: {camera_position}")

    if style not in ['surface', 'wireframe', 'points']:
        raise ValueError(f"不支持的渲染样式: {style}")

    if not 0.0 <= opacity <= 1.0:
        raise ValueError(f"透明度必须在0-1之间")

    if 'ipykernel' in sys.modules:
        # 在 Jupyter 环境中
        pv.global_theme.trame.jupyter_extension_enabled = True
        pv.set_jupyter_backend("client")

        # 更新显示设置
    plotter = pv.Plotter(window_size=window_size)
    plotter.background_color = background_color

    # 读取模型
    mesh = pv.read(file_path)

    # 设置显示属性
    plotter.add_mesh(
        mesh,
        color=color,
        show_edges=show_edges,
        opacity=opacity,
        point_size=point_size,
        line_width=line_width,
        lighting=lighting,
        style=style
    )

    # 设置相机
    plotter.camera_position = camera_position
    plotter.camera.zoom(zoom_factor)

    # 显示
    plotter.show()


import pyvista as pv
