import streamlit as st
import matplotlib.pyplot as plt
from financial_analyst import financial_analyst

def main():
    st.title("AI Financial Analyst App")

    company_name = st.text_input("Company name:")
    analyze_button = st.button("Analyze")

    if analyze_button:
        if company_name:
            st.write("Analyzing... Please wait.")

            investment_thesis, hist = financial_analyst(company_name)

            # Select 'Open' and 'Close' columns from the hist dataframe
            hist_selected = hist[['Open', 'Close']]

            # Create a new figure in matplotlib
            fig, ax = plt.subplots()

            # Plot the selected data
            hist_selected.plot(kind='line', ax=ax)

            # Set the title and labels
            ax.set_title(f"{company_name} Stock Price")
            ax.set_xlabel("Date")
            ax.set_ylabel("Stock Price")

            # Display the plot in Streamlit
            st.pyplot(fig)

            st.write("Investment Thesis / Recommendation:")

            st.markdown(investment_thesis, unsafe_allow_html=True)
        else:
            st.write("Please enter the company name.")


if __name__ == "__main__":
    main()