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

            st.markdown(f"#### 🧋 {index + 1}. {ten_mon}")

            col1, col2 = st.columns(2)

            with col1:

                so_luong = st.number_input(
                    f"Số lượng - {ten_mon}",
                    min_value=1,
                    max_value=20,
                    value=1,
                    step=1,
                    key=f"so_luong_{index}_{ten_mon}"
                )

            with col2:

                muc_duong = st.selectbox(
                    f"Mức độ đường - {ten_mon}",
                    MUC_DUONG,
                    key=f"duong_{index}_{ten_mon}"
                )

            topping_chon = st.multiselect(
                f"Chọn topping - {ten_mon}",
                list(TOPPING.keys()),
                key=f"topping_{index}_{ten_mon}"
            )

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
# NÚT THÊM NHIỀU MÓN VÀO HÓA ĐƠN
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


# =========================================================
# =========================================================
# 🤖 CHATBOT - PHẦN BỔ SUNG
# =========================================================
# =========================================================

st.divider()

st.header("🤖 Chatbot hỗ trợ khách hàng")

st.write(
    "Xin chào! Tôi có thể hỗ trợ bạn về menu, giá món, "
    "topping và hóa đơn."
)


# =========================================================
# KHỞI TẠO LỊCH SỬ CHAT
# =========================================================

if "lich_su_chat" not in st.session_state:
    st.session_state.lich_su_chat = []


# =========================================================
# HÀM CHATBOT
# =========================================================

def chatbot(cau_hoi):

    cau_hoi = cau_hoi.lower().strip()

    # -----------------------------------------
    # CHÀO HỎI
    # -----------------------------------------

    if (
        "xin chào" in cau_hoi
        or "xin chao" in cau_hoi
        or "hello" in cau_hoi
        or cau_hoi == "hi"
    ):

        return (
            "👋 Xin chào! Tôi là chatbot của Quán Trà Sữa. "
            "Tôi có thể giúp bạn xem menu, giá món, topping "
            "và kiểm tra hóa đơn."
        )


    # -----------------------------------------
    # XEM MENU
    # -----------------------------------------

    if (
        "menu" in cau_hoi
        or "có món gì" in cau_hoi
        or "co mon gi" in cau_hoi
    ):

        ket_qua = "🧋 **MENU TRÀ SỮA:**\n\n"

        for ten_mon, gia in TRA_SUA.items():

            ket_qua += (
                f"• {ten_mon}: "
                f"{dinh_dang_tien(gia)}\n"
            )

        return ket_qua


    # -----------------------------------------
    # XEM TOPPING
    # -----------------------------------------

    if (
        "topping" in cau_hoi
        or "topping gì" in cau_hoi
        or "topping gi" in cau_hoi
    ):

        ket_qua = "🍡 **TOPPING:**\n\n"

        for ten_topping, gia in TOPPING.items():

            ket_qua += (
                f"• {ten_topping}: "
                f"{dinh_dang_tien(gia)}\n"
            )

        return ket_qua


    # -----------------------------------------
    # MỨC ĐƯỜNG
    # -----------------------------------------

    if (
        "mức đường" in cau_hoi
        or "muc duong" in cau_hoi
        or "đường" in cau_hoi
    ):

        return (
            "🍬 Quán có 3 mức đường:\n\n"
            "• 100%\n"
            "• 70%\n"
            "• 0%"
        )


    # -----------------------------------------
    # TỔNG TIỀN
    # -----------------------------------------

    if (
        "tổng tiền" in cau_hoi
        or "tong tien" in cau_hoi
        or "thanh toán" in cau_hoi
        or "thanh toan" in cau_hoi
    ):

        if len(st.session_state.gio_hang) == 0:

            return (
                "🧾 Hiện tại hóa đơn chưa có món nào."
            )

        tong = sum(
            mon["thanh_tien"]
            for mon in st.session_state.gio_hang
        )

        return (
            "🧾 Tổng tiền hiện tại của hóa đơn là: "
            f"**{dinh_dang_tien(tong)}**"
        )


    # -----------------------------------------
    # SỐ MÓN ĐÃ ORDER
    # -----------------------------------------

    if (
        "đã order" in cau_hoi
        or "da order" in cau_hoi
        or "hóa đơn có" in cau_hoi
        or "hoa don co" in cau_hoi
    ):

        so_mon = len(
            st.session_state.gio_hang
        )

        return (
            f"🧾 Hiện tại hóa đơn có "
            f"**{so_mon} loại món**."
        )


    # -----------------------------------------
    # GỢI Ý MÓN
    # -----------------------------------------

    if (
        "gợi ý" in cau_hoi
        or "goi y" in cau_hoi
        or "nên uống gì" in cau_hoi
        or "nen uong gi" in cau_hoi
    ):

        return (
            "⭐ Tôi gợi ý cho bạn:\n\n"
            "🧋 Trà sữa truyền thống – 30.000 VNĐ\n"
            "🍵 Trà sữa matcha – 35.000 VNĐ\n"
            "🍫 Trà sữa socola – 35.000 VNĐ\n"
            "🍠 Trà sữa khoai môn – 35.000 VNĐ\n\n"
            "Bạn có thể thêm trân châu đen hoặc kem cheese."
        )


    # -----------------------------------------
    # GIÁ MÓN CỤ THỂ
    # -----------------------------------------

    for ten_mon, gia in TRA_SUA.items():

        if ten_mon.lower() in cau_hoi:

            return (
                f"🧋 {ten_mon} có giá "
                f"**{dinh_dang_tien(gia)}/ly**."
            )


    # -----------------------------------------
    # GIÁ TOPPING CỤ THỂ
    # -----------------------------------------

    for ten_topping, gia in TOPPING.items():

        if ten_topping.lower() in cau_hoi:

            return (
                f"🍡 {ten_topping} có giá "
                f"**{dinh_dang_tien(gia)}/phần**."
            )


    # -----------------------------------------
    # CẢM ƠN
    # -----------------------------------------

    if (
        "cảm ơn" in cau_hoi
        or "cam on" in cau_hoi
    ):

        return (
            "🥰 Cảm ơn bạn! Chúc bạn thưởng thức "
            "trà sữa thật ngon! 🧋"
        )


    # -----------------------------------------
    # KHÔNG HIỂU
    # -----------------------------------------

    return (
        "🤖 Xin lỗi, tôi chưa hiểu câu hỏi.\n\n"
        "Bạn có thể hỏi:\n"
        "• Menu có những món gì?\n"
        "• Trà sữa matcha bao nhiêu tiền?\n"
        "• Topping có những gì?\n"
        "• Tổng tiền hiện tại bao nhiêu?\n"
        "• Tôi nên uống món gì?"
    )


# =========================================================
# HIỂN THỊ LỊCH SỬ CHAT
# =========================================================

for nguoi_gui, noi_dung in st.session_state.lich_su_chat:

    if nguoi_gui == "Bạn":

        st.chat_message("user").write(
            noi_dung
        )

    else:

        st.chat_message("assistant").write(
            noi_dung
        )


# =========================================================
# Ô CHATBOT
# =========================================================

cau_hoi = st.chat_input(
    "💬 Nhập câu hỏi cho chatbot..."
)

if cau_hoi:

    # Lưu câu hỏi của khách
    st.session_state.lich_su_chat.append(
        ("Bạn", cau_hoi)
    )

    # Chatbot trả lời
    tra_loi = chatbot(cau_hoi)

    # Lưu câu trả lời
    st.session_state.lich_su_chat.append(
        ("Chatbot", tra_loi)
    )

    # Load lại giao diện
    st.rerun()


# =========================================================
# XÓA LỊCH SỬ CHAT
# =========================================================

if st.session_state.lich_su_chat:

    if st.button(
        "🗑️ Xóa lịch sử chatbot",
        use_container_width=True
    ):

        st.session_state.lich_su_chat = []

        st.rerun()
```
