import os
import streamlit as st

# Setted up a session variable to store authentication status
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


def app():
    op_dir = "output_files"
    os.makedirs(op_dir, exist_ok=True)

    #----------Necessary Fucntions----------
    def save_to_file(document, filename):
        filepath = os.path.join(op_dir, filename)
        
        with open(filepath, "w") as file:
            file.write(document)
        return filepath

    def open_file(filename):
        filepath = os.path.join(op_dir, filename)
        try:
            with open(filepath, "r") as file:
                file_contents = file.read()
            return file_contents
        except FileNotFoundError:
            return None

    #--------Creation of new file---------------
    filename= st.text_input("enter the filename (including file extension (e.g document.txt))")  
    document = st.text_area("Write you Document: " , height= 500)
    if(st.button("Save to a file")):
        if document:
            file_path = save_to_file(document, filename)
            
            st.success(f"Document saved to {file_path}")
        else:
            st.warning("Cannot save an empty document. Write something before saving.")


    #-------------tabs of RUD---------------
    View_Save_files, Edit_Save_files, Delete_Saved_file = st.tabs(["View_Save_files", "Edit_Save_files", "Delete_Saved_file"])
    saved_files = os.listdir(op_dir)


    #---------------View(READ) tab---------------------
    with View_Save_files:
        op_filename = st.selectbox("Select a file to view" , saved_files, key="View_file")
        if(st.button("Open Saved File")):
                file_path = os.path.join(op_dir, op_filename)
                with open(file_path , "r") as file:
                    file_content = file.read()
                    st.write(f"The following is the content of the file {op_filename}")
                    st.write(file_content)

                home_directory = os.path.expanduser("~")
                complete_file_path = os.path.abspath(os.path.join(home_directory, file_path))
                st.write(f"Complete File Path: {complete_file_path}")  # Displaying the complete file path
    
                st.download_button(
                    label="Download the saved file",
                    data=file_content,
                    file_name=op_filename,
                    key="download_button"
                )


    #--------------edit(UPDATE) tab---------------------
    with Edit_Save_files:
        # existing_files = os.listdir(op_dir)
        selected_file = st.selectbox("Select a file to rewrite:", saved_files, key="rewrite_file")

        file_contents = open_file(selected_file)
        if file_contents is not None:
            st.write("Content of the Selected File (Do you want to change it?):")
            st.write(file_contents)

        edited_document = st.text_area("Edit the document:", value=file_contents, height=200)
        if st.button("Rewrite File"):
            if edited_document:
                file_path = save_to_file(edited_document, selected_file)
                st.success(f"File '{selected_file}' rewritten successfully.")
            else:
                st.warning("Cannot save an empty document. Write something before rewriting.")  



    #---------------remove(DELETE) tab-------------------------
    with Delete_Saved_file:
        selected_file = st.selectbox("Select a file to delete: ", saved_files, key="delete_file")
        file_path = os.path.join(op_dir, selected_file)
        file_contents = open_file(selected_file)
        if file_contents is not None:
            st.write("Content of the Selected File:")
            st.write(file_contents)

        if st.button("Delete"): 
            os.remove(file_path)
            st.success(f"you have sucessfully deleted {selected_file}")









# ---------Checking authentication status---------------
if st.session_state.authenticated:
    # If authenticated, run the app
    app()
else:
    # -----------If not authenticated, display a login form-----------
    username = st.text_input("Enter Username:")
    password = st.text_input("Enter Password:", type="password")

    if st.button("Login"):
        #-------------------Replace the following condition with your authentication logic----------------  
        if username == "admin" and password == "admin":
            st.session_state.authenticated = True
        else:
            st.error("Invalid credentials. Please try again.")
