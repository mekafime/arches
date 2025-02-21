import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

st.set_page_config(layout="wide")

with st.sidebar:
    st.header("Parámetros de la Nave con Techo Curvo")

    column_height = st.number_input("Altura de Columnas", min_value=1.0, max_value=20.0, value=10.0, step=0.1)
    arch_height = st.number_input("Altura del Arco", min_value=1.0, max_value=15.0, value=5.0, step=0.1)
    frame_spacing = st.number_input("Espaciado de Pórticos", min_value=1.0, max_value=15.0, value=5.0, step=0.1)
    num_frames = st.number_input("Número de Pórticos", min_value=1, max_value=10, value=3, step=1)
    width = st.number_input("Ancho de la Nave", min_value=1.0, max_value=25.0, value=10.0, step=0.1)

def plot_circular_roof_warehouse(column_height, arch_height, frame_spacing, num_frames, width):
    fig = plt.figure(figsize=(6, 4), dpi=120)  # 🔹 Ajuste de tamaño y resolución
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim([0, (num_frames - 1) * frame_spacing])
    ax.set_ylim([0, width])
    ax.set_zlim([0, column_height + arch_height])

    # 🔹 Ajustes para hacer los ejes más limpios
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))  # 🔹 Eje X cuenta de 1 en 1
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.zaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    ax.tick_params(axis='both', which='major', labelsize=8)  # 🔹 Reducir tamaño de los números en los ejes
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)  # 🔹 Líneas de la rejilla más delgadas

    num_points = 20  # Mayor número de puntos para una curva más suave

    for i in range(num_frames):
        x_offset = i * frame_spacing

        column1 = [(x_offset, 0, 0), (x_offset, 0, column_height)]
        column2 = [(x_offset, width, 0), (x_offset, width, column_height)]

        angles = np.linspace(0, np.pi, num_points)  # De 0° a 180°
        roof_curve = [(x_offset, width / 2 + (width / 2) * np.cos(angle), column_height + arch_height * np.sin(angle)) for angle in angles]

        for element in [column1, column2]:
            x, y, z = zip(*element)
            ax.plot(x, y, z, color='red', linewidth=2)

        x, y, z = zip(*roof_curve)
        ax.plot(x, y, z, color='red', linewidth=2)

        if i == 0 or i == num_frames - 1:
            horizontal_beam = [(x_offset, 0, column_height), (x_offset, width, column_height)]
            x, y, z = zip(*horizontal_beam)
            ax.plot(x, y, z, color='red', linewidth=2)

        if i > 0:
            prev_x_offset = (i - 1) * frame_spacing
            beam1 = [(prev_x_offset, 0, column_height), (x_offset, 0, column_height)]
            beam2 = [(prev_x_offset, width, column_height), (x_offset, width, column_height)]
            beam3 = [(prev_x_offset, width / 2, column_height + arch_height), (x_offset, width / 2, column_height + arch_height)]
            
            for element in [beam1, beam2, beam3]:
                x, y, z = zip(*element)
                ax.plot(x, y, z, color='blue', linewidth=2)
    
    return fig

fig = plot_circular_roof_warehouse(column_height, arch_height, frame_spacing, num_frames, width)
st.pyplot(fig)
