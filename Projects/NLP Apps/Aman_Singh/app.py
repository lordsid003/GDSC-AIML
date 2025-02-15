from model import Model
model = Model()
import streamlit as st
import pandas as pd
import altair as alt


st.title('📊 Expense Tracker & Finance Manager')
st.write("This app allows you to track your expenses and manage your finances efficiently. 💸")




# conversation = st.text_area("💬 Enter your conversation with the chatbot here:", height=68)
# response_placeholder = st.empty()
# def eventhandler():
#     if conversation == "":
#         return
#     with st.spinner("Chatting with the Finance Assistant..."):
#         response = model.chat(conversation)

#     st.write(response["output"])
#     response_placeholder.write("Chat initiated")
# st.button("Send",on_click=eventhandler)

st.header("📂 Upload your CSV data")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])


if uploaded_file is not None:

    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)

    uploaded_file.seek(0)
    model.read_csv(uploaded_file)

    # Display the data
    st.subheader('📈 Uploaded Data')
    st.write(df)

    # Generate graphs
    st.subheader('📊 Data Visualization')

    # Create a pie chart of expenses by category
    if 'Category' in df.columns and 'Amount' in df.columns:
        pie_chart = alt.Chart(df).mark_arc().encode(
            theta='Amount',
            color='Category',
            tooltip=['Category', 'Amount']
        ).properties(
            title='Expenses by Category'
        )
        st.altair_chart(pie_chart, use_container_width=True)
    else:
        st.write("The CSV file does not have 'Category' and 'Amount' columns. Please upload a file with these columns for visualization.")
    st.subheader('🏦 Assets and Liabilities Visualization')
    if 'Assets' in df.columns and 'Liabilities' in df.columns:
        # Preparing data for the pie chart
        total_assets = df['Assets'].sum()
        total_liabilities = df['Liabilities'].sum()
        pie_data = pd.DataFrame({
            'Type': ['Assets', 'Liabilities'],
            'Value': [total_assets, total_liabilities]
        })
        pie_chart_assets_liabilities = alt.Chart(pie_data).mark_arc().encode(
            theta='Value',
            color='Type',
            tooltip=['Type', 'Value']
        ).properties(
            title='Assets and Liabilities'
        )
        st.altair_chart(pie_chart_assets_liabilities, use_container_width=True)
    else:
        st.write("The CSV file does not have 'Assets' and 'Liabilities' columns. Please upload a file with these columns for assets and liabilities visualization.")

st.header("🤖 Chat with your Finance Assistant")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.history.append({ "user": prompt})

    response = f"Kento-Bento: {model.chat(prompt, st.session_state.history)}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.history.append({ "assistant": response})
st.write("Feel free to ask any other questions or manage your finances! 📬")
