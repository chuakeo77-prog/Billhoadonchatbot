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
# CSS - GIAO DIỆN
# =========================================================

st.markdown("""
<style>

    .stApp {
        background-color: #FFF5E1;
    }

    h1 {
        color: #5C3A21;
        text-align: center;
        font-weight: 800;
    }

    h2, h3 {
        color: #8B5E3C;
    }

    .stButton > button {
        background-color: #8B5E3C;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #5C3A21;
        color: white;
    }

    .bill-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #D7B899;
        margin-bottom: 15px;
    }

    .total-box {
        background-color: #F3E0C0;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #8B5E3C;
    }

    .total-money {
        color: #8B5E3C;
        font-size: 32px;
        font-weight: bold;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOGO
# =========================================================

try:
    st.image("logo.jpg", width=180)
except:
    pass


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

MUC_DUONG = [
    "100%",
    "70%",
    "0%"
]


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def dinh_dang_tien(tien):
    return f"{tien:,.0f} VNĐ"


# =========================================================
# SESSION STATE
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
# TẠO ORDER NHIỀU MÓN
# =========================================================

st.header("🛒 TẠO ĐƠN HÀNG")

st.write(
    "Bạn có thể thêm **nhiều loại trà sữa trong cùng một đơn hàng**."
)


# =========================================================
# THÊM DÒNG ORDER
# =========================================================

if "so_dong_order" not in st.session_state:
    st.session_state.so_dong_order = 1


# Nút thêm món
if st.button(
    "➕ Thêm loại trà sữa",
    use_container_width=True
):
    st.session_state.so_dong_order += 1


# =========================================================
# NHẬP NHIỀU MÓN
# =========================================================

danh_sach_order = []

for i in range(st.session_state.so_dong_order):

    st.markdown(
        f"### 🧋 Món {i + 1}"
    )

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # TÊN TRÀ SỮA
    # -----------------------------------------------------

    with col1:

        ten_mon = st.selectbox(
            "Loại trà sữa",
            list(TRA_SUA.keys()),
            key=f"ten_mon_{i}"
        )

    # -----------------------------------------------------
    # SỐ LƯỢNG
    # -----------------------------------------------------

    with col2:

        so_luong = st.number_input(
            "Số lượng",
            min_value=1,
            max_value=50,
            value=1,
            step=1,
            key=f"so_luong_{i}"
        )


    # -----------------------------------------------------
    # MỨC ĐƯỜNG
    # -----------------------------------------------------

    muc_duong = st.selectbox(
        "Mức độ đường",
        MUC_DUONG,
        key=f"duong_{i}"
    )


    # -----------------------------------------------------
    # TOPPING
    # -----------------------------------------------------

    topping_chon = st.multiselect(
        "Chọn topping",
        list(TOPPING.keys()),
        key=f"topping_{i}"
    )


    # -----------------------------------------------------
    # TÍNH TIỀN
    # -----------------------------------------------------

    gia_goc = TRA_SUA[ten_mon]

    tien_topping = sum(
        TOPPING[x]
        for x in topping_chon
    )

    don_gia = gia_goc + tien_topping

    thanh_tien = don_gia * so_luong


    # -----------------------------------------------------
    # HIỂN THỊ TIỀN MÓN
    # -----------------------------------------------------

    st.info(
        f"""
        **{ten_mon}**

        Đường: **{muc_duong}**

        Topping: **{
            ", ".join(topping_chon)
            if topping_chon
            else "Không có"
        }**

        Đơn giá: **{dinh_dang_tien(don_gia)}**

        Số lượng: **{so_luong}**

        Thành tiền: **{dinh_dang_tien(thanh_tien)}**
        """
    )


    # -----------------------------------------------------
    # LƯU ORDER
    # -----------------------------------------------------

    danh_sach_order.append({
        "ten_mon": ten_mon,
        "so_luong": so_luong,
        "duong": muc_duong,
        "topping": topping_chon,
        "don_gia": don_gia,
        "thanh_tien": thanh_tien
    })

    st.divider()


# =========================================================
# XÁC NHẬN ĐƠN HÀNG
# =========================================================

if st.button(
    "✅ XÁC NHẬN ĐẶT HÀNG",
    use_container_width=True
):

    for mon in danh_sach_order:

        st.session_state.gio_hang.append(mon)

    st.success(
        "🎉 Đã thêm toàn bộ món vào hóa đơn!"
    )


# =========================================================
# HIỂN THỊ HÓA ĐƠN
# =========================================================

st.divider()

st.header("🧾 HÓA ĐƠN")


if len(st.session_state.gio_hang) == 0:

    st.warning(
        "Chưa có món nào trong hóa đơn."
    )

else:

    tong_hoa_don = 0


    # =====================================================
    # DUYỆT DANH SÁCH MÓN
    # =====================================================

    for i, mon in enumerate(
        st.session_state.gio_hang
    ):

        tong_hoa_don += mon["thanh_tien"]


        st.markdown(
            f"""
            <div class="bill-box">

            <h3>
            🧋 {i + 1}. {mon['ten_mon']}
            </h3>

            <b>Số lượng:</b>
            {mon['so_luong']}
            <br>

            <b>Mức đường:</b>
            {mon['duong']}
            <br>

            <b>Topping:</b>
            {
                ", ".join(mon["topping"])
                if mon["topping"]
                else "Không có"
            }
            <br>

            <b>Đơn giá:</b>
            {dinh_dang_tien(mon["don_gia"])}
            <br>

            <b>Thành tiền:</b>
            {dinh_dang_tien(mon["thanh_tien"])}

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # TỔNG TIỀN
    # =====================================================

    st.markdown(
        f"""
        <div class="total-box">

        <h2>💰 TỔNG THANH TOÁN</h2>

        <div class="total-money">
        {dinh_dang_tien(tong_hoa_don)}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # TẠO HÓA ĐƠN FILE TXT
    # =====================================================

    thoi_gian = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )


    noi_dung_hoa_don = ""

    noi_dung_hoa_don += "=" * 55 + "\n"
    noi_dung_hoa_don += "              QUÁN TRÀ SỮA\n"
    noi_dung_hoa_don += "             HÓA ĐƠN THANH TOÁN\n"
    noi_dung_hoa_don += "=" * 55 + "\n\n"

    noi_dung_hoa_don += (
        f"Khách hàng: "
        f"{ten_khach if ten_khach else 'Khách lẻ'}\n"
    )

    noi_dung_hoa_don += (
        f"Thời gian: {thoi_gian}\n"
    )

    noi_dung_hoa_don += "\n"
    noi_dung_hoa_don += "-" * 55 + "\n"


    # =====================================================
    # CHI TIẾT MÓN
    # =====================================================

    for i, mon in enumerate(
        st.session_state.gio_hang
    ):

        noi_dung_hoa_don += (
            f"Món {i + 1}: "
            f"{mon['ten_mon']}\n"
        )

        noi_dung_hoa_don += (
            f"  Số lượng: "
            f"{mon['so_luong']}\n"
        )

        noi_dung_hoa_don += (
            f"  Đường: "
            f"{mon['duong']}\n"
        )

        noi_dung_hoa_don += (
            f"  Topping: "
            f"{
                ', '.join(mon['topping'])
                if mon['topping']
                else 'Không có'
            }\n"
        )

        noi_dung_hoa_don += (
            f"  Đơn giá: "
            f"{dinh_dang_tien(mon['don_gia'])}\n"
        )

        noi_dung_hoa_don += (
            f"  Thành tiền: "
            f"{dinh_dang_tien(mon['thanh_tien'])}\n"
        )

        noi_dung_hoa_don += (
            "-" * 55 + "\n"
        )


    # =====================================================
    # TỔNG HÓA ĐƠN
    # =====================================================

    noi_dung_hoa_don += "\n"

    noi_dung_hoa_don += (
        f"TỔNG THANH TOÁN: "
        f"{dinh_dang_tien(tong_hoa_don)}\n"
    )

    noi_dung_hoa_don += "\n"

    noi_dung_hoa_don += (
        "=" * 55 + "\n"
    )

    noi_dung_hoa_don += (
        "          CẢM ƠN QUÝ KHÁCH!\n"
    )

    noi_dung_hoa_don += (
        "=" * 55 + "\n"
    )


    # =====================================================
    # TẢI HÓA ĐƠN
    # =====================================================

    st.divider()

    st.subheader("📥 Xuất hóa đơn")

    ten_file = (
        "hoa_don_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        + ".txt"
    )


    st.download_button(
        label="📄 TẢI HÓA ĐƠN",
        data=noi_dung_hoa_don.encode("utf-8"),
        file_name=ten_file,
        mime="text/plain",
        use_container_width=True
    )


# =========================================================
# XÓA TOÀN BỘ ĐƠN
# =========================================================

st.divider()

if st.button(
    "🗑️ XÓA TOÀN BỘ HÓA ĐƠN",
    use_container_width=True
):

    st.session_state.gio_hang = []

    st.session_state.so_dong_order = 1

    st.rerun()
