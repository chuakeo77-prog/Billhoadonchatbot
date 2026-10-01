import streamlit as st
from datetime import datetime
from io import BytesIO
st.image("logo.jpg")
# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Milk Tea Billing",
    page_icon="🧋",
    layout="centered"
)

# =========================================================
# DỮ LIỆU MENU
# =========================================================

TRA_SUA = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa caramel": 38000,
    "Trà sữa ô long": 38000,
    "Trà sữa bạc hà": 35000,
}

TOPPING = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 6000,
    "Thạch trái cây": 5000,
    "Thạch phô mai": 8000,
    "Pudding trứng": 8000,
    "Kem cheese": 10000,
    "Trân châu hoàng kim": 8000,
}

MUC_DUONG = ["100%", "70%", "0%"]

# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def dinh_dang_tien(tien):
    return f"{tien:,.0f} VNĐ"


# =========================================================
# KHỞI TẠO SESSION STATE
# =========================================================

if "gio_hang" not in st.session_state:
    st.session_state.gio_hang = []


# =========================================================
# HEADER
# =========================================================

st.title("🧋 QUÁN TRÀ SỮA")
st.subheader("Hệ thống gọi món & tính hóa đơn")

st.divider()


# =========================================================
# THÔNG TIN KHÁCH HÀNG
# =========================================================

st.header("👤 Thông tin khách hàng")

ten_khach = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)

st.divider()


# =========================================================
# CHỌN MÓN
# =========================================================

st.header("🧋 Chọn món")

col1, col2 = st.columns(2)

with col1:
    loai_tra_sua = st.selectbox(
        "Loại trà sữa",
        list(TRA_SUA.keys())
    )

with col2:
    so_luong = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=20,
        value=1,
        step=1
    )

muc_duong = st.selectbox(
    "Mức độ đường",
    MUC_DUONG
)

topping_chon = st.multiselect(
    "Chọn topping",
    list(TOPPING.keys())
)

# =========================================================
# TÍNH GIÁ MÓN
# =========================================================

gia_tra_sua = TRA_SUA[loai_tra_sua]

tong_tien_topping_mot_ly = sum(
    TOPPING[topping] for topping in topping_chon
)

gia_mot_ly = gia_tra_sua + tong_tien_topping_mot_ly

thanh_tien = gia_mot_ly * so_luong


# =========================================================
# HIỂN THỊ THÔNG TIN ĐƠN ĐANG CHỌN
# =========================================================

st.info(
    f"""
    **Món:** {loai_tra_sua}

    **Đường:** {muc_duong}

    **Topping:** {", ".join(topping_chon) if topping_chon else "Không có"}

    **Đơn giá:** {dinh_dang_tien(gia_mot_ly)}

    **Số lượng:** {so_luong}

    **Thành tiền:** {dinh_dang_tien(thanh_tien)}
    """
)


# =========================================================
# THÊM MÓN VÀO ĐƠN
# =========================================================

if st.button("➕ Thêm món vào hóa đơn", use_container_width=True):

    mon = {
        "ten_mon": loai_tra_sua,
        "so_luong": so_luong,
        "duong": muc_duong,
        "topping": topping_chon.copy(),
        "don_gia": gia_mot_ly,
        "thanh_tien": thanh_tien
    }

    st.session_state.gio_hang.append(mon)

    st.success("✅ Đã thêm món vào hóa đơn!")


# =========================================================
# HIỂN THỊ HÓA ĐƠN
# =========================================================

st.divider()

st.header("🧾 HÓA ĐƠN")

if len(st.session_state.gio_hang) == 0:

    st.warning("Chưa có món nào trong hóa đơn.")

else:

    tong_hoa_don = 0

    for i, mon in enumerate(st.session_state.gio_hang):

        tong_hoa_don += mon["thanh_tien"]

        st.markdown(f"### {i + 1}. {mon['ten_mon']}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(f"**Số lượng:** {mon['so_luong']}")

        with col2:
            st.write(f"**Đường:** {mon['duong']}")

        with col3:
            st.write(
                f"**Thành tiền:** "
                f"{dinh_dang_tien(mon['thanh_tien'])}"
            )

        if mon["topping"]:
            st.write(
                "**Topping:** " +
                ", ".join(mon["topping"])
            )
        else:
            st.write("**Topping:** Không có")

        st.divider()


    # =====================================================
    # TỔNG TIỀN
    # =====================================================

    st.markdown(
        f"""
        <div style="
            padding:20px;
            border-radius:10px;
            background-color:#f5f5f5;
            text-align:center;
            border:1px solid #ddd;
        ">
            <h2>TỔNG THANH TOÁN</h2>
            <h1>{dinh_dang_tien(tong_hoa_don)}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # TẠO NỘI DUNG FILE HÓA ĐƠN
    # =====================================================

    thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    noi_dung_hoa_don = ""

    noi_dung_hoa_don += "=" * 50 + "\n"
    noi_dung_hoa_don += "             QUÁN TRÀ SỮA\n"
    noi_dung_hoa_don += "             HÓA ĐƠN THANH TOÁN\n"
    noi_dung_hoa_don += "=" * 50 + "\n\n"

    noi_dung_hoa_don += f"Khách hàng: {ten_khach if ten_khach else 'Khách lẻ'}\n"
    noi_dung_hoa_don += f"Thời gian: {thoi_gian}\n\n"

    noi_dung_hoa_don += "-" * 50 + "\n"

    for i, mon in enumerate(st.session_state.gio_hang):

        noi_dung_hoa_don += f"{i + 1}. {mon['ten_mon']}\n"
        noi_dung_hoa_don += f"   Số lượng: {mon['so_luong']}\n"
        noi_dung_hoa_don += f"   Đường: {mon['duong']}\n"

        if mon["topping"]:
            noi_dung_hoa_don += (
                "   Topping: " +
                ", ".join(mon["topping"]) +
                "\n"
            )
        else:
            noi_dung_hoa_don += "   Topping: Không có\n"

        noi_dung_hoa_don += (
            f"   Đơn giá: {dinh_dang_tien(mon['don_gia'])}\n"
        )

        noi_dung_hoa_don += (
            f"   Thành tiền: "
            f"{dinh_dang_tien(mon['thanh_tien'])}\n"
        )

        noi_dung_hoa_don += "-" * 50 + "\n"


    noi_dung_hoa_don += "\n"
    noi_dung_hoa_don += (
        f"TỔNG THANH TOÁN: "
        f"{dinh_dang_tien(tong_hoa_don)}\n"
    )

    noi_dung_hoa_don += "\n"
    noi_dung_hoa_don += "=" * 50 + "\n"
    noi_dung_hoa_don += "       CẢM ƠN QUÝ KHÁCH!\n"
    noi_dung_hoa_don += "=" * 50 + "\n"


    # =====================================================
    # XUẤT FILE HÓA ĐƠN
    # =====================================================

    st.divider()

    st.subheader("📥 Xuất hóa đơn")

    ten_file = (
        f"hoa_don_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    st.download_button(
        label="📄 Tải hóa đơn",
        data=noi_dung_hoa_don.encode("utf-8"),
        file_name=ten_file,
        mime="text/plain",
        use_container_width=True
    )


    # =====================================================
    # XÓA ĐƠN HÀNG
    # =====================================================

    if st.button(
        "🗑️ Xóa toàn bộ hóa đơn",
        use_container_width=True
    ):
        st.session_state.gio_hang = []
        st.rerun()
