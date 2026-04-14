import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Ерөнхий тохиргоо
st.set_page_config(page_title="Soyombo Lab", layout="wide")

# Дизайн: Лабораторийн харанхуй орчин (Dark Theme)
plt.rcParams.update({
    "figure.facecolor": "#121212", 
    "axes.facecolor": "#121212",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#00FF41", 
    "xtick.color": "#444444",
    "ytick.color": "#444444",
    "grid.color": "#222222",
    "text.color": "#00FF41"
})

st.markdown("<h1 style='text-align: center; color: #00FF41;'> SOYOMBO LAB - Физик Туршилтын Төв</h1>", unsafe_allow_html=True)

# 2. Хажуугийн цэс
st.sidebar.markdown("<h2 style='color: #00FF41;'>Soyombo Lab</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "Туршилт сонгох:",
    ("Дууны долгион", "Тойргоор эргэх хөдөлгөөн", "Молекул физик")
)

# --- ТУРШИЛТ 1: ДУУНЫ ДОЛГИОН ---
if menu == "Дууны долгион":
    st.header(" Дууны долгионы шинжилгээ")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        freq = st.slider("Давтамж (Hz):", 20, 25000, 1000)
        amp = st.slider("Далайц (Volume):", 0.0, 1.0, 0.5)
        
        # Өндөр давтамжийг алдаагүй гаргах Sample Rate
        sr = 96000 
        t_audio = np.linspace(0, 2.0, int(sr * 2.0), endpoint=False)
        audio_wave = amp * np.sin(2 * np.pi * freq * t_audio)
        st.audio(audio_wave, sample_rate=sr, loop=True)
        st.info("⬆ Play дарж тасралтгүй дууг сонсоно уу.")

    with col2:
        # Автомат Zoom хийх график
        t_end = 5 / freq if freq > 0 else 0.01
        t_plot = np.linspace(0, t_end, 1000)
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.plot(t_plot, amp * np.sin(2 * np.pi * freq * t_plot), color='#00FF41', lw=2)
        ax1.set_ylim(-1.1, 1.1)
        ax1.grid(True, alpha=0.2)
        ax1.set_title(f"Осциллограф: {freq} Hz", color='#00FF41')
        st.pyplot(fig1)

# --- ТУРШИЛТ 2: ТОЙРГООР ЭРГЭХ ХӨДӨЛГӨӨН ---
elif menu == "Тойргоор эргэх хөдөлгөөн":
    st.header(" Кинематик: Тойргоор эргэх")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        r = st.slider("Радиус (m):", 1.0, 10.0, 5.0)
        speed = st.slider("Эргэх хурд (w):", 0.05, 0.8, 0.3)
        st.metric("Төвөөс зугтах хурдатгал", f"{(speed**2 * r):.2f} m/s²")

    with col2:
        placeholder = st.empty()
        # Тасралтгүй анимэйшн (50 фрейм)
        for i in range(50):
            angle = i * speed
            x, y = r * np.cos(angle), r * np.sin(angle)
            fig, ax = plt.subplots(figsize=(6, 6))
            for c in [2, 4, 6, 8, 10]: 
                ax.add_artist(plt.Circle((0, 0), c, color='#222222', fill=False, lw=0.5))
            ax.plot([0, x], [0, y], color='#00FF41', alpha=0.3)
            ax.plot(x, y, 'o', color='#00FF41', markersize=12, markeredgecolor='white')
            ax.set_xlim(-12, 12); ax.set_ylim(-12, 12); ax.set_aspect('equal'); ax.axis('off')
            placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(0.01)

# --- ТУРШИЛТ 3: МОЛЕКУЛ ФИЗИК (ЗӨӨЛӨН ШИЛЖИЛТТЭЙ) ---
elif menu == "Молекул физик":
    st.header(" Бодисын төлөв ба Шилжилт")
    state = st.select_slider("Төлөв:", options=["Хатуу", "Шингэн", "Хий"])
    
    n = 64
    def get_positions(s):
        if s == "Хатуу":
            x, y = np.meshgrid(np.linspace(2, 8, 8), np.linspace(1, 4, 8))
            return x.flatten(), y.flatten()
        elif s == "Шингэн":
            return np.random.uniform(2, 8, n), np.random.uniform(0.5, 2.5, n)
        else: # Хий
            return np.random.uniform(0.5, 9.5, n), np.random.uniform(0.5, 4.5, n)

    if 'prev_x' not in st.session_state:
        st.session_state.prev_x, st.session_state.prev_y = get_positions("Хатуу")
        st.session_state.curr_state = "Хатуу"

    # Шилжилтийн анимэйшн
    if st.session_state.curr_state != state:
        target_x, target_y = get_positions(state)
        p_holder = st.empty()
        steps = 15
        for i in range(steps + 1):
            alpha = i / steps
            curr_x = st.session_state.prev_x + (target_x - st.session_state.prev_x) * alpha
            curr_y = st.session_state.prev_y + (target_y - st.session_state.prev_y) * alpha
            
            fig, ax = plt.subplots(figsize=(8, 5))
            color = "#FF3131" if state == "Хатуу" else "#39FF14" if state == "Шингэн" else "#00FFFF"
            ax.scatter(curr_x, curr_y, color=color, s=80, edgecolor='white')
            ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.set_axis_off()
            ax.add_patch(plt.Rectangle((0, 0), 10, 5, color="#333333", fill=False, lw=2))
            p_holder.pyplot(fig)
            plt.close(fig)
            time.sleep(0.01)
        
        st.session_state.prev_x, st.session_state.prev_y = target_x, target_y
        st.session_state.curr_state = state
    else:
        fig, ax = plt.subplots(figsize=(8, 5))
        color = "#FF3131" if state == "Хатуу" else "#39FF14" if state == "Шингэн" else "#00FFFF"
        ax.scatter(st.session_state.prev_x, st.session_state.prev_y, color=color, s=80, edgecolor='white')
        ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.set_axis_off()
        ax.add_patch(plt.Rectangle((0, 0), 10, 5, color="#333333", fill=False, lw=2))
        st.pyplot(fig)

st.sidebar.markdown("---")
st.sidebar.write(" Operator: **User**")
st.sidebar.write(" Lab: **Soyombo Lab**")