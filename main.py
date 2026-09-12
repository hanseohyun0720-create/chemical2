import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# =========================================================
# 가화실 - 가상 화학 실험실
# =========================================================

st.set_page_config(
    page_title="가화실 | 가상 화학 실험실",
    page_icon="🧪",
    layout="wide"
)

# -----------------------------
# 세션 상태
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "experiment" not in st.session_state:
    st.session_state.experiment = None

if "history" not in st.session_state:
    st.session_state.history = []

if "added_volume" not in st.session_state:
    st.session_state.added_volume = 0.0


# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.hero {
    padding: 35px;
    border-radius: 25px;
    background: linear-gradient(135deg, #e8f1ff, #f5edff);
    margin-bottom: 30px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
}

.hero-sub {
    font-size: 18px;
    color: #64748b;
}

.card {
    padding: 25px;
    border-radius: 20px;
    background: white;
    border: 1px solid #e5e7eb;
    min-height: 210px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
}

.card-icon {
    font-size: 40px;
}

.card-title {
    font-size: 21px;
    font-weight: 700;
}

.card-text {
    color: #64748b;
}

.lab {
    padding: 25px;
    border-radius: 20px;
    background: white;
    border: 1px solid #e5e7eb;
}

.beaker-area {
    height: 320px;
    position: relative;
    background: linear-gradient(
        to bottom,
        #eef2f7 0%,
        #eef2f7 65%,
        #d1d5db 65%,
        #d1d5db 100%
    );
    border-radius: 20px;
    overflow: hidden;
}

.beaker {
    position: absolute;
    width: 220px;
    height: 180px;
    left: 50%;
    bottom: 35px;
    transform: translateX(-50%);
    border: 5px solid #64748b;
    border-top: none;
    border-radius: 0 0 30px 30px;
    overflow: hidden;
    background: rgba(255,255,255,0.4);
}

.liquid {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    transition: all 0.5s;
}

.beaker-text {
    position: absolute;
    width: 100%;
    text-align: center;
    top: 70px;
    font-weight: bold;
    font-size: 20px;
    z-index: 5;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 공통 함수
# =========================================================

def go_home():
    st.session_state.page = "home"
    st.session_state.experiment = None
    st.session_state.added_volume = 0.0


def select_experiment(name):
    st.session_state.experiment = name
    st.session_state.page = "setup"
    st.session_state.added_volume = 0.0


def save_result(experiment, conditions, result):

    st.session_state.history.append({
        "실험": experiment,
        "조건": conditions,
        "결과": result
    })


# =========================================================
# 화학 계산
# =========================================================

def calculate_moles(concentration, volume_ml):
    """
    n = CV
    concentration : mol/L
    volume : mL
    """
    return concentration * volume_ml / 1000


def calculate_ph_strong_acid_base(
    acid_concentration,
    acid_volume,
    base_concentration,
    base_volume
):
    """
    강산 + 강염기 단순 중화 모델
    """

    acid_moles = calculate_moles(
        acid_concentration,
        acid_volume
    )

    base_moles = calculate_moles(
        base_concentration,
        base_volume
    )

    total_volume = (
        acid_volume + base_volume
    ) / 1000

    if total_volume <= 0:
        return 7.0

    difference = acid_moles - base_moles

    # 거의 정확히 중화
    if abs(difference) < 1e-12:
        return 7.0

    concentration = abs(difference) / total_volume

    if difference > 0:

        # H+가 남음
        ph = -math.log10(concentration)

    else:

        # OH-가 남음
        poh = -math.log10(concentration)
        ph = 14 - poh

    return max(0, min(14, ph))


def ph_color(ph):

    if ph < 3:
        return "#ef4444"

    elif ph < 5:
        return "#f97316"

    elif ph < 6.5:
        return "#facc15"

    elif ph < 7.5:
        return "#22c55e"

    elif ph < 9:
        return "#60a5fa"

    elif ph < 11:
        return "#3b82f6"

    else:
        return "#7c3aed"


def ph_description(ph):

    if ph < 7:
        return "산성"
    elif ph > 7:
        return "염기성"
    else:
        return "중성"


# =========================================================
# 사이드바
# =========================================================

with st.sidebar:

    st.markdown("# 🧪 가화실")

    st.caption("가상 화학 실험실")

    st.divider()

    if st.button(
        "🏠 홈",
        use_container_width=True
    ):
        go_home()
        st.rerun()

    if st.button(
        "📚 실험 기록",
        use_container_width=True
    ):
        st.session_state.page = "history"
        st.rerun()

    st.divider()

    st.info(
        """
        🛡️ 안전 안내

        이 프로그램은 실제 화학 실험을 수행하지 않는
        교육용 가상 실험 시뮬레이션입니다.
        """
    )


# =========================================================
# 홈 화면
# =========================================================

if st.session_state.page == "home":

    st.markdown("""
    <div class="hero">

        <div class="hero-title">
            🧪 가상 화학 실험실
        </div>

        <div style="
            font-size:25px;
            font-weight:700;
            margin-top:5px;
        ">
            가화실
        </div>

        <div class="hero-sub">
            실제 실험의 비용과 안전상의 제약 없이
            다양한 화학 실험을 가상으로 체험해 보세요.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.header("🔬 실험 선택")

    experiments = [

        (
            "산-염기 중화",
            "🧪",
            "산과 염기를 섞으며 pH가 어떻게 변화하는지 관찰합니다."
        ),

        (
            "산-염기 적정",
            "📈",
            "적정액을 조금씩 첨가하면서 적정 곡선과 당량점을 확인합니다."
        ),

        (
            "용액 제조 및 희석",
            "⚗️",
            "농도와 부피를 설정하고 희석 전후의 농도를 계산합니다."
        ),

        (
            "침전 반응",
            "🧊",
            "두 용액을 섞었을 때 생성되는 침전을 관찰합니다."
        )
    ]

    cols = st.columns(4)

    for i, experiment in enumerate(experiments):

        name, icon, description = experiment

        with cols[i]:

            st.markdown(
                f"""
                <div class="card">

                    <div class="card-icon">
                        {icon}
                    </div>

                    <div class="card-title">
                        {name}
                    </div>

                    <p class="card-text">
                        {description}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "실험 시작",
                key=f"start_{i}",
                use_container_width=True
            ):

                select_experiment(name)

                st.rerun()

    st.divider()

    st.header("✨ 주요 기능")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🧮 화학 계산",
            "pH / 몰수 / 농도"
        )

    with c2:
        st.metric(
            "📊 결과 시각화",
            "그래프"
        )

    with c3:
        st.metric(
            "🔬 가상 실험",
            "실시간 변화"
        )

    with c4:
        st.metric(
            "📝 실험 기록",
            f"{len(st.session_state.history)}회"
        )


# =========================================================
# 실험 설정 화면
# =========================================================

elif st.session_state.page == "setup":

    experiment = st.session_state.experiment

    if st.button("← 실험 선택으로 돌아가기"):
        go_home()
        st.rerun()

    st.title(
        f"{experiment}"
    )

    st.caption(
        "실험 조건을 설정하세요."
    )

    # -----------------------------------------------------
    # 중화 / 적정
    # -----------------------------------------------------

    if experiment in [
        "산-염기 중화",
        "산-염기 적정"
    ]:

        left, right = st.columns(2)

        with left:

            st.subheader("🔴 산 용액")

            acid_type = st.selectbox(
                "산 종류",
                [
                    "염산 (HCl)",
                    "질산 (HNO₃)",
                    "황산 (H₂SO₄)"
                ]
            )

            acid_concentration = st.number_input(
                "산 농도 (mol/L)",
                min_value=0.001,
                max_value=1.0,
                value=0.100,
                step=0.001
            )

            acid_volume = st.number_input(
                "산 부피 (mL)",
                min_value=1.0,
                max_value=100.0,
                value=10.0,
                step=1.0
            )

        with right:

            st.subheader("🔵 염기 용액")

            base_type = st.selectbox(
                "염기 종류",
                [
                    "수산화나트륨 (NaOH)",
                    "수산화칼륨 (KOH)",
                    "수산화칼슘 (Ca(OH)₂)"
                ]
            )

            base_concentration = st.number_input(
                "염기 농도 (mol/L)",
                min_value=0.001,
                max_value=1.0,
                value=0.100,
                step=0.001
            )

            base_volume = st.number_input(
                "염기 부피 (mL)",
                min_value=1.0,
                max_value=100.0,
                value=20.0,
                step=1.0
            )

        temperature = st.slider(
            "🌡️ 온도 (°C)",
            15,
            40,
            25
        )

        acid_moles = calculate_moles(
            acid_concentration,
            acid_volume
        )

        base_moles = calculate_moles(
            base_concentration,
            base_volume
        )

        # 강산-강염기 1:1 모델
        equivalent_volume = (
            acid_concentration
            * acid_volume
            / base_concentration
        )

        st.divider()

        st.subheader("📋 예상 실험 정보")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "산 몰수",
                f"{acid_moles:.5f} mol"
            )

        with c2:
            st.metric(
                "염기 몰수",
                f"{base_moles:.5f} mol"
            )

        with c3:
            st.metric(
                "예상 당량점",
                f"{equivalent_volume:.2f} mL"
            )

        st.info(
            "현재 모델은 교육용 강산-강염기 중화 모델입니다."
        )

        if st.button(
            "🔬 실험 시작",
            type="primary",
            use_container_width=True
        ):

            st.session_state.setup = {

                "acid_type": acid_type,
                "acid_concentration": acid_concentration,
                "acid_volume": acid_volume,

                "base_type": base_type,
                "base_concentration": base_concentration,
                "base_volume": base_volume,

                "temperature": temperature

            }

            st.session_state.page = "experiment"

            st.rerun()

    # -----------------------------------------------------
    # 희석
    # -----------------------------------------------------

    elif experiment == "용액 제조 및 희석":

        c1, c2 = st.columns(2)

        with c1:

            stock_concentration = st.number_input(
                "원액 농도 C₁ (mol/L)",
                min_value=0.001,
                max_value=10.0,
                value=1.0,
                step=0.01
            )

            stock_volume = st.number_input(
                "원액 부피 V₁ (mL)",
                min_value=0.1,
                max_value=1000.0,
                value=10.0,
                step=0.1
            )

        with c2:

            final_volume = st.number_input(
                "최종 부피 V₂ (mL)",
                min_value=0.1,
                max_value=2000.0,
                value=100.0,
                step=0.1
            )

            final_concentration = (
                stock_concentration
                * stock_volume
                / final_volume
            )

            st.metric(
                "최종 농도 C₂",
                f"{final_concentration:.4f} M"
            )

        st.info(
            "희석 계산: C₁V₁ = C₂V₂"
        )

        if st.button(
            "🔬 실험 시작",
            type="primary",
            use_container_width=True
        ):

            st.session_state.setup = {

                "stock_concentration":
                    stock_concentration,

                "stock_volume":
                    stock_volume,

                "final_volume":
                    final_volume,

                "final_concentration":
                    final_concentration
            }

            st.session_state.page = "experiment"

            st.rerun()

    # -----------------------------------------------------
    # 침전
    # -----------------------------------------------------

    else:

        left, right = st.columns(2)

        with left:

            st.subheader("용액 A")

            solution_a = st.selectbox(
                "시약 A",
                [
                    "AgNO₃",
                    "BaCl₂",
                    "CaCl₂"
                ]
            )

            concentration_a = st.number_input(
                "A 농도 (mol/L)",
                min_value=0.001,
                max_value=1.0,
                value=0.100,
                step=0.01
            )

            volume_a = st.number_input(
                "A 부피 (mL)",
                min_value=1.0,
                max_value=100.0,
                value=10.0,
                step=1.0
            )

        with right:

            st.subheader("용액 B")

            solution_b = st.selectbox(
                "시약 B",
                [
                    "NaCl",
                    "Na₂SO₄",
                    "Na₂CO₃"
                ]
            )

            concentration_b = st.number_input(
                "B 농도 (mol/L)",
                min_value=0.001,
                max_value=1.0,
                value=0.100,
                step=0.01
            )

            volume_b = st.number_input(
                "B 부피 (mL)",
                min_value=1.0,
                max_value=100.0,
                value=10.0,
                step=1.0
            )

        st.info(
            "대표적인 고등학교 수준의 침전 반응을 교육용으로 구현합니다."
        )

        if st.button(
            "🔬 실험 시작",
            type="primary",
            use_container_width=True
        ):

            st.session_state.setup = {

                "solution_a": solution_a,
                "concentration_a": concentration_a,
                "volume_a": volume_a,

                "solution_b": solution_b,
                "concentration_b": concentration_b,
                "volume_b": volume_b
            }

            st.session_state.page = "experiment"

            st.rerun()


# =========================================================
# 실험 진행
# =========================================================

elif st.session_state.page == "experiment":

    experiment = st.session_state.experiment
    setup = st.session_state.setup

    if st.button("← 설정으로 돌아가기"):
        st.session_state.page = "setup"
        st.rerun()

    st.title("🔬 실험 진행")

    st.caption(
        "아래 조작은 모두 가상으로 이루어집니다."
    )

    # =====================================================
    # 중화 실험
    # =====================================================

    if experiment == "산-염기 중화":

        acid_c = setup["acid_concentration"]
        acid_v = setup["acid_volume"]

        base_c = setup["base_concentration"]
        base_v = setup["base_volume"]

        added = st.slider(
            "🔵 염기 용액 첨가량 (mL)",
            0.0,
            float(base_v),
            float(st.session_state.added_volume),
            0.5
        )

        st.session_state.added_volume = added

        current_ph = calculate_ph_strong_acid_base(
            acid_c,
            acid_v,
            base_c,
            added
        )

        equivalent = (
            acid_c
            * acid_v
            / base_c
        )

        left, right = st.columns([1.2, 1])

        with left:

            st.subheader("🧪 가상 비커")

            color = ph_color(current_ph)

            liquid_height = (
                35
                + min(
                    50,
                    added / max(base_v, 1) * 50
                )
            )

            st.markdown(
                f"""
                <div class="beaker-area">

                    <div class="beaker">

                        <div
                            class="liquid"
                            style="
                            height:{liquid_height}%;
                            background:{color};
                            opacity:0.7;
                            "
                        ></div>

                        <div class="beaker-text">
                            pH {current_ph:.2f}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            st.subheader("📊 실시간 결과")

            st.metric(
                "현재 pH",
                f"{current_ph:.2f}"
            )

            st.metric(
                "상태",
                ph_description(current_ph)
            )

            st.metric(
                "첨가한 염기",
                f"{added:.1f} mL"
            )

            st.metric(
                "당량점",
                f"{equivalent:.2f} mL"
            )

            if abs(added - equivalent) < 0.5:

                st.success(
                    "🎯 당량점에 도달했습니다!"
                )

            elif added < equivalent:

                st.info(
                    "산이 아직 남아 있습니다."
                )

            else:

                st.info(
                    "염기가 과량으로 존재합니다."
                )

        # pH 그래프

        st.divider()

        st.subheader("📈 pH 변화")

        volumes = np.linspace(
            0,
            base_v,
            150
        )

        ph_values = [

            calculate_ph_strong_acid_base(
                acid_c,
                acid_v,
                base_c,
                v
            )

            for v in volumes
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=volumes,
                y=ph_values,
                mode="lines",
                name="pH"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[added],
                y=[current_ph],
                mode="markers",
                marker=dict(size=12),
                name="현재 위치"
            )
        )

        fig.add_vline(
            x=equivalent,
            line_dash="dash",
            annotation_text="당량점"
        )

        fig.update_layout(
            xaxis_title="첨가한 염기 부피 (mL)",
            yaxis_title="pH",
            yaxis=dict(range=[0, 14]),
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        if st.button(
            "💾 실험 결과 저장",
            type="primary"
        ):

            save_result(
                "산-염기 중화",
                f"""
                산: {setup['acid_type']}
                {acid_c} M / {acid_v} mL

                염기: {setup['base_type']}
                {base_c} M
                """,
                f"""
                염기 첨가량:
                {added:.1f} mL

                최종 pH:
                {current_ph:.2f}

                당량점:
                {equivalent:.2f} mL
                """
            )

            st.success(
                "실험 결과가 저장되었습니다!"
            )

    # =====================================================
    # 적정 실험
    # =====================================================

    elif experiment == "산-염기 적정":

        acid_c = setup["acid_concentration"]
        acid_v = setup["acid_volume"]

        base_c = setup["base_concentration"]
        base_v = setup["base_volume"]

        equivalent = (
            acid_c
            * acid_v
            / base_c
        )

        added = st.slider(
            "💧 적정액 첨가량 (mL)",
            0.0,
            float(base_v),
            float(st.session_state.added_volume),
            0.2
        )

        st.session_state.added_volume = added

        current_ph = calculate_ph_strong_acid_base(
            acid_c,
            acid_v,
            base_c,
            added
        )

        # 적정 곡선

        volumes = np.linspace(
            0.01,
            base_v,
            200
        )

        ph_values = [

            calculate_ph_strong_acid_base(
                acid_c,
                acid_v,
                base_c,
                v
            )

            for v in volumes
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=volumes,
                y=ph_values,
                mode="lines",
                name="적정 곡선"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[added],
                y=[current_ph],
                mode="markers",
                marker=dict(size=13),
                name="현재 상태"
            )
        )

        fig.add_vline(
            x=equivalent,
            line_dash="dash",
            annotation_text="당량점"
        )

        fig.update_layout(
            title="산-염기 적정 곡선",
            xaxis_title="염기 첨가량 (mL)",
            yaxis_title="pH",
            yaxis=dict(range=[0, 14]),
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "현재 pH",
                f"{current_ph:.2f}"
            )

        with c2:
            st.metric(
                "현재 첨가량",
                f"{added:.1f} mL"
            )

        with c3:
            st.metric(
                "당량점",
                f"{equivalent:.2f} mL"
            )

        if abs(added - equivalent) < 0.5:

            st.success(
                "🎯 당량점 근처입니다."
            )

        if st.button(
            "💾 적정 결과 저장",
            type="primary"
        ):

            save_result(
                "산-염기 적정",
                f"""
                산 {acid_c} M / {acid_v} mL
                염기 {base_c} M
                """,
                f"""
                당량점: {equivalent:.2f} mL
                현재 첨가량: {added:.1f} mL
                현재 pH: {current_ph:.2f}
                """
            )

            st.success(
                "적정 결과가 저장되었습니다!"
            )

    # =====================================================
    # 희석 실험
    # =====================================================

    elif experiment == "용액 제조 및 희석":

        stock_c = setup["stock_concentration"]
        stock_v = setup["stock_volume"]
        final_v = setup["final_volume"]

        added = st.slider(
            "⚗️ 원액 사용량 (mL)",
            0.0,
            float(stock_v),
            float(st.session_state.added_volume),
            0.1
        )

        st.session_state.added_volume = added

        current_c = (
            stock_c
            * added
            / final_v
        )

        left, right = st.columns([1.2, 1])

        with left:

            st.subheader("⚗️ 가상 플라스크")

            height = (
                20
                + min(
                    65,
                    added / max(stock_v, 0.1) * 60
                )
            )

            st.markdown(
                f"""
                <div class="beaker-area">

                    <div class="beaker">

                        <div
                            class="liquid"
                            style="
                            height:{height}%;
                            background:#60a5fa;
                            opacity:0.65;
                            "
                        ></div>

                        <div class="beaker-text">
                            {current_c:.4f} M
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            st.subheader("🧮 실시간 계산")

            st.metric(
                "원액 사용량",
                f"{added:.1f} mL"
            )

            st.metric(
                "현재 농도",
                f"{current_c:.4f} M"
            )

            st.metric(
                "목표 농도",
                f"{setup['final_concentration']:.4f} M"
            )

            st.progress(
                min(
                    1.0,
                    added / max(stock_v, 0.1)
                )
            )

        st.divider()

        st.subheader("📚 화학 원리")

        st.latex(
            r"C_1V_1=C_2V_2"
        )

        st.write(
            """
            희석 과정에서는 용질의 몰수가 변하지 않는다고
            가정하므로 C₁V₁ = C₂V₂ 관계를 이용할 수 있습니다.
            """
        )

        if st.button(
            "💾 희석 결과 저장",
            type="primary"
        ):

            save_result(
                "용액 제조 및 희석",
                f"""
                원액: {stock_c} M
                원액 부피: {stock_v} mL
                최종 부피: {final_v} mL
                """,
                f"""
                원액 사용량: {added:.1f} mL
                현재 농도: {current_c:.4f} M
                """
            )

            st.success(
                "실험 결과가 저장되었습니다!"
            )

    # =====================================================
    # 침전 반응
    # =====================================================

    else:

        a = setup["solution_a"]
        b = setup["solution_b"]

        a_c = setup["concentration_a"]
        a_v = setup["volume_a"]

        b_c = setup["concentration_b"]
        b_v = setup["volume_b"]

        added = st.slider(
            "💧 B 용액 첨가량 (mL)",
            0.0,
            float(b_v),
            float(st.session_state.added_volume),
            0.5
        )

        st.session_state.added_volume = added

        reactions = {

            ("AgNO₃", "NaCl"):
                ("AgCl", "흰색", "Ag⁺ + Cl⁻ → AgCl(s)"),

            ("AgNO₃", "Na₂SO₄"):
                ("Ag₂SO₄", "흰색", "2Ag⁺ + SO₄²⁻ → Ag₂SO₄(s)"),

            ("AgNO₃", "Na₂CO₃"):
                ("Ag₂CO₃", "연한 노란색",
                 "2Ag⁺ + CO₃²⁻ → Ag₂CO₃(s)"),

            ("BaCl₂", "Na₂SO₄"):
                ("BaSO₄", "흰색",
                 "Ba²⁺ + SO₄²⁻ → BaSO₄(s)"),

            ("CaCl₂", "Na₂CO₃"):
                ("CaCO₃", "흰색",
                 "Ca²⁺ + CO₃²⁻ → CaCO₃(s)")
        }

        if (a, b) in reactions:

            product, color, equation = reactions[(a, b)]

            precipitate = True

        else:

            product = "뚜렷한 침전 없음"
            color = "변화 없음"
            equation = "뚜렷한 순이온 반응 없음"

            precipitate = False

        left, right = st.columns([1.2, 1])

        with left:

            st.subheader("🧊 가상 비커")

            if precipitate and added > 0:

                precip_height = min(
                    25,
                    5 + added / max(b_v, 1) * 20
                )

                liquid_color = "#bfdbfe"

            else:

                precip_height = 0
                liquid_color = "#bfdbfe"

            st.markdown(
                f"""
                <div class="beaker-area">

                    <div class="beaker">

                        <div
                            class="liquid"
                            style="
                            height:60%;
                            background:{liquid_color};
                            opacity:0.55;
                            "
                        ></div>

                        <div
                            style="
                            position:absolute;
                            bottom:0;
                            left:0;
                            right:0;
                            height:{precip_height}%;
                            background:#e5e7eb;
                            z-index:3;
                            "
                        ></div>

                        <div class="beaker-text">
                            {product if added > 0 else "용액"}
                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            st.subheader("📊 반응 결과")

            st.metric(
                "첨가량",
                f"{added:.1f} mL"
            )

            st.write(
                f"**생성 물질:** {product}"
            )

            st.write(
                f"**침전 색:** {color}"
            )

            st.code(equation)

            if precipitate and added > 0:

                st.success(
                    "🧊 침전이 생성되었습니다."
                )

            elif added > 0:

                st.info(
                    "뚜렷한 침전이 생성되지 않습니다."
                )

        if st.button(
            "💾 침전 실험 결과 저장",
            type="primary"
        ):

            save_result(
                "침전 반응",
                f"""
                {a}: {a_c} M / {a_v} mL
                {b}: {b_c} M
                """,
                f"""
                생성 물질: {product}
                색: {color}
                B 첨가량: {added:.1f} mL
                """
            )

            st.success(
                "실험 결과가 저장되었습니다!"
            )


# =========================================================
# 실험 기록
# =========================================================

elif st.session_state.page == "history":

    st.title("📚 실험 기록")

    st.caption(
        "현재 세션에서 저장한 실험 결과를 확인하고 비교할 수 있습니다."
    )

    if len(st.session_state.history) == 0:

        st.info(
            "아직 저장된 실험 결과가 없습니다."
        )

    else:

        data = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("📊 실험 결과 비교")

        experiment_types = data["실험"].unique()

        selected = st.multiselect(
            "비교할 실험",
            experiment_types,
            default=list(experiment_types)
        )

        comparison = data[
            data["실험"].isin(selected)
        ]

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        if st.button(
            "🗑️ 모든 기록 삭제"
        ):

            st.session_state.history = []

            st.rerun()
