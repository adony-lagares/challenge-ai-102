import streamlit as st
from services.blob_service import upload_blob
from services.card_service import analyse_card

def show_image_and_info(blob_url, card_info):
    """ This function is used to display the card image, as well as
    its detected information, if said card is valid."""

    st.image(blob_url, caption = "Image sent", use_column_width = True)
    st.write("Analysis results:")

    if card_info and card_info["card_name"]:
        st.markdown(f"<h1 style='color: green;'>Valid Card</h1>", unsafe_allow_html = True)
        st.write(f"Owner name: {card_info['card_name']}")
        st.write(f"Bank: {card_info['bank_name']}")
        st.write(f"Expiry date: {card_info['expiry_date']}")
    else:
        st.markdown(f"<h1 style='color: red;'>Not Valid Card</h1>", unsafe_allow_html = True)
        st.write("This is not a valid card.")

def configure_interface():
    st.title("File Upload - DIO Challenges Azure Document Intelligence")
    uploaded_file = st.file_uploader("Select a file...", type = ["png", "jpg", "jpeg"])

    # if file was uploaded, get its info
    if uploaded_file is not None:
        file_name = uploaded_file.name
    
        # send file to Azure Blob Storage
        blob_url = upload_blob(uploaded_file, file_name)
        if blob_url:
            st.write(f"File {file_name} was successfully sent to Azure Blob Storage")
            card_info = analyse_card(blob_url)
            show_image_and_info(blob_url, card_info)
        else:
            st.write(f"Error sending file {file_name} to Azure Blob Storage")


# run main function
if __name__ == "__main__":
    configure_interface()