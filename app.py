import streamlit as st
from datetime import datetime

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Milk Tea Billing",
    page_icon="🧋",
    layout="centered"
)

# =========================================================
# HIỂN THỊ LOGO
# =========================================================

try:
    st.image("logo.jpg")
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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


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
# CHỌN NHIỀU MÓN TRONG CÙNG MỘT LẦN ORDER
# =========================================================

st.header("🧋 Chọn món")

st.info(
    "💡 Bạn có thể chọn nhiều loại trà sữa cùng lúc. "
    "Mỗi loại có thể cài đặt số lượng, mức đường và topping riêng."
)

cac_mon_chon = st.multiselect(
    "Chọn các loại trà sữa",
    list(TRA_SUA.keys()),
    placeholder="Chọn một hoặc nhiều loại trà sữa..."
)


# =========================================================
# THIẾT LẬP CHI TIẾT CHO TỪNG MÓN
# =========================================================

danh_sach_mon_tam = []

if cac_mon_chon:

    st.markdown("### ⚙️ Thiết lập từng món")

    for index, ten_mon in enumerate(cac_mon_chon):

        with st.container(border=True):

            st.markdown(
                f"#### 🧋 {index + 1}. {ten_mon}"
            )

            col1, col2 = st.columns(2)

            # -------------------------------------------------
            # SỐ LƯỢNG
            # -------------------------------------------------

            with col1:

                so_luong = st.number_input(
                    f"Số lượng - {ten_mon}",
                    min_value=1,
                    max_value=20,
                    value=1,
                    step=1,
                    key=f"so_luong_{index}_{ten_mon}"
                )

            # -------------------------------------------------
            # MỨC ĐƯỜNG
            # -------------------------------------------------

            with col2:

                muc_duong = st.selectbox(
                    f"Mức độ đường - {ten_mon}",
                    MUC_DUONG,
                    key=f"duong_{index}_{ten_mon}"
                )

            # -------------------------------------------------
            # TOPPING
            # -------------------------------------------------

            topping_chon = st.multiselect(
                f"Chọn topping - {ten_mon}",
                list(TOPPING.keys()),
                key=f"topping_{index}_{ten_mon}"
            )

            # -------------------------------------------------
            # TÍNH GIÁ
            # -------------------------------------------------

            gia_tra_sua = TRA_SUA[ten_mon]

            tong_tien_topping_mot_ly = sum(
                TOPPING[topping]
                for topping in topping_chon
            )

            gia_mot_ly = (
                gia_tra_sua +
                tong_tien_topping_mot_ly
            )

            thanh_tien = gia_mot_ly * so_luong

            # -------------------------------------------------
            # HIỂN THỊ THÔNG TIN MÓN
            # -------------------------------------------------

            st.info(
                f"""
**Món:** {ten_mon}

**Đường:** {muc_duong}

**Topping:** {
    ", ".join(topping_chon)
    if topping_chon
    else "Không có"
}

**Giá trà sữa:** {dinh_dang_tien(gia_tra_sua)}

**Giá topping / ly:** {
    dinh_dang_tien(tong_tien_topping_mot_ly)
}

**Đơn giá / ly:** {dinh_dang_tien(gia_mot_ly)}

**Số lượng:** {so_luong}

**Thành tiền:** {dinh_dang_tien(thanh_tien)}
"""
            )

            # -------------------------------------------------
            # LƯU MÓN TẠM THỜI
            # -------------------------------------------------

            mon = {
                "ten_mon": ten_mon,
                "so_luong": so_luong,
                "duong": muc_duong,
                "topping": topping_chon.copy(),
                "don_gia": gia_mot_ly,
                "thanh_tien": thanh_tien
            }

            danh_sach_mon_tam.append(mon)


# =========================================================
# THÊM NHIỀU MÓN VÀO HÓA ĐƠN
# =========================================================

if cac_mon_chon:

    st.divider()

    if st.button(
        "➕ Thêm tất cả món vào hóa đơn",
        use_container_width=True,
        type="primary"
    ):

        for mon in danh_sach_mon_tam:
            st.session_state.gio_hang.append(mon)

        st.success(
            f"✅ Đã thêm {len(danh_sach_mon_tam)} loại món vào hóa đơn!"
        )

        st.rerun()


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

        st.markdown(
            f"### {i + 1}. {mon['ten_mon']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(
                f"**Số lượng:** {mon['so_luong']}"
            )

        with col2:
            st.write(
                f"**Đường:** {mon['duong']}"
            )

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

            st.write(
                "**Topping:** Không có"
            )

        st.write(
            f"**Đơn giá:** {dinh_dang_tien(mon['don_gia'])}"
        )

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

            <h1>
                {dinh_dang_tien(tong_hoa_don)}
            </h1>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # TẠO NỘI DUNG FILE HÓA ĐƠN
    # =====================================================

    thoi_gian = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    noi_dung_hoa_don = ""

    noi_dung_hoa_don += "=" * 50 + "\n"
    noi_dung_hoa_don += "             QUÁN TRÀ SỮA\n"
    noi_dung_hoa_don += "             HÓA ĐƠN THANH TOÁN\n"
    noi_dung_hoa_don += "=" * 50 + "\n\n"

    noi_dung_hoa_don += (
        f"Khách hàng: "
        f"{ten_khach if ten_khach else 'Khách lẻ'}\n"
    )

    noi_dung_hoa_don += (
        f"Thời gian: {thoi_gian}\n\n"
    )

    noi_dung_hoa_don += "-" * 50 + "\n"


    # =====================================================
    # CHI TIẾT CÁC MÓN
    # =====================================================

    for i, mon in enumerate(
        st.session_state.gio_hang
    ):

        noi_dung_hoa_don += (
            f"{i + 1}. {mon['ten_mon']}\n"
        )

        noi_dung_hoa_don += (
            f"   Số lượng: "
            f"{mon['so_luong']}\n"
        )

        noi_dung_hoa_don += (
            f"   Đường: "
            f"{mon['duong']}\n"
        )

        if mon["topping"]:

            noi_dung_hoa_don += (
                "   Topping: " +
                ", ".join(mon["topping"]) +
                "\n"
            )

        else:

            noi_dung_hoa_don += (
                "   Topping: Không có\n"
            )

        noi_dung_hoa_don += (
            f"   Đơn giá: "
            f"{dinh_dang_tien(mon['don_gia'])}\n"
        )

        noi_dung_hoa_don += (
            f"   Thành tiền: "
            f"{dinh_dang_tien(mon['thanh_tien'])}\n"
        )

        noi_dung_hoa_don += "-" * 50 + "\n"


    # =====================================================
    # TỔNG THANH TOÁN
    # =====================================================

    noi_dung_hoa_don += "\n"

    noi_dung_hoa_don += (
        f"TỔNG THANH TOÁN: "
        f"{dinh_dang_tien(tong_hoa_don)}\n"
    )

    noi_dung_hoa_don += "\n"

    noi_dung_hoa_don += "=" * 50 + "\n"

    noi_dung_hoa_don += (
        "       CẢM ƠN QUÝ KHÁCH!\n"
    )

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


# =========================================================
# =========================================================
# CHATBOT TRỢ LÝ QUÁN TRÀ SỮA
# =========================================================
# =========================================================

st.divider()

st.header("🤖 Chatbot trợ lý")

st.caption(
    "Trợ lý tự động hỗ trợ khách hàng về menu, giá món, "
    "topping, cách order và hóa đơn."
)


# =========================================================
# HÀM XỬ LÝ CHATBOT
# =========================================================

def chatbot_tra_loi(cau_hoi):

    cau_hoi_goc = cau_hoi.strip()

    cau_hoi = cau_hoi_goc.lower()

    # -----------------------------------------------------
    # TỔNG TIỀN HIỆN TẠI
    # -----------------------------------------------------

    if (
        "tổng tiền" in cau_hoi
        or "tong tien" in cau_hoi
        or "thanh toán" in cau_hoi
        or "thanh toan" in cau_hoi
        or "bao nhiêu tiền" in cau_hoi
        or "bao nhieu tien" in cau_hoi
    ):

        if len(st.session_state.gio_hang) == 0:

            return (
                "🧾 Hiện tại hóa đơn chưa có món nào. "
                "Bạn hãy chọn món để bắt đầu order nhé!"
            )

        tong = sum(
            mon["thanh_tien"]
            for mon in st.session_state.gio_hang
        )

        so_loai = len(st.session_state.gio_hang)

        return (
            f"🧾 Hóa đơn hiện có **{so_loai} món**.\n\n"
            f"💰 Tổng thanh toán: **{dinh_dang_tien(tong)}**."
        )


    # -----------------------------------------------------
    # SỐ MÓN TRONG HÓA ĐƠN
    # -----------------------------------------------------

    if (
        "hóa đơn có" in cau_hoi
        or "hoa don co" in cau_hoi
        or "đã gọi" in cau_hoi
        or "da goi" in cau_hoi
        or "đã order" in cau_hoi
        or "da order" in cau_hoi
    ):

        so_mon = len(st.session_state.gio_hang)

        if so_mon == 0:
            return "🧾 Hóa đơn hiện chưa có món nào."

        return (
            f"🧾 Hiện tại hóa đơn có **{so_mon} loại món**."
        )


    # -----------------------------------------------------
    # MENU
    # -----------------------------------------------------

    if (
        "menu" in cau_hoi
        or "có món gì" in cau_hoi
        or "co mon gi" in cau_hoi
        or "có những món" in cau_hoi
        or "co nhung mon" in cau_hoi
    ):

        danh_sach = "\n".join(
            [
                f"• **{mon}** – {dinh_dang_tien(gia)}"
                for mon, gia in TRA_SUA.items()
            ]
        )

        return (
            "🧋 **MENU TRÀ SỮA:**\n\n"
            + danh_sach
            + "\n\nBạn có thể chọn nhiều món cùng lúc."
        )


    # -----------------------------------------------------
    # TOPPING
    # -----------------------------------------------------

    if (
        "topping" in cau_hoi
        or "thêm gì" in cau_hoi
        or "them gi" in cau_hoi
    ):

        danh_sach = "\n".join(
            [
                f"• **{topping}** – {dinh_dang_tien(gia)}"
                for topping, gia in TOPPING.items()
            ]
        )

        return (
            "🍡 **DANH SÁCH TOPPING:**\n\n"
            + danh_sach
        )


    # -----------------------------------------------------
    # MỨC ĐƯỜNG
    # -----------------------------------------------------

    if (
        "mức đường" in cau_hoi
        or "muc duong" in cau_hoi
        or "đường" in cau_hoi
        or "duong" in cau_hoi
    ):

        return (
            "🍬 Quán hiện có 3 mức đường:\n\n"
            "• **100%** – ngọt bình thường\n"
            "• **70%** – ít ngọt\n"
            "• **0%** – không thêm đường\n\n"
            "Bạn có thể cài đặt mức đường riêng cho từng món."
        )


    # -----------------------------------------------------
    # GỢI Ý MÓN
    # -----------------------------------------------------

    if (
        "gợi ý" in cau_hoi
        or "goi y" in cau_hoi
        or "nên uống gì" in cau_hoi
        or "nen uong gi" in cau_hoi
        or "món nào ngon" in cau_hoi
        or "mon nao ngon" in cau_hoi
    ):

        return (
            "🥤 Mình gợi ý một số lựa chọn:\n\n"
            "⭐ **Trà sữa truyền thống** – lựa chọn cơ bản, dễ uống.\n\n"
            "🍵 **Trà sữa matcha** – phù hợp nếu bạn thích vị trà xanh.\n\n"
            "🍫 **Trà sữa socola** – phù hợp nếu bạn thích vị ngọt và socola.\n\n"
            "🍠 **Trà sữa khoai môn** – vị béo, thơm.\n\n"
            "🧀 Nếu thích topping, bạn có thể thêm **kem cheese** hoặc **pudding trứng**."
        )


    # -----------------------------------------------------
    # GIÁ MỘT MÓN CỤ THỂ
    # -----------------------------------------------------

    for ten_mon, gia in TRA_SUA.items():

        if ten_mon.lower() in cau_hoi:

            return (
                f"🧋 **{ten_mon}** có giá "
                f"**{dinh_dang_tien(gia)}/ly** "
                "chưa bao gồm topping."
            )


    # -----------------------------------------------------
    # GIÁ TOPPING CỤ THỂ
    # -----------------------------------------------------

    for ten_topping, gia in TOPPING.items():

        if ten_topping.lower() in cau_hoi:

            return (
                f"🍡 **{ten_topping}** có giá "
                f"**{dinh_dang_tien(gia)}/phần**."
            )


    # -----------------------------------------------------
    # CÁCH ORDER
    # -----------------------------------------------------

    if (
        "order" in cau_hoi
        or "gọi món" in cau_hoi
        or "goi mon" in cau_hoi
        or "đặt món" in cau_hoi
        or "dat mon" in cau_hoi
        or "đặt hàng" in cau_hoi
    ):

        return (
            "🛒 **Cách order rất đơn giản:**\n\n"
            "1️⃣ Chọn một hoặc nhiều loại trà sữa.\n\n"
            "2️⃣ Chọn số lượng cho từng món.\n\n"
            "3️⃣ Chọn mức đường.\n\n"
            "4️⃣ Chọn topping nếu muốn.\n\n"
            "5️⃣ Bấm **'Thêm tất cả món vào hóa đơn'**.\n\n"
            "6️⃣ Kiểm tra tổng tiền và tải hóa đơn."
        )


    # -----------------------------------------------------
    # XIN CHÀO
    # -----------------------------------------------------

    if (
        "xin chào" in cau_hoi
        or "xin chao" in cau_hoi
        or "hello" in cau_hoi
        or "hi" == cau_hoi
        or cau_hoi.startswith("chào")
        or cau_hoi.startswith("chao")
    ):

        return (
            "👋 Xin chào! Mình là **trợ lý ảo của Quán Trà Sữa**.\n\n"
            "Mình có thể giúp bạn:\n"
            "• Xem menu 🧋\n"
            "• Xem giá 💰\n"
            "• Xem topping 🍡\n"
            "• Gợi ý món ⭐\n"
            "• Kiểm tra hóa đơn 🧾\n"
            "• Hướng dẫn order 🛒"
        )


    # -----------------------------------------------------
    # CẢM ƠN
    # -----------------------------------------------------

    if (
        "cảm ơn" in cau_hoi
        or "cam on" in cau_hoi
        or "thanks" in cau_hoi
    ):

        return (
            "🥰 Rất vui được hỗ trợ bạn! "
            "Chúc bạn có một ly trà sữa thật ngon! 🧋"
        )


    # -----------------------------------------------------
    # TRẢ LỜI MẶC ĐỊNH
    # -----------------------------------------------------

    return (
        "🤖 Mình chưa hiểu câu hỏi của bạn.\n\n"
        "Bạn có thể hỏi mình những câu như:\n\n"
        "• **Menu có những món gì?**\n"
        "• **Trà sữa matcha bao nhiêu tiền?**\n"
        "• **Topping có những gì?**\n"
        "• **Kem cheese bao nhiêu tiền?**\n"
        "• **Gợi ý cho tôi một món ngon.**\n"
        "• **Hóa đơn hiện tại bao nhiêu tiền?**\n"
        "• **Cách order như thế nào?**"
    )


# =========================================================
# CÂU HỎI NHANH
# =========================================================

st.markdown("### 💬 Câu hỏi nhanh")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🧋 Xem menu",
        use_container_width=True
    ):

        cau_hoi_nhanh = "Menu có những món gì?"

        tra_loi = chatbot_tra_loi(
            cau_hoi_nhanh
        )

        st.session_state.chat_history.append(
            ("Bạn", cau_hoi_nhanh)
        )

        st.session_state.chat_history.append(
            ("Chatbot", tra_loi)
        )


with col2:

    if st.button(
        "🍡 Xem topping",
        use_container_width=True
    ):

        cau_hoi_nhanh = "Topping có những gì?"

        tra_loi = chatbot_tra_loi(
            cau_hoi_nhanh
        )

        st.session_state.chat_history.append(
            ("Bạn", cau_hoi_nhanh)
        )

        st.session_state.chat_history.append(
            ("Chatbot", tra_loi)
        )


col3, col4 = st.columns(2)

with col3:

    if st.button(
        "⭐ Gợi ý món",
        use_container_width=True
    ):

        cau_hoi_nhanh = "Gợi ý cho tôi một món ngon"

        tra_loi = chatbot_tra_loi(
            cau_hoi_nhanh
        )

        st.session_state.chat_history.append(
            ("Bạn", cau_hoi_nhanh)
        )

        st.session_state.chat_history.append(
            ("Chatbot", tra_loi)
        )


with col4:

    if st.button(
        "🧾 Xem tổng tiền",
        use_container_width=True
    ):

        cau_hoi_nhanh = "Tổng tiền hiện tại bao nhiêu?"

        tra_loi = chatbot_tra_loi(
            cau_hoi_nhanh
        )

        st.session_state.chat_history.append(
            ("Bạn", cau_hoi_nhanh)
        )

        st.session_state.chat_history.append(
            ("Chatbot", tra_loi)
        )


# =========================================================
# HIỂN THỊ LỊCH SỬ CHAT
# =========================================================

if st.session_state.chat_history:

    st.markdown("### 💭 Hội thoại")

    for nguoi_gui, noi_dung in st.session_state.chat_history:

        if nguoi_gui == "Bạn":

            st.markdown(
                f"""
                <div style="
                    background-color:#DCF8C6;
                    padding:10px;
                    border-radius:10px;
                    margin-bottom:8px;
                    text-align:right;
                ">
                    <b>👤 Bạn</b><br>
                    {noi_dung}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div style="
                    background-color:#F1F1F1;
                    padding:10px;
                    border-radius:10px;
                    margin-bottom:8px;
                ">
                    <b>🤖 Chatbot</b><br>
                    {noi_dung}
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# Ô NHẬP CHAT
# =========================================================

cau_hoi = st.chat_input(
    "💬 Nhập câu hỏi cho trợ lý..."
)

if cau_hoi:

    # Lưu câu hỏi
    st.session_state.chat_history.append(
        ("Bạn", cau_hoi)
    )

    # Chatbot xử lý
    tra_loi = chatbot_tra_loi(
        cau_hoi
    )

    # Lưu câu trả lời
    st.session_state.chat_history.append(
        ("Chatbot", tra_loi)
    )

    st.rerun()


# =========================================================
# XÓA LỊCH SỬ CHAT
# =========================================================

if st.session_state.chat_history:

    if st.button(
        "🗑️ Xóa lịch sử chatbot",
        use_container_width=True
    ):

        st.session_state.chat_history = []

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🧋 Milk Tea Billing System | "
    "Order - Billing - Chatbot"
)
```
